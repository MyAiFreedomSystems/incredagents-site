#!/usr/bin/env python3
"""Walk a Circle.so course tree into a manifest.

Circle pages are SERVER-RENDERED HTML, so this works over plain HTTP once you
give it the user's session cookies. (Skool is different — see skool_tree.js.)

Usage:
  # Live fetch with a Netscape-format cookies.txt:
  python3 circle_walk.py --url 'https://YOUR.circle.so/c/community/post/...' \
      --cookies cookies.txt --out manifest.json

  # Parse a saved HTML file (save the course page in the real browser first):
  python3 circle_walk.py --html saved_page.html --url 'https://YOUR.circle.so/...' \
      --out manifest.json

How to get cookies.txt (choose one):
  - a browser extension that exports "cookies.txt" (Netscape format), or
  - a cookie-export library (e.g. the `browser_cookie3` pip package on macOS/Chrome).

Standard library only. `requests` is optional — falls back to urllib.

Note on video_url: Circle manifests do NOT populate video_url. The course tree
page lists lesson links but not each lesson's embedded video — the player lives
on the individual lesson page, which this walker does not fetch. Pull videos
per-lesson in Step 4 (yt-dlp on the lesson page's Wistia/Vimeo iframe or
<video src> URL) instead.
"""
import argparse
import html as htmlmod
import json
import re
import sys
from urllib.parse import urljoin, urlparse

import urllib.request

try:
    import requests  # optional, nicer
except ImportError:
    requests = None


# ---------------------------------------------------------------- cookies

def load_cookies(path):
    """Parse a Netscape-format cookies.txt into a list of (domain, path, name, value)."""
    # Keep in sync with scripts/extract_course.py load_cookies_file.
    cookies = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) >= 7:
                domain, _flag, cpath, _secure, _expires, name, value = parts[:7]
                cookies.append((domain, cpath, name, value))
    return cookies


def cookie_header(url, cookies):
    """Build a Cookie header for `url` from the parsed cookies."""
    host = urlparse(url).netloc.split(":")[0]
    pairs = []
    for domain, cpath, name, value in cookies:
        d = domain.lstrip(".")
        if host == d or host.endswith("." + d):
            pairs.append("%s=%s" % (name, value))
    return "; ".join(pairs)


# ---------------------------------------------------------------- fetch

def _host_of(url):
    return urlparse(url).netloc.split(":")[0]


# Keep in sync with scripts/extract_course.py _CookieSafeRedirect (public-skill
# copies stay self-contained — no cross-file import).
class _CookieSafeRedirect(urllib.request.HTTPRedirectHandler):
    """Follow redirects but strip the Cookie header on any cross-host hop.

    urllib's default redirect handler forwards the original headers (including
    Cookie) to the redirect target even when it lives on a DIFFERENT host. A
    Circle tree page that redirects to an external host would then receive the
    user's session cookie. Overriding redirect_request drops Cookie the moment
    the host changes.
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new_req = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new_req is not None:
            if _host_of(req.full_url) != _host_of(newurl):
                new_req.remove_header("Cookie")
        return new_req


def fetch(url, cookies):
    """Return (html, final_url). Raises on failure.

    Redirects are followed without leaking the session Cookie to a different
    host: the requests path disables auto-redirects and follows manually (drop
    Cookie on each cross-host hop), and the urllib fallback uses a
    _CookieSafeRedirect opener that does the same.
    """
    header = cookie_header(url, cookies) if cookies else ""
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "text/html"}
    if header:
        headers["Cookie"] = header
    if requests is not None:
        current = url
        hdrs = dict(headers)
        for _ in range(30):
            r = requests.get(current, headers=hdrs, timeout=30, allow_redirects=False)
            r.raise_for_status()
            if not r.is_redirect:
                return r.text, r.url
            location = r.headers.get("Location")
            if not location:
                return r.text, r.url
            nxt = urljoin(current, location)
            if _host_of(nxt) != _host_of(current):
                hdrs = {k: v for k, v in hdrs.items() if k.lower() != "cookie"}
            current = nxt
        raise RuntimeError("too many redirects")
    opener = urllib.request.build_opener(_CookieSafeRedirect())
    req = urllib.request.Request(url, headers=headers)
    with opener.open(req, timeout=30) as resp:
        body = resp.read()
        return body.decode("utf-8", "replace"), resp.geturl()


# ---------------------------------------------------------------- parsing

LINK_RE = re.compile(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', re.I | re.S)
LESSON_HINT = re.compile(r'post|lesson|module|unit|watch|learn|course|chapter', re.I)
# Non-lesson paths that LESSON_HINT would otherwise match (nav, bios, help).
NON_LESSON_PATH = re.compile(r'/(help|settings|profile|discussion|chat|members)(/|$)', re.I)
TAG_RE = re.compile(r"<[^>]+>")


def text_of(inner):
    t = TAG_RE.sub(" ", inner)
    t = htmlmod.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def extract_links(html, base_url):
    """Extract lesson-looking anchor links -> list of (title, url)."""
    links = []
    seen = set()
    for m in LINK_RE.finditer(html):
        href, inner = m.group(1), m.group(2)
        if href.startswith("#") or href.startswith("javascript:"):
            continue
        title = text_of(inner)
        url = urljoin(base_url, href)
        if not title or url in seen:
            continue
        if NON_LESSON_PATH.search(url):
            continue
        if LESSON_HINT.search(url) or LESSON_HINT.search(title):
            seen.add(url)
            links.append((title, url))
    return links


# ---------------------------------------------------------------- main

def main(argv):
    ap = argparse.ArgumentParser(description="Walk a Circle.so course tree into a manifest.")
    ap.add_argument("--url", help="Circle course/community URL (base for relative links)")
    ap.add_argument("--html", help="Path to a saved HTML file to parse instead of fetching")
    ap.add_argument("--cookies", help="Netscape cookies.txt (for live fetch)")
    ap.add_argument("--out", default="manifest.json", help="Output manifest path")
    ap.add_argument("--course", default="Circle Course", help="Course title for the manifest")
    args = ap.parse_args(argv)

    if args.html:
        with open(args.html, "r", encoding="utf-8") as f:
            page = f.read()
        base_url = args.url or "https://example.circle.so/"
    elif args.url:
        page, base_url = fetch(args.url, load_cookies(args.cookies) if args.cookies else [])
    else:
        ap.error("provide --url or --html")

    links = extract_links(page, base_url)

    # Group into a single section; refine section grouping manually if needed.
    manifest = {
        "platform": "circle",
        "course": args.course,
        "url": base_url,
        "sections": [
            {
                "title": "Course",
                "modules": [
                    {"title": t, "url": u, "video_url": None,  # Circle tree pages don't carry the video — see docstring + Step 4
                     "resources": [], "status": "pending",
                     "files": {"text": None, "transcript": None, "screenshot": None}}
                    for t, u in links
                ],
            }
        ],
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print("Wrote %d lessons to %s" % (len(links), args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
