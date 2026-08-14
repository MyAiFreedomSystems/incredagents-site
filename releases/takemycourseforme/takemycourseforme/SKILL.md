---
name: takemycourseforme
description: >-
  Extract a paid online course from Skool or Circle into ADHD-friendly cliff
  notes (a TLDR + scannable study guide) plus a "know enough to build/implement
  it" handoff. Trigger on phrases like "extract this course", "cliff notes",
  "study this course", "TLDR the course", "summarize my course", "study guide",
  "course extraction", or when the user names Skool or Circle. Teaches the full
  pipeline: auth (never headless for Skool), course-tree mapping, resumable
  lesson capture (text + resource links to the downloadable ZIP/PDF files that
  are the real deliverables), video + transcript pull (yt-dlp/Whisper, Step 4),
  transcript cleanup, deep read, gap analysis, and the implementation handoff.
---

# TakeMyCourseForMe

Extract a course you paid for, then turn it into **cliff notes you can scan in
under a minute** and a **"know enough to build/implement it"** handoff for your
team. Works on **Skool** and **Circle** from one skill, one entry point.

The capture (extraction) is the means. The **cliff notes + build handoff** are
the point. You are not archiving a course — you are converting a paid course
into something you can *act on*.

---

## When to use

Use this skill when the user says any of:

- "extract this course" / "pull this course down"
- "cliff notes" / "study this course" / "TLDR this course" / "summarize my course"
- "I bought this Skool/Circle course, go get it"
- "turn this into a study guide" / "give me the cliff notes for my team"

---

## ⚠️ THE ONE RULE THAT SAVES YOU HOURS

**NEVER use a headless browser for Skool.**

Skool sits behind a login wall *plus* CloudFront **signed URLs** that only a real
session — a physical click or JavaScript running inside the user's *actual
logged-in Chrome tab* — can produce. A headless browser gets a **403** on every
asset (and a 146-byte `MissingKey` error body is the tell).

The user has already logged in. **Drive their real Chrome.** Do not try to
replicate the session in a headless browser — you will burn hours and fail.

```
Skool   -> osascript "execute javascript" in the live logged-in Chrome tab
Circle  -> two options: live Chrome (same bridge), OR Chrome cookie
           decrypt -> import into a headless fetch (Circle HTML is
           server-rendered, so plain HTTP with the right cookies works)
```

---

## The pipeline at a glance (8 steps)

| # | Step | What you produce |
|---|------|------------------|
| 1 | **Auth** | A working way to read the course (live Chrome, never headless for Skool) |
| 2 | **Map** | Full course/module tree as a JSON manifest |
| 3 | **Capture** (resumable) | Lesson text + resource links (driver); video, screenshots, transcripts are manual (Step 4) |
| 4 | **Transcripts** | Clean text transcript per video lesson |
| 5 | **Cliff notes** | TLDR + scannable study guide (the centerpiece) |
| 6 | **Deep read** | Read every lesson line-by-line — never summarize summaries |
| 7 | **Gap analysis** | Compare to what you already have; build only real gaps |
| 8 | **Handoff** | "Here's everything you need to build/implement this" |

The scripts in `scripts/` automate steps 1–4. Steps 5–8 are done by the agent
(you) using the captured files — with `make_cliff_notes.py` scaffolding step 5.

---

## Step 1 — Auth (never headless)

**Personal-use boundary:** for personal study of content you've paid for. Do
not redistribute the extracted material.

**Skool — drive the live Chrome tab.** Use `scripts/chrome_js.py`, an
AppleScript bridge that runs JavaScript in the user's already-open, already
logged-in Chrome tab:

```bash
python3 scripts/chrome_js.py 'skool.com' 'document.title'
```

It finds the tab whose URL contains the substring you pass (e.g. `skool.com`)
and runs your JS there. You can also pass a JS file with `@path`:

```bash
python3 scripts/chrome_js.py 'skool.com' '@scripts/skool_tree.js'
```

> `chrome_js.py` is macOS-only (it shells out to `osascript`). On other OSes,
> use an equivalent "run JS in the real browser" mechanism — or fall back to the
> cookie-import path below. The rule is the same: **real session, never
> headless.**

