# Changelog

All notable changes to the SkillManager_Public pipeline and its released skills
are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Take My Course For Me v1.0.0 published: [MyAiFreedomSystems/takemycourseforme](https://github.com/MyAiFreedomSystems/takemycourseforme)
  with a GitHub release carrying the `.skill` zip (SKILL.md + 7 capture
  scripts + ONBOARDING walkthrough). Extracts a paid Skool or Circle course
  into ADHD-friendly cliff notes plus a build/implement handoff — live-Chrome
  bridge (never headless), resumable manifest capture, transcript pipeline.
  Full treatment: house-style icon (`skill-takemycourseforme.svg`), labeled
  illustrative demo image, skill page, homepage card + index row, gallery card
  under a new "Courses" category, MIT LICENSE, skills.sh indexing requested
  (vercel-labs/skills#1963). Also installed to the Brain nucleus-canon
  `.agent/skills/` for the Hermes team (index regenerated, skill #475).
  QA subagent: SHIP on both the release and the page.
- Site v28: the Take My Course For Me page (`site/skills/takemycourseforme.html`),
  homepage pack-card + Skill Index row, gallery card, and the homepage
  hooks-guide / provision-project GitHub links repointed to their standalone
  repos (v26 only fixed the skill pages, not the homepage cards).
  Snapshot in `versions/v28/`.
- Site v27: the Shipped Skills gallery (`site/gallery.html`). Modeled on the
  owner's FreedomAIOS page-gallery format — kicker + title header, category
  filter pills with live count, card grid with per-skill icons, version badge,
  license badge, repo/release/skill-page links, and an expandable version
  history per card. Lists all five shipped skills at v1.0.0. Linked from the
  homepage nav ("Shipped"). Snapshot in `versions/v27/`.
- All five published repos standardized on MIT per owner direction
  (2026-08-14: "MIT license is fine" — distinct from "not free forever",
  which is a pricing promise, not a license). Added LICENSE files to
  graphic-testimonials, pre-flight-check, hooks-guide, provision-project
  (harvest-testimonials already had one) and updated every README license
  section. harvest-testimonials and graphic-testimonials got their first
  tagged v1.0.0 releases with `.skill` zips, so all five repos now have
  releases with installable artifacts.
- Hooks Guide v1.0.0 published: [MyAiFreedomSystems/hooks-guide](https://github.com/MyAiFreedomSystems/hooks-guide)
  with a GitHub release carrying the `.skill` zip. Agent lifecycle hooks across
  platforms — concept core, safety rules, three universal patterns
  (pre-dispatch validation, post-converge logging, compaction survival), and
  per-platform registration for Hermes, Claude Code, Codex, Cursor, and
  OpenCode. Scrubbed clean; QA subagent caught one owner-infra reference
  (Hermes kill-switch interface list) — fixed and re-zipped before publish.
  NO LICENSE file per owner direction. skills.sh indexing requested
  (vercel-labs/skills#1959).
- Provision Project v1.0.0 published: [MyAiFreedomSystems/provision-project](https://github.com/MyAiFreedomSystems/provision-project)
  with a GitHub release carrying the `.skill` zip. Agent-ready workspace
  scaffolding: governance files, canonical skeleton, session ledger,
  per-platform instruction files, optional agent auto-provisioning,
  self-verification. Scrubbed clean; QA subagent caught a README claim that
  didn't match the skill (`.cursorrules` vs. the real `.cursor/rules/project.md`)
  — fixed before publish. NO LICENSE file per owner direction. skills.sh
  indexing requested (vercel-labs/skills#1960).
- Site v26: the hooks-guide and provision-project pages' GitHub buttons now
  point at their new standalone repos instead of the incredagents mod-pack
  tree. Snapshot in `versions/v26/`.
- Library evaluation pass: all 10 remaining skill-src candidates scrubbed
  clean by `scrub_personal.py`. Standalone verdicts recorded in
  `registry/pipeline.md` — `graphics`, `wrapup`, `provision-agent`,
  `provision-team` near-ready (footer only); `pre-build-sop`, `kaizen`,
  `goal` blocked on owner-coupled infra references (Swarm Heartbeat,
  Telegram, Prime Directive) that need rewrites; `routing-matrix` and
  `moe-build-team` held pending owner-requested content updates.
- Fixed harvest-testimonials YAML frontmatter: the description contained an
  unquoted `Sources: ` colon that broke skills.sh parsing ("No valid skills
  found"). Quoted the scalar in the repo and in `skill-src/`; the skill now
  lists and installs via `npx skills add MyAiFreedomSystems/harvest-testimonials`.
- skills.sh indexing requests filed for the three previously published repos
  (vercel-labs/skills#1956 pre-flight-check, #1957 harvest-testimonials,
  #1958 graphic-testimonials); all three verified installable via the CLI.
- Directory submission: PR opened to ComposioHQ/awesome-claude-skills
  ([#1626](https://github.com/ComposioHQ/awesome-claude-skills/pull/1626))
  adding Pre-Flight Check in their template format. VoltAgent/awesome-agent-skills
  and hesreallyhim/awesome-claude-code deferred — both reject brand-new repos
  (14-day minimum / community-usage requirements); revisit dates recorded in
  `launch/show-hn-kit.md`.
- `launch/show-hn-kit.md`: complete Show HN kit for Pre-Flight Check — title,
  URL, first-comment story (the true 690px incident), timing, two-hour reply
  playbook, and the not-to-do list.
- Site v25: every skill page is now shareable. All 16 pages under
  `site/skills/` carried no social meta at all — pasting a skill link into
  LinkedIn, X, or iMessage rendered a bare URL. Each page now ships the full
  og/twitter tag set (type, url, title, description, image, twitter:card)
  with per-page title and description drawn from its own `<title>` and
  meta description, all pointing at the shared 1280×640
  `assets/og-image.png` share card. Snapshot in `versions/v25/`.
- Site v24: the transformation strip becomes the signature. New "How a skill
  works" section after the hero — Source → bee bot → Finished product rows for
  Harvest-Testimonials, Graphic-Testimonials, and Pre-Flight Check, per the
  owner's direction after the v2 social cards ("This is how we show what
  skills do!"). Social meta shipped too: the site had no og/twitter tags at
  all (opengraph.xyz scan showed title/image missing); added the full tag set
  plus a branded 1280×640 `assets/og-image.png` share card (headline + bee
  bot, feet margin verified). QA subagent caught a 721–860px panel-clipping
  band, a missing caption, and a gates-count mismatch — all fixed and
  re-verified across 8 widths before publish. Snapshot in `versions/v24/`.
- Pre-Flight Check v1.0.0 published: the house QA gate is now a public repo
  at [MyAiFreedomSystems/pre-flight-check](https://github.com/MyAiFreedomSystems/pre-flight-check)
  with a GitHub release carrying the `.skill` zip. Updated with every lesson
  from the v21–v23 site corrections: breakpoint sweep (test B−1/B/B+1 and
  every mid-gap width, plus the owner's real window width), breakpoint
  pairing (a child un-pins at the same breakpoint as its stacking container),
  transform-centering vs. animation conflict, the two-screenshot frozen-frame
  rule, geometry-based overlap checks, and measurable acceptance criteria for
  review subagents — new reference `responsive-breakpoint-audit.md`. Scrubbed
  clean, QA-subagent reviewed (SHIP, 4 nits fixed), no LICENSE file and no
  license claims per owner direction.
- Site v23: the bot stacks when the stage stacks. v22 only un-pinned the bot
  at ≤640px, but the hero stage switches to its stacked layout at ≤720px —
  so at 641–720px (the owner's own window width) the bot was still absolutely
  centered over the sub-headline, with the stacked tiles painting over it.
  The bot now joins the flow at the same ≤720px breakpoint. Verified at 8
  widths (390–1654px, including the 720/721 boundary) by an independent QA
  subagent pass: zero overlaps, zero center drift, no overflow. Snapshot in
  `versions/v23/`.
- Site v22: the bee bot stands alone. The robot-window frame is gone from the
  hero — the bee-chest robot now sits bare in the center, dead-centered with
  `translate(-50%,-50%)` and floating on a margin-top animation so centering
  can never fight the bob. No overlap with headline, sub, tiles, chips, or
  CTAs on desktop or 390px mobile; verified by an independent QA subagent
  pass (all 7 criteria, geometry + screenshots). Snapshot in `versions/v22/`.
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
