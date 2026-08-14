# TakeMyCourseForMe — Onboarding

How to install and use this skill from scratch, on a fresh machine, for
extracting a Skool or Circle course into cliff notes + a build handoff.

---

## Install

1. Clone or copy this folder to your machine, then `cd` into it.
2. Run every command below **from the skill root** (the folder that holds
   `scripts/` and these `.md` files).
3. No `pip install` for the core pipeline — Python 3.8+ standard library only
   (yt-dlp, ffmpeg, and Whisper are extras for video/transcripts).

---

## Quick Start (Skool, end-to-end)

```bash
python3 scripts/chrome_js.py 'skool.com' '@scripts/skool_tree.js' > tree.json
python3 scripts/extract_course.py --make-manifest --tree tree.json --platform skool --course "Course Title" --url 'https://www.skool.com/...' --out manifest.json
python3 scripts/extract_course.py --manifest manifest.json --out-dir ./captured --platform skool --backend chrome --tab 'skool.com'
python3 scripts/make_cliff_notes.py --manifest manifest.json --captured ./captured --out cliff-notes.md
```

The detailed walkthrough (all platforms, video/transcripts) follows.

---

## What you need (prerequisites)

- **Google Chrome (macOS), already logged in to the course.** `chrome_js.py`
  hardcodes "Google Chrome" — Chrome-based browsers (Brave/Chromium) are not
  supported without editing the AppleScript. Non-negotiable for Skool — see
  "The one rule" below.
- **Python 3.8+** — the scripts use only the standard library, so there is
  *nothing to pip-install for the core pipeline*.
- **macOS** for `scripts/chrome_js.py` (it drives Chrome via AppleScript /
  `osascript`). On Windows/Linux, substitute your own "run JS in the real
  browser" mechanism, or use the cookie-import path for Circle.

### Dependencies

| Package | Why you'd install it | Command |
|---|---|---|
| `yt-dlp` | **Required for transcripts/video** (optional for text-only courses). Manual subs need `--write-subs` (not `--write-auto-subs`). | `pip install yt-dlp` |
| `requests` | Nicer HTTP for the Circle walker (it auto-falls-back to urllib). | `pip install requests` |
| `browser_cookie3` | Programmatic cookie export for the Circle path (it does NOT write `cookies.txt` by itself — see note below). | `pip install browser_cookie3` |
| `openai-whisper` or `faster-whisper` | Local transcript fallback when a lesson has no captions. | `pip install openai-whisper` |

No `brew` packages are required for the core pipeline. **Video downloads via
`yt-dlp` typically need `ffmpeg`** (`brew install ffmpeg`) — HLS/streaming
videos won't merge without it.

**On `browser_cookie3`:** it is a programmatic API and does not emit a
`cookies.txt` by itself. Simplest: use a "cookies.txt" browser extension. Or
export to Netscape format yourself:

```bash
python3 -c "import browser_cookie3; [print('\t'.join([c.domain,'TRUE',c.path,'TRUE' if c.secure else 'FALSE',str(c.expires or 0),c.name,c.value])) for c in browser_cookie3.chrome()]" > cookies.txt
```

---

## The one rule (read this first)

**NEVER use a headless browser for Skool.**

Skool sits behind a login wall *and* CloudFront **signed URLs**. A headless
browser gets a **403** on every asset — the tell is a ~146-byte response body
containing `MissingKey`. Only JavaScript running inside the user's *actual
logged-in* tab can read the course. The user logs in; you drive their real
Chrome. Do not try to recreate the session headlessly.

- **Skool** → `chrome_js.py` (AppleScript `execute javascript` in the live tab).
- **Circle** → the live Chrome bridge *or* cookie decrypt → headless import
  (Circle pages are server-rendered HTML, so plain HTTP + cookies works).

---

## Step 1 — Log in

1. Open Chrome, go to the course, and make sure you're **logged in** and can
   see the lessons.
2. Leave that tab open. Everything below runs *in that tab*.
3. Verify the bridge works (should print the page title):

   ```bash
   python3 scripts/chrome_js.py 'skool.com' 'document.title'
   ```

---

## Step 2 — Map the course

**Skool:**

```bash
python3 scripts/chrome_js.py 'skool.com' '@scripts/skool_tree.js' > tree.json
python3 scripts/extract_course.py --make-manifest --tree tree.json \
  --platform skool --course "Course Title" \
  --url 'https://www.skool.com/...' --out manifest.json
```

**Circle** (get a `cookies.txt` first — a "cookies.txt" browser extension, or
`browser_cookie3`):

```bash
python3 scripts/circle_walk.py --url 'https://YOUR.circle.so/c/...' \
  --cookies cookies.txt --out manifest.json
```

Inspect `manifest.json`. It lists every section and lesson with its URL,
video link, and resource links. This is your **resumable checkpoint** — treat
it as precious. The Skool walker is heuristic (it looks for `title` + a
URL-ish field); if it catches noise or misses lessons, that's normal — prune
the JSON by hand and move on.

---

## Step 3 — Capture every lesson (resumable)

```bash
# Skool (drive the live Chrome tab):
python3 scripts/extract_course.py --manifest manifest.json \
  --out-dir ./captured --platform skool --backend chrome --tab 'skool.com'

# Circle (server-rendered HTML over HTTP):
python3 scripts/extract_course.py --manifest manifest.json \
  --out-dir ./captured --platform circle --backend http --cookies cookies.txt
```

