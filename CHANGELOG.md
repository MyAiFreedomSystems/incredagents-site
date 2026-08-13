# Changelog

All notable changes to the SkillManager_Public pipeline and its released skills
are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Site v21: the bee bot takes the hero window. The three-bot logo inside the
  hero's robot window is replaced by the bee-chest robot per owner vote; the
  floating side bot from v20 folded into it. Original window centering
  restored after the taller image exposed a chips/buttons overlap (windowSway
  animation owns `transform`; image sized to the original footprint).
  Snapshot in `versions/v21/`.
- Site v20: the bots come home. The bee-chest robot (`robot-single-bee.png`)
  floats beside the hero window; the high-five robot gif celebrates above the
  CTA band. Script accent font retired (Yellowtail → Cormorant Garamond light
  italic — thinner per owner vote; applies site-wide via `--script`). Scroll
  reveal hardened: pre-triggers 220px early with a fallback sweep so fast
  scrolling never leaves a blank section. Snapshot in `versions/v20/`.
- Site v19: the Hive layer. One fixed canvas now paints the page background —
  hero/CTA/footer bands, the honeycomb with its glimmer sweep, and three
  cell-hopping bees run uninterrupted behind every section (section
  backgrounds went transparent; the canvas owns band colors). Same words, same
  layout, same palette as v18. Snapshot in `versions/v19/`.
- GitHub Pages: the catalog is live at
  https://myaifreedomsystems.github.io/incredagents-site/ via a workflow that
  deploys `site/` on every push to main.
- Repo presentation pass, modeled on a study of top GitHub repos
  (microsoft/generative-ai-for-beginners, anthropics/skills, awesome-list):
  visitor-facing README with live-site banner, badge row, catalog preview,
  skill tables cross-linking every repo to its page and back (pipeline doc
  preserved as `PIPELINE.md`); thorough About descriptions; 10 validated
  topics on the site repo; homepage + topics set on all public skill repos;
  empty descriptions filled for harvest-testimonials and graphic-testimonials;
  org profile README published at MyAiFreedomSystems/.github.
- Social preview images (1280×640, branded navy/gold with each skill's SVG
  logo) set on all six public repos (incredagents-site, harvest-testimonials,
  graphic-testimonials, testimonial-display, logo-theme-manager, incredagents).
  GitHub exposes no API for this, so the images were attached through the
  owner's real browser via WebBridge base64 injection into the repo settings
  upload control; each repo's og:image now resolves to its own
  repository-images.githubusercontent.com URL.
- New skill: `pre-flight-check` — the mandatory pre-delivery quality gate
  distilled from this project's own review history. Truth check (nothing
  fabricated, examples labeled), copy pass, visual verification at 1440px and
  true 390px (with `references/mobile-visual-audit.md` documenting the iframe
  harness and the frozen-animation tooling trap), link/claim verification,
  versioning, review-team pass, delivery honesty. Installed in the agent's
  skills root and staged for the public repo at `public-skills/pre-flight-check/`
  with a packaged `pre-flight-check.skill` zip.

### Changed
- Site v18: the exhaustive mobile pass. After the owner reported cut-offs at
  phone width a second time, every page got a true-390px audit instead of the
  usual 500px approximation — first a full visual read of the index, then a
  programmatic overflow sweep (temporary `_audit.html`, since removed) that
  loaded all 17 pages in 390px iframes and flagged any element wider than the
  viewport: all 16 skill pages came back CLEAN; the only flag on the index
  was the intentionally off-canvas Skill Index panel. The one real truncation
  found and fixed: the Get Started terminal clipped its `git clone` URLs
  behind a horizontal scroll — on ≤720px the terminal now wraps in full
  (`overflow-wrap: anywhere` + `<wbr>` hints so URLs break at slash
  boundaries, no mid-word danglers). Verification note: headless screenshots
  at 390px require `--force-prefers-reduced-motion`, otherwise virtual-time
  freezes entrance animations mid-delay and hides words — a tooling artifact,
  not a page bug; now documented here so future audits don't chase it.
