---
name: graphic-testimonials
description: Create branded testimonial card images from quotes and photos — via the user's Canva template (duplicate, edit text with Canva MCP transactions, export PNG) or the bundled standalone HTML template rendered with headless Chrome. Then recolor to the brand color, composite circular client photos, and wire cards into a web page. Use when the user asks to make, design, or update testimonial cards/graphics/images, or to add social-proof sections to a page. Input is harvested material (quote + name + role + face per client), e.g. from harvest-testimonials.
---

# Graphic Testimonials

Makes the images. Takes quote + name + role (+ optional face) per client and produces branded square cards wired into a site. Fully standalone — all brand inputs come from a config, not from this skill.

## Inputs (collect before starting)

Check the project for a `brand.json` (schema: [references/brand-config.md](references/brand-config.md)). If none, ask the user for:

1. **Template**: a Canva design ID of a single-card template they own, OR use `assets/card-template.html` (no Canva needed).
2. **Brand color** for the card background (hex), plus text/accent/ring colors.
3. **Site target**: HTML file, grid CSS class, image naming, git repo if any.
4. **Copy rules**: banned words, tone, section heading.

## Card source A — Canva (preferred when the user has a template)

1. `copy-design` (use `page_numbers` for one card). NEVER edit the user's original.
2. `start-editing-transaction` → `perform-editing-operations` → `commit-editing-transaction`:
   - Read element IDs from the transaction response; never guess. Store stable suffixes in `brand.json`.
   - Fixed pages: `replace_text`. Responsive pages: `find_and_replace_text` ONLY.
   - Before deleting/replacing any photo, call `get-assets` on every fill asset ID and view thumbnails — stacked shapes can hide stock photos behind client photos.
   - `update_title` to `Testimonial — <Name>`; rename unusable cards `DO NOT USE — <reason>` instead of deleting.
3. `export-design` png `pro`; download the signed URL with curl.

## Card source B — standalone HTML template (no Canva required)

`assets/card-template.html` renders a 1080×1080 card (stars, heading, quote, script name, role, optional circular photo) driven by CSS variables and a `window.CARD` object (fields documented in the file header). Render:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --screenshot=card.png --window-size=1080,1080 --hide-scrollbars file:///abs/path/card.html
```

Substitute the local Chrome/Chromium binary on other platforms.

## Post-process (Canva-source cards)

- **Recolor** background: `python3 scripts/recolor_bg.py <png>... --target "#1B3A5C"` (corner-samples bg, blends `w=clip((90-dist)/60)` to preserve anti-aliasing).
- **Circular photo**: `python3 scripts/circle_face.py <card.png> <face.png> [--left 420 --top 55 --size 240 --bg "#1B3A5C" --ring "#F1EFE9"]`.
  Canva's API cannot insert local files (`upload-asset-from-url` requires an ALREADY-public URL — never public-host local files), so faces are baked into exported PNGs only. Warn the user: re-exporting from Canva loses the face; re-run this step after any Canva text edit.

## Wire in

Add `<div class="asset-wrap"><img src="./card-N.png" alt="Name, role: short quote"></div>` to the page grid. Rank cards by relevance to the offer — put the ones whose stories match what is being sold first; overflow goes under a "More Client Wins"-style subheading. Verify every `src` exists on disk, then git commit + push if a repo exists.

## Hard rules

- Real, verifiable clients only — every name/quote traceable to a source.
- Version files; never overwrite user originals.
