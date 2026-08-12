---
name: pre-build-sop
description: Force real preparation before building anything. Activate whenever the request contains "build", "create", "make", "set up", "train", "implement", "develop", "scaffold", "add a feature", "integrate", or any word that means producing code, files, schemas, pipelines, or systems. This skill prevents the most destructive failure mode in this workspace — pattern-matched building without verified current knowledge or observed inputs. Pairs with qa-protocol (which enforces verification at the end); this skill enforces verification at the beginning. If both skills apply, run pre-build-sop first and qa-protocol last.
---

# Pre-Build Standard Operating Procedure

## Why this exists

Agents default to writing code immediately. They pattern-match from memory, skip research, never look at real inputs, make a dozen unstated assumptions, and then patch bugs forever instead of admitting the initial approach was wrong.

Every bug stacks on top of the wrong foundation. The work looks like progress. It isn't. the user pays for every hour of "making it look like it's working."

This SOP replaces that default with a discipline: **no code until six steps are done.**

## Relationship to Constitution Part 13 (Signals Gap Law + Progression Law)

This skill pairs with CONSTITUTION.md Part 13. Pre-build-sop governs PREPARATION discipline before building. Part 13 governs EXECUTION discipline after approval — including in-scope discovered work surfaced during prep. Together they close the full cycle: prepare completely, then execute completely.

If a prep step surfaces work adjacent to the authorized task (a bug in a dependency, a missing test, a README that needs writing, an upstream issue worth filing), Part 13's Progression Law says execute it the same session with subagents — not "save for version two." Dismissal during prep is the same failure mode as dismissal during execution.

The practical pattern: when you surface adjacent work during the six prep steps, name it in Step 5 (the plan), get the user's nod, then execute it as a subagent thread while proceeding with the main build. Do NOT present it as a menu item for "next session."

## The Rule

Until all six prep steps are complete and the plan is approved by the user, the agent produces **no code, no file creation, no architectural decisions, no scaffolding, no package installs**.

Reading, searching, querying APIs by hand, inspecting real data — allowed.

Writing anything the user could mistake for "starting to build" — not allowed.

## The Six Prep Steps

### 1. State the task in one sentence — AND name the spirit separately

Write two sentences before anything else.

**Sentence one — the task.** What is actually being built and why, in the agent's own words.

**Sentence two — the spirit.** The outcome the user is reaching for, stated as the result she wants to be true when the work is done. Not the mechanism she described to get there. the user may not be a coder; they describe outcomes in the shape of mechanisms, because the mechanism is the handle they can see. If the agent takes the mechanism as the ask and misses the outcome, the agent builds the letter of the request and misses the spirit. That is the most expensive failure mode in this workspace.

If the two sentences point in different directions, something is off. Surface the gap to the user and propose the approach that honors the spirit — even if that approach differs from the literal request. If the task does not fit in one sentence, the agent does not understand it yet. Ask the user clarifying questions until it does fit.

Common failures this catches:

- Mistaking a directory for a marketplace
- Mistaking a prototype for a production system
- Mistaking "clone this site" for "clone this site's UX and data model" vs "clone this site's business logic"
- Mistaking "delete the secret from git history" for "delete the secret from git history AND the working file AND make a backup of the secrets AND…" (scope expansion in the shape of being thorough)
- Assuming scope that wasn't requested

See the "Spirit Over Letter" section in the anchor skill for the full discipline.

### 2. Name the domain

What field of software is this task actually in?

- Fine-tuning an LLM? → ML ops domain
- Scraping business data? → Data aggregation domain
- Building a directory? → Local search + geocoding domain
- Building auth? → Identity/security domain
- Building a form → CRUD UI domain

The domain name determines what research is needed in Step 3. Naming it wrong means researching the wrong thing. If the agent is unsure of the domain, it should ask the user rather than guess.

### 3. Do REAL research on the domain

**Spawn a research agent.** Not inline research from memory. Not a single WebFetch of the target site. A dedicated sub-agent with a research prompt.

The research agent's job is to find **current** (last 12 months) practitioner consensus on:

- The correct approach for this type of task
- Current tools, frameworks, libraries, and their versions
- Recommended configurations and parameter values
- **Known failure modes in this domain** — what breaks in production
- Alternative approaches and their trade-offs
- Anything specific to the target environment (hardware, region, user locale, data source)
- Pricing, rate limits, and quotas for any third-party service being considered

The research agent prompt must require:
- **Dated sources** — URLs with publication dates, not "as of my training cutoff"
- **Direct reading** of official docs and GitHub READMEs (not blog recaps)
- **Structured output** with sections for each bullet above
- **Explicit flagging** of anything the agent could not find or verify
- **A concrete recommendation** for the specific situation, not generic advice

**Read the full report.** Not just the summary. Quote from it in the plan.

If the research agent returns generalities, re-prompt it. Accept no hand-waving.

### 4. Inspect the actual inputs

Before designing anything that will consume or produce data, **see the real data**.

