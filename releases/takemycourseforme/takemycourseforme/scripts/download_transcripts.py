#!/usr/bin/env python3
"""Turn caption/transcript files into clean plain text.

Handles:
  1. VTT files (WEBVTT) -> text, stripping cue timings and inline tags.
  2. SRT files -> text.
  3. Single-line transcript dumps -> split on timestamp markers (a common
     export bug that otherwise leaves you one unreadable wall of text).

Usage:
  python3 download_transcripts.py --input subs/ --out transcripts/
  python3 download_transcripts.py --input subs/lecture.en.vtt --out transcript.txt
  python3 download_transcripts.py --input dump.txt --out clean.txt --split-timestamps

Note on WHERE captions come from (see the skill): prefer the platform's UI
transcript first, then VTT captions. For yt-dlp, MANUAL (human) subtitles need
`--write-subs`, NOT `--write-auto-subs` (auto subs are machine-generated and
noisy). Whisper (local) is the fallback when no captions exist.

Standard library only.
"""
import argparse
import os
import re
import sys

# VTT/SRT cue timing: 00:00:00.000 --> 00:00:03.000  (with or without hour, , or .)
TIMING_RE = re.compile(
    r"^\s*(\d{1,2}:)?\d{1,2}:\d{2}[.,]\d{3}\s*-->\s*(\d{1,2}:)?\d{1,2}:\d{2}[.,]\d{3}"
)
# A loose timestamp anywhere in a line: [00:00], (00:00), 00:00:00, 00:00.0
TS_RE = re.compile(r"[\[\(]?(?:\d{1,2}:)?\d{1,2}:\d{2}(?::\d{2})?(?:[.,]\d{1,3})?[\]\)]?")

TAG_RE = re.compile(r"<[^>]+>")
ENTITY_RE = {
    "&nbsp;": " ", "&amp;": "&", "&lt;": "<", "&gt;": ">",
    "&quot;": '"', "&#39;": "'", "&apos;": "'",
}


def clean_line(line):
    line = TAG_RE.sub("", line)
    for k, v in ENTITY_RE.items():
        line = line.replace(k, v)
    return line.strip()


def is_skippable(line):
    s = line.strip()
    if not s:
        return True
    if s == "WEBVTT":
        return True
    if "-->" in s or TIMING_RE.match(s):
        return True
    if s.upper().startswith(("NOTE", "STYLE", "REGION", "KIND:", "LANGUAGE:")):
        return True
    if re.match(r"^\d+$", s):
        return True
    return False


def parse_timed(text):
    """VTT/SRT -> list of caption lines (timings and metadata removed)."""
    out = []
    for raw in text.splitlines():
        if is_skippable(raw):
            continue
        line = clean_line(raw)
        if line:
            out.append(line)
    return out


def split_single_line(text):
    """Split a single giant line on timestamp markers into readable chunks,
    keeping each timestamp at the start of its own line."""
    matches = list(TS_RE.finditer(text))
    if not matches:
        return [text.strip()]
    out = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        ts = m.group(0).strip()
        if body:
            out.append((ts + " " + body) if ts else body)
    return out


def process(text, split_ts):
    if split_ts or (len(text.splitlines()) <= 2 and TS_RE.search(text)):
        return split_single_line(text)
    return parse_timed(text)


def main(argv):
    ap = argparse.ArgumentParser(description="VTT/SRT/single-line -> clean text.")
    ap.add_argument("--input", required=True, help="VTT/SRT/txt file, or a directory of them")
    ap.add_argument("--out", required=True, help="Output file or directory")
    ap.add_argument("--split-timestamps", action="store_true",
                    help="Force single-line timestamp splitting")
    args = ap.parse_args(argv)

    # --input and --out must match: a directory in means a directory out, and a
    # file in means a file out. Mismatches silently overwrite or scatter files.
    if os.path.isdir(args.input) and os.path.isfile(args.out):
        ap.error("--input is a directory, but --out is an existing file; "
                 "when --input is a directory, --out must be a directory")
    if os.path.isfile(args.input) and os.path.isdir(args.out):
        ap.error("--input is a file, but --out is an existing directory; "
                 "when --input is a file, --out must be a file")

    if os.path.isdir(args.input):
        os.makedirs(args.out, exist_ok=True)
        files = [f for f in sorted(os.listdir(args.input))
                 if f.lower().endswith((".vtt", ".srt", ".txt"))]
        for f in files:
            with open(os.path.join(args.input, f), "r", encoding="utf-8", errors="replace") as fh:
                lines = process(fh.read(), args.split_timestamps)
            out_path = os.path.join(args.out, os.path.splitext(f)[0] + ".txt")
            with open(out_path, "w", encoding="utf-8") as fh:
                fh.write("\n".join(lines) + "\n")
            print("Wrote %s (%d lines)" % (out_path, len(lines)))
    else:
        with open(args.input, "r", encoding="utf-8", errors="replace") as fh:
            lines = process(fh.read(), args.split_timestamps)
        out_path = args.out
        if os.path.isdir(args.out):
            out_path = os.path.join(args.out, os.path.splitext(os.path.basename(args.input))[0] + ".txt")
        out_dir = os.path.dirname(out_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        print("Wrote %s (%d lines)" % (out_path, len(lines)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
