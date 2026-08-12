---
name: goal
description: IncredAgents /goal command — structured planning + launch infrastructure (Swarm Heartbeat, Telegram) + stateful execution + workspace governance. Fuses plan-for-goal (planning discipline) with persistent state management plus quad-logging, approval gates, completion audit, and Pacific Time.
argument-hint: "[status|pause|resume|clear|complete] [--tokens N] <objective>"
metadata:

  install_path: ./goal/
  requires:
    - python3 (system)
    - sqlite3 (stdlib)
    - ./goal/scripts/goal.py
---

# Goal — IncredAgents Structured Execution

Two-phase protocol: every new objective is **planned** before it is **executed**.
State persists across turns in SQLite. Completion is gated by a real audit against evidence.

## Phase 0 — Parse the User's Intent

What did the user actually type after `/goal`?

| User Input | Action |
|---|---|
| `/goal` (no args) | Show current goal state → **Phase 3** |
| `/goal status` | Show current goal state → **Phase 3** |
| `/goal pause` | Pause active goal → **Phase 3** |
| `/goal resume` | Resume paused goal → **Phase 3** |
| `/goal clear` | Archive current goal → **Phase 3** |
| `/goal complete` | Run completion audit, then complete → **Phase 4** |
| `/goal <anything else>` | Treat as new objective → **Phase 1** |

## Phase 1 — Plan (New Objectives Only)

Takes the raw objective and forces it through a structured planning pass BEFORE
any execution begins. This is non-negotiable. Skipping this phase is how /goal
runs burn 500 turns on an unbounded task with a vibe-word DoD.

### 1.1 — Extract the Core

Reduce the user's words to:
- **Outcome**: what is true when this is done (one sentence, no vibe words)
- **Medium**: code, content, ops, design, research, or mix
- **Urgency**: is there a hard deadline or is this exploratory

If the objective is missing any of these, ask ONE tight question before drafting.

### 1.2 — Draft the Structured Plan

Write a plan file to `./plans/{slug}_{YYYY-MM-DD}.md` (create the folder if needed).
Slug = lowercase, dashes, first 3-5 words of the objective.

Locked sections (do NOT add new ones, do NOT skip marked with *):

```markdown
# Plan · {Title}

## Brief
[1-2 sentences. State the goal, not the steps.]

## Stack
- Tool, framework, API, model — one per bullet
- Name version when load-bearing; flag paid APIs that need cost approval

## Scope
**Visuals** — [only when visual; drop header otherwise]
- [What it looks like]

**Functionality**
- [What it does]

## Out of Scope *
- Explicit non-goals. At least 2 bullets. This section is load-bearing.

## Constraints
- Rules that hold throughout (single file, no build step, no new deps, brand rules)

## Definition of Done *
[ONE verifiable sentence. A small evaluator can judge it from the transcript.
No vibe words: "clean", "polished", "great UX", "feels nice."]

## Acceptance Criteria *
- 5-10 bullets, each independently true/false
- Bad: "looks good on mobile"  →  Good: "renders at 360px width with no horizontal scroll"

## Verification
- Exact commands or checks run each turn to produce evidence
- Skip only when DoD IS a literal runnable command

## Turn Budget *
Stop after {N} turns. Light=15-25, Medium=30-50, Heavy=60-100. Cap at 100.

## References / Risks
- Optional. Skip if empty. Don't pad.
```

### 1.3 — Present the Plan

Show the user:
1. The plan file path
2. A copy-paste-ready one-liner summarizing DoD + top 3 acceptance criteria + turn budget
3. Ask: "Proceed with this plan?"

Do NOT execute until the user confirms. This is the Planning First Law (Coding Rule 5).

If the user says go, proceed to Phase 2.

## Phase 2 — Execute

### 2.1 — Launch Infrastructure

When a new goal is invoked, two infrastructure systems fire simultaneously
via the `launch()` function in goal.py:

1. **Agent Swarm Heartbeat** — `start_swarm_heartbeat()` runs
   `swarm_heartbeat.sh` in a background process. It monitors all active agent processes via `pgrep`, posts vitals to WatchTower every 60s,
   and sends alerts on health state changes. Returns the PID which is stored
   in the goal's `swarm_pid` column.