- Site v17: room to breathe. The before/after frames on the index no longer
  clip their content — the fixed 16:10 aspect boxes with `overflow: hidden`
  cropped the FB-post figcaption and could graze the square card; both frames
  now grow to fit the art (`.media-mock` and `.media-top-square` break out of
  the ratio), and the hover zoom no longer re-crops the after-card. The
  Brief-Me tone trio (terracotta, sage, slate) now runs site-wide: card top
  borders cycle gold → terra → sage across the singles and pack grids, slate
  darkened to `#5f7b9e` for AA contrast on cream. De-compaction pass per
  owner feedback ("everything is so tiny"): pack-card art ~20% taller on a
  navy frame (contain, so demos never crop), bigger card logos (44px) and
  type, bigger standalone icons (168px), wider gaps. Base `.media-top` rule
  now carries a comment marking it icon-cards-only so future content can't
  silently clip. Review-team verdict: SHIP, all three low-severity findings
  fixed before snapshot.
- Site v16: the real-person testimonial is gone from the public site. The
  before/after pair now uses an invented example persona — Danielle Ruiz of
  Blue Door Bakery — with an AI-generated headshot
  (`assets/example-persona-photo.png`, watermark cropped), a Facebook-style
  post mock (`assets/example-fb-post.png`, source in `demos/example-fb-post.html`),
  and a rebuilt 1080×1080 card (`assets/card-example.png`, source moved to
  `demos/card-example.html` so no unlabeled template is publicly servable).
  Every Matt-era asset left `site/` (preserved in `versions/v15-assets-attic/`);
  zero references remain. The persona is visibly labeled as invented on all
  three pages that show her — index figcaption and card copy, plus caption
  strips under both skill-page heroes added after the review team flagged
  that the skill pages showed a realistic testimonial with no disclaimer
  while their own footers promise every attributed word is real. Mobile hero
  fixed for real this time: the robot window was shifted right by a leftover
  `left: 50%` under the flex-column media query — now reset with
  `top/left: auto` and centered; headline gets `text-wrap: balance` and a
  smaller clamp so it breaks into two clean lines at phone width.
- Site v15: every skill now has its own logo. A cohesive 16-mark SVG set
  (`assets/skill-*.svg` — navy badge, gold ring, one distinct glyph per skill)
  replaces the placeholder squares on the twelve pack cards and anchors each
  skill page's hero art. Shipped after a review-team pass that caught real
  blockers, all fixed: seven skill-page headlines truncated mid-sentence (a
  generator helper dropped every word after the first — rewrote the affected
  title arrays), "Watchtower" leaked into a shipped demo image (scrubbed to
  "client briefs," re-shot `demo-graphics.png`), the pack title claimed "Seven
  Platforms" (now "Every Platform" — no invented counts), the harvest hero
  image didn't fill its frame, and mobile had no layout rules (tiles now stack
  statically, orbit/pulse rings hidden, nav wraps). Also hardened the headline
  entrance animation so words can never stick invisible. Screenshot tooling
  fixed in `demos/fullpage.sh` — overshoots to 12000px then crops at the first
  blank gap, background sampled from the real page, right edge excluded to
  dodge the offscreen Skill Index panel's shadow. No more cut-off screenshots.
- Site v14: the full catalog treatment. All 15 remaining skills now have their
  own mini pages under `skills/` (16 total with Brief-Me), each with a
  direct-response headline, copy mined from the real SKILL.md files, and a
  screenshot of the skill's actual output format. Two screenshots are the
  skills' real shipped files (testimonial-display's pattern demo and the
  graphics eight-style example brief, pulled from the repos); harvest/graphic
  pages use the real Matthew Davis before/after assets; the other eleven are
  faithful renditions built from each skill's own documented output spec and
  screenshotted with headless Chrome (plan files, evidence tables, lineup
  tables, YAML + validator output, scaffold trees, hook block messages).
  Main page: the twelve mod-pack pills are now full cards with demo
  thumbnails + Full Page / GitHub links; the four standalone cards gained
  "See The Full Page →" links; the Skill Index panel now routes to the local
  pages. Working files live in `skill-src/` (downloaded SKILL.md copies) and
  `demos/` (demo generators + real example files).
