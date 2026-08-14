#!/usr/bin/env python3
"""Resumable, lesson-by-lesson course capture for Skool and Circle.

This is the workhorse. Given a manifest (from skool_tree.js / circle_walk.py),
it walks every lesson and captures text + resource links, tracking progress in
the manifest so a crash loses nothing. Re-run it and it resumes.

Usage:
  # Build a manifest from a raw Skool tree dump (output of skool_tree.js):
  python3 extract_course.py --make-manifest --tree tree.json --platform skool \
      --course "Course Title" --url 'https://www.skool.com/...' --out manifest.json

  # Capture text + resources, lesson by lesson:
  #   Skool -> drive the real logged-in Chrome tab (never headless):
  python3 extract_course.py --manifest manifest.json --out-dir ./captured \
      --platform skool --backend chrome --tab 'skool.com'
  #   Circle -> server-rendered HTML over HTTP with cookies:
  python3 extract_course.py --manifest manifest.json --out-dir ./captured \
      --platform circle --backend http --cookies cookies.txt

  # Test on the first few lessons before the full run:
  ... --limit 3

  # Undo a smoke test — reset every lesson back to pending (and clear files):
  ... --reset

Run long extractions in a BACKGROUND terminal process — they can outlive
short-lived subagent timeouts. Kill and rerun; it resumes from `status`.

Note on downloadable files: a scripted GET often hits CloudFront's signed-URL
wall (403 / ~146-byte MissingKey body). Only the links that FAIL to download
are logged to manual-downloads.txt — chrome-backend resources are all manual
(every one is signed) — click them in the real browser to download.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME_JS = os.path.join(HERE, "chrome_js.py")
LESSON_CAPTURE_JS = os.path.join(HERE, "lesson_capture.js")


# ---------------------------------------------------------------- helpers

def slugify(text):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text or "").strip("-").lower()
    return s or "untitled"


def abs_url(value, base):
    """Return an absolute URL. `value` may be absolute, relative, or empty.

    A bare relative slug must not be stored as the module URL — it can't be
    fetched later. Resolve it against the course URL so the manifest always
    carries absolute URLs.
    """
    value = value or ""
    if not value:
        return base or ""
    parsed = urlparse(value)
    if parsed.scheme and parsed.netloc:
        return value
    return urljoin(base, value) if base else value


def atomic_write_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- manifest

def make_manifest(tree_path, platform, course, url):
    """Build a manifest from a raw tree JSON (skool_tree.js output)."""
    raw = load_json(tree_path)
    nodes = raw.get("nodes", [])
    sections = {}
    for n in nodes:
        sec = n.get("section") or "Course"
        sections.setdefault(sec, []).append({
            "title": n.get("title") or "(untitled)",
            "url": abs_url(n.get("url") or n.get("slug") or url, url),
            "video_url": n.get("videoUrl"),
            "resources": [],
            "status": "pending",
            # "transcript" is reserved — populated by download_transcripts.py if you wire it.
            "files": {"text": None, "transcript": None, "screenshot": None},
        })
    return {
        "platform": platform,
        "course": course,
        "url": url,
        "sections": [{"title": t, "modules": ms} for t, ms in sections.items()],
    }


def iter_modules(manifest):
    for si, section in enumerate(manifest.get("sections", [])):
        for mi, mod in enumerate(section.get("modules", [])):
            yield si, mi, section, mod


# ---------------------------------------------------------------- chrome backend

def run_js(tab_substr, js, js_is_file=False):
    args = [sys.executable, CHROME_JS, tab_substr, "@" + js if js_is_file else js]
    r = subprocess.run(args, capture_output=True, text=True)
    return r.stdout, r.stderr


def chrome_navigate_and_wait(tab_substr, url, timeout=60, poll=2.0):
    """Navigate the live tab, then poll until the lesson body is ready."""
    run_js(tab_substr, "location.href=%r;" % url)
    deadline = time.time() + timeout
    while time.time() < deadline:
        out, _ = run_js(
            tab_substr,
            "document.readyState + '|' + "
            "(document.querySelector('.ProseMirror,article,[contenteditable=true],main') ? '1' : '0')",
        )
        if "complete|1" in out:
            return True
        time.sleep(poll)
    return False


def _normalize_url(u):
    """Strip a trailing slash so URL comparison ignores that cosmetic diff."""
    return (u or "").rstrip("/")


def chrome_capture(tab_substr, url):
    """Navigate to a lesson and capture its markdown + resources via live Chrome.

    Returns a dict with ``markdown``, ``resources``, and ``ok``. ``ok`` is
    False when the page didn't load, the captured URL doesn't match the
    requested lesson URL, or the markdown came back empty — callers must treat
    those as failures and NOT mark the lesson done (a stale/login page must
    never be saved under a new lesson's filename).
    """
    ok = chrome_navigate_and_wait(tab_substr, url)
    out, err = run_js(tab_substr, LESSON_CAPTURE_JS, js_is_file=True)
    if err:
        print("  [warn] chrome stderr:", err, file=sys.stderr)
    try:
        res = json.loads(out)
    except json.JSONDecodeError:
        # out may be an AppleScript error string
        print("  [warn] could not parse capture output; raw:", out[:200], file=sys.stderr)
        res = {"markdown": "", "resources": [], "ok": bool(ok)}
    # lesson_capture.js returns location.href in `url`. Verify it matches the
    # requested lesson URL (ignoring a trailing slash). A mismatch means the
    # tab still shows a previous/login page — not this lesson.
    if not ok:
        res["ok"] = False
    elif _normalize_url(res.get("url")) != _normalize_url(url):
        print("  [warn] captured URL mismatch: requested %s, got %s"
              % (url, res.get("url")), file=sys.stderr)
        res["ok"] = False
    elif not (res.get("markdown") or "").strip():
        print("  [warn] empty markdown for %s" % url, file=sys.stderr)
        res["ok"] = False
    else:
        res["ok"] = True
    return res


# ---------------------------------------------------------------- http backend

class _MD(HTMLParser):
    """Minimal HTML -> markdown for Circle's server-rendered lesson pages."""

    def __init__(self, base_url=None):
        super().__init__()
        self.out = []
        self.skip = 0
        self.block = None  # current block tag
        self.base_url = base_url

    def handle_starttag(self, tag, attrs):
        if self.skip:
            self.skip += 1
            return
        tag = tag.lower()
        if tag in ("script", "style", "noscript"):
            self.skip = 1
            return
        if tag in ("p", "div", "br"):
            self.out.append("\n")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.out.append("\n" + "#" * int(tag[1]) + " ")
        elif tag == "li":
            self.out.append("\n- ")
        elif tag in ("strong", "b"):
            self.out.append("**")
        elif tag in ("em", "i"):
            self.out.append("*")
        elif tag == "a":
            href = dict(attrs).get("href", "")
            if self.base_url and href:
                href = urljoin(self.base_url, href)
            self.out.append("[")
            self._href = href
        elif tag == "img":
            src = dict(attrs).get("src", "") or ""
            alt = dict(attrs).get("alt", "") or ""
            if self.base_url and src:
                src = urljoin(self.base_url, src)
            self.out.append("\n![%s](%s)\n" % (alt, src))
        elif tag in ("pre", "code"):
            self.out.append("`")

    def handle_endtag(self, tag):
        if self.skip:
            self.skip -= 1
            return
        tag = tag.lower()
        if tag in ("strong", "b"):
            self.out.append("**")
        elif tag in ("em", "i"):
            self.out.append("*")
        elif tag == "a":
            href = getattr(self, "_href", "")
            self.out.append("](" + href + ")")
        elif tag in ("pre", "code"):
            self.out.append("`")

    def handle_data(self, data):
        if self.skip:
            return
        self.out.append(data)


def html_to_markdown(html_text, base_url=None):
    p = _MD(base_url=base_url)
    p.feed(html_text)
    text = "".join(p.out)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _cookie_header(url, cookies):
    """Build a Cookie header for `url` from (domain, path, name, value) tuples."""
    if not cookies:
        return ""
    host = urlparse(url).netloc.split(":")[0]
    pairs = [("%s=%s" % (c[2], c[3])) for c in cookies
             if host == c[0].lstrip(".") or host.endswith("." + c[0].lstrip("."))]
    return "; ".join(pairs)


# Keep in sync with scripts/circle_walk.py _CookieSafeRedirect (public-skill
# copies stay self-contained — no cross-file import).
class _CookieSafeRedirect(urllib.request.HTTPRedirectHandler):
    """Follow redirects but strip the Cookie header on any cross-host hop.

    urllib's default redirect handler forwards the original headers (including
    Cookie) to the redirect target even when it lives on a DIFFERENT host. A
    lesson that links to a redirect-to-attacker would then receive the user's
    session cookie. Overriding redirect_request drops Cookie the moment the
    host changes.
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new_req = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new_req is not None:
            old_host = urlparse(req.full_url).netloc.split(":")[0]
            new_host = urlparse(newurl).netloc.split(":")[0]
            if old_host != new_host:
                new_req.remove_header("Cookie")
        return new_req


def _http_fetch_raw(url, cookies):
    """Fetch `url` and return (raw_bytes, final_url), raising on failure.

    Uses a cookie-safe redirect opener (see _CookieSafeRedirect) so the session
    cookie is never forwarded to a different host on a redirect.
    """
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "*/*"}
    header = _cookie_header(url, cookies)
    if header:
        headers["Cookie"] = header
    req = urllib.request.Request(url, headers=headers)
    opener = urllib.request.build_opener(_CookieSafeRedirect())
    with opener.open(req, timeout=30) as resp:
        return resp.read(), resp.geturl()


def http_fetch(url, cookies):
    """Fetch an HTML page and return it as text (utf-8, replacement on error).

    Text-only path for server-rendered lesson HTML. Resource downloads must use
    http_fetch_bytes — decoding then re-encoding would corrupt binary files.
    """
    body, _ = _http_fetch_raw(url, cookies)
    return body.decode("utf-8", "replace")


def http_fetch_bytes(url, cookies):
    """Fetch a resource and return the raw bytes (no decode — binary-safe).

    Use this for ZIP/PDF/MP4/any downloadable file. The raw bytes are written
    straight to disk with "wb", so nothing is text-decoded-and-re-encoded.
    """
    body, _ = _http_fetch_raw(url, cookies)
    return body


def load_cookies_file(path):
    # Keep in sync with scripts/circle_walk.py load_cookies.
    cookies = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) >= 7:
                cookies.append((parts[0], parts[2], parts[5], parts[6]))
    return cookies


def _dedupe_name(path):
    """Return `path` with a -2, -3, ... suffix inserted before the extension if
    a file already exists there. Two resources that sanitize to the same name
    (e.g. two ``workbook.zip`` from different lessons) would otherwise silently
    clobber each other — the ZIPs are the deliverables."""
    if not os.path.exists(path):
        return path
    root, ext = os.path.splitext(path)
    n = 2
    while os.path.exists("%s-%d%s" % (root, n, ext)):
        n += 1
    return "%s-%d%s" % (root, n, ext)


# ---------------------------------------------------------------- capture loop

def capture(manifest, manifest_path, out_dir, platform, backend, tab_substr, cookies,
            limit, want_screenshots):
    os.makedirs(out_dir, exist_ok=True)
    lessons_dir = os.path.join(out_dir, "lessons")
    downloads_dir = os.path.join(out_dir, "downloads")
    screenshots_dir = os.path.join(out_dir, "screenshots")
    manual_file = os.path.join(out_dir, "manual-downloads.txt")
    os.makedirs(lessons_dir, exist_ok=True)
    os.makedirs(downloads_dir, exist_ok=True)
    if want_screenshots:
        os.makedirs(screenshots_dir, exist_ok=True)

    count = 0
    total = sum(len(s.get("modules", [])) for s in manifest.get("sections", []))

    for si, mi, section, mod in iter_modules(manifest):
        if limit is not None and count >= limit:
            break
        if mod.get("status") == "done":
            continue

        sec_dir = os.path.join(lessons_dir, "%02d-%s" % (si + 1, slugify(section["title"])))
        os.makedirs(sec_dir, exist_ok=True)
        fname = "%02d-%s.md" % (mi + 1, slugify(mod["title"]))
        text_path = os.path.join(sec_dir, fname)
        rel_text = os.path.relpath(text_path, out_dir)

        print("[%d/%d] %s / %s" % (count + 1, total, section["title"], mod["title"]))

        markdown = ""
        resources = []
        if backend == "chrome":
            url = mod.get("url") or manifest.get("url")
            res = chrome_capture(tab_substr, url)
            markdown = res.get("markdown", "")
            resources = res.get("resources", [])
            if not res.get("ok") or not (markdown or "").strip():
                print("  [fail] chrome capture failed (URL mismatch or empty) — "
                      "status=failed, will retry on resume")
                mod["status"] = "failed"
                atomic_write_json(manifest_path, manifest)
                continue
        else:  # http
            url = mod.get("url")
            if not url:
                print("  [skip] no url")
                continue
            try:
                html_text = http_fetch(url, cookies)
                markdown = html_to_markdown(html_text, url)
                # scrape resource links from the raw HTML too. Resolve each
                # href against the lesson URL so a relative /pack.zip is an
                # absolute URL before it's stored or downloaded.
                for m in re.finditer(r'<a\b[^>]*href=["\']([^"\']+)["\']', html_text, re.I):
                    href = urljoin(url, m.group(1))
                    if re.search(r"\.(zip|pdf|mp4|mp3|mov|webm|m4a|docx?|xlsx?|pptx?|csv|txt|srt|vtt)(\?|$)", href, re.I):
                        resources.append({"name": href.split("/")[-1].split("?")[0], "url": href})
            except Exception as e:
                print("  [fail] %s" % e)
                mod["status"] = "failed"
                atomic_write_json(manifest_path, manifest)
                continue
            if not (markdown or "").strip():
                print("  [fail] empty markdown (session expiry / login page?) — "
                      "status=failed, will retry on resume")
                mod["status"] = "failed"
                atomic_write_json(manifest_path, manifest)
                continue

        # write text
        if markdown:
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(markdown)
            mod["files"]["text"] = rel_text
        else:
            mod["files"]["text"] = None

        # resources: record each one, then attempt download. Persist a
        # per-resource `downloaded` flag in the manifest so the end-of-run
        # manual-downloads rebuild can key off persisted state (resumable-safe).
        mod["resources"] = resources
        for r in resources:
            r["downloaded"] = False
            if not r.get("url"):
                continue
            if backend == "http" and cookies:
                try:
                    data = http_fetch_bytes(r["url"], cookies)
                    if b"MissingKey" in data:
                        # ~146-byte body = CloudFront signed-URL wall (a 403 in disguise)
                        raise ValueError("signed-URL wall (MissingKey body)")
                    safe = re.sub(r"[^a-zA-Z0-9._-]", "_", r.get("name") or "file")
                    dest = _dedupe_name(os.path.join(downloads_dir, safe))
                    with open(dest, "wb") as f:
                        f.write(data)
                    r["downloaded"] = True
                    print("  [downloaded] %s" % os.path.basename(dest))
                except Exception as e:
                    print("  [manual] %s -> %s" % (r.get("name"), e))
                    # `downloaded` stays False — it will reappear in manual-downloads.txt.
            else:
                # chrome backend: every resource is behind the signed-URL wall,
                # so `downloaded` stays False (never actually downloaded).
                pass

        mod["status"] = "done"
        count += 1
        # save progress after every lesson so a crash loses nothing
        atomic_write_json(manifest_path, manifest)

    # Rebuild manual-downloads.txt from the PERSISTED manifest state, not a
    # transient per-run accumulator. Iterate EVERY lesson (including `done`
    # ones — their resources were captured in an earlier run and still carry
    # their `downloaded` flag) and list every resource whose download did not
    # succeed. This keeps the list cumulative across resumable runs: a resource
    # that 403'd in run 1 stays listed even after its lesson flipped to `done`.
    manual = []
    seen_urls = set()
    for _, _, _, mod in iter_modules(manifest):
        title = mod.get("title", "")
        for r in mod.get("resources", []):
            url = r.get("url") or ""
            if r.get("downloaded") is True:
                continue
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            manual.append("%s\t%s\t%s" % (title, r.get("name", ""), url))

    with open(manual_file, "w", encoding="utf-8") as f:
        f.write("# Click these in the real logged-in browser (signed URLs):\n")
        if manual:
            f.write("\n".join(manual))
            f.write("\n")
    if manual:
        print("Wrote %d resource links to %s (click signed-URL ones manually)"
              % (len(manual), manual_file))
    else:
        print("No manual downloads; %s refreshed (empty)." % manual_file)

    return count


# ---------------------------------------------------------------- main


def main(argv):
    ap = argparse.ArgumentParser(description="Resumable course capture (Skool + Circle).")
    ap.add_argument("--make-manifest", action="store_true",
                    help="Build a manifest from a raw tree JSON, then exit")
    ap.add_argument("--tree", help="Raw tree JSON (skool_tree.js output) for --make-manifest")
    ap.add_argument("--course", help="Course title (for --make-manifest)")
    ap.add_argument("--url", help="Course URL (for --make-manifest)")
    ap.add_argument("--out", help="Manifest output path (for --make-manifest)")

    ap.add_argument("--manifest", help="Manifest JSON to capture from")
    ap.add_argument("--out-dir", default="./captured", help="Where captured files go")
    ap.add_argument("--platform", choices=["skool", "circle"], help="Platform")
    ap.add_argument("--backend", choices=["chrome", "http"], help="chrome (Skool) or http (Circle)")
    ap.add_argument("--tab", help="URL substring of the live Chrome tab (chrome backend)")
    ap.add_argument("--cookies", help="cookies.txt path (http backend)")
    ap.add_argument("--limit", type=int, help="Only process this many pending lessons")
    ap.add_argument("--reset", action="store_true",
                    help="Reset every lesson to pending (and clear files) before capture")
    ap.add_argument("--screenshots", action="store_true", help="Reserve a screenshots dir")
    args = ap.parse_args(argv)

    if args.make_manifest:
        if not (args.tree and args.platform):
            ap.error("--make-manifest needs --tree and --platform")
        m = make_manifest(args.tree, args.platform, args.course or "Course",
                          args.url or "")
        out = args.out or "manifest.json"
        atomic_write_json(out, m)
        print("Wrote manifest to %s" % out)
        return 0

    if not args.manifest:
        ap.error("provide --manifest (or --make-manifest)")
    manifest = load_json(args.manifest)

    if not args.backend:
        ap.error("--manifest requires --backend (chrome or http)")
    if args.backend == "chrome" and not args.tab:
        ap.error("--backend chrome needs --tab (URL substring of the live tab)")
    if args.reset:
        n_reset = 0
        for _, _, _, mod in iter_modules(manifest):
            mod["status"] = "pending"
            mod["files"] = {"text": None, "transcript": None, "screenshot": None}
            n_reset += 1
        atomic_write_json(os.path.abspath(args.manifest), manifest)
        print("Reset %d lessons to pending (files cleared)." % n_reset)
    cookies = load_cookies_file(args.cookies) if (args.backend == "http" and args.cookies) else []

    n = capture(manifest, os.path.abspath(args.manifest), args.out_dir,
                args.platform or manifest.get("platform"),
                args.backend, args.tab, cookies, args.limit, args.screenshots)
    print("Done. Captured %d lessons in this run." % n)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
