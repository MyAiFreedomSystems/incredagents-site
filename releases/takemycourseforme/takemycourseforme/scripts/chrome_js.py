#!/usr/bin/env python3
"""Run JavaScript inside the user's already-open, already-logged-in Chrome tab.

Usage:
  python3 chrome_js.py '<url-substring>' '<js-expression>'
  python3 chrome_js.py '<url-substring>' '@path/to/payload.js'

Finds the Chrome tab whose URL contains <url-substring>, runs the JavaScript in
that tab, and prints the result to stdout.

WHY THIS EXISTS: Skool and Circle sit behind login + CloudFront signed URLs.
Only JavaScript running in the REAL logged-in session can read them. A headless
browser gets a 403 on every asset. Drive the real browser instead.

macOS only (shells out to osascript / AppleScript). For other platforms use an
equivalent "run JS in the real browser" mechanism — the rule is the same:
real session, never headless.

Note: if more than one Chrome tab's URL matches the substring you pass, the
FIRST match is driven and a warning listing every match is printed to stderr —
close stray course tabs first so the wrong tab is never hijacked.
"""
import subprocess
import sys


def js_on_tab(url_substr, js):
    """Run `js` in the first Chrome tab whose URL contains url_substr.

    When more than one tab matches the substring, a warning listing every
    matching URL is logged to stderr (a stray Skool/Circle tab could otherwise
    be hijacked). The FIRST matching tab is still the one driven.

    Returns (stdout, stderr) as strings. On an osascript timeout (e.g. a hung
    Chrome tab), stderr carries a clear failure message and stdout is empty.
    """
    # Escape for embedding inside an AppleScript double-quoted string.
    # AppleScript escaping: backslash then double-quote; newlines become \n.
    esc_js = (
        js.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "")
    )
    esc_sub = url_substr.replace("\\", "\\\\").replace('"', '\\"')
    # Collect every matching tab, keep the first, and `log` a warning (which
    # osascript routes to stderr) when more than one matches.
    script = (
        'tell application "Google Chrome"\n'
        '  set firstTab to missing value\n'
        '  set matchURLs to {}\n'
        '  repeat with w in windows\n'
        '    repeat with t in tabs of w\n'
        f'      if (URL of t) contains "{esc_sub}" then\n'
        '        if firstTab is missing value then set firstTab to t\n'
        '        set end of matchURLs to (URL of t)\n'
        '      end if\n'
        '    end repeat\n'
        '  end repeat\n'
        '  if firstTab is missing value then\n'
        '    return "__NOT_FOUND__"\n'
        '  end if\n'
        '  if (count of matchURLs) > 1 then\n'
        '    log "MULTI-TAB WARNING: " & (count of matchURLs) & " tabs matched, driving the first"\n'
        '    repeat with u in matchURLs\n'
        '      log "  tab: " & u\n'
        '    end repeat\n'
        '  end if\n'
        f'  return (execute firstTab javascript "{esc_js}")\n'
        'end tell\n'
    )
    try:
        r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        return "", "osascript timed out after 30s (hung Chrome tab? re-check the page and retry)"
    return r.stdout.strip(), r.stderr.strip()


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    url_substr = argv[1]
    js = argv[2]
    if js.startswith("@"):
        with open(js[1:], "r", encoding="utf-8") as f:
            js = f.read()
    out, err = js_on_tab(url_substr, js)
    if out == "__NOT_FOUND__":
        # Print the sentinel to stderr (not stdout) so a `> tree.json` redirect
        # never writes the error sentinel into a data file, and exit non-zero
        # so callers can tell the tab lookup failed.
        print("__NOT_FOUND__", file=sys.stderr)
        return 1
    if err:
        # stderr carries either a multi-tab warning (non-fatal — stdout still
        # holds the JS result) or a real osascript error/timeout (fatal — no
        # stdout). Emit it either way, but only fail when there's no result.
        print(err, file=sys.stderr)
        if not out:
            return 1
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