**Circle — two options.** (1) Same live-Chrome bridge above; or (2) **cookie
decrypt → headless import**: Circle pages are server-rendered HTML, so a plain
HTTP request with the user's session cookies returns the full lesson content.
Export the cookies (a browser extension's "cookies.txt", or a cookie-export
library), then:

```bash
python3 scripts/circle_walk.py --url 'https://YOUR.circle.so/c/...' --cookies cookies.txt
```

Document both in your run notes; Skool needs the bridge, Circle is happy either way.

---

## Step 2 — Map the course

Pull the full course/module tree and save it as a **manifest** (JSON) with
title, URL, video link, and resource links per module. This is your resumable
checkpoint — never lose it.

**Skool** — Skool is a Next.js app; the tree lives in `__NEXT_DATA__` and in
`_next/data/<buildId>/...json`. Run the walker in the live tab:

```bash
python3 scripts/chrome_js.py 'skool.com' '@scripts/skool_tree.js' > tree.json
```

Then build the manifest from it:

```bash
python3 scripts/extract_course.py --make-manifest --tree tree.json \
  --platform skool --course "Course Title" \
  --url 'https://www.skool.com/...' --out manifest.json
```

**Circle** — server-rendered HTML; the walker extracts lesson links directly
and writes a manifest:

```bash
python3 scripts/circle_walk.py --url 'https://YOUR.circle.so/c/...' \
  --cookies cookies.txt --out manifest.json
```

**Circle manifests do not carry `video_url`.** The course tree page lists
lesson links but not each lesson's embedded video — the player lives on the
individual lesson page. Leave `video_url` null for Circle and pull videos
per-lesson in Step 4 (yt-dlp on the lesson page's Wistia/Vimeo iframe or
`<video src>`).

**Manifest shape** (the contract every script reads/writes):

```json
{
  "platform": "skool",
  "course": "Course Title",
  "url": "https://...",
  "sections": [
    {
      "title": "Section 1",
      "modules": [
        {
          "title": "Lesson 1",
          "url": "https://...",
          "video_url": "https://...",
          "resources": [{"name": "workbook.zip", "url": "https://..."}],
          "status": "pending",
          "files": {"text": "lessons/01-section-slug/01-lesson-slug.md", "transcript": null, "screenshot": null}
        }
      ]
    }
  ]
}
```

---

## Step 3 — Capture every lesson (resumable)

The driver captures **text + resource links** per lesson. Video, screenshots,
and transcripts are manual jobs (see below and Step 4).

**Automated (the driver does this):**

1. **Text** — the lesson body as markdown (Skool rich text is ProseMirror;
   the capture JS converts it).
2. **Resource links** — ZIP/PDF/workbook/video links. On the Circle http
   backend the driver also downloads them; on Skool it records the links for
   you to click. **These files are the actual course deliverables and the
   most-missed target.**

**Manual (you do these; the driver does NOT):**

3. **Video** — the MP4. Download it yourself with yt-dlp in Step 4, to an
   external drive (courses can be tens of GB). The driver does not download
   video.
4. **Screenshot** — not automated; the Chrome backend can be extended (see
   ONBOARDING). The driver only reserves a `screenshots/` dir with
   `--screenshots`.
5. **Transcript** — see Step 4.

The driver does text + resource capture lesson-by-lesson and is **resumable**
— it tracks `status` in the manifest and skips anything already `done`, so a
crash loses nothing:

```bash
# Skool (drive live Chrome):
python3 scripts/extract_course.py --manifest manifest.json \
  --out-dir ./captured --platform skool --backend chrome --tab 'skool.com'

# Circle (server-rendered HTML over HTTP):
python3 scripts/extract_course.py --manifest manifest.json \
  --out-dir ./captured --platform circle --backend http --cookies cookies.txt
```

- Use `--limit 3` to test on the first 3 lessons before the full run. A smoke
  test marks those lessons `done`; add `--reset` to clear all `status` and
  `files` back to pending for a clean re-run.
- Run it as a **background terminal process** — long extractions outlive
  short-lived subagent timeouts. Kill and rerun; it resumes.

