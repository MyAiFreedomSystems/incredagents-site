---
name: provision-agent
description: >-
  Provision a new AI agent with identity overlays, scoped skills, tool constraints,
  handler profile, and memory structure. Creates SOUL.md, TOOLS.md, MEMORY.md, and USER.md
  files on top of the project scaffold. Extends provision-project with agent-specific identity.
  Use when creating a named agent, standing up an agent identity, or binding skills and tools
  to a new agent instance.
type: procedure
status: active
version: 1.0.0
---

# Provision an Agent

This skill creates a fully provisioned AI agent identity that follows the canonical
project structure AND adds agent-specific overlays: personality (SOUL.md), capabilities
(TOOLS.md), memory scaffold (MEMORY.md), and handler profile (USER.md).

## When to invoke

Invoke when the user says any of:

- "Provision a new agent called X."
- "Create agent X for Y."
- "Stand up agent X."
- "Scaffold a new agent at `<path>/X`."
- "Initialize X as an agent."

Do NOT invoke for:

- A plain project folder (use `provision-project` instead).
- An agent folder that already has `SOUL.md` and `TOOLS.md` — it's already provisioned.
- A governance or nucleus directory.

## Inputs

1. **Agent name** — Preserve casing. Examples: `TestAgent`, `Forge`, `Sentinel`.
2. **Role description** — One paragraph: what this agent does, its purpose.
3. **Handler** — The human who directs this agent (name, timezone).
4. **Initial skill set** — List of skill names this agent can invoke.
5. **Tool constraints** — Which tools, APIs, or CLIs this agent may use (optional;
   defaults to all available tools).
6. **Optional one-line purpose** — Captured in AGENTS.md and SOUL.md.

If any required input is missing, ask once. Do not provision with a guessed identity.

## The steps

Execute completely and autonomously.

### Step 1 — Verify prerequisites

```bash
if [ -z "$GOVERNANCE_HOME" ]; then
  echo "ERROR: GOVERNANCE_HOME is not set. Set it to your governance nucleus path."
  exit 1
fi
```

### Step 2 — Call provision-project

Run `provision-project` to create the base folder with governance files, directory
skeleton, handoff, session ledger, and troubleshooting stub. The agent folder lives
at the specified project path.

### Step 3 — Create agent-specific identity overlays

Create four files on top of the project-folder scaffold:

| File | Purpose |
|---|---|
| `SOUL.md` | Agent-specific identity: name, role, behavioral boundaries, communication style. This is the agent's PERSONALITY — not the governance nucleus identity. |
| `TOOLS.md` | Capabilities available to this agent: which tools, which APIs, which CLIs, any constraints or restrictions. |
| `MEMORY.md` | Empty but scoped memory structure: long-term facts section, session scratchpad section, learning log section. |
| `USER.md` | Handler profile: who the human is, timezone, preferences, communication style. |

Use templates from `templates/agent/` as starting points. Replace all `<placeholder>`
values with actual agent details.

### Step 4 — Create skills/ reference file

Create `skills/SKILL-REFERENCE.md` — a reference file (not a copy) listing which
governance-nucleus skills this agent can use. Each entry points to the canonical
skill location via `$GOVERNANCE_HOME`:

```markdown
# Skill Reference — <AgentName>

This agent references shared skills from `$GOVERNANCE_HOME/.agent/skills/`.
Skills are NOT copied — they are loaded from the governance nucleus at runtime.

## Authorized Skills

| Skill | Path | Load Trigger |
|---|---|---|
| <skill-name> | $GOVERNANCE_HOME/.agent/skills/<skill-name>/SKILL.md | <trigger> |
```

### Step 5 — Register the agent

Append or update the agent entry in `$GOVERNANCE_HOME/config/agent_registry.yaml`:

```yaml
- name: <AgentName>
  role: "<one-line role description>"
  folder_path: <AgentPath>
  skills:
    - <skill-1>
    - <skill-2>
  tools:
    - <tool-1>
  status: active
  provisioned_date: "<YYYY-MM-DD>"
  handler: "<handler name>"
```

### Step 6 — Self-verify

```bash
AGENT_PATH="<AgentPath>"

for f in AGENTS.md SOUL.md TOOLS.md MEMORY.md USER.md \
         skills/SKILL-REFERENCE.md TROUBLESHOOTING.md .env .gitignore; do
  [ -f "$AGENT_PATH/$f" ] && echo "OK file: $f" || echo "MISSING file: $f"
done

for d in handoffs logs terminal-sessions .backups .remember skills; do
  [ -d "$AGENT_PATH/$d" ] && echo "OK dir: $d" || echo "MISSING dir: $d"
done
```

Every line must print `OK`.

### Step 7 — Hand back

Tell the user the agent is ready. Give the absolute path. Report which skills were
bound. Do not hand the user a list of follow-up tasks — next steps belong in the
agent's handoff.

## What this skill does NOT do

- Does not define the agent's full behavioral rules (that's in SOUL.md, authored
  per-agent).
- Does not copy skills into the agent folder (skills are referenced, not copied).
- Does not duplicate governance documents (inherited from governance nucleus at
  runtime).
- Does not create a Git repository or push to GitHub.
- Does not deploy the agent or start a runtime.

## Scaffold layout

```
<AgentName>/
├── AGENTS.md                 (platform-agnostic overlay — from provision-project)
├── instructions.md           (Hermes portal — from provision-project, if Hermes detected)
├── SOUL.md                   (agent-specific identity — NEW)
├── TOOLS.md                  (capabilities and constraints — NEW)
├── MEMORY.md                 (scoped memory structure — NEW)
├── USER.md                   (handler profile — NEW)
├── TROUBLESHOOTING.md        (from provision-project)
├── .env                      (from provision-project)
├── .gitignore                (from provision-project)
├── skills/
│   └── SKILL-REFERENCE.md    (reference to governance nucleus skills — NEW)
├── handoffs/
│   └── <YYYY-MM-DD>_initial-provisioning.md
├── logs/<lowercased-name>/
│   └── 00_SESSION_LEDGER.md
├── terminal-sessions/
├── .backups/
├── .remember/
│   └── recent.md
└──
```

## Gotchas

1. **Casing is load-bearing.** `TestAgent`, not `testagent`.
2. **SOUL.md is agent-specific.** The governance nucleus SOUL.md is the workspace
   identity. The agent SOUL.md is this agent's personality. They coexist — the agent
   reads both.
3. **No copied skills.** The `skills/` directory contains a reference file, not
   skill copies. Skills load from `$GOVERNANCE_HOME/.agent/skills/` at runtime.
4. **No duplicated governance documents.** The agent inherits governance from the
   nucleus. Do not copy governance files into agent folders.
5. **Timestamps in user's configured timezone.** Defaults to UTC.
6. **Registry is append-only.** Never delete an agent entry. Mark status as
   `archived` if an agent is retired.
7. **USER.md is handler-scoped.** It describes the human who directs THIS agent,
   not the workspace owner generally.

## Templates

- `templates/agent/SOUL.template.md` — Agent identity and personality template
- `templates/agent/TOOLS.template.md` — Capabilities and constraints template
- `templates/agent/MEMORY.template.md` — Memory structure scaffold
- `templates/agent/USER.template.md` — Handler profile template

## Works best with…

- `provision-project` — creates the base project scaffold this skill extends
- `provision-team` — assemble multiple provisioned agents into a coordinated team
- `routing-matrix` — assign models to this agent's roles

---

© IncredAgents. This skill is part of the IncredAgents-Skills repository.
Distributable, user-agnostic, platform-agnostic.
