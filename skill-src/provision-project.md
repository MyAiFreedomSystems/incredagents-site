---
name: provision-project
description: >-
  Provision a project folder for AI agent work with governance files, directory skeleton,
  session ledger, and platform-specific agent overlays. Produces a fully scaffolded workspace
  that agents on any platform (Hermes, Claude Code, Codex, Cursor, OpenCode, etc.) can use
  immediately. Use when creating a new project, initializing a workspace, or standing up a
  fresh agent-ready folder.
type: procedure
status: active
version: 1.0.0
---

# Provision a Project

This skill creates a project folder that is immediately usable by AI agents on any
platform. The folder follows a canonical structure and inherits governance from a
central nucleus directory configured via the `GOVERNANCE_HOME` environment variable.

## When to invoke

Invoke when the user says any of:

- "Provision a new project called X."
- "Create a new project folder called X and set up."
- "Stand up X."
- "Scaffold a new project at `<path>/X`."
- "Initialize X as a project."

Do NOT invoke for:

- A governance-only folder or nucleus directory.
- A folder that already has `instructions.md` and `AGENTS.md` — it's already provisioned.
- A worktree of an existing project — worktrees inherit their parent's scaffolding.

## Prerequisites

```bash
# Set this to the path of your governance nucleus (the single source of truth)
export GOVERNANCE_HOME="$HOME/path/to/governance-nucleus"
```

All path references in this skill use `GOVERNANCE_HOME`. If unset, the skill errors
with instructions to set it.

## Inputs

1. **Project name** — Preserve the casing. Examples: `Rubric`, `Forge`, `Sentinel`.
2. **Absolute project path** — Where the folder will live (e.g., `~/Documents/MyProject`).
3. **Optional one-line purpose** — Captured in `AGENTS.md` and the initial handoff.
   Placeholder text if not stated.
4. **Optional `agents:` block** — A YAML list of agents to auto-provision into the
   project. Each entry requires `name`, `role`, and `skills`. When present,
   `provision-agent` is invoked for every agent after the project skeleton is built.

   ```yaml
   agents:
     - name: Researcher
       role: Market research and analysis
       skills: [market-research, web_search]
     - name: Builder
       role: Implementation and builds
       skills: [software-development, terminal]
   ```

If any required input is missing, ask once. Do not provision with a guessed name.

## Platform detection

Before provisioning, detect which agent platforms are present. The skill auto-generates
platform-specific instruction files:

| Platform | File created | Detection |
|---|---|---|
| Hermes | `instructions.md` | `HERMES_SESSION_ID` env var or `~/.hermes/` exists |
| Claude Code | `CLAUDE.md` | `claude` CLI in PATH |
| Codex (OpenAI) | `.codex/AGENTS.md` | `codex` CLI in PATH |
| Cursor | `.cursor/rules/project.md` | `.cursor/` directory exists |
| OpenCode | `AGENTS.md` | `opencode` CLI or `OPENCODE_API_KEY` set |
| Generic / unknown | `AGENTS.md` | Always created as fallback |

At minimum, `AGENTS.md` is always generated. Platform-specific files are additive —
they do not replace `AGENTS.md`, they supplement it.

## The steps

Execute completely and autonomously. Do not hand the user a checklist.

### Step 1 — Verify nothing is already provisioned

```bash
TARGET="<ProjectPath>"
if [ -d "$TARGET" ] && [ -f "$TARGET/AGENTS.md" ]; then
  echo "ALREADY PROVISIONED: $TARGET"
  exit 1
fi
```

### Step 2 — Create the canonical directory skeleton

```bash
PROJECT_PATH="<ProjectPath>"
LOGS_SUBDIR=$(basename "$PROJECT_PATH" | tr '[:upper:] ' '[:lower:]-')

mkdir -p "$PROJECT_PATH/handoffs" \
         "$PROJECT_PATH/logs/$LOGS_SUBDIR" \
         "$PROJECT_PATH/terminal-sessions" \
         "$PROJECT_PATH/.backups" \
         "$PROJECT_PATH/.remember"
```

### Step 3 — Generate platform-specific instruction files

Generate from `templates/instructions.template.md`:

| File | Content |
|---|---|
| `AGENTS.md` | Platform-agnostic overlay — always created |
| `instructions.md` | Hermes portal — identical content to AGENTS.md |
| `CLAUDE.md` | Claude Code overlay — if claude CLI detected |
| `.codex/AGENTS.md` | Codex overlay — if codex CLI detected |
| `.cursor/rules/project.md` | Cursor rules — if .cursor/ exists |

All files share the same core content with platform-specific frontmatter:

1. Title: `# <ProjectName> — AI Agent Workspace`
2. One-paragraph description (from user statement or placeholder).
3. Governance section pointing to `$GOVERNANCE_HOME/`.
4. Primary Skills block listing key skills with load triggers.
5. Credentials section pointing to `$GOVERNANCE_HOME/.env` and `.secrets/` as canonical.
6. Timezone (user-configured; defaults to UTC if not set).
7. Staging boundary rule: build in staging, merge/deploy/push on approval only.

