---
name: provision-team
description: >-
  Provision a new agent team with identity, composition, governance, and orchestration
  protocol. Creates TEAM_IDENTITY.md, TEAM_COMPOSITION.md, TEAM_GOVERNANCE.md, and registers
  the team in the governance nucleus. Use when assembling multiple agents into a coordinated
  team for a shared purpose — code review squads, build teams, research panels, or any
  multi-agent workflow.
type: procedure
status: active
version: 1.0.0
---

# Provision a Team

This skill creates a fully provisioned team folder that coordinates multiple agents
toward a shared purpose. The team inherits governance from `$GOVERNANCE_HOME` and
references existing orchestration infrastructure — it does not reinvent it.

## When to invoke

Invoke when the user says any of:

- "Provision a new team called X."
- "Create team X for Y."
- "Stand up team X."
- "Scaffold a new team at `<path>/X`."
- "Initialize X as a team."

Do NOT invoke for:

- A single agent (use `provision-agent` instead).
- A plain project folder (use `provision-project` instead).
- A team folder that already has `TEAM_IDENTITY.md` and `TEAM_COMPOSITION.md` —
  it's already provisioned.

## Prerequisites

1. `GOVERNANCE_HOME` must be set.
2. Each agent in the team composition must already be provisioned via `provision-agent`.

## Inputs

1. **Team name** — Preserve casing. Examples: `BuildTeam`, `ResearchSquad`, `GrowthTeam`.
2. **Purpose** — One paragraph: what this team collectively accomplishes.
3. **Agent composition** — List of agent names that form the team (each should already
   be provisioned).
4. **Orchestration protocol** — How agents hand work to each other. Default: sequential
   dispatch with convergence voting. Specify if custom.

If any required input is missing, ask once. Do not provision with a guessed composition.

## The steps

Execute completely and autonomously.

### Step 1 — Verify nothing is already provisioned

```bash
TARGET="<TeamPath>"
if [ -d "$TARGET" ] && [ -f "$TARGET/TEAM_IDENTITY.md" ] && [ -f "$TARGET/TEAM_COMPOSITION.md" ]; then
  echo "ALREADY PROVISIONED: $TARGET"
  exit 1
fi
```

### Step 2 — Create the team directory skeleton

```bash
TEAM_PATH="<TeamPath>"
LOGS_SUBDIR=$(basename "$TEAM_PATH" | tr '[:upper:] ' '[:lower:]-')

mkdir -p "$TEAM_PATH/handoffs" \
         "$TEAM_PATH/logs/$LOGS_SUBDIR" \
         "$TEAM_PATH/.backups" \
         "$TEAM_PATH/.remember"
```

### Step 3 — Create the core team files

| File | Content |
|---|---|
| `TEAM_IDENTITY.md` | Team name, purpose, shared blackboard concept, collective behavioral boundaries |
| `TEAM_COMPOSITION.md` | Which agents are on the team, their roles, their folder paths, their skill sets |
| `TEAM_GOVERNANCE.md` | How agents hand work to each other, approval rules, escalation paths, dispatch contract |
| `.env` | Empty file with header comment pointing at `$GOVERNANCE_HOME/.env` as canonical |
| `.gitignore` | `.env`, `.backups/`, `.DS_Store`, `node_modules/`, `dist/`, `build/`, `*.log` |
| `logs/<lowercased>/00_SESSION_LEDGER.md` | Header + first entry recording this provisioning |
| `handoffs/<YYYY-MM-DD>_initial-provisioning.md` | See Step 5 |
| `.remember/recent.md` | Header + provisioning entry |

### Step 4 — Write team files from templates

Use templates from `templates/team/` as starting points. Replace all `<placeholder>`
values with actual team details:

| Placeholder | Replacement |
|---|---|
| `<TEAM_NAME>` | Team name (preserve casing) |
| `<PURPOSE>` | One-paragraph team purpose |
| `<AGENT_LIST>` | Markdown table of agents with roles, paths, skills |
| `<ORCHESTRATION_PROTOCOL>` | How agents coordinate (default: sequential dispatch) |

### Step 5 — Write the initial handoff

Create `handoffs/<YYYY-MM-DD>_initial-provisioning.md`:

- Date, agent, session purpose.
- What was done (directory and file list).
- What is still pending (team purpose refinement, first coordinated task, agent
  additions/removals).
