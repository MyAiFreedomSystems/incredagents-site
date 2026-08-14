---
name: pre-flight-check
description: Mandatory pre-delivery quality gate for any artifact — websites, pages, images, documents, generated files. Use before delivering, shipping, deploying, or presenting any work as done, and whenever the user asks for a review, QA pass, or pre-launch check. Runs truth checks (no fabricated people, quotes, or numbers), copy review, versioning, link verification, geometry-based visual verification across the full breakpoint sweep (not just desktop and phone), a measurable review-team pass, and an honest delivery report. Prevents shipping unverified work.
---

# Pre-Flight Check

Run every section in order before delivering anything. A failing gate stops delivery — fix it or flag it, never ship past it.

## 1. Truth check

- Trace every name, quote, number, and factual claim to a real source retrieved this session. If it does not trace, delete it or flag the gap to the owner — never fill gaps with invention.
- Invented example material is allowed only when openly labeled as invented on every surface where it appears (visible caption, not just alt text).
- Ban hype unless the owner wrote it: "free forever", "live now", license claims (e.g. MIT) that were not specified.
- Public material contains no owner-internal names, machine details, or private infrastructure references.
- Check deliverables AND their source files for text in a language the owner did not request (e.g. watermarks burned into generated images). Crop or regenerate before use.

## 2. Copy pass

- Use direct-response, human phrasing throughout — headlines AND body copy, not headlines only.
- Write product/skill names in Title Case everywhere.
- Read the actual source material before summarizing it; state the real point, not a plausible one.

## 3. Visual verification (for anything rendered)

- Enumerate the page's breakpoints first (`grep -oE "max-width: *[0-9]+px|min-width: *[0-9]+px"`), then screenshot at: desktop width (1440px), true phone width (390px), the owner's actual window width if known, **one width inside every gap between breakpoints, and one pixel either side of each breakpoint value**. A page that passes at 390 and 1440 can still be broken at 690 — mid-width bands are where absolute-positioned elements collide with stacked layouts.
- Verify overlaps with geometry, not eyes: `getBoundingClientRect()` intersection tests between every floating/decorative element and every text, button, and card, at every tested width. Check `scrollWidth <= innerWidth` for horizontal overflow.
- Frozen frames: occluded tabs freeze CSS mid-transition while computed styles show the final state. Take two screenshots 2–3 seconds apart before judging; never declare an element missing from a single capture.
- Follow `references/mobile-visual-audit.md` for the true-phone-width harness, and `references/responsive-breakpoint-audit.md` for the sweep method, overlap snippet, and the CSS traps (mismatched breakpoints, transform-centering vs. animation).
- Fix every cut-off, overflow, overlap, or invisible element, then re-shoot. Clean means clean at every tested width.

## 4. Links and claims

- Verify every button and link resolves (curl or fetch each href).
- Match counts and lists in copy against reality (platform counts, item counts — "twelve skills" must be twelve).

## 5. Versioning (for iterated projects)

- Never overwrite. Before changes: snapshot to `versions/vN/` with a VERSION file. After changes: add a CHANGELOG entry and bump any visible version footer.

## 6. Review team

- When the owner has authorized subagent use, dispatch a reviewer subagent before delivering. Give it **measurable acceptance criteria** — exact viewport widths, the element lists that must not overlap, pixel tolerances, required evidence (geometry measurements + screenshot paths) — not "look it over." A review without numbers is an opinion, not a gate.
- Fix every blocker it finds; fix nits or consciously waive them with a reason.
- Never present work as reviewed that was not.

## 7. Delivery honesty

- Build what was asked, literally. Do not add containers, frames, sections, or structure the owner did not request — if an instruction is ambiguous, ask before improvising structure around their content.
- State in the final reply: what was done, what was verified (and how), what failed, what remains unverified. No confident language over unverified work.
