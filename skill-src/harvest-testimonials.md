---
name: harvest-testimonials
description: Fetch testimonials that already exist and collect each client's words and photo. Sources: YouTube channel videos (titles, auto-caption transcripts, face frames via yt-dlp + ffmpeg), web pages (blog testimonial sections), and social/community platforms (Skool, Facebook, LinkedIn, Instagram, blog comments — via a browser-control or computer-use skill in the owner's own logged-in session). Use whenever the user asks to gather, collect, pull, or mine testimonials, reviews, or client quotes from their YouTube channel, website, blog, or social communities — before anything is designed. Output is raw material (quote + name + role + face image per client), and EVERY candidate passes a mandatory qualification gate (script pre-filter + scored rubric) before design. Pair with graphic-testimonials to turn the harvest into branded card images.
---

# Harvest Testimonials

Fetches existing client proof and returns, per client: **quote, name, role, face image**. Requires `yt-dlp`, `ffmpeg`, `ffprobe`. Work in a scratch dir inside the project workspace; delete `.mp4` files when done, keep `.txt` transcripts and contact sheets as source material.

## 0. Dedupe first

List what the user already has (existing Canva cards via `get-design-content`; site cards via alt texts) and skip those people. Users hate duplicate proof.

> **Tool fallback:** `get-design-content` is a Canva-specific tool. If you don't have it, use whatever design-listing/export capability you do have (list designs, export thumbnails, screenshot the card gallery), or simply ask the user for the names already on cards and record them manually. Never skip dedupe entirely just because the exact tool is missing.

## 1. YouTube source

```bash
# list every video on the channel
yt-dlp --flat-playlist --print "%(id)s | %(title)s" "https://www.youtube.com/@CHANNEL/videos"

# transcript (auto-captions)
yt-dlp --skip-download --write-auto-subs --write-subs --sub-langs "en.*" --sub-format vtt -o "%(id)s.%(ext)s" "https://www.youtube.com/watch?v=ID"
python3 scripts/clean_vtt.py <id>   # reads <id>.en.vtt, writes <id>.txt

# low-res video for face frames
yt-dlp -f "worst[ext=mp4]/worst" -o "%(id)s.%(ext)s" "https://www.youtube.com/watch?v=ID"
python3 scripts/contact_sheets.py <id> [<id>...]   # writes sheet_<id>.png
```

- Channel pages are JS-rendered — plain HTTP fetches return boilerplate. yt-dlp is the reliable path.
- Some videos fail first pass; retry with `worst[ext=mp4]/worst[ext=webm]/worst`.
- Names/roles come from the video TITLE ("Testimonial from Jane Doe of Example Agency") — titles are more reliable than captions for spelling.

## 2. Web page source

Fetch the page (kimi_fetch_v2 or curl). Testimonial sections are often theme filler — VERIFY each person is a real client with the user before use; a fake one shipped once and had to be pulled. Photos: grep the raw HTML for upload/CDN image URLs near the person's name (lazy-loaded images hide in `data-src`; check the live DOM if curl HTML lacks them).

> **Tool fallback:** `kimi_fetch_v2` is one agent's web-fetch tool — any web-fetch capability works here (curl/wget, a FetchURL-style tool, or a browser read). If the page is JS-rendered and plain fetches return boilerplate, switch to a browser-control/computer-use skill if you have one; if you have neither, tell the user and skip that page rather than guessing at its contents.

## 3. Quotes

- Faithful condensation only — auto-captions garble names/terms; fix obvious caption errors, never add claims or numbers.
- Prefer specifics (revenue, timeframes, outcomes) matching the target offer's themes.
- Keep under ~280 chars so it fits a card; flag quotes for user wording review.

## 4. Faces

Read each contact sheet (3 frames at 25%/55%/80%, labeled with timestamps); pick eye-contact, eyes-open, no-caption-overlay frames. Extract:

```bash
ffmpeg -y -ss <t> -i <id>.mp4 -frames:v 1 face.png
```

Crop: landscape → center square (side=height); portrait → 0.9×width square, VERTICALLY CENTERED (top-biased crops cut foreheads). Clients who already have a good photo on an existing card or the user's site — reuse that instead.

## 5. Social and community sources

Testimonials also live in Skool communities, Facebook pages/groups, LinkedIn comments and recommendations, Instagram comments, and blog comment sections. These are JS-rendered, login-gated spaces — yt-dlp cannot reach them. Use this route when you have a **browser-control skill** (drives the owner's own logged-in browser) or a **computer-use skill**. If you have neither, say so and stick to sections 1–2.

**Which tool for which source:**

- YouTube → yt-dlp (section 1). Web pages → plain fetch (section 2).
- Skool / Facebook / LinkedIn / Instagram / blog comments → browser-control or computer-use, following the per-platform playbooks in **references/social-sources.md**.

**Capture workflow (every platform):**

1. **Navigate** — open the space in the owner's own logged-in session. Never handle credentials; the session exists already.
2. **Capture the candidate** — record per person: display name, quote (verbatim), source permalink, profile URL, avatar URL, platform, date, one line of thread context. These map directly onto the JSONL fields the pre-filter reads.
3. **Screenshot the region** showing the comment and its author — this is the proof of provenance. No screenshot + no permalink = automatic reject.
4. **Fetch the face** — `python3 scripts/fetch_avatar.py <avatar_url> -o face.png`, or `--from-screenshot proof.png --crop x,y,w,h` when the avatar isn't a fetchable URL. Output is a 512px square PNG ready for graphic-testimonials' circle_face.py.

**Etiquette (hard rules):** owner's own logged-in session only; respect robots and rate limits; never circumvent blocks — HTTP 999 or a captcha means STOP and tell the user; private content stays private; harvest only from spaces where the owner is a participant/admin or where the praise is about the owner. Full rules per platform: references/social-sources.md §0.

## 6. The qualification gate — MANDATORY

Nothing goes to design unqualified. Every candidate, from every source, passes:

```
candidates.jsonl
  → python3 scripts/qualify_candidates.py        (deterministic pre-filter)
  → score survivors with references/qualification-rubric.md   (0–100)
  → 70+ accept · 40–69 human review pile · <40 reject
```

- The script catches mechanical failures: missing source URL, missing/anon author, placeholder/theme-filler patterns, too-short/overlong quotes, exact and near duplicates.
- The rubric catches judgment failures: vagueness, hearsay, unverifiable profiles, people who cannot be clients. It includes three fully worked fictional examples — follow them.
- The review pile goes to the user with reasons attached. They decide.

```
┌─ FOR LESS CAPABLE MODELS — follow this exactly ─────────────────────┐
│ 1. Collect candidates into JSONL (name, quote, source_url,          │
│    profile_url, avatar_url, platform).                              │
│ 2. Run scripts/qualify_candidates.py. Rejects are gone — do not     │
│    argue with them.                                                 │
│ 3. Open references/qualification-rubric.md. Apply the 6 hard-reject │
│    rules, then score B1–B6 and SUM THE NUMBERS. Do not estimate.    │
│ 4. 70+ → design. 40–69 → show the user. <40 → discard.              │
│ 5. IF ANY DOUBT, PUT IT IN REVIEW — never auto-ship on a hunch.     │
│ 6. Never ship an unverified "client". This rule exists because a    │
│    fake once shipped: theme-filler content on a blog template —     │
│    praising a generic person who was never a client — made it onto  │
│    a finished card and had to be pulled. Verify the human exists.   │
└─────────────────────────────────────────────────────────────────────┘
```