- Site v13: corrected the Brief-Me page's core framing after owner review — it
  is the ORCHESTRATOR that gets no vote, not "your agent," and the split is
  the point: the orchestrator handles delegation only while the six voices do
  the thinking. Rewrote the hero sub, feature-card copy, and rule card to say
  so. Deleted the three giant circular stat badges (owner: "an absolute waste
  of space" repeating what the text already says); the three rules now sit in
  one tight three-up `.truth-grid` with plain gold-ruled cards. Split-decision
  copy sharpened to the real rule: dissenters get re-dispatched until every
  voice passes, and true deadlock reaches you as one question to break — never
  a scoreboard.
- Site v12: first per-skill mini page — Brief-Me gets the full treatment as the
  template for the rest of the catalog. New `skills/brief-me.html`: navy hero
  with script-accent headline, hand-drawn SVG scene (`assets/brief-me-art.svg`,
  code-drawn because the image gateway is still returning HTTP 424), a
  one-command terminal block, six voice cards in the product's real
  terracotta/sage/slate tones (Researcher, Advisor, Kaizen One, Kaizen Two,
  Linter, Builder), three alternating point rows with stat badges ("your agent
  gets no vote", "no split decisions", "plain speak, real numbers"), and an
  install block — every claim sourced from the real `brief-me/SKILL.md`, with
  owner-internal infra names (Watchtower, roster) deliberately kept off the
  public page. Main page gains a full-width navy "Featured Skill" card between
  the singles grid and the mod-pack block, linking to the mini page and GitHub.
- Site v11: the whole public catalog is on the page now. Added
  Testimonial-Display and Logo-Theme-Manager cards (new SVG logos), plus a
  full-width "Mod Pack" block presenting all twelve skills inside the
  `incredagents` repo — each pill links straight to its repo folder. Hero
  floating tiles are now real links to their GitHub repos (they were dead
  divs). New gold slide-in "Skill Index" panel (nav button, dotted-leader
  rows, every skill linked) and a mono "> " prefix reveal on card-link
  hover. zoom-transcript-fetch deliberately left off — owner says it is not
  ready, though the repo is currently public (flagged to her).
- Site v10: owner supplied Matthew Davis's real headshot, so the after-card's
  MD monogram placeholder is replaced with his actual photo (circular,
  gold-ringed, `matthew-davis-photo.png`). Quote unchanged — still his real
  condensed words.
- Site v9: the library now shows the before → after the skills actually
  perform. Harvest-Testimonials card keeps Matthew Davis's real Facebook
  screenshot with a "Before" chip; Graphic-Testimonials card now shows the
  branded card built from that same post (new `card-matthew-davis.png`,
  his real condensed words — nothing invented) with an "After" chip and a
  gold arrow between the two cards. Card copy reframed from praising Tina to
  demonstrating the process ("Same post, minutes later..."). Fixed the
  "Shear Strength Labs" misspelling — it is Sheer Strength Labs. After-card
  displays full-square instead of cropped. LinkedIn blocked his headshot
  (authwall), so the card uses an MD monogram until he sends a photo.
- Site v8: replaced the fabricated Facebook-post mock (a mistake — invented
  words attributed to a real person) with Matthew Davis's actual testimonial
  screenshot, his real words only; "How We Ship" pipeline section removed
  (visitors don't care about our process); new FreedomAIOS logo in the footer;
  footer now states the real-words rule publicly. New house rule #1: never
  fabricate quotes, names, numbers, or screenshots.
- Site v7: headline words "agent" and "skills." now gold script (owner directive,
  supersedes the old no-gold-text-on-navy note); stats band removed as noise;
  HTML-Mailer-Builder and Repo-Audit removed — both turned out to be stock
  bundled skills, not ours; Harvest card now shows a Facebook-post example
  (Matt Davis / Shear Strength Labs mock — swap in the real screenshot when
  available); Graphic card shows a real finished testimonial card; full
  copy pass applying the copywriting rules to every remaining string
  (killed "every kind word, one pile" and similar non-human phrasing).
- Site v6: hero restructured top-down — "Your agent is only as good as its
  skills." is now the H1 sitting ~10px under the nav's gold line, with the robot
  window + orbit + four floating skill tiles center-stage above the fold. New
  motion: per-word headline stagger, sonar pulse rings behind the window, pulsing
  primary CTA, bouncing scroll hint. Footer now shows the site version.
- Versioning is now a house rule (README): snapshot to `versions/v<N>/` before
  every iteration; v5 and v6 preserved. Nothing gets overwritten.
- Site v5: full hero rebuild — 3D-tilted "robot window" (IncredAgents logo) inside
  a rotating dashed orbit ring with four floating skill tiles; skill names in full
  title case (Harvest-Testimonials, Graphic-Testimonials, HTML-Mailer-Builder,
  Repo-Audit); ON GITHUB / IN FINAL PREP pills moved to card bottoms; library
  expanded to four skills with animated SVG scenes for the mailer and audit skills;
  Zoom-Transcript-Fetch removed from the site (not ready). AI-generated hero/card
  artwork planned via the image-generation plugin once the gateway recovers
  (HTTP 424 during this session).
- Site v4: hero is now the product — three floating skill tiles (logo, name, pill)
  instead of testimonial imagery; bespoke animated SVG scenes per skill card
  (harvest source-flow, before/after brand recolor, Zoom transcript mock);
  terminal-style install block; dot-textured navy sections. Patterns lifted from
  Linear/Raycast (floating depth), Vercel (terminal proof), Stripe (animated flow).
- All license and "free/open source" claims removed from site, template, README,
  registry, and pipeline SKILL.md — license and price are decided per release and
  public pages only state what a repo actually ships.
- Site v2: split hero with floating real-output proof cards, scroll-reveal motion
  (IntersectionObserver, staggered), animated stat counters, media-style skill cards
  with LIVE / IN-PIPELINE badges, animated Zoom transcript SVG mock, numbered
  pipeline flow, skim chips, `prefers-reduced-motion` support, mobile overflow fixes.
- Site v3: IncredAgents logo in nav/footer/favicon; simple SVG logo marks for each
  skill; skill names capitalized in display copy; all "free forever"-style claims
  removed (releases may be paid later); copy rewritten direct-response style via the
  copywriting + copy-editing workflow; same "free"-claim cleanup applied to the
  reusable site template.

### Planned
- Stage `zoom-transcript-fetch` for public release (currently in private skill-fixes).
- Promote the landing site from local preview to a deployed URL.
- Port the v2 motion/media components back into `assets/site-template/`.

## [0.1.0] - 2026-08-10

### Added
- Initial project structure: `registry/`, `releases/`, `skills/`, `site/`.
- `package-public-skill` agent skill: evaluate → scrub → document → theme → package pipeline.
- `scripts/scrub_personal.py` — personal-data scanner (paths, emails, hostnames, tokens).
- House templates: release checklist, README template, CHANGELOG template.
- Shared web theme template (`assets/site-template/`) matching the IncredAgents
  skill-site theme (navy `#1B3A5C`, cream `#FAFAF8`, gold `#D9A441`, Georgia italic
  headings, Yellowtail script accent).
- Public landing site (`site/`) for the skills program with dev server
  (`npm run dev`, port-forwarding like our other skill sites).

### Notes
- Released siblings already live on GitHub:
  [harvest-testimonials](https://github.com/MyAiFreedomSystems/harvest-testimonials) and
  [graphic-testimonials](https://github.com/MyAiFreedomSystems/graphic-testimonials).

[Unreleased]: https://github.com/MyAiFreedomSystems/SkillManager_Public/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/MyAiFreedomSystems/SkillManager_Public/releases/tag/v0.1.0
