---
name: hooks-guide
description: >-
  Comprehensive guide to agent lifecycle hooks across platforms. Covers what hooks are,
  when they fire, safety rules, universal patterns (pre-dispatch validation, post-converge
  logging, compaction survival), platform-specific adapters for Hermes, Claude Code, Codex,
  Cursor, OpenCode, and others, and registration/installation instructions per platform.
  Use when designing governance enforcement, pre-flight checks, audit trails, or any
  hook-based automation.
type: reference
status: active
version: 1.0.0
---

# Hooks Guide — Agent Lifecycle Interception

A hook is a function or script that fires at a specific point in an agent's lifecycle —
before a tool call, after a tool call, on session start, on session end, or on compaction.
Hooks enable governance enforcement, audit logging, credential scanning, and pre-flight
validation without modifying the agent runtime's source code.

## Layer 1: Concept Core

### What hooks are

Hooks are interception points in the agent's execution loop. Instead of modifying the
agent runtime, you register scripts or callbacks that the runtime invokes at defined
moments. The hook receives the pending action as input and returns a decision: allow,
block, or modify.

### Key lifecycle events

| Event | Fires when | Use cases |
|---|---|---|
| `pre_tool_use` | Before any tool call is executed | Governance enforcement, file-write gates, credential scanning, scope limiting |
| `post_tool_use` | After a tool call completes | Audit logging, result validation, auto-commit, metrics collection |
| `on_session_start` | When a new agent session begins | Bootstrap checks, environment validation, injection of standing instructions |
| `on_session_end` | Before the session is finalized | Wrapup triggers, session summaries, cleanup |
| `on_compaction` | When context is being compressed | Save critical state before compression, checkpoint summaries |
| `on_error` | When the agent encounters an unrecoverable error | Alerting, graceful degradation, fallback dispatch |

Not all platforms support all events. See Layer 3 for platform-specific availability.

### Safety rules (universal)

1. **Fail-open on exceptions.** If a hook crashes, the tool call proceeds. A broken
   hook must NEVER deadlock the agent. Wrap all hook logic in try/except and exit 0 on
   failure.

2. **Kill-switch sentinel.** Every hook should check for a kill-switch file at the top
   of its execution, before any logic runs. If the sentinel exists, bypass all hook
   logic and allow.

   ```
   KILL_SWITCH = ~/.agent/.hooks-disabled
   if os.path.exists(KILL_SWITCH): sys.exit(0)
   ```

3. **Idempotent.** Running the same hook twice on the same input must produce the same
   result. No side effects that compound across invocations.

4. **Timeout-bounded.** A hook that takes longer than 5 seconds should be considered
   hung. The runtime should time it out and fail-open.

5. **No network calls in pre_tool_use hooks.** A tool call fires dozens or hundreds of
   times per session. Adding a network round-trip to every invocation will make the
   agent unusable. If you need external validation, cache the result or use a
   post-converge logging hook instead.

## Layer 2: Universal Patterns

These patterns apply across all platforms. The implementation details differ per
platform (see Layer 3), but the pattern logic is universal.

### Pattern A: Pre-dispatch validation

**Goal:** Block tool calls that would write to protected paths, execute banned commands,
or operate outside an approved scope.

**Logic:**
1. Receive `tool_name` and `tool_input` from the hook event.
2. Check if the tool is in the gated set (write_file, patch, terminal, execute, etc.).
3. If gated, check if the target path or command matches a protected pattern.
4. If protected → block with a human-readable reason.
5. If not protected → allow.

**Session-scoped sentinel pattern:** For hooks that gate all tools until a specific
file is read (e.g., governance file acknowledgment), create a session-scoped sentinel
on first observation of the required read:

```python
SENTINEL_DIR = os.path.expanduser("~/.agent/sentinels")
session_id = os.environ.get("AGENT_SESSION_ID", "unknown")
sentinel = os.path.join(SENTINEL_DIR, f"governance-ack.{session_id}.sentinel")

if tool_name == "read_file" and is_target_governance_file(tool_input):
    # Mark acknowledged — create sentinel
    os.makedirs(SENTINEL_DIR, exist_ok=True)
    Path(sentinel).touch()
    sys.exit(0)

if not os.path.exists(sentinel):
    # Block all mutating tools until governance is read
    if tool_name in MUTATING_TOOLS:
        print(json.dumps({"action": "block",
              "message": "Read the governance file first."}))
        sys.exit(1)
```

Key design decisions:
- **Session-scoped sentinel names prevent cross-session leaks.** Include the session
  ID in the sentinel filename.
- **Canonical path resolution.** Use `os.path.realpath()` to resolve symlinks and
  relative paths when comparing target paths.
- **Gate all mutating tool families.** Block `write_file`, `patch`, `terminal`,
  `delegate_task`, and `execute_code`. Also gate `search_files` if it can be used
  to read files that should trigger the sentinel.

### Pattern B: Post-converge logging

**Goal:** Record every tool call's outcome for audit and debugging, without slowing
down the agent.

**Logic:**
1. Fire on `post_tool_use`.
2. Serialize tool_name, tool_input (sanitized), exit status, and timestamp to a
   JSONL log file.
3. Never fail — this is a side effect.

```python
LOG_FILE = os.path.expanduser("~/.agent/logs/tool-audit.jsonl")

def log_tool_call(timestamp, session_id, tool_name, tool_input, success, duration_ms):
    entry = {"ts": timestamp, "session": session_id, "tool": tool_name,
             "input": sanitize(tool_input), "ok": success, "ms": duration_ms}
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass  # never fail
```

### Pattern C: Compaction survival

**Goal:** Ensure hook state survives context compression.

Hooks registered in configuration files (not in-memory) survive compaction automatically.
For hooks that reference plan files or session state:

1. Use persistent file names (e.g., `active.plan.md`) rather than session-scoped naming
   (`<session_id>.plan.md`). Session-scoped files become orphaned when the session ID
   changes after compaction.
2. Store checkpoint data in a known location (`~/.agent/checkpoints/`) that the hook
   reads on every invocation.
3. If your hook injects context into the agent (e.g., standing instructions on session
   start), re-inject on the first post-compaction tool call by checking for a
   compaction marker.

## Layer 3: Platform Adapters

Each platform has a different hook mechanism. The table below maps universal patterns
to platform-specific implementations.

| Platform | Hook Type | Mechanism | pre_tool_use | post_tool_use | on_session_start | Notes |
|---|---|---|---|---|---|---|
| **Hermes** | Shell script hooks | `config.yaml` → `hooks.pre_tool_use` array | ✅ stdin JSON contract | ✅ via plugin system | ✅ via plugin system | Most mature hook system. Separate shell hooks (config) and Python plugins (~/.hermes/plugins/). Shell hooks use exit-code protocol. |
| **Claude Code** | `.claude/settings.json` hooks | `hooks` object in settings | ❌ not native | ❌ not native | ✅ `PostToolUse` (limited) | Claude Code's native hook support is minimal. Most Patterns A-C require a wrapper script that pipes through the Claude CLI. |
| **Codex (OpenAI)** | Custom middleware | OpenAI Agent SDK middleware | ❌ not native | ❌ not native | ✅ via `AgentHooks` class | SDK-based. Pre/post tool use require wrapping the `Runner` or implementing custom `Tool` subclasses. |
| **Cursor** | `.cursor/rules/` + `.cursor/commands.json` | Rule files + custom commands | ❌ not native | ❌ not native | ❌ not native | No native hook system. Use rule files for static constraints and custom commands for manual invocation. |
| **OpenCode** | Plugin system (TypeScript) | `opencode` plugin API | ❌ not native | ❌ not native | ❌ not native | Plugin API is evolving. Check opencode documentation for current hook support. |
| **Continue** | `.continue/config.json` | `slashCommands` + system messages | ❌ not native | ❌ not native | ❌ not native | No hook system. Use system messages for static constraints. |
| **Aider** | `.aider.conf.yml` | Configuration + pre-commit hooks | ❌ not native | ❌ not native | ❌ not native | Pre-commit hooks via `--pre-commit` flag. Limited to code checkers, not general-purpose interception. |
| **Cline** | `.clinerules` + MCP servers | Rule files + MCP tool hooks | ❌ not native | ❌ not native | ❌ not native | MCP server tools can act as post_tool_use monitors for specific tool families. |

