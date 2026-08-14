# Hooks Guide

Agent lifecycle hooks, explained from zero to registered: what hooks are, when
they fire, the safety rules, the three patterns worth stealing, and the exact
registration steps for Hermes, Claude Code, Codex, Cursor, and OpenCode.

Part of the open skills program by
[My AI Freedom Systems](https://github.com/MyAiFreedomSystems).
Landing page + more skills: [incredagents-site](https://myaifreedomsystems.github.io/incredagents-site/)

## What it does

- Teaches your agent what lifecycle hooks are and when each one fires —
  before/after a tool call, on session start, on session end, on compaction
- Ships three universal patterns: pre-dispatch validation, post-converge
  logging, and compaction survival (so your agent's rules survive context
  compression)
- Gives per-platform adapters and registration instructions instead of vague
  "it depends" advice
- Covers the manual workarounds for platforms with no native hook support

## Why it exists

Hooks are how you enforce governance without forking the agent runtime —
credential scanning, audit trails, pre-flight gates. But every platform names,
fires, and registers them differently, and most agents guess. This skill is
the reference that stops the guessing.

## Requirements

- An AI agent that can follow a `SKILL.md`
- No other dependencies

## Install

```bash
cd <your-agent-skills-folder>
git clone https://github.com/MyAiFreedomSystems/hooks-guide.git
```

Or download `hooks-guide.skill` from the
[latest release](https://github.com/MyAiFreedomSystems/hooks-guide/releases)
and unzip it into your skills folder.

One-command install for 70+ agents:

```bash
npx skills add MyAiFreedomSystems/hooks-guide
```

## Use it

Tell your agent:

> "Add a pre-flight gate that blocks git pushes with secrets, using hooks."

The agent reads the guide, picks the right lifecycle event for your platform,
writes the hook script, and gives you the exact registration steps — with the
safety rules baked in (hooks must be fast, side-effect-free unless that's
their job, and never silently swallow errors).

## How it works (30 seconds)

1. **Concept core** — what hooks are, the key lifecycle events, and the
   universal safety rules.
2. **Universal patterns** — pre-dispatch validation, post-converge logging,
   compaction survival, each with working skeleton code.
3. **Platform adapters** — what Hermes, Claude Code, Codex, Cursor, and
   OpenCode actually support, and the workaround when the answer is "nothing."
4. **Registration** — the config file, the key, and the command per platform.

## License

MIT — see [LICENSE](LICENSE).