**Downloadable files:** the driver records every resource URL. On the http
backend it tries to download each one; any that fail (**403 / a ~146-byte
`MissingKey` body** = the CloudFront signed-URL wall) are logged to
`manual-downloads.txt` for you to click in the real browser — a real click
renews the signed URL and the download succeeds. On the chrome backend every
resource is signed, so all of them go to `manual-downloads.txt`. Successful
downloads never appear in the list.

---

## Step 4 — Transcripts

Priority order (proven):

1. **Platform UI transcript** — if the platform shows a transcript, grab it first.
2. **VTT captions** — for Wistia/Vimeo/YouTube-hosted lessons, pull the caption
   file. **Manual (human) subtitles need `--write-subs`, NOT `--write-auto-subs`**
   (auto subs are the machine-generated ones and are wrong/noisy):
   ```bash
   yt-dlp --skip-download --write-subs --sub-langs en "VIDEO_URL"  # en = your course's language; "all" also pulls noisy auto-subs
   ```
   Then clean the VTT into text:
   ```bash
   python3 scripts/download_transcripts.py --input subs/ --out transcripts/
   ```
3. **Whisper fallback** — if there are no captions, transcribe the downloaded
   audio/video locally (e.g. `whisper` or `faster-whisper`).

The cleanup script also **splits single-line transcripts on timestamp
markers** (a common export bug that otherwise produces one unreadable wall).

---

## Step 5 — Cliff notes (THE DELIVERABLE)

Run the scaffolder, then *you* fill in the TLDR and takeaways from your deep
read (Step 6):

```bash
python3 scripts/make_cliff_notes.py --manifest manifest.json \
  --captured ./captured --out cliff-notes.md
```

The output must be **scannable in under a minute**. Concrete target format:

````markdown
# Course Name — Cliff Notes

## ⚡ TLDR (30 seconds)
**What it is:** <one sentence — what the course actually teaches>
**Who it's for:** <one line>
**The one big idea:** <the core method / mindset>
**To build it you need:** <1–2 sentences — the implementation in a nutshell>

## 🗺️ Course at a glance
- **Section 1 — Setup** (6 lessons) → <one-line point>
- **Section 2 — The method** (9 lessons) → <one-line point>
- **Section 3 — Launch** (4 lessons) → <one-line point>

## 📚 Lesson index
1. **Pick a niche** — <one-line takeaway>
2. **Build the offer** — <one-line takeaway>
...

## 🛠️ To build/implement this you need:
- <tool / step 1>
- <tool / step 2>
- <tool / step 3>

## 📦 Files you downloaded
- <file.zip> · <file.pdf> · <video.mp4> (×N)
````

**ADHD-friendly rules (non-negotiable):**
- TLDR block at the **top**, bolded.
- **Short sections**, headers you can scan.
- **Bold the takeaways** — one bolded line per lesson, no walls of text.
- Over ~30 lessons, the index collapses to section-level takeaways; the full per-lesson index moves to an appendix — keep it scannable.
- Bullet lists, never paragraphs of prose.
- Scannable in under a minute.

---

## Step 6 — Deep read (know enough to build)

**Read every lesson line-by-line. NEVER summarize summaries.**

This is the step that separates "extracted a course" from "can actually build
the thing." Do not read the course's *architecture labels* and call it done —
read the **lesson files themselves**. A past run was rejected for summarizing
the summary of the summary. Three layers of abstraction = failure.

Read each captured `.md`, transcript, and the downloaded ZIP/PDF contents, then
extract what is *buildable*: steps, prompts, configs, scripts, templates,
pricing, funnels, checklists.

---

## Step 7 — Gap analysis