- Open questions (does the team need custom orchestration, what's the first task).

### Step 6 — Register the team

Append or update the team entry in `$GOVERNANCE_HOME/config/team_registry.yaml`:

```yaml
- name: <TeamName>
  purpose: "<one-line purpose>"
  folder_path: <TeamPath>
  agents:
    - <agent-1>
    - <agent-2>
  orchestration: "sequential-dispatch"
  status: active
  provisioned_date: "<YYYY-MM-DD>"
```

### Step 7 — Self-verify

```bash
TEAM_PATH="<TeamPath>"
LOGS_SUBDIR=$(basename "$TEAM_PATH" | tr '[:upper:] ' '[:lower:]-')

for f in TEAM_IDENTITY.md TEAM_COMPOSITION.md TEAM_GOVERNANCE.md .env .gitignore \
         "logs/$LOGS_SUBDIR/00_SESSION_LEDGER.md" ".remember/recent.md"; do
  [ -f "$TEAM_PATH/$f" ] && echo "OK file: $f" || echo "MISSING file: $f"
done

for d in handoffs "logs/$LOGS_SUBDIR" .backups .remember; do
  [ -d "$TEAM_PATH/$d" ] && echo "OK dir: $d" || echo "MISSING dir: $d"
done
```

Every line must print `OK`.

### Step 8 — Hand back

Tell the user the team is ready. Give the absolute path. List which agents are on the
team. Do not hand the user a list of follow-up tasks — next steps belong in the team
handoff.

## What this skill does NOT do

- Does not provision individual agents — each agent must be provisioned via
  `provision-agent` first.
- Does not reinvent orchestration — references the dispatch contract declared in
  `provision-project`.
- Does not create a Git repository or push to GitHub.
- Does not deploy the team or start a runtime.
- Does not duplicate governance documents — inherited from governance nucleus.

## Scaffold layout

```
<TeamName>/
├── TEAM_IDENTITY.md          (team name, purpose, shared blackboard — NEW)
├── TEAM_COMPOSITION.md       (which agents, their roles — NEW)
├── TEAM_GOVERNANCE.md        (handoff rules, approval, escalation — NEW)
├── .env
├── .gitignore
├── handoffs/
│   └── <YYYY-MM-DD>_initial-provisioning.md
├── logs/<lowercased-name>/
│   └── 00_SESSION_LEDGER.md
├── .backups/
├── .remember/
│   └── recent.md
└──
```

## Dispatch contract

Teams use the same dispatch contract as individual projects (see `provision-project`
skill). The orchestrator dispatches tasks to team members, each agent reports a
convergence verdict, and the orchestrator resolves disagreements. The specific
implementation is configured per-platform, not enforced by this skill.

If the team requires custom orchestration beyond the standard dispatch contract,
document it in `TEAM_GOVERNANCE.md` as a pending task — do not invent it during
provisioning.

## Gotchas

1. **Casing is load-bearing.** `BuildTeam`, not `buildteam`.
2. **Agents must be provisioned first.** Each agent in the composition list should
   already exist with its own SOUL.md and TOOLS.md. If an agent doesn't exist yet,
   provision it first.
3. **No duplicated orchestration.** Reference the existing dispatch contract, don't
   rebuild it.
4. **No duplicated governance documents.** The team inherits governance from the
   nucleus.
5. **Timestamps in user's configured timezone.** Defaults to UTC.
6. **Registry is append-only.** Never delete a team entry. Mark status as `archived`
   if a team is retired.
7. **Shared blackboard is conceptual.** TEAM_IDENTITY.md describes a shared blackboard
   concept — the actual implementation (shared file, Notion board, dispatch queue) is
   determined by the orchestration protocol.

## Templates

- `templates/team/TEAM_IDENTITY.template.md` — Team identity and purpose template
- `templates/team/TEAM_COMPOSITION.template.md` — Agent composition and roster template
- `templates/team/TEAM_GOVERNANCE.template.md` — Handoff rules, approval, escalation template

## Works best with…

- `provision-agent` — provision individual agents before assembling them into a team
- `provision-project` — the base scaffold convention this skill builds on
- `routing-matrix` — assign models to team roles via the matrix

---

© IncredAgents. This skill is part of the IncredAgents-Skills repository.
Distributable, user-agnostic, platform-agnostic.
