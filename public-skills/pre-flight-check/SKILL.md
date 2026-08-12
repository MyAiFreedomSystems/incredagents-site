---
name: pre-flight-check
description: Mandatory pre-delivery quality gate for any artifact — websites, pages, images, documents, generated files. Use before delivering, shipping, deploying, or presenting any work as done, and whenever the user asks for a review, QA pass, or pre-launch check. Runs truth checks (no fabricated people, quotes, or numbers), visual verification at desktop AND true phone width, versioning, copy review, link verification, and a review-team pass. Prevents shipping unverified work.
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

- Screenshot at desktop width (1440px) AND true phone width (390px), full page height, and read the images back — every strip, not just the top.
- Follow `references/mobile-visual-audit.md` for the exact harness, commands, and tooling traps (Chrome's 500px minimum window, frozen entrance animations under virtual-time).
- Fix every cut-off, overflow, overlap, or invisible element, then re-shoot. Clean means clean at both widths.

## 4. Links and claims

- Verify every button and link resolves (curl or fetch each href).
- Match counts and lists in copy against reality (platform counts, item counts — "twelve skills" must be twelve).

## 5. Versioning (for iterated projects)

- Never overwrite. Before changes: snapshot to `versions/vN/` with a VERSION file. After changes: add a CHANGELOG entry and bump any visible version footer.

## 6. Review team

- When the owner has authorized subagent use, dispatch a reviewer subagent with a specific checklist before delivering. Fix every blocker it finds; fix nits or consciously waive them with a reason.
- Never present work as reviewed that was not.

## 7. Delivery honesty

State in the final reply: what was done, what was verified (and how), what failed, what remains unverified. No confident language over unverified work.
