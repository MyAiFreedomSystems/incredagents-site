#!/usr/bin/env python3
"""Scan a skill folder for personal data that must not ship publicly.

Checks every text file for:
  - absolute user paths (/Users/<name>, /home/<name>, C:\\Users\\<name>)
  - the current machine's home directory, username, and hostname (literal matches)
  - email addresses
  - private IPv4 addresses and localhost-with-port URLs
  - common credential patterns (API keys, tokens, sk-..., ghp_..., etc.)

Exit 0 = clean, 1 = findings, 2 = usage error.
Findings print as  file:line: [rule] matched-text  so they are easy to fix.

Usage:
  python3 scrub_personal.py <skill-dir> [--allow name1,name2,...]

--allow lists extra literal strings to ignore (e.g. a public brand name).
"""
import os
import platform
import re
import sys

TEXT_EXT = {
    ".md", ".txt", ".py", ".sh", ".js", ".ts", ".json", ".yaml", ".yml",
    ".html", ".css", ".csv", ".toml", ".cfg", ".ini", ".xml", ".env",
    ".example", ".sample",
}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "releases"}
# The scanner's own source contains the patterns it looks for; never self-scan.
SKIP_FILES = {"scrub_personal.py"}

RULES = [
    ("user-path", re.compile(r"(/Users/|/home/|[A-Z]:\\\\Users\\\\)[^/\s\\\"']+")),
    ("email", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("private-ip", re.compile(r"\b(10\.\d{1,3}|172\.(1[6-9]|2\d|3[01])|192\.168)\.\d{1,3}\.\d{1,3}\b")),
    ("localhost-url", re.compile(r"https?://(localhost|127\.0\.0\.1)(:\d+)?")),
    ("secret-token", re.compile(r"\b(sk-[A-Za-z0-9]{12,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|xox[bap]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16})\b")),
    ("api-key-assignment", re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}")),
]

# Obvious non-personal addresses that the email rule should not flag.
EMAIL_ALLOWLIST = {"example.com", "example.org", "example.net", "email.com", "domain.com"}


def personal_literals():
    """Build literal strings unique to this machine/user."""
    lits = set()
    home = os.path.expanduser("~")
    user = os.path.basename(home.rstrip(os.sep)) or os.environ.get("USER", "")
    host = platform.node()
    for v in (home, user, host):
        if v and len(v) >= 3:
            lits.add(v)
    return lits


def iter_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in sorted(filenames):
            if fn in SKIP_FILES:
                continue
            path = os.path.join(dirpath, fn)
            ext = os.path.splitext(fn)[1].lower()
            if ext and ext not in TEXT_EXT:
                continue  # binary or unknown: skip content scan
            yield path


def scan(root, allow):
    findings = []
    literals = [l for l in personal_literals() if l not in allow]
    for path in iter_files(root):
        try:
            with open(path, "r", encoding="utf-8", errors="strict") as f:
                lines = f.readlines()
        except (UnicodeDecodeError, OSError):
            continue
        rel = os.path.relpath(path, root)
        for i, line in enumerate(lines, 1):
            if "<your-" in line or "YOUR_" in line:
                continue  # placeholder lines in templates/docs are fine
            for lit in literals:
                if lit in line:
                    findings.append((rel, i, "personal-literal", lit))
            for name, rx in RULES:
                for m in rx.finditer(line):
                    hit = m.group(0)
                    if name == "email" and hit.split("@", 1)[1].lower() in EMAIL_ALLOWLIST:
                        continue
                    if hit in allow:
                        continue
                    findings.append((rel, i, name, hit))
    return findings


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    root = argv[1]
    allow = set()
    if "--allow" in argv:
        i = argv.index("--allow")
        if i + 1 < len(argv):
            allow = {a.strip() for a in argv[i + 1].split(",") if a.strip()}
    if not os.path.isdir(root):
        print(f"error: not a directory: {root}")
        return 2
    findings = scan(root, allow)
    if not findings:
        print(f"CLEAN: no personal data found in {root}")
        return 0
    print(f"FOUND {len(findings)} potential personal-data item(s) in {root}:\n")
    for rel, line, rule, hit in findings:
        shown = hit if len(hit) <= 60 else hit[:57] + "..."
        print(f"  {rel}:{line}: [{rule}] {shown}")
    print("\nNothing ships until every line above is resolved or allow-listed.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