- Run `--limit 3` first to smoke-test on the first 3 lessons (a smoke test
  marks them `done`; use `--reset` to clear all `status`/`files` back to
  pending for a clean re-run).
- Run the full extraction as a **background terminal process** — it can outlive
  short subagent timeouts, and it **resumes** (it skips lessons already marked
  `done` in the manifest).
- For each lesson it captures the **text** (markdown) and records **resource
  links**. Videos, screenshots, and transcripts are manual (see below and
  Step 4) — the driver does not capture them.

### Downloadable files (ZIP/PDF — the real deliverables)

The driver records every resource URL. On the http (Circle) backend it tries to
download each one; any that fail (**403 / ~146-byte `MissingKey`** = the
CloudFront signed-URL wall) are logged to `captured/manual-downloads.txt`.
**Click those links in the real browser** — a real click renews the signed URL
and the download succeeds. On the chrome (Skool) backend every resource is
signed, so all of them go to `manual-downloads.txt`. Successful downloads never
appear in the list. Attachments are the actual course deliverables; do not skip
them.

### Videos + screenshots

- **Videos**: copy the `video_url` from the manifest and download with
  `yt-dlp` (or the platform's own download button) to an **external drive** —
  courses can be tens of GB. **Circle manifests do not carry `video_url`** —
  the tree page lists lesson links but not each lesson's embedded video, so for
  Circle grab the video URL from the individual lesson page (Wistia/Vimeo
  iframe or `<video src>`) in Step 4.
- **Screenshots**: not automated — the Chrome backend can be extended to
  screenshot each lesson (see `chrome_capture` in `scripts/extract_course.py`);
  the driver only reserves a `screenshots/` dir with `--screenshots`.

---

## Step 4 — Transcripts

Priority order:

1. **Platform UI transcript** — if the platform shows one, grab it first.
2. **VTT captions** — for Wistia/Vimeo/YouTube-hosted videos:
   ```bash
   yt-dlp --skip-download --write-subs --sub-langs en "VIDEO_URL"  # en = your course's language; "all" also pulls noisy auto-subs
   ```
   > Manual subtitles need `--write-subs`, **not** `--write-auto-subs`
   > (auto subs are machine-generated and wrong).
3. **Whisper fallback** — transcribe the downloaded audio locally when there
   are no captions.

Clean them into text (this also fixes single-line transcript dumps):

```bash
python3 scripts/download_transcripts.py --input subs/ --out transcripts/
```

---

## Step 5 — Cliff notes (the deliverable)

```bash
python3 scripts/make_cliff_notes.py --manifest manifest.json \
  --captured ./captured --out cliff-notes.md
```

This writes `cliff-notes.md` (TLDR + course-at-a-glance + lesson index) and
`build-handoff.md` (the "know enough to build it" brief). **Then you fill in
the bolded takeaways** from your deep read — the script scaffolds, you
summarize. The target format is in `SKILL.md` (Step 5): TLDR at the top,
bolded takeaways, short scannable sections, readable in under a minute.

---

## Step 6–8 — Deep read, gap analysis, handoff

1. **Deep read**: read every captured `.md` and transcript line-by-line — and
   the contents of the downloaded ZIPs/PDFs. **Never summarize summaries** —
   read the lesson files, not the architecture labels.
2. **Gap analysis**: compare against what you already have; build only the
   genuine gaps. Respect scope exactly — what the user names is the whole job.
3. **Handoff**: finish `build-handoff.md` with the method, steps, tools, files,
   and gaps, so a builder can start without re-reading the course.

---

## Output layout

```
manifest.json            # resumable checkpoint — written where --out points
                         #   (cwd by default), NOT inside captured/
captured/                # the --out-dir you passed (default ./captured)
  lessons/<sec>/<n>.md   # lesson text (markdown)
  downloads/             # ZIP/PDF — the real deliverables
  screenshots/           # reserved dir (screenshots are not auto-captured)
  manual-downloads.txt   # resource URLs the driver could NOT download (403/signed-URL wall) — click in the browser
transcripts/             # cleaned transcripts — written where Step 4's --out
                         #   points, NOT inside captured/
cliff-notes.md           # THE deliverable
build-handoff.md         # "know enough to build/implement it"
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `chrome_js.py` hangs / never returns | macOS Apple Events permission missing. In Chrome: View → Developer → "Allow JavaScript from Apple Events" (and accept the "Terminal wants to control Google Chrome" dialog). |
| `__NOT_FOUND__` from `chrome_js.py` | No Chrome tab's URL contains your `--tab` substring. Open the course and match the substring (e.g. `skool.com`). |
| Skool downloads return 403 / 146-byte `MissingKey` | Signed URL — click the link in the real browser, don't script it. |
| Skool tree is empty or noisy | The walker is heuristic. Open DevTools → Network, inspect `__NEXT_DATA__`, adjust `skool_tree.js`'s key detection, re-run. |
| Circle fetch 401/403 | Cookies are stale/partial. Re-export a fresh `cookies.txt` and make sure it includes the `.circle.so` domain. |
| Extraction died mid-run | Re-run the same command — it resumes from `status: done` lessons. |
