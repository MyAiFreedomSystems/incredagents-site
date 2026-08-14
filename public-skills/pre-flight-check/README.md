# Pre-Flight Check

A quality gate your agent runs before it calls any work "done" — so you stop
finding the bugs it should have caught.

Part of the open skills program by
[My AI Freedom Systems](https://github.com/MyAiFreedomSystems).
Landing page + more skills: [incredagents-site](https://myaifreedomsystems.github.io/incredagents-site/)

## What it does

- Catches invented names, quotes, and numbers before they reach your customer
- Makes your agent screenshot its own work and actually look at it — at every
  breakpoint, not just "desktop and mobile"
- Finds overlaps and overflow with pixel measurements instead of eyeballs
- Forces an independent review pass with measurable acceptance criteria
- Ends every delivery with an honest account of what was verified and what wasn't

## Why it exists

Agents pass their own work too easily. A page can look perfect at 1440px and
390px and still be broken at the 690px window you actually use — an element
left floating where the layout switched to stacked. This skill exists because
we shipped exactly that bug, got the screenshot from an unhappy owner, and
wrote down every lesson so it can't happen twice.

## Requirements

- An AI agent that can follow a `SKILL.md`
- A way to screenshot rendered pages (headless Chrome or a browser bridge)

## Install

```bash
cd <your-agent-skills-folder>
git clone https://github.com/MyAiFreedomSystems/pre-flight-check.git
```

Or download `pre-flight-check.skill` from the
[latest release](https://github.com/MyAiFreedomSystems/pre-flight-check/releases)
and unzip it into your skills folder.

## Use it

Tell your agent:

> "Run the pre-flight check before you send me anything."

Seven gates run in order: truth, copy, visual verification, links, versioning,
review team, delivery honesty. A failing gate stops delivery — the agent fixes
it or flags it, never ships past it.

## How it works (30 seconds)

1. **Truth check** — every name, quote, and number traces to a real source or gets cut.
2. **Copy pass** — human, direct phrasing everywhere, not just the headlines.
3. **Visual verification** — breakpoint sweep with geometry overlap checks, plus
   the two-screenshot rule that defeats frozen animation frames.
4. **Links, versioning, review team, honesty** — the boring parts that make the
   difference between "done" and done.

## License

All rights reserved for now. License terms are being decided — watch the repo.