**Do NOT include:** personal names, hardcoded paths, model preferences, or a mandatory
init chain that assumes a specific platform's read model.

### Step 4 — Create supporting files

| File | Content |
|---|---|
| `.env` | Empty file with header comment pointing at `$GOVERNANCE_HOME/.env` as canonical |
| `.gitignore` | `.env`, `.backups/`, `.DS_Store`, `node_modules/`, `dist/`, `build/`, `*.log` |
| `logs/<lowercased>/00_SESSION_LEDGER.md` | Header + first entry recording this provisioning |
| `TROUBLESHOOTING.md` | Placeholder with project name and date |
| `.remember/recent.md` | Header + provisioning entry for quick session context |

### Step 5 — Write the initial handoff

Create `handoffs/<YYYY-MM-DD>_initial-provisioning.md`:

- Date, agent, session purpose.
- What was done (directory and file list).
- What is still pending (project purpose, tech stack, port assignment, first
  content-bearing handoff).
- Open questions (what does the project build, does it need its own credentials).

### Step 6 — Auto-provision agents (conditional)

If the manifest includes an `agents:` block, provision each agent into the project.

For every entry in the `agents:` list, load the `provision-agent` skill and execute
it with these parameters:

| Parameter | Source |
|---|---|
| Agent name | `agents[].name` |
| Agent role | `agents[].role` |
| Skills list | `agents[].skills` |
| Target project path | The project folder just created |

Agents are provisioned into `<ProjectPath>/.agent/team/<AgentName>/`. Each gets its
identity overlay, scoped skills, and session ledger stub per `provision-agent`'s spec.

If the `agents:` block is absent, skip this step without comment.

### Step 7 — Self-verify

```bash
PROJECT_PATH="<ProjectPath>"
LOGS_SUBDIR=$(basename "$PROJECT_PATH" | tr '[:upper:] ' '[:lower:]-')

for p in handoffs "logs/$LOGS_SUBDIR" terminal-sessions .backups .remember; do
  [ -d "$PROJECT_PATH/$p" ] && echo "OK dir: $p" || echo "MISSING dir: $p"
done

for f in AGENTS.md instructions.md .env .gitignore TROUBLESHOOTING.md \
         "logs/$LOGS_SUBDIR/00_SESSION_LEDGER.md" ".remember/recent.md"; do
  [ -f "$PROJECT_PATH/$f" ] && echo "OK file: $f" || echo "MISSING file: $f"
done
```

Every line must print `OK`.

## What this skill does NOT do

- Does not define the project's purpose.
- Does not assign a port or tech stack.
- Does not copy code from other projects.
- Does not create a Git repository or push to GitHub.
- Does not invoke a build team — provisioning is mechanical scaffolding.

## Scaffold layout

```
<ProjectName>/
├── AGENTS.md                 (platform-agnostic agent overlay)
├── instructions.md           (Hermes portal — same content as AGENTS.md)
├── CLAUDE.md                 (if Claude Code detected)
├── .codex/AGENTS.md          (if Codex detected)
├── .cursor/rules/project.md  (if Cursor detected)
├── TROUBLESHOOTING.md
├── .env
├── .gitignore
├── handoffs/
│   └── <YYYY-MM-DD>_initial-provisioning.md
├── logs/<lowercased-name>/
│   └── 00_SESSION_LEDGER.md
├── terminal-sessions/
├── .backups/
├── .agent/                   (if agents: block was provided)
│   └── team/
│       └── <AgentName>/      (identity overlay, scoped skills, ledger)
├── .remember/
│   └── recent.md
└──
```

## Dispatch contract

Agents provisioned into this project are expected to coordinate via a dispatch
mechanism. The specific implementation (Hermes `delegate_task`, Claude Code
sub-agents, Codex task delegation, custom dispatch script) is configured per-platform
in the platform-specific instruction file. This skill does not enforce a particular
dispatch tool — it declares the contract that agents observe:

1. **Orchestrator dispatches, workers execute.**
2. **Each worker reports a convergence verdict** (pass, fail, needs-revision).
3. **The orchestrator resolves disagreements before proceeding.**

## Gotchas

1. **Casing is load-bearing.** `Rubric`, not `rubric`.
2. **No hardcoded paths.** Derive every path from `GOVERNANCE_HOME` and the target
   folder's actual location.
3. **No symlinks.** Copy templates once, reference nucleus by path everywhere else.
4. **Both `AGENTS.md` and platform-specific files** — identical core content,
   different filenames, same portal contract.
5. **Set `GOVERNANCE_HOME` before running.** The skill errors immediately if unset.

## Templates

- `templates/instructions.template.md` — Core content template for AGENTS.md and all
  platform-specific instruction files. Replace `<PROJECT_NAME>`, `<PURPOSE>`,
  `<GOVERNANCE_HOME>`, and `<TIMEZONE>` placeholders.

## Works best with…

- `provision-agent` — auto-provision agents into a freshly created project
- `provision-team` — assemble provisioned agents into a coordinated team
- `routing-matrix` — configure model assignments for the agents in this project

---

© IncredAgents. This skill is part of the IncredAgents-Skills repository.
Distributable, user-agnostic, platform-agnostic.
