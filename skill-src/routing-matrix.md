---
name: routing-matrix
description: >-
  Configure a multi-model routing matrix for AI agent orchestration. Define role assignments,
  model pools, provider lanes, fallback chains, and dispatch policies. Ships as a user-fillable
  YAML template — pre-populated with role structure and governance policies; the user fills in
  model names, providers, and ban lists. Use when setting up agent team orchestration, defining
  which models serve which roles, or configuring automated model dispatch.
type: template
status: active
version: 1.0.0
---

# Routing Matrix — Model Dispatch Configuration

This skill defines a routing matrix: which AI models are assigned to which agent roles,
how fallback chains resolve, and what policies govern model selection at dispatch time.

## What this is

A structured YAML configuration that maps model pools (cloud, local, direct API, MLX)
onto agent roles (orchestrator, advisor, builder, qa, linter, kaizen, logger) and
declares the policies that shape dispatch behavior.

**This skill ships as a template.** The role structure and governance policies are
pre-configured. You fill in model names, provider lanes, and ban lists.

## Quick start

1. Copy `templates/routing-matrix.template.yaml` to your project root.
2. Rename it to `routing-matrix.yaml`.
3. Fill in the `<...>` placeholders with your model names, providers, and context windows.
4. Run the schema validator: `python3 routing-matrix/scripts/validate.py routing-matrix.yaml`

## Role structure

The matrix pre-defines 10 roles in a fixed sequence. Each role has:

| Field | Description |
|---|---|
| `primary` | Model ID to use when available |
| `provider` | Provider lane (openai, anthropic, ollama-local, ollama-cloud, openrouter, zai, mlx-local, etc.) |
| `strength` | Human-readable description of why this model fits this role |
| `sequence_order` | Position in the sequential pipeline (1 = first to run after orchestrator) |
| `fallback_chain` | Ordered list of `provider/model-id` alternatives if primary is unavailable |
| `lens` | What this role evaluates: correctness, security, design quality, implementation fidelity |

| Role | Sequence | Purpose | Parallel? |
|---|---|---|---|
| `orchestrator` | coordinator | Holds the sequence, dispatches, tracks convergence | No |
| `advisor1` | 1 | Synthesis, second-order consequences, security watch | No |
| `advisor2` | 2 | Distinct lens from advisor1 — different model | No |
| `advisor3` | 3 | Distinct lens from advisor1/2 — different model | No |
| `builder` | 4 | Implementation, file paths, diff size | No |
| `qa` | 5 | Evidence verification, visual QA | No |
| `linter` | 6 | Correctness, schemas, contracts, security watch | No |
| `kaizen1` | 7 | Continuous improvement, leave-it-better-than-found | No |
| `kaizen2` | 8 | Sequential after kaizen1, distinct model | No |
| `logger` | final | Read-only audit trail, compresses raw output | No |

Additional optional roles: `researcher` (can run in parallel), `council_deliberator`, `council_chairman`.

## Policies

These are pre-configured in the template and should be adjusted to your preferences:

### `no_repeat_model_in_sequence`
**Default: `true`.** No model may appear in two consecutive roles. This forces perspective
diversity — each voice in the chain uses a different model, catching blind spots that
a single model's training data would miss.

### `team_shape`
**Default: 3 advisors + 2 kaizen (8 voices total).** Defines how many instances of each
role type run. You can shrink this to 2+1 for lighter tasks or expand for critical work.

### `always_be_testing`
**Default: `true`.** Every new model is tested in real work — never synthetic benchmarks.
A model under test is used in actual tasks alongside the team so quality is evaluated
by other voices. The team's convergence verdict determines whether a model stays in the
rotation or is removed.

### `parallel_allowed_roles`
**Default: `[researcher]`.** Which roles can run in parallel. Researchers can fan out
because research is isolated analysis — no sequential dependency.

### `single_model_mode`
**Default: `false`.** When `true`, all roles use the same model (first available from
a configured pool). This bypasses the diversity policies. Useful for rapid prototyping,
low-stakes tasks, or when only one model is available. The orchestrator still dispatches
sequentially — only the model assignment changes.

### `reject_dispatch_for_banned`
**Default: `true`.** If a dispatch request names a model in the `banned` list, reject
the dispatch instead of silently substituting.

## Fallback logic

When the primary model for a role is unavailable (provider down, rate-limited, context
window exhausted), the dispatcher walks the `fallback_chain` in order:

1. Check if provider is reachable (HTTP 200 on health endpoint).
2. If reachable and model is not in `banned` list → use it.
3. If unreachable or banned → advance to next entry in chain.
4. If chain exhausted → escalate: use the orchestrator's fallback chain instead.
5. If orchestrator chain also exhausted → abort with an error that lists every model
   tried and why each failed.

A model is "unavailable" when:
- Provider returns 5xx or timeout on three successive health checks
- Provider reports the model as not found
- Rate limit headers indicate exhaustion with no retry window
- Context window is smaller than the task requires

A model is NOT unavailable just because another instance is busy — queue, don't fall back.

## Provider lanes

The matrix supports these provider types:

| Lane | Description |
|---|---|
| `openai` | OpenAI API (gpt-4o, o4-mini, etc.) |
| `anthropic` | Anthropic API (claude-sonnet-4-20250514, etc.) |
| `ollama-local` | Local Ollama daemon (no rate limits, zero cost) |
| `ollama-cloud` | Ollama Cloud hosted endpoints |
| `openrouter` | OpenRouter unified API |
| `google` | Google Gemini API |
| `deepseek` | DeepSeek API |
| `zai` | Z.AI / GLM direct API |
| `mlx-local` | Apple Silicon MLX (fast local inference) |
| `custom-*` | Any custom provider registered in your agent config |

## Template file

The fillable template is at `templates/routing-matrix.template.yaml`. It includes:
- All role entries with `<PLACEHOLDER>` values
- Commented example rows showing realistic model assignments
- The full policy block with defaults
- A `banned` list (initially empty)
- Schema version tracking

## Scripts

- `scripts/validate.py` — Validates a routing-matrix.yaml against the schema. Reports
  missing required fields, duplicate roles, malformed fallback chains, and banned models
  inadvertently assigned to roles.

## Works best with…

- `provision-team` — after defining your routing matrix, provision a team that uses it
- `provision-agent` — each agent references the matrix for its model assignments
- `hooks-guide` — add a pre-dispatch validation hook that checks the matrix before routing

---

© IncredAgents. This skill is part of the IncredAgents-Skills repository.
Distributable, user-agnostic, platform-agnostic. Fill in your own models and providers.
