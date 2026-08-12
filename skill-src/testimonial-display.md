---
name: testimonial-display
description: >-
  Place testimonials on websites and sales pages for maximum trust and
  conversion. Use when placing testimonials on a page, building a wall of
  love, adding a testimonial slider or carousel, deciding where social proof
  goes on a sales page, designing a testimonial section layout, choosing
  between grid/masonry/slider/video embed/star-rating snippet patterns,
  interleaving testimonials through long-form copy, or auditing testimonial
  placement for accessibility, performance, and authenticity.
---

# Testimonial Display

You have real testimonials (collected, harvested, or turned into cards). This
skill answers the next question: **where and how do they go on the page** so
they build trust and lift conversion instead of becoming decoration nobody
reads.

Full per-pattern detail lives in `references/pattern-library.md`. Research
sources and takeaways live in `references/research-notes.md`. A working
self-contained demo of three core patterns lives in
`examples/testimonial-patterns.html`.

## The pattern library (quick map)

| Pattern | One-line use |
|---|---|
| Featured single (hero proof) | One strong quote near the hero or a key CTA |
| Interleaved singles through copy | Singles placed at the exact section arguing that point |
| Wall of love grid | Many cards in a uniform grid; volume = trust |
| Masonry collage | Mixed-length quotes, social-feed feel |
| Auto-advancing slider | Rarely; only with full pause/keyboard controls |
| Static carousel (manual controls) | Space-saving rotation, user-driven |
| Video embed block | Highest-credibility proof; one per key section |
| Star-rating + count snippet | Compact aggregate proof near CTAs and titles |
| Pull-quote inline | One sentence lifted inside body copy |
| Popup / exit-intent | Last resort; high annoyance risk — see cautions |

## PATTERN SELECTION GUIDE (page type x goal)

- **Long-form sales page / sales letter:** slider or featured single near the
  top (first screenful gets most attention), then **singles interleaved at
  relevance points** through the copy, then a **wall of love near the close**
  (price / final CTA) to handle the "does this work for people like me?"
  objection. Optional star snippet beside each CTA.
- **SaaS / product homepage:** logo strip or star snippet under the hero,
  featured single after the first value-prop block, wall of love or masonry
  lower down, single quote beside the pricing CTA.
- **E-commerce product page:** star-rating + count snippet at the product
  title, customer quotes near "Add to cart", photo/video proof in the
  description zone. No sliders above the fold.
- **Service / agency site:** featured single on the homepage, interleaved
  singles inside each service section, full wall on a dedicated proof page
  linked from nav.
- **Landing page (one offer, one CTA):** one featured single under the hero
  claim, 1–3 interleaved singles before each repeated CTA, nothing else.
  Every element must serve the single conversion goal.
- **Email capture / lead magnet page:** one short, specific single + star
  snippet. Keep it light; the page is short.
- **Dedicated testimonials page:** wall of love or masonry, filterable by
  topic if you have 20+, video embeds at the top.

## RELEVANCE MATCHING (the core method)

Never place testimonials randomly. For each placement:

1. **Read each testimonial and tag its topic**: what objection, fear, result,
   or use case does it speak to? ("was skeptical it'd work for a small shop",
   "setup took one afternoon", "paid for itself in a month").
2. **Map page sections to the objection they argue.** A section about ease of
   setup argues "this won't be hard". A pricing section raises "is it worth
   the money?".
3. **Place each testimonial at the section arguing the same point.** Setup
   testimonial goes in the setup section. ROI testimonial goes beside pricing.
4. **Match the reader, not just the topic** when you can segment: a quote
   from a plumber converts plumbers better than a quote from a CEO.
5. Leftover testimonials that match no section go to the wall near the close —
   never forced into a section they don't support.

## Mobile rules

- Walls and grids collapse to a single column; 2 columns max on tablets.
- Sliders must support swipe, but swipe must never be the only control —
  visible prev/next buttons remain.
- Keep tap targets (slider controls, "read more", video play) at least
  44 x 44 px.
- Video embeds: thumbnail with play button, load the player only on tap.
- Testimonial text minimum 16px; long quotes get a "read more" clamp, not
  tiny text.
- Attention concentrates at the top on mobile even more than desktop: the
  first proof element must appear within the first two screenfuls.

## Accessibility requirements (non-negotiable for sliders/carousels)

- **No auto-play traps.** Auto-advancing content must have a visible
  pause/stop control (WCAG 2.2.2), must pause on hover and on keyboard focus,
  and must not auto-advance at all when the user prefers reduced motion
  (`prefers-reduced-motion`).
- **Keyboard operable:** prev/next buttons reachable and usable via Tab and
  Enter/Space; visible focus styles.
- **Semantics:** labelled region (`role="region"` + `aria-label` or a heading
  such as "What customers say"), slides as list items.
- **No-JS fallback:** without JavaScript, the first slide (or all slides,
  stacked) must be visible. Never render an empty box without JS.
- Screen readers: announce slide changes politely or not at all — never
  interrupt with `aria-live="assertive"`.
- Star ratings: expose as text ("Rated 4.8 out of 5 from 212 reviews"), not
  star glyphs alone.

## Performance rules

- Lazy-load testimonial images and all video embeds (`loading="lazy"`,
  facade thumbnails for video).
- Always set `width`/`height` (or `aspect-ratio`) on photos and embeds so
  walls don't cause layout shift (CLS) as cards load.
- Walls render fine with plain CSS grid/columns — you do not need a JS
  masonry library for most testimonial layouts.
- If using a third-party embed widget (Testimonial.to, Senja, Famewall),
  load its script `async`/`defer` and keep it out of the critical rendering
  path; weigh its JS cost against a hand-rolled static wall, which is faster
  and fully under your control.
- Prefer real text over card images when possible: text is searchable,
  selectable, translatable, and cheaper. Use card images (e.g. from a
  graphics pipeline) when brand consistency matters more.

## TRUST RULES (hard constraints)

- **Real only.** Use real names, real photos, real companies, real sources.
  Never invent a testimonial, never "merge" two people's words, never write
  a quote and attribute it to a customer.
- **No laundering.** A quote from a public video or post may be displayed
  with attribution to its source; do not strip context to make it say
  something the person didn't.
- **Link to the source when public** (video timestamp, post URL, review
  site). Verifiability is what makes social proof credible.
- **Mark edits honestly.** Condensed or trimmed quotes should be indicated
  (ellipsis, or "edited for length"). Never change meaning.
- Placeholder/demo content must be visibly marked as example filler — never
  ship fake quotes to a production page.
- Get permission for photos and full names when the source wasn't a public
  review.

## Placement checklist

Run through this before shipping:

- [ ] First proof element appears within the first two screenfuls
- [ ] Every CTA has proof on the same screen or adjacent to it
- [ ] Each interleaved testimonial's topic matches the section it sits in
- [ ] No testimonial is random filler; each answers a specific objection
- [ ] Wall/grid collapses cleanly to one column on mobile
- [ ] Slider (if any) has visible controls, pause on hover/focus, keyboard
      nav, reduced-motion respect, and a no-JS fallback
- [ ] All images lazy-loaded and sized; no layout shift
- [ ] Every quote is real, attributed, and source-linked where public
- [ ] Condensed quotes marked; no invented or merged quotes
- [ ] Star ratings exposed as text for screen readers
- [ ] Total testimonial count > 1 on money pages (multiple beats single)