- Open the real data files with Read or `head`
- Query the real database with actual SELECTs
- Hit the real API with curl and look at the JSON
- Look at the actual web page with WebFetch
- Sample the actual user's request patterns if they exist

Design decisions must be grounded in the real state of the inputs. Never design against an imagined API contract or an assumed data shape.

Things to actively check:
- Format, structure, encoding
- Edge cases in the existing data (missing fields, nulls, unicode, oversized records)
- Noise level — is this clean production data or messy scraped data?
- Size — how much data are we dealing with?
- Error responses — what does the API return when things go wrong?
- Rate limits observed in practice (not just documented)

### 3.5 Name the failure modes you expect to hit in production

Before the plan, write down **at least 8 things that will go wrong** in the chosen approach.

If the agent can't name 8 failure modes, the research in Step 3 was not thorough enough. Go back.

Examples from the local-business-directory domain:
- Rate limit from geocoding provider
- Rate limit from business search provider
- Provider returns HTML instead of JSON (maintenance page, captcha)
- Provider returns empty result set for legitimate queries
- Duplicate businesses across sources (same place, different IDs)
- User types a misspelled city
- User types 1 or 2 characters
- User spams the search box (race conditions)
- Stale cache from previous search
- Image CDN blocks hotlinking in some browsers
- Network timeout mid-populate
- Database constraint violation on upsert

Each failure mode becomes something the plan must account for — either by handling it, or by explicitly deferring it with the user's approval.

### 5. Write the assumption log

List every assumption the plan depends on. Mark each one:

- ✅ **Verified** — describe how it was verified (which source, which query, which test)
- ⚠️ **Unverified** — describe what would verify it
- ❓ **Unknown** — describe what question would answer it

**Resolve or explicitly accept every ⚠️ and ❓ before building.** If the user approves building on an unverified assumption, note that in the log ("the user accepted this risk on YYYY-MM-DD").

### 6. Present the plan

Every choice in the plan must be justified by either:
- A cited source from Step 3 research, or
- An observation from Step 4 input inspection

If a choice cannot be justified by either, it is a guess. Guesses become questions for the user, not decisions.

The plan must include:
- **The one-sentence task** (from Step 1)
- **The domain** (from Step 2)
- **Research findings** with dated citations (from Step 3)
- **Failure modes we're designing for** (from Step 3.5)
- **Observed input shape** (from Step 4)
- **Assumption log** (from Step 5)
- **Proposed approach** with justification per choice
- **The "done" definition** (see next section)
- **What's explicitly out of scope**
- **Questions for the User** — anything that couldn't be resolved by research or observation

Wait for **explicit** approval. "Sounds good" counts. "Start" counts. Silence does not count.

## Step 7: Define "done" in observable terms

Before writing any code, write down the acceptance tests as plain-English observable statements.

These are not unit tests. They are statements a human can verify by looking at the running system, without reading code.

**Template:**
- "I can [action] and see [specific observable result]"
- "I can [edge case action] and [system behaves this way]"
- "I can [failure scenario] and [system degrades gracefully this way]"

**Example for a city-search feature:**
- I can search "Denver" and see 15+ real businesses with distinct names, addresses, photos, and ratings
- I can search a misspelled city ("denvr") and still get Denver results
- I can search three cities in a row and never see data from a previous city
- I can type "d", "de", "den" rapidly and only the final query fires an API call
- I can refresh the page mid-search and not get a broken state
- I can search a city the system has never seen and it populates fresh data within 10 seconds
- I can search a city the system has seen before and it returns cached results in under 500ms
- I can search during a provider outage and see a graceful error, not a blank screen

**"Done" is non-negotiable.** Every item on the list must pass before the work is reported complete. A screenshot is not verification. A passing build is not verification. A 200 response is not verification. Verification is: **every observable acceptance test from Step 7 passes, in the target environment, with a cold cache, under the failure modes from Step 3.5.**

This hooks directly into the `qa-protocol` skill — that skill runs at the end to enforce the same rule.

## Execution Discipline

Once the plan and acceptance tests are approved, launch the autonomous infrastructure BEFORE any build work begins:

```bash
python3 scripts/goalteam_orchestrator.py "<objective>"
```
This starts the swarm heartbeat, touches the pulse, writes the session descriptor, and dispatches the 14-step pipeline. You never start swarm scripts manually.

Then: 

1. **Work one milestone at a time.** Do not chain milestones silently.
2. **At each milestone, stop and verify output.** Not a build check. Actually run the observable test for that milestone and confirm it passes.
3. **If reality contradicts the plan mid-execution, STOP.** Do not patch. Do not add a fallback. Do not add a retry.
   - Return to the prep steps.
   - Figure out which assumption was wrong.
   - Revise the plan.
   - Get re-approval if the architecture changes.
4. **A patch to hide a symptom is a red flag.** If the agent catches itself adding "just a retry" or "just a fallback" or "just a band-aid", that is the signal to stop and diagnose the root cause.

## The Anti-Patterns This Skill Prevents

The agent will recognize these behaviors in itself and stop:

