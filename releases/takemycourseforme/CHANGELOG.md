# Changelog

All notable changes to takemycourseforme are documented here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2026-08-14

### Added
- Initial public release: extract a paid course from Skool or Circle into
  ADHD-friendly cliff notes (TLDR + scannable study guide) plus a
  build/implement handoff. Live-Chrome bridge for Skool (never headless),
  cookie-import path for Circle, resumable manifest-based capture, transcript
  pipeline (yt-dlp/Whisper), deep-read and gap-analysis steps.
- Bundled scripts: `chrome_js.py`, `skool_tree.js`, `circle_walk.py`,
  `lesson_capture.js`, `download_transcripts.py`, `extract_course.py`,
  `make_cliff_notes.py`.
- Scrubbed of all personal names, paths, and machine details. MIT licensed.