2. **Telegram Notification** — `telegram_send()` delivers a message to the user
   with the goal title, objective, and plan file path.
   Credentials are loaded from your .env file. The notification
   is non-blocking and degrades gracefully if credentials are missing.

Both are non-negotiable for new goal invocations. The launch output is
printed to the terminal so the agent sees it.

### 2.2 — Persist Goal State

Run the helper to record the goal in SQLite:

```bash
python3 ./goal/scripts/goal.py invoke "<objective>" --plan "{plan_file_path}"
```

### 2.3 — Log to Session Ledger

Append to `00_SESSION_LEDGER.md`:
```
### {Pacific Date} {Pacific Time} — /goal Started: {Title}
- Plan: {plan_file_path}
- DoD: {Definition of Done sentence}
- Turn budget: {N} turns
- Status: active
```

### 2.4 — Execute Turn by Turn

Work the plan. Each turn:
1. Check the acceptance criteria — what's still unverified?
2. Take the next concrete action
3. Update `tokens_used` and `time_used_seconds` in the goal state via:
   ```bash
   python3 ./goal/scripts/goal.py update --tokens-used {estimated} --time-used {seconds}
   ```
4. Swarm Heartbeat continues running in the background (PID in `swarm_pid` column).
   Verify it is still alive if the goal runs longer than a few minutes.
5. If you hit the turn budget, pause and report: "Turn budget reached. /goal resume to continue."
6. If you hit a destructive action (deleting files, pushing to production, modifying cloud resources), STOP and ask the user..
7. If you hit something that needs a credential you don't have, STOP and ask. Name the missing credential specifically.

### 2.5 — Governance Within Execution

- **No deletion** — archive, don't delete. Applies to files, DB rows, vector records.
- **WatchTower surface** — if the work produces a decision, finding, or report worth preserving, post a brief.
- **Pacific Time** — all timestamps in `America/Los_Angeles`.
- **Dual-layer** — any new artifact gets YAML frontmatter + human prose.

## Phase 3 — State Operations (Status / Pause / Resume / Clear)

### /goal status
Show current goal with elapsed time, token state, and remaining acceptance criteria.

### /goal pause
Pause the active goal. Record pause reason in the ledger. The session may be paused and resumed.

### /goal resume
Resume the paused goal. Re-read the plan file first. Log continuation to the ledger.

### /goal clear
Archive the goal — do NOT delete the SQLite row. Mark status `archived` and log
the closure to the session ledger with final state (what was done, what was not,
why it was cleared).

## Phase 4 — Completion Audit (Before /goal complete)

This is the anti-vaporware gate. Do NOT mark a goal complete without running
every step here against real, current evidence.

### 4.1 — Audit Steps

1. **Restate the objective** as concrete deliverables and success criteria
2. **Build a prompt-to-artifact checklist** — map every requirement, named file,
   command, test, gate, and deliverable to concrete evidence
3. **Inspect relevant files, command output, test results, repo state, or other
   real evidence** — use Read, Bash, or ls; do not recall from memory
4. **Identify missing, incomplete, or weakly verified requirements** — flag each
   specifically
5. **If anything is missing, continue work** — do not proceed to complete
6. **Only when the audit passes**, mark complete:

```bash
python3 ./goal/scripts/goal.py complete
```

### 4.2 — Log Completion

Append to `00_SESSION_LEDGER.md`:
```
### {Pacific Date} {Pacific Time} — /goal Complete: {Title}
- Turn count: {N}
- Time used: {elapsed}
- Tokens used: {tokens}
- Acceptance criteria met: {X}/{Y}
- Completion audit: passed at {Pacific Time}
```

### 4.3 — Report to User

```
/goal complete: {Title}
- {X}/{Y} acceptance criteria met
- Time: {elapsed}
- Evidence: {plan file path}
- Ledger: {session ledger entry}
```

Do NOT report a list of things the user still needs to do.

## Anti-Patterns

- Don't skip the planning phase for "quick" goals — the quick ones are where scope creeps
- Don't write DoDs with vibe words — if you can't prove it, don't promise it
- Don't skip Out of Scope — it IS load-bearing
- Don't pad sections — empty is fine, weak is not
- Don't ask multiple clarifying questions — one or none
- Don't defer discovered work to "version two" — if it is in scope, do it now
- Don't claim completion without inspecting real files — memory is not evidence