1. **Screenshot-as-verification.** Taking a screenshot and saying "working." Pixels rendering ≠ system working.
2. **Happy-path testing.** Testing one input that works and declaring the whole feature done.
3. **Ignoring own logs.** Seeing errors in logs and not acting on them.
4. **Patching symptoms, not causes.** Stacking retries, fallbacks, mirrors, and bounding-box tweaks on a bad initial choice.
5. **Declaring "all bugs found" from code review.** Without running the thing.
6. **Not defining done.** Jumping into build without acceptance criteria.
7. **Skipping the break-it pass.** Never trying edge cases (empty input, misspelling, rapid typing, refresh, back button, duplicate submit).
8. **Sunk-cost patching.** Refusing to delete bad work because "there's so much of it already."
9. **"That's how it's usually done."** Reaching for the default pattern instead of verifying it fits this situation.
10. **Silent milestone chaining.** Building phases 1 through 8 without verifying phase 1 actually works.

## Self-Check Before Presenting a Plan

Before showing the plan to the user, the agent runs this checklist. If any answer is "no" or "not really," go back.

1. Did I spawn a research agent and read its **full report**?
2. Did I open the actual input files / API responses / database rows with my own tools in this session?
3. Can every choice in the plan be traced to a **citation** (from Step 3) or an **observation** (from Step 4)?
4. Did I name at least 8 failure modes for this domain?
5. Have I resolved every ⚠️ and ❓ in the assumption log, or explicitly flagged them for the user?
6. Did I write the "done" definition as observable acceptance tests?
7. Is there anything in this plan I'm including because "that's how it's usually done"? If yes, go back to Step 3.
8. Am I about to delete real work-in-progress because I realized the foundation is wrong? **Good.** That's the invariant working. Do it.

## The Invariant

> If the agent ever catches itself writing code, creating files, or making architectural decisions before completing Steps 1 through 7: **stop, delete the work-in-progress, and start the SOP over.**
>
> The cost of restarting is always less than the cost of finishing on bad prep.

This invariant is the most important sentence in this skill. Everything else is support for it. Without the invariant, agents do the prep steps and then ignore them when they're inconvenient. With the invariant, the agent has a hard stop when reality diverges from the plan.

## When NOT to use this skill

This SOP is for **building**. It is **not** for:

- Answering questions about existing code
- Reading or exploring a codebase
- Making trivial edits (typos, copy changes, renaming a variable)
- Debugging an existing feature where the plan was already approved
- Responding to urgent one-off requests that the user explicitly marks as "just a quick fix"

If the task is genuinely trivial, the agent can skip this SOP. But "trivial" means "one file, one concept, no new dependencies, no new data sources, no new architecture decisions." Anything larger triggers the SOP.

When in doubt, run the SOP. The cost of running it on a task that didn't need it is a few minutes of thinking. The cost of skipping it on a task that did need it is days of patching.

## Relationship to other skills

- **`plan-for-goal` & `goal`** — MUST be used for stateful execution of long-running tasks. Before execution begins, invoke `/plan-for-goal` to structure the approach, then use `/goal` to provide resilience and persistence across context compactions.
- **`qa-protocol`** — runs at the END of work to enforce "don't claim done without verification." This skill (`pre-build-sop`) runs at the BEGINNING of work to enforce "don't start without preparation." They are complementary. Both should fire on most build tasks.
- **`autonomy-first`** — governs "execute directly instead of producing instructions." This skill is compatible — the agent still executes autonomously, it just prepares properly first.
- **`plan-to-tasks`** — converts an approved plan into structured tasks. This skill produces the plan; `plan-to-tasks` operates on the output.
- **`visual-architecture-mapping`** — for large system builds, can run after Step 6 to diagram the approved architecture before execution.
- **`swarm_heartbeat.sh`** — `scripts/swarm_heartbeat.sh`. When the plan involves long-running sub-agents, include heartbeat monitoring in the execution phase. Run `bash swarm_heartbeat.sh` to pgrep nemotron/deepseek and report vitals to WatchTower every 60s.

## Output format for the plan

When presenting the plan to the user, use this structure:

```
## Task (one sentence)
[From Step 1]

## Domain
[From Step 2]

## Research Summary
[3-6 bullets with dated citations from Step 3. Include the research agent's concrete recommendation.]

## Failure Modes We're Designing For
[The 8+ failure modes from Step 3.5, with how the plan handles each]

## Real Inputs Observed
[What we actually saw when we inspected inputs in Step 4. Include 1-2 sample records or responses.]

## Assumption Log
✅ [Verified assumptions with how]
⚠️ [Unverified with what would verify]
❓ [Unknown with what would answer]

## Approach
[The proposed architecture / design. Every choice cited.]

## Done Definition (Acceptance Tests)
[Observable statements from Step 7]

## Out of Scope
[What we are NOT building]

## Questions for the User
[Things that could not be resolved by research or observation]
```

If the user approves, execution begins. If the user asks questions, the plan is revised and re-presented. If the user rejects, back to Step 1.
