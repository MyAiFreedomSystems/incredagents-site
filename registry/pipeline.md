# Release Pipeline Registry

One row per candidate skill. Status flow:
`candidate → evaluated → scrubbed → documented → themed → packaged → published`

| Skill | Source location | Verdict | Status | License | Price | GitHub repo | Notes |
|---|---|---|---|---|---|---|---|
| harvest-testimonials | skill-fixes/harvest-testimonials | useful + standalone | **published** | MIT | free | [MyAiFreedomSystems/harvest-testimonials](https://github.com/MyAiFreedomSystems/harvest-testimonials) | Live; paired with graphic-testimonials |
| graphic-testimonials | managed skills | useful + standalone | **published** | MIT | free | [MyAiFreedomSystems/graphic-testimonials](https://github.com/MyAiFreedomSystems/graphic-testimonials) | Live |
| pre-flight-check | public-skills/pre-flight-check | useful + standalone | **published** | all rights reserved (terms TBD) | TBD | [MyAiFreedomSystems/pre-flight-check](https://github.com/MyAiFreedomSystems/pre-flight-check) | v1.0.0 released 2026-08-13; strengthened with the v21–v23 site corrections (breakpoint sweep, breakpoint pairing, transform-centering, frozen frames, measurable QA criteria). NO LICENSE file per owner — do not claim MIT |
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
