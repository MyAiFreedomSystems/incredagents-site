# Release Pipeline Registry

One row per candidate skill. Status flow:
`candidate → evaluated → scrubbed → documented → themed → packaged → published`

| Skill | Source location | Verdict | Status | License | Price | GitHub repo | Notes |
|---|---|---|---|---|---|---|---|
| harvest-testimonials | skill-fixes/harvest-testimonials | useful + standalone | **published** | MIT (owner-confirmed 2026-08-14) | TBD | [MyAiFreedomSystems/harvest-testimonials](https://github.com/MyAiFreedomSystems/harvest-testimonials) | Live; YAML frontmatter fixed 2026-08-14 (unquoted colon broke skills.sh); v1.0.0 release cut 2026-08-14 with `.skill` zip |
| graphic-testimonials | managed skills | useful + standalone | **published** | MIT (owner-confirmed 2026-08-14) | TBD | [MyAiFreedomSystems/graphic-testimonials](https://github.com/MyAiFreedomSystems/graphic-testimonials) | Live; LICENSE added + v1.0.0 release cut 2026-08-14 |
| pre-flight-check | public-skills/pre-flight-check | useful + standalone | **published** | MIT (owner-confirmed 2026-08-14) | TBD | [MyAiFreedomSystems/pre-flight-check](https://github.com/MyAiFreedomSystems/pre-flight-check) | v1.0.0 released 2026-08-13; strengthened with the v21–v23 site corrections (breakpoint sweep, breakpoint pairing, transform-centering, frozen frames, measurable QA criteria). LICENSE added 2026-08-14 |
| hooks-guide | skill-src/hooks-guide.md | useful + standalone | **published** | MIT (owner-confirmed 2026-08-14) | TBD | [MyAiFreedomSystems/hooks-guide](https://github.com/MyAiFreedomSystems/hooks-guide) | v1.0.0 released 2026-08-14. Scrub clean; QA caught owner-infra mention (Hermes interface list) — fixed pre-publish. LICENSE added 2026-08-14 |
| provision-project | skill-src/provision-project.md | useful + standalone | **published** | MIT (owner-confirmed 2026-08-14) | TBD | [MyAiFreedomSystems/provision-project](https://github.com/MyAiFreedomSystems/provision-project) | v1.0.0 released 2026-08-14. Scrub clean; QA caught README/skill mismatch (.cursorrules) — fixed pre-publish. LICENSE added 2026-08-14 |
| provision-agent | skill-src/provision-agent.md | useful + standalone | evaluated | TBD per release | TBD | — | Scrub clean 2026-08-14; only the internal brand footer to genericize. Ready to package |
| provision-team | skill-src/provision-team.md | useful + standalone | evaluated | TBD per release | TBD | — | Scrub clean 2026-08-14; only the internal brand footer to genericize. Ready to package |
| graphics | skill-src/graphics.md | useful + standalone | evaluated | TBD per release | TBD | — | Scrub clean 2026-08-14; no owner-coupled terms. Ready to package |
| wrapup | skill-src/wrapup.md | useful + standalone | evaluated | TBD per release | TBD | — | Scrub clean 2026-08-14; no owner-coupled terms. Ready to package |
| pre-build-sop | skill-src/pre-build-sop.md | useful, not yet standalone | evaluated — blocked | — | — | — | References owner swarm-heartbeat infra (line ~197). Needs a rewrite pass to genericize the pipeline kickoff |
| kaizen | skill-src/kaizen.md | useful, not yet standalone | evaluated — blocked | — | — | — | Built around owner's Prime Directive + Four Currencies frameworks. Needs rework to stand alone |
| goal | skill-src/goal.md | useful, not yet standalone | evaluated — blocked | — | — | — | Coupled to owner infra: Swarm Heartbeat, telegram_send, Pacific Time. Needs rework to stand alone |
| routing-matrix | skill-src/routing-matrix.md | promising | evaluated — held | TBD per release | TBD | — | Owner flagged content needs updating before publish (2026-08-13). Footer-only otherwise |
| moe-build-team | skill-src/moe-build-team.md | promising | evaluated — held | TBD per release | TBD | — | Owner flagged content needs updating before publish (2026-08-13) |
| brief-me | — | promising | candidate | TBD per release | TBD | — | Source not in skill-src; site page exists. Locate canonical source before evaluating |
| zoom-transcript-fetch | skill-fixes/zoom-transcript-fetch | promising | evaluated | TBD per release | TBD | — | Not ready — pulled from the public site until it is |
| html-mailer-builder | managed skills | **not ours — stock bundle** | removed from site v7 | — | — | — | Mistakenly listed; not a MyAiFreedomSystems skill |
| repo-audit | managed skills | **not ours — stock bundle** ("Git Forensics Contributors") | removed from site v7 | — | — | — | Mistakenly listed; restore only if the owner says it's theirs |
| package-public-skill | skills/package-public-skill | meta-skill | candidate | TBD per release | TBD | — | The pipeline itself; release once battle-tested |

> License and price are decided per release by the owner. Public pages never
> promise "free", "open source", or a specific license — only what each repo
> actually ships with.

## Evaluation questions (per candidate)

1. Would a stranger install this and get value in under 10 minutes?
2. Does it run without our accounts, brand files, or machine layout?
3. Does `scrub_personal.py` come back clean (or cleanable)?
4. Can its value be explained on one themed web page?

Any "no" → stays private, note the blocker in Notes.
