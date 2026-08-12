---
name: logo-theme-manager
description: >-
  Build and maintain a true theme system for websites. Use when replacing a
  logo, swapping a favicon, generating a favicon set, building a token-based
  theme.css with CSS variables, auditing brand consistency across a site,
  hunting down hard-coded hex colors in pages, tracking every copy of a logo
  across a project, or making sure a brand change reaches every page, template,
  and clone. Prevents the classic failure where logo files, colors, and
  favicons get missed when a brand changes.
---

# Logo & Theme Manager

## Why this skill exists

AI site builders rarely produce what a web developer would call a *theme*.
They scatter hex colors inline across pages, copy-paste logo files into
random folders, forget the apple-touch-icon on half the pages, and leave no
single source of truth. Then the brand changes — a new logo, a new accent
color — and updating the site becomes a scavenger hunt: some files get
replaced, some don't, and nobody notices the missed ones until a customer
does.

This skill fixes both halves of the problem:

1. **A real theme system** — one `theme.css` full of CSS custom properties
   (tokens) that every page links to and consumes. Colors, fonts, spacing,
   radii, and dark-mode variants live in exactly one file.
2. **A manifest-driven asset tracker** — a JSON manifest listing *every*
   copy of the logo/favicon set across the project (and its clones), with
   sha256 fingerprints, so `--check` proves nothing drifted and `--replace`
   regenerates and redistributes the full asset set in one command.

## Part 1 — Build a true theme system

### 1.1 Create the token file

Create `assets/theme.css` (exact path is your choice; one file, one location):

```css
/* theme.css — the ONLY place brand values are defined */
:root {
  /* Brand palette */
  --color-primary: #2E5BFF;
  --color-primary-hover: #1F44CC;
  --color-accent: #FFB020;
  --color-bg: #FFFFFF;
  --color-surface: #F5F6F8;
  --color-text: #1A1D24;
  --color-text-muted: #5A6070;
  --color-border: #E2E4EA;

  /* Typography */
  --font-heading: "Inter", system-ui, sans-serif;
  --font-body: "Inter", system-ui, sans-serif;

  /* Shape & spacing */
  --radius-sm: 6px;
  --radius-md: 12px;
  --space-1: 0.5rem;
  --space-2: 1rem;
  --space-4: 2rem;

  /* Brand assets */
  --logo-url: url("./logo-transparent.png");
}

[data-theme="dark"] {
  --color-bg: #12141A;
  --color-surface: #1B1E26;
  --color-text: #F0F2F6;
  --color-text-muted: #9AA1B0;
  --color-border: #2C3038;
}
```

### 1.2 Wire every page to it

- Every HTML page links `<link rel="stylesheet" href="assets/theme.css">`
  (adjust the relative path per page depth) **before** any page-specific CSS.
- Every component, module template, and email-template HTML that carries
  brand styling consumes the tokens: `color: var(--color-primary)`, never
  `color: #2E5BFF`.
- Inline `style="#..."` attributes and page-local hex re-definitions are
  forbidden. When you find one, move the value into a token (or reuse an
  existing token) and reference it.
- If the site is multi-page with shared headers/footers, extract the header
  (which shows the logo) into one shared partial so the logo is referenced
  once, not re-pasted per page.

### 1.3 Find the strays

```bash
# Hard-coded hex colors outside theme.css — every hit is a bug or a comment
grep -rInE '#[0-9a-fA-F]{3,8}\b' --include='*.html' --include='*.css' . \
  | grep -v 'theme.css'

# Inline styles that should be token-driven
grep -rIn 'style="' --include='*.html' .

# rgb()/rgba() literals outside theme.css
grep -rInE 'rgba?\(' --include='*.css' . | grep -v 'theme.css'
```

Review every hit; fix or whitelist with a comment explaining why.

### 1.4 Favicon + identity set

Every site gets the full set in one known location (see Part 2 for
generating it), referenced from every page's `<head>`:

```html
<link rel="icon" href="assets/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon-180.png">
<link rel="manifest" href="site.webmanifest">
```

