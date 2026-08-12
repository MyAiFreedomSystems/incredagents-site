---
name: package-public-skill
description: Prepare a private agent skill for public release on GitHub — evaluate standalone usefulness, scrub personal names/paths/machine details, generate README + CHANGELOG + LICENSE, build a themed landing page from the house site template, and package a .skill zip. Use when the user wants to publish, open-source, sell, give away, or "prep for GitHub" any skill, or when working inside the SkillManager_Public release pipeline.
---

# Package Public Skill

Run the release pipeline that turns a private skill into a public GitHub release.
Pipeline order is fixed: **evaluate → scrub → document → theme → package → stage**.
Do not skip scrub. Nothing ships with unresolved scrub findings.

## 1. Evaluate

Answer the four questions in `registry/pipeline.md` (worth installing? standalone?
scrubbable? explainable on one page?). Any "no" → stop, report the blocker, keep
the skill private. Record the verdict in the registry.

## 2. Scrub

Run the scanner and resolve every finding before continuing:

```bash
python3 scripts/scrub_personal.py <skill-dir>
```

- Replace personal paths with generic ones (`/Users/you/...`, `<your-project>/`).
- Replace personal names/emails with the public brand contact or a placeholder.
- Remove credentials outright — never allow-list a real secret.
- Re-run until exit code 0. Use `--allow` only for intentional public strings
  (e.g. the brand name).

## 3. Document

Copy from `references/` into the candidate skill root and fill every placeholder:

- `readme-template.md` → `README.md` (problem, install, usage, license)
- `changelog-template.md` → `CHANGELOG.md`, first entry `## [1.0.0] - <today>`
- Add `LICENSE` — the owner picks per release (open or commercial). Never state
  a license or price on any public page that the repo doesn't actually ship with.

## 4. Theme the web page

Copy `assets/site-template/` to the release's site folder and replace the
`{{PLACEHOLDER}}` tokens (skill name, tagline, repo URL, features, install
command). Do not change the palette, fonts, or layout rules — the header comment
in `styles.css` documents the brand votes (no yellow highlights, no glow blobs,
no gold text on navy, script font for accents only).

## 5. Package

Validate structure (SKILL.md frontmatter has `name` + `description`; only
`scripts/`, `references/`, `assets/` resources that actually exist), then zip:

```bash
cd <staging-parent> && zip -r <skill-name>.skill <skill-name>
```

## 6. Stage and register

- Move the scrubbed folder + `.skill` zip + web page into `releases/<skill-name>/`.
- Update `registry/pipeline.md` status and the project `CHANGELOG.md`.
- Report: what shipped, scrub results, remaining manual steps (git init, GitHub
  repo creation, pushing — these need the owner's go-ahead and credentials).

See `references/release-checklist.md` for the full pre-flight checklist; run
through it before declaring any release done.