Compare what the course teaches against what already exists (your prior work,
your team's existing systems, other courses you already have). Build **only the
genuine gaps**.

- If a superset already exists, don't rebuild it — note the overlap.
- When the user names what they want, **everything else is excluded** — respect
  that scope exactly; don't pad it and don't trim it.
- On overlap, still glean: "there's no way there's not something we glean from
  that."

---

## Step 8 — Handoff

End with a **"here's everything you need to build/implement this"** brief:
the method, the steps, the tools, the files, and the gaps — written so a
builder can start immediately without re-reading the course.

---

## Pitfalls (dedicated list — memorize these)

- **CloudFront signed-URL 403 on downloads** — 146-byte `MissingKey` error body
  is the tell. Needs a **real click** in the logged-in browser, not a scripted
  `GET`. Log to `manual-downloads.txt`.
- **"Don't summarize summaries."** Read lesson files line-by-line, not
  architecture labels. Three layers of abstraction got a course rejected.
- **Download the ZIP files.** Attachments are the *deliverables* — the
  most-missed target. Your first QA check: did you capture every ZIP/PDF
  attachment? They are the actual deliverables.
- **Scope.** When the user names what they want, everything else is excluded.
  Don't pad, don't trim, don't ask for a second correction.
- **`async fetch` never resolves through Chrome's `execute javascript`
  bridge** → use **synchronous XHR** (`xhr.open('GET', url, false)`). This is
  baked into `skool_tree.js`.
- **Manual captions need `--write-subs`, not `--write-auto-subs`.** Auto subs
  are machine-generated and wrong.
- **Long extraction must be resumable.** Track `status` in the manifest and
  skip `done` lessons — never lose the manifest on a crash.
- **Single-line transcript files** need timestamp splitting —
  `download_transcripts.py` does this automatically.
- **Subagents timeout at ~600s.** Run long extraction in a background terminal
  process, not a delegated subagent.
- **Apple Events permission (macOS).** `chrome_js.py` hangs silently until
  Chrome > View > Developer > "Allow JavaScript from Apple Events" is checked
  (accept the "Terminal wants to control Google Chrome" dialog too).
- **Rate-limiting / Cloudflare bot-challenge on long runs.** Space lessons out
  (a 1–3s delay between lessons) if the platform starts throwing challenges.
  The run is resumable, so back off and re-run rather than hammering.
- **Course schema drift.** Skool changes its `__NEXT_DATA__` shape. If
  `tree.json` comes back empty or noisy, inspect the Network tab for
  `_next/data/…json` keys and adjust `skool_tree.js`'s key detection.
- **Session expiry mid-run.** If captures come back empty or show a login page,
  your session expired — re-auth in the real browser and re-run. Do NOT mark
  those lessons `done` (they stay `failed`, so resume retries them).
- **Wrong-tab hijack.** Extra Skool/Circle tabs matching the `--tab` substring
  can steal the extraction — the driver uses the first match and warns on
  stderr when more than one matches. Close stray tabs first.
- **Print FULL absolute paths when there are errors** — never a shorthand.

---

## Scripts reference

| Script | Purpose |
|--------|---------|
| `scripts/chrome_js.py` | Run JS in the live logged-in Chrome tab (macOS/osascript). |
| `scripts/skool_tree.js` | JS payload: walk Skool `__NEXT_DATA__` / `_next/data` (sync XHR). |
| `scripts/circle_walk.py` | Walk Circle server-rendered HTML into a manifest. |
| `scripts/lesson_capture.js` | JS payload: ProseMirror/rich text → markdown + resource links. |
| `scripts/extract_course.py` | Resumable lesson-by-lesson capture driver (both platforms). |
| `scripts/download_transcripts.py` | VTT → clean text; splits single-line timestamp dumps. |
| `scripts/make_cliff_notes.py` | Scaffold the ADHD cliff notes + build handoff from captures. |

See `ONBOARDING.md` for installation and a full walkthrough.

---

## Output layout

Three separate outputs live in three separate places — keep them straight:

```
manifest.json           # resumable checkpoint (tree + per-lesson status).
                        #   Written where --out points (cwd by default), NOT
                        #   inside the capture dir.

<out-dir>/              # the --out-dir you passed (default ./captured)
  lessons/<sec>/<n>.md  # lesson text as markdown
  downloads/            # ZIP/PDF/video — the real deliverables
  screenshots/          # reserved dir (screenshots are not auto-captured)
  manual-downloads.txt  # resource URLs the driver could NOT download (403/signed-URL wall) — click them in the real browser

transcripts/            # cleaned transcripts — written where Step 4's --out
                        #   points (NOT inside the capture dir)

cliff-notes.md          # THE deliverable (TLDR + study guide)
build-handoff.md        # "know enough to build/implement it"
                        #   both written next to make_cliff_notes.py --out
```
