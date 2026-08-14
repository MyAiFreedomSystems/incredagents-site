# Provision Project

Turn an empty folder into an agent-ready workspace: governance files, a
canonical directory skeleton, a session ledger, and platform-specific
instruction files for Hermes, Claude Code, Codex, Cursor, and OpenCode —
self-verified before it hands back.

Part of the open skills program by
[My AI Freedom Systems](https://github.com/MyAiFreedomSystems).
Landing page + more skills: [incredagents-site](https://myaifreedomsystems.github.io/incredagents-site/)

## What it does

- Verifies nothing is already provisioned before touching anything
- Creates the canonical directory skeleton every agent on the project shares
- Generates the right instruction file per platform (AGENTS.md, CLAUDE.md,
  .cursor/rules/project.md, and friends) from one governance source
- Writes an initial handoff so the next session starts with context, not
  archaeology
- Optionally auto-provisions named agents into the project from a YAML block
- Self-verifies the scaffold before reporting done

## Why it exists

Every agent project starts the same way: someone rebuilds the same folders,
forgets a platform's instruction file, and the second session opens with no
memory of the first. This skill makes project setup a one-command, verifiable
event instead of a ritual.

## Requirements

- An AI agent that can follow a `SKILL.md`
- `GOVERNANCE_HOME` set to your governance nucleus folder (the skill errors
  with instructions if unset)

## Install

```bash
cd <your-agent-skills-folder>
git clone https://github.com/MyAiFreedomSystems/provision-project.git
```

Or download `provision-project.skill` from the
[latest release](https://github.com/MyAiFreedomSystems/provision-project/releases)
and unzip it into your skills folder.

One-command install for 70+ agents:

```bash
npx skills add MyAiFreedomSystems/provision-project
```

## Use it

Tell your agent:

> "Provision a new project called Forge at ~/Documents/Forge — it's for
> testing outbound copy."

The agent asks once if anything required is missing, builds the skeleton,
writes the platform files, logs the initial handoff, and verifies its own
work before telling you the folder is ready.

## How it works (30 seconds)

1. **Guard** — refuses to provision over an existing scaffold.
2. **Skeleton** — canonical directories, governance files, session ledger.
3. **Platform overlays** — the instruction file each agent platform reads.
4. **Handoff** — the next session opens knowing what this project is.
5. **Self-verify** — the scaffold is checked, not assumed.

## License

All rights reserved for now. License terms are being decided — watch the repo.
