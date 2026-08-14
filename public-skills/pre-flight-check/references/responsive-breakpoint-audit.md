# Responsive Breakpoint Audit

The gap between "works at desktop" and "works at 390px" is where layout bugs
live. This reference is the sweep method, the geometry snippets, and the three
CSS traps that cause mid-width breakage. Pair with `mobile-visual-audit.md`
for the true-phone-width harness.

## The sweep: test the widths that break, not the widths that are canonical

Canonical widths (1440 / 390) miss the danger zone. Build the test list from
the stylesheet itself:

```bash
grep -oE "max-width: *[0-9]+px|min-width: *[0-9]+px" styles.css | sort -u
```

For every breakpoint value B found, test: **B−1, B, B+1**. Then add 390, a
mid-width inside every gap between consecutive breakpoints (e.g. breakpoints
at 720 and 960 → test ~840), and the owner's actual window width when known.
A page that passes at 390 and 1440 can still be broken at 690 — this is the
single most common "but it worked on my screen" failure.

At every width, check three things:

1. **Horizontal overflow**: `document.documentElement.scrollWidth <= innerWidth`
2. **Overlap**: rectangle-intersection tests (snippet below) between every
   absolutely-positioned or decorative element and every text/button/card element
3. **Visibility**: every chip, button, and heading is inside the viewport when
   scrolled to, unobstructed

## Geometry beats eyeballs

Run inside the page (any evaluate/console mechanism). Returns every offender:

```js
function rectsOverlap(a, b) {
  return a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;
}
const floaters = [...document.querySelectorAll('img, .decoration, [class*="float"], [class*="bot"]')]
  .filter(el => ['absolute', 'fixed'].includes(getComputedStyle(el).position));
const protectedEls = [...document.querySelectorAll('h1, h2, p, a, button, .chip')];
const hits = [];
for (const f of floaters) for (const p of protectedEls) {
  const fr = f.getBoundingClientRect(), pr = p.getBoundingClientRect();
  if (rectsOverlap(fr, pr)) hits.push(`${f.className} covers ${p.tagName}.${p.className} "${(p.textContent||'').slice(0,40)}"`);
}
hits.length ? hits : 'NO OVERLAPS';
```

For narrow widths, iframe the page at exact width (see `mobile-visual-audit.md`)
and run this against `iframe.contentDocument`.

## Trap 1 — mismatched breakpoints (the overlap band)

When a container switches to a stacked layout at breakpoint B (flex-column,
tiles go `position: static`), every child that was absolutely positioned must
switch to static at **the same B**. If the child switches at a smaller
breakpoint (e.g. container stacks at 720px, child un-pins at 640px), widths
641–720 render the child floating dead-center over the stacked content.

Audit: for each `@media` block that changes a container's `display` or
`position` scheme, list the child selectors it affects and confirm each child
has a rule at the same breakpoint. Fix by moving the child's override to the
container's breakpoint — never by adding a third breakpoint.

## Trap 2 — transform-centering vs. animation

An element centered with `transform: translate(-50%, -50%)` loses its
centering the moment any animation or keyframe writes `transform` — the
animated value replaces the centering value, and the element jumps to a
corner or drifts.

Fixes, in order of preference:

1. Animate a different property: `margin-top: 0 → -14px` keyframes give the
   same bob without touching `transform`.
2. Wrap it: outer element owns `translate(-50%,-50%)`, inner element owns the
   transform animation.

## Trap 3 — frozen frames in a real browser

An occluded or background tab freezes CSS transitions mid-flight. Computed
styles report the final state while the paint shows a stale or blank frame —
so a screenshot can "prove" an element is missing when it is not.

- Always take **two screenshots 2–3 seconds apart** before judging anything.
- Never declare an element missing, invisible, or broken from a single capture.
- If the two captures disagree, bring the tab to the front and reshoot.
- (Headless Chrome has the sibling trap — entrance animations frozen under
  `--virtual-time-budget`; see `mobile-visual-audit.md`.)

## QA subagent acceptance criteria

When dispatching a reviewer, give measurable criteria, not "look it over":
exact viewport widths to test, the element list that must not overlap, pixel
tolerances (e.g. "centered within 5px"), and the requirement to attach
geometry measurements and screenshot paths as evidence. A review without
numbers is an opinion, not a gate.
