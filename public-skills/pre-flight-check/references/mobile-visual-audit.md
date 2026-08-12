# Mobile Visual Audit

How to verify pages at true phone width when headless Chrome fights you.

## Why a harness is needed

Headless Chrome on macOS enforces a ~500px minimum window width. Asking for `--window-size=390,...` silently gives you a 500px render, so overflow that breaks a real phone looks fine. To audit true 390px rendering, embed the page in a 390px iframe inside a wider host page and screenshot the host.

## The harness file

Save as `mobile-harness.html` anywhere reachable by `file://`:

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; background: #111; }
  iframe { width: 390px; height: 16000px; border: 0; display: block; margin: 0 auto; }
</style>
</head>
<body>
<iframe id="f"></iframe>
<script>
  document.getElementById('f').src = decodeURIComponent(location.hash.slice(1));
</script>
</body>
</html>
```

The iframe reads its target URL from `location.hash`, so one harness file audits any page.

## Screenshot command

```
"<chrome binary>" --headless=new --disable-gpu --hide-scrollbars \
  --force-prefers-reduced-motion \
  --window-size=500,16200 \
  --screenshot=out.png \
  --virtual-time-budget=15000 \
  "file:///path/to/mobile-harness.html#http://localhost:PORT/page.html"
```

- Window is 500px wide (Chrome's floor); the audited page lives in the center 390px.
- `--force-prefers-reduced-motion` is REQUIRED. Under `--virtual-time-budget`, CSS entrance animations freeze in their delay phase (opacity: 0, transform offset), hiding words and producing false "missing text" findings. Reduced motion short-circuits those animations to their final state.
- Raise `--virtual-time-budget` if the page lazy-loads content; a too-small budget captures a half-rendered page.

## Reading the capture back

The PNG is ~500x16200. Do not eyeball the whole thing downscaled — slice it into strips and view every strip at full size:

```python
from PIL import Image
img = Image.open('out.png')
w, h = img.size
strip = 1800
for i, y in enumerate(range(0, h, strip)):
    img.crop((0, y, w, min(y + strip, h))).save(f'strip_{i:02d}.png')
```

Content occupies the center 390px of the 500px shot (roughly x=55 to x=445 with the default centered harness). Read all strips, not just the top — cut-off bugs usually hide mid-page.

## Fast programmatic alternative

When you only need "does anything overflow", skip screenshots. Serve a temporary `_audit.html` from the same origin as the site (same `localhost:PORT` server), which iframes each page at 390px and reports offenders:

```html
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
<pre id="out">RUNNING</pre>
<script>
const pages = ['index.html']; // EDIT: list every page to audit
const W = 390;
function audit(src) {
  return new Promise(resolve => {
    const f = document.createElement('iframe');
    f.style.cssText = `width:${W}px;height:2000px;border:0`;
    f.src = src;
    f.onload = () => setTimeout(() => {
      const doc = f.contentDocument;
      const lines = [src + ':'];
      let flagged = [];
      if (doc.documentElement.scrollWidth > W + 1)
        lines.push('  PAGE: horizontal scroll, scrollWidth=' + doc.documentElement.scrollWidth);
      for (const el of doc.querySelectorAll('*')) {
        const r = el.getBoundingClientRect();
        if (!r.width || !r.height) continue;
        if (r.right > W + 1 || r.left < -1) {
          // dedupe: skip if an ancestor was already flagged
          if (flagged.some(a => a.contains(el))) continue;
          flagged.push(el);
          const cls = String(el.className).split(' ')[0] || '';
          lines.push(`  ${el.tagName}.${cls} left=${Math.round(r.left)} right=${Math.round(r.right)}`);
        }
      }
      if (lines.length === 1) lines.push('  OK');
      f.remove();
      resolve(lines.join('\n'));
    }, 1500);
    document.body.appendChild(f);
  });
}
(async () => {
  const out = [];
  for (const p of pages) out.push(await audit(p));
  document.getElementById('out').textContent = out.join('\n\n');
})();
</script>
</body>
</html>
```

Read the report with:

```
"<chrome binary>" --headless=new --disable-gpu \
  --force-prefers-reduced-motion --virtual-time-budget=15000 \
  --dump-dom "http://localhost:PORT/_audit.html" | sed -n '/<pre/,/<\/pre>/p'
```

Delete `_audit.html` afterward — it is scaffolding, not deliverable.

## Common mobile cut-off culprits

- **Fixed aspect-ratio boxes with `overflow: hidden`** — content scaled for desktop gets cropped inside the box. Give the box a min-height or relax the ratio on small screens.
- **Nowrap terminal/code lines** — long URLs and commands overflow silently. Fix: `overflow-wrap: anywhere` plus `<wbr>` at URL slash boundaries so breaks land in sensible places.
- **Absolute-centered elements with leftover `left`/`top` offsets under flex media queries** — the media query switches the container to flex but the child's absolute offsets remain, pushing it off-screen. Reset `position`, `left`, and `top` in the breakpoint.
- **Hover transforms that re-crop uncropped images** — a `scale()` on hover re-triggers cropping inside an `overflow: hidden` frame. Test hover states too, or bound the transform.