And Organization JSON-LD in the home page `<head>` so search engines get the
canonical logo URL:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Northbeam Studio",
  "url": "https://northbeam.example.com/",
  "logo": "https://northbeam.example.com/assets/logo-transparent.png"
}
</script>
```

## Part 2 — Track and replace logo assets from a manifest

The scripts live under `scripts/` in this skill. Copy them into the project
(e.g. `scripts/logo/`) or run them in place with `--manifest` pointing at the
project's manifest.

### 2.1 Generate the starter manifest (the "files get missed" killer)

Do **not** write the manifest by hand — crawl the project first:

```bash
python scripts/generate-manifest.py /path/to/project \
    --root-alias site --output scripts/logo/logo-manifest.json
```

It finds `favicon.ico`, `*logo*.png/svg`, `apple-touch-icon*`, `icon-*.png`,
scans HTML for `<link rel="icon|apple-touch-icon|manifest">` and `<img>`
logo references, infers a role per file, fingerprints each with sha256, and
emits a starter manifest. Review its report: anything it found that you
didn't know about was exactly the kind of file that gets missed later.

To track several projects (site + clones + shared templates), run it per
project and merge the `assets` arrays, adding one alias per project under
`roots`. See `scripts/logo-manifest.template.json` for the shape.

### 2.2 Verify integrity

```bash
python scripts/update-logo.py --manifest scripts/logo/logo-manifest.json --check
```

Every entry prints `OK`, `MISSING`, or `DRIFTED`; exit code 1 if anything is
wrong. Run this before and after any brand work, and in CI if you have it.

### 2.3 Replace the logo everywhere (one command)

```bash
# Preview first — writes nothing
python scripts/update-logo.py --replace /path/to/new-logo.png --dry-run

# Do it
python scripts/update-logo.py --replace /path/to/new-logo.png
```

The pipeline: convert to RGBA → key near-white background to transparent →
crop to bounding box → pad 20px → save transparent master → LANCZOS resizes
(32 / 180 / 192 / 512) → multi-size `favicon.ico` (16/32/48) → copy over
**every** manifest location → rewrite the manifest with fresh sha256s.

Options:

- `--bg R,G,B` — key an explicit background color instead of near-white
  (required when the source has a colored background; the script refuses
  and tells you the corner color it found).
- `--keep-bg` — keep an opaque, full-bleed tile logo as-is (no keying).
- `--force` — skip the pre-flight `--check` (use only when you know why
  drift exists).
- `--commit` — after a replace, `git add` + `git commit` the changed assets
  in each repo listed under `git_repos`. **Never pushes.** Repos inside a
  root marked protected in the manifest are skipped.

### 2.4 Adding a new location later

1. Copy the asset file(s) into place (or run `--replace` and let it write
   them — destinations' parent dirs are created automatically).
2. Add one entry per file to the manifest's `assets` array with the right
   `role` and the file's sha256 (`shasum -a 256 <file>`). Placeholder hashes
   are fine if you immediately run `--replace` — it rewrites them.
3. Run `--check` to confirm green.

### 2.5 Fallbacks for constrained agents

- **No Pillow installed:** try `pip install Pillow`. If that is impossible,
  you can still do the *tracking* half: write the manifest entries by hand
  with sha256s from `shasum -a 256`, and implement `--check` yourself (hash
  each file, compare). For replacement, ask the human for a pre-generated
  favicon set (favicon-generator tools produce the standard
  ico/32/180/192/512 bundle) and copy those files over every manifest
  location by hand, updating hashes as you go.
- **No shell access at all:** do the audit with file tools: list the
  project tree, grep HTML/CSS for logo and hex references as in §1.3,
  assemble the manifest JSON yourself, and report to the human exactly which
  files must be replaced. Never claim a replace happened that you could not
  execute.
- **SVG sources:** the scripts take PNG input. Rasterize an SVG first
  (e.g. `rsvg-convert`, Inkscape, or an online converter) at ≥1024px, then
  feed the PNG to `--replace`.

## True-theme checklist

Before declaring a site done, verify every item in
[references/theme-checklist.md](references/theme-checklist.md):

- [ ] Single token file (`theme.css`) is the only place brand values live
- [ ] Zero inline hex colors / `style=""` attributes in pages
- [ ] Every page links the theme file before page-specific CSS
- [ ] Full favicon set present (ico, 32, apple-touch-180, 192, 512) and
      linked from every page
- [ ] Organization JSON-LD with absolute logo URL on the home page
- [ ] Dark-mode tokens defined under `[data-theme="dark"]`
- [ ] Manifest generated by crawling (not by memory), `--check` all green
- [ ] Logo appears in exactly one shared header partial, not re-pasted
      per page