### Manual workarounds for platforms with no native hooks

For platforms without native hook support (Cursor, Continue, Aider, Cline, etc.):

1. **Static constraints (Pattern A-lite):** Use system messages, rule files, or
   `.cursor/rules/` to declare what the agent must not do. This is advisory, not
   enforceable — the agent can ignore it.

2. **Wrapper script (Pattern A full):** Run the agent CLI through a wrapper that
   intercepts tool calls:
   ```bash
   # concept — implementation varies per platform
   agent-cli 2>&1 | hook-filter.py
   ```
   The filter reads the agent's output stream, detects tool calls, and can inject
   block responses or modify parameters before they reach execution.

3. **Pre-commit hooks (Pattern A — write-only):** If the platform supports git
   pre-commit hooks (Aider does), use them to validate files before they're committed.
   This catches write_file and patch but not terminal or execute.

4. **Post-hoc audit (Pattern B):** Parse session transcripts/logs after the session
   ends. Not real-time, but provides an audit trail.

## Layer 4: Registration — Where to Install Hooks

### Hermes

**Shell hooks (pre_tool_use):**
```yaml
# ~/.hermes/config.yaml
hooks:
  pre_tool_use:
    - command: python3 ~/.hermes/scripts/governance-gate.py
      matcher: ^(write_file|patch|terminal|delegate_task)$
    - command: python3 ~/.hermes/scripts/credential-scanner.py
      matcher: ^(write_file|patch)$
```

Scripts live in `~/.hermes/scripts/`. The `matcher` field is a regex applied against
the tool name. See the `hermes-hook-authoring` and `hermes-hook-wire-protocol` skills
for the full stdin/stdout I/O contract.

**Python plugins (post_tool_use, on_session_start, on_session_end):**
```
~/.hermes/plugins/
└── my-plugin/
    ├── plugin.json    # manifest: name, version, hooks[] list
    └── main.py        # hook callbacks
```

Plugins run inside the Hermes process. Use `sys.stderr.write()` for logging, never
`print()` (Electron IPC channel corruption).

**Kill-switch:** Create `~/.hermes/.hooks-disabled` to bypass all hooks. Works from
any interface (CLI, Telegram, cron).

### Claude Code

```json
// .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|Bash",
        "command": "python3 ~/.claude/hooks/audit-logger.py"
      }
    ]
  }
}
```

Limited to `PostToolUse` and `Notification`. For pre-tool-use enforcement, use a
wrapper script.

### Codex (OpenAI)

```python
# In your agent entry point
from openai import AgentHooks

class GovernanceHooks(AgentHooks):
    async def on_tool_start(self, context, agent, tool):
        # Pre-tool-use logic here
        pass

    async def on_tool_end(self, context, agent, tool, result):
        # Post-tool-use logic here
        pass
```

Register with the `Agent` or `Runner` constructor.

### Cursor

No native hooks. Alternatives:
- `.cursor/rules/project.md` — static constraints (advisory)
- `.cursor/commands.json` — manual slash commands for pre/post checks

### OpenCode

Check the OpenCode plugin API. If plugin hooks are unavailable, use a wrapper script
or post-hoc audit.

---

## Works best with…

- `provision-project` — adds hook configuration stubs to freshly provisioned projects
- `routing-matrix` — add a pre-dispatch hook that validates dispatches against the matrix
- `provision-team` — team governance hooks for enforcement across the agent crew

---

© IncredAgents. This skill is part of the IncredAgents-Skills repository.
Distributable, user-agnostic, platform-agnostic.
