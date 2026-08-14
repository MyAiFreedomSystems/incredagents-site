# Changelog

All notable changes to this skill are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-13

### Added
- First public release. A seven-gate quality check agents run before
  delivering any artifact: truth, copy, visual verification, links,
  versioning, review team, delivery honesty.
- `SKILL.md` with the seven-gate workflow.
- `references/mobile-visual-audit.md` — true-phone-width harness, headless
  Chrome traps, overflow audit script, common cut-off culprits.
- `references/responsive-breakpoint-audit.md` — the breakpoint sweep method
  (test B−1/B/B+1 and every gap, not just canonical widths), geometry-based
  overlap checks, and three CSS traps: mismatched breakpoints between a
  container and its absolutely-positioned children, transform-centering
  destroyed by transform animations, and frozen frames in occluded tabs.
  Written from real production corrections.

[1.0.0]: https://github.com/MyAiFreedomSystems/pre-flight-check/releases/tag/v1.0.0
