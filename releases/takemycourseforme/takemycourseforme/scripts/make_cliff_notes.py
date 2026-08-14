#!/usr/bin/env python3
"""Scaffold ADHD-friendly cliff notes + a build handoff from captured lessons.

Reads the manifest (which points at each lesson's captured markdown) and emits
two files:
  - cliff-notes.md   : TLDR block + course-at-a-glance + lesson index
  - build-handoff.md : "here's everything you need to build/implement this"

The scaffolder does the MECHANICAL part (TLDR skeleton, section summaries,
one-line lesson index, file inventory). The agent then fills in the bolded
takeaways and the build plan from its deep read (never summarize summaries —
read the lesson files themselves). Auto-extracted first lines are prefixed
``[auto] `` so a scaffolded line never looks like a finished takeaway.

Usage:
  python3 make_cliff_notes.py --manifest manifest.json --captured ./captured \
      --out cliff-notes.md

Standard library only.
"""
import argparse
import json
import os
import re
import sys


def first_meaningful_line(md):
    """Return the first non-empty, non-heading, non-image line of a lesson."""
    if not md:
        return ""
    for line in md.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            continue
        if s.startswith("![") or s.startswith("["):
            continue
        if s.startswith("```"):
            continue
        s = re.sub(r"[*_`#>]", "", s).strip()
        if s:
            return s
    return ""


def truncate(s, n=110):
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def read_lesson(mod, captured_dir):
    rel = (mod.get("files") or {}).get("text")
    if not rel:
        return ""
    path = os.path.join(captured_dir, rel)
    if not os.path.exists(path):
        path = rel  # allow absolute
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def build(manifest, captured_dir):
    course = manifest.get("course") or "Course"
    platform = manifest.get("platform") or "unknown"
    sections = manifest.get("sections", [])
    n_lessons = sum(len(s.get("modules", [])) for s in sections)
    n_sections = len(sections)

    # inventory of downloadable files (the deliverables)
    resources = []
    for s in sections:
        for m in s.get("modules", []):
            for r in m.get("resources", []):
                if r.get("url"):
                    resources.append(r.get("name") or r["url"].split("/")[-1])

    lines = []
    A = lines.append
    A("# %s — Cliff Notes" % course)
    A("")
    A("## ⚡ TLDR (30 seconds)")
    A("**What it is:** <one sentence — what the course actually teaches>")
    A("**Who it's for:** <one line>")
    A("**The one big idea:** <the core method / mindset>")
    A("**To build it you need:** <1–2 sentences — the implementation in a nutshell>")
    A("")
    A("## 🗺️ Course at a glance")
    A("**Size:** %d %s · %d %s · %d downloadable %s · platform: %s"
      % (n_sections, "section" if n_sections == 1 else "sections",
         n_lessons, "lesson" if n_lessons == 1 else "lessons",
         len(resources), "file" if len(resources) == 1 else "files",
         platform))
    A("")
    for i, s in enumerate(sections, 1):
        mods = s.get("modules", [])
        A("- **%s** (%d lessons) → <one-line point>" % (s.get("title") or "Section", len(mods)))
    A("")
    A("## 📚 Lesson index")
    if n_lessons > 30:
        # Collapsed index: one line per section, full list moves to the appendix.
        for s in sections:
            mods = s.get("modules", [])
            first = mods[0] if mods else None
            take = first_meaningful_line(read_lesson(first, captured_dir)) if first else ""
            take_label = ("[auto] " + truncate(take)) if take else "<add takeaway>"
            A("- **%s** (%d lessons) → %s"
              % (s.get("title") or "Section", len(mods), take_label))
    else:
        idx = 1
        for s in sections:
            for m in s.get("modules", []):
                take = first_meaningful_line(read_lesson(m, captured_dir))
                take_label = ("[auto] " + truncate(take)) if take else "<add takeaway>"
                A("%d. **%s** — %s" % (idx, m.get("title") or "(untitled)", take_label))
                idx += 1
    A("")
    A("## 🛠️ To build/implement this you need:")
    A("- <tool / step 1>")
    A("- <tool / step 2>")
    A("- <tool / step 3>")
    A("")
    A("## 📦 Files you downloaded")
    if resources:
        for r in resources:
            A("- %s" % r)
    else:
        A("- (none yet — check downloads/ and manual-downloads.txt)")
    if n_lessons > 30:
        A("")
        A("## Appendix: full lesson index")
        idx = 1
        for s in sections:
            A("")
            A("### %s" % (s.get("title") or "Section"))
            for m in s.get("modules", []):
                take = first_meaningful_line(read_lesson(m, captured_dir))
                take_label = ("[auto] " + truncate(take)) if take else "<add takeaway>"
                A("%d. **%s** — %s" % (idx, m.get("title") or "(untitled)", take_label))
                idx += 1
    return "\n".join(lines) + "\n"


def build_handoff(manifest, captured_dir):
    course = manifest.get("course") or "Course"
    sections = manifest.get("sections", [])
    lines = []
    A = lines.append
    A("# %s — Build Handoff" % course)
    A("")
    A("Everything you need to build/implement the thing this course teaches.")
    A("")
    A("## The method (fill from your deep read)")
    A("- <step 1>")
    A("- <step 2>")
    A("- <step 3>")
    A("")
    A("## Per-lesson takeaways (read the lesson files, not the labels)")
    for s in sections:
        A("")
        A("### %s" % (s.get("title") or "Section"))
        for m in s.get("modules", []):
            take = first_meaningful_line(read_lesson(m, captured_dir))
            take_label = ("[auto] " + truncate(take)) if take else "<add takeaway>"
            A("- **%s** — %s" % (m.get("title") or "(untitled)", take_label))
    A("")
    A("## Gaps vs. what already exists")
    A("- <only build the genuine gaps>")
    A("")
    A("## Files")
    A("- manifest.json · captured lessons · downloads/ · transcripts/")
    return "\n".join(lines) + "\n"


def main(argv):
    ap = argparse.ArgumentParser(description="Scaffold cliff notes + build handoff.")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--captured", default="./captured", help="Dir holding captured lesson files")
    ap.add_argument("--out", default="cliff-notes.md", help="Output path for cliff notes")
    args = ap.parse_args(argv)

    with open(args.manifest, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    notes = build(manifest, args.captured)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(notes)

    handoff_path = os.path.join(os.path.dirname(os.path.abspath(args.out)), "build-handoff.md")
    with open(handoff_path, "w", encoding="utf-8") as f:
        f.write(build_handoff(manifest, args.captured))

    print("Wrote %s" % args.out)
    print("Wrote %s" % handoff_path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
