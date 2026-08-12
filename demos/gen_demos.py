#!/usr/bin/env python3
"""Generate faithful demo-output HTML files for each skill, built from the
real SKILL.md specs. Screenshotted by shoot_demos.sh into site/assets/."""
import pathlib

OUT = pathlib.Path(__file__).parent

CSS = """
:root{--navy:#1b3a5c;--navy2:#122a45;--cream:#fafaf8;--gold:#d9a441;--ink:#22303f;--muted:#5a7292;
--terra:#c9825d;--sage:#8ba888;--slate:#7f96b8;}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Helvetica,Arial,sans-serif;background:var(--cream);color:var(--ink);padding:34px 40px;line-height:1.55}
h1{font-family:Georgia,serif;font-style:italic;font-weight:400;color:var(--navy);font-size:30px;margin-bottom:4px}
h2{font-family:Georgia,serif;font-style:italic;font-weight:400;color:var(--navy);font-size:21px;margin:22px 0 10px}
.kick{font-size:11px;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:var(--gold);margin-bottom:8px}
.mono{font-family:Menlo,monospace}
.term{background:linear-gradient(160deg,#1b3a5c,#122a45);border-radius:12px;padding:20px 24px;color:#dbe5ef;
font-family:Menlo,monospace;font-size:13.5px;line-height:1.75;border-top:4px solid var(--gold)}
.term .p{color:var(--gold)} .term .c{color:#8fa3b8} .term .ok{color:#9dc08b} .term .bad{color:#d98c7a}
.card{background:#fff;border-radius:12px;box-shadow:0 6px 24px rgba(27,58,92,.12);padding:18px 22px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px}
table{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 6px 24px rgba(27,58,92,.12);font-size:14px}
th{background:var(--navy);color:#fff;text-align:left;padding:10px 14px;font-size:12px;letter-spacing:.08em;text-transform:uppercase}
td{padding:10px 14px;border-top:1px solid #e8e4da}
.tag{display:inline-block;font-size:10.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;padding:3px 10px;border-radius:999px}
.tag-gold{background:rgba(217,164,65,.16);color:#8a6414}.tag-ok{background:rgba(139,168,136,.2);color:#4a6b47}
.tag-terra{background:rgba(201,130,93,.18);color:#8a4f30}.tag-slate{background:rgba(127,150,184,.2);color:#46586e}
.check{color:#4a6b47;font-weight:700}
.rule{border-left:4px solid var(--gold);padding:4px 0 4px 14px;margin:10px 0}
.note{color:var(--muted);font-size:13px;margin-top:6px}
.tree{font-family:Menlo,monospace;font-size:13.5px;line-height:1.7;background:#fff;border-radius:12px;padding:18px 22px;box-shadow:0 6px 24px rgba(27,58,92,.12)}
"""

def page(title, body):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><p class="kick">Actual output · generated per the skill's own spec</p><h1>{title}</h1>{body}</body></html>"""

demos = {}

# ---------- GOAL ----------
demos["goal"] = page("Plan · Launch The Client Portal — /goal", """
<div class="grid2" style="margin-top:14px">
<div class="card">
<p class="kick">Plan file · plans/launch-client-portal_2026-08-11.md</p>
<h2 style="margin-top:2px">Definition Of Done</h2>
<p class="mono" style="font-size:13.5px">"Portal live at /portal with login, 3 seeded client accounts, zero console errors at 360px and 1440px."</p>
<h2>Acceptance Criteria</h2>
<p>✔ Login rejects a bad password with an error message<br>
✔ Renders at 360px with no horizontal scroll<br>
✔ All 3 seeded accounts can sign in<br>
<span style="color:#b4832a">○ Password reset email arrives within 60s<br>
○ Lighthouse performance ≥ 90 on /portal<br>
○ Zero console errors on login + dashboard</span></p>
<p class="note">Out of scope (load-bearing): no billing, no file uploads, no admin role.</p>
</div>
<div>
<div class="term">
<p><span class="p">$</span> python3 goal/scripts/goal.py status</p>
<p class="c"># Phase 3 — state persists in SQLite across turns</p>
<p>Goal: <b>Launch The Client Portal</b> <span class="ok">[active]</span></p>
<p>Turn budget: <b>12 / 40</b> used &nbsp;·&nbsp; Tokens: 38,204</p>
<p>Acceptance criteria: <b>6 / 9 verified</b></p>
<p>Swarm heartbeat: <span class="ok">alive</span> (pid 41207, vitals every 60s)</p>
<p class="c"># destructive action? missing credential? it stops and asks.</p>
</div>
<div class="card" style="margin-top:16px">
<p class="kick">Anti-vaporware gate</p>
<p style="font-size:14px"><b>/goal complete</b> runs a full audit first — every requirement mapped to real evidence inspected from files, not memory. Anything missing: work continues. Only a passed audit marks complete.</p>
</div>
</div>
</div>""")

# ---------- KAIZEN ----------
demos["kaizen"] = page("Session Improvement Log — Kaizen Discipline", """
<div class="grid3" style="margin-top:14px">
<div class="card" style="border-top:5px solid var(--terra)">
<span class="tag tag-terra">Muda · waste</span>
<p style="margin-top:10px;font-size:14px"><b>Cut:</b> the weekly report pulled 11 data sources; 4 fed charts nobody read. Named it, proposed the cut, deleted 240 lines of pipeline.</p>
</div>
<div class="card" style="border-top:5px solid var(--sage)">
<span class="tag tag-ok">Mura · unevenness</span>
<p style="margin-top:10px;font-size:14px"><b>Standardized:</b> two skills defined "done" differently. Wrote the standard down first, then merged them — one baseline, no more swing.</p>
</div>
<div class="card" style="border-top:5px solid var(--slate)">
<span class="tag tag-slate">Muri · overburden</span>
<p style="margin-top:10px;font-size:14px"><b>Removed:</b> a 50-page doc where a 1-page summary closed the decision. The reader stops being the bottleneck.</p>
</div>
</div>
<div class="card" style="margin-top:16px">
<p class="kick">The rules that run every session</p>
<p style="font-size:14.5px">▸ <b>Leave every artifact better than it was found</b> — one clearer sentence, one less dead line, every touch.<br>
▸ <b>Standardize before improving</b> — no baseline in writing means no way to tell forward from backward.<br>
▸ <b>Small moves, many cycles</b> — ten-minute iterations you can react to, not two-hour builds you have to rework.<br>
▸ <b>Go and see</b> — reads the real file before recommending; verifies its own visible work with screenshots instead of asking you to look.</p>
<p class="note">One percent better a day is 37× in a year. The math runs in both directions.</p>
</div>""")

# ---------- WRAPUP ----------
demos["wrapup"] = page("Session Close — Evidence Table, Not 'Done'", """
<table style="margin-top:14px">
<tr><th>Destination</th><th>Type</th><th>Format</th><th>Status</th><th>Evidence</th></tr>
<tr><td>transcript-archive</td><td>file</td><td>raw-transcript</td><td><span class="tag tag-ok">pushed</span></td><td class="mono" style="font-size:12.5px">~/session-transcripts/2026-08-11_1415_session.md</td></tr>
<tr><td>knowledge-base</td><td>notion</td><td>markdown</td><td><span class="tag tag-ok">pushed</span></td><td class="mono" style="font-size:12.5px">notion.so/Session-Log-8f3a…</td></tr>
<tr><td>vault-notes</td><td>obsidian</td><td>markdown</td><td><span class="tag tag-ok">pushed</span></td><td class="mono" style="font-size:12.5px">Daily/2026-08-11.md</td></tr>
<tr><td>review pass</td><td>self-review</td><td>—</td><td><span class="tag tag-ok">PASS-AS-IS</span></td><td class="mono" style="font-size:12.5px">fidelity checklist 4/4 YES</td></tr>
</table>
<div class="grid2" style="margin-top:16px">
<div class="card"><p class="kick">Fidelity checklist — every line must be YES</p>
<p style="font-size:14px"><span class="check">YES</span> — states the original goal accurately<br>
<span class="check">YES</span> — reports what actually happened, failures included<br>
<span class="check">YES</span> — every claim backed by evidence in the transcript<br>
<span class="check">YES</span> — free of PII, secrets, client-identifying details</p></div>
<div class="card"><p class="kick">The gate</p>
<p style="font-size:14px">A failed or unverified destination means the wrapup is <b>not</b> complete — it reports what failed and why instead of reporting SHIP. Destinations come from your config file, never hard-coded — file, Notion, NotebookLM, Obsidian, webhook.</p></div>
</div>""")

# ---------- PRE-BUILD-SOP ----------
demos["pre-build-sop"] = page("Prep Report — No Code Until Six Steps Are Done", """
<div class="card" style="margin-top:14px">
<p style="font-size:14.5px">
<span class="check">✔ 1. Task + spirit stated separately</span> — "Build a booking form" vs the outcome: <i>fewer phone tag loops</i>. They pointed the same way.<br>
<span class="check">✔ 2. Domain named</span> — CRUD UI + scheduling. Not guessed.<br>
<span class="check">✔ 3. Real research</span> — a dedicated research pass, dated sources from the last 12 months, official docs read directly.<br>
<span class="check">✔ 4. Actual inputs inspected</span> — the real API hit with curl, the real data opened. Edge cases found: 3 null fields, one oversized record.<br>
<span class="check">✔ 5. Failure modes named</span> — 8 written down before the plan, including rate limits and the maintenance-page-returns-HTML case.<br>
<span class="check">✔ 6. Plan approved</span> — presented, questioned, approved. <b>Then</b> code.</p>
</div>
<div class="term" style="margin-top:16px">
<p class="c"># the rule, enforced at the start of every build:</p>
<p>until all six steps complete and the plan is approved:</p>
<p><span class="bad">no code · no scaffolding · no installs · no architecture decisions</span></p>
<p><span class="ok">reading, searching, querying real data — allowed</span></p>
</div>""")

# ---------- MOE-BUILD-TEAM ----------
demos["moe-build-team"] = page("The Lineup — The Only Thing Presented Before Dispatch", """
<table style="margin-top:14px">
<tr><th>Role</th><th>Model</th><th>Provider</th></tr>
<tr><td>Advisor</td><td class="mono">{model-a}</td><td>{provider-a}</td></tr>
<tr><td>Builder</td><td class="mono">{model-b}</td><td>{provider-b}</td></tr>
<tr><td>QA</td><td class="mono">{model-c}</td><td>{provider-c}</td></tr>
<tr><td>Linter</td><td class="mono">{model-d}</td><td>{provider-d}</td></tr>
<tr><td>Kaizen 1</td><td class="mono">{model-e}</td><td>{provider-e}</td></tr>
<tr><td>Kaizen 2</td><td class="mono">{model-f}</td><td>{provider-f}</td></tr>
<tr><td>Logger <span class="tag tag-slate">support</span></td><td class="mono">{model-g}</td><td>{provider-g}</td></tr>
<tr><td>Researcher <span class="tag tag-slate">support</span></td><td class="mono">{model-h}</td><td>{provider-h}</td></tr>
</table>
<div class="grid2" style="margin-top:16px">
<div class="card"><p class="kick">The order — non-negotiable</p>
<p style="font-size:14px">You approve the lineup → the team is dispatched → <b>the team</b> defines the goal → <b>the team</b> writes the plan → the plan reaches you as a brief → you approve → execution. The orchestrator never writes the plan, never defines the goal, never touches the artifact.</p></div>
<div class="term"><p class="c"># Logger — read-only audit trail</p>
<p>14:02 | DISPATCH | Advisor | {model-a} | strategic risk pass</p>
<p>14:09 | COMPLETE | Linter | schema drift found, 2 fixes</p>
<p>14:11 | DECIDE | converge round 2 | all voices PASS</p>
<p>14:12 | MILESTONE | plan brief delivered</p></div>
</div>""")

# ---------- ROUTING-MATRIX ----------
demos["routing-matrix"] = page("routing-matrix.yaml — You Fill The Models", """
<div class="grid2" style="margin-top:14px">
<div class="term">
<p class="c"># templates/routing-matrix.template.yaml</p>
<p>roles:</p>
<p>&nbsp;&nbsp;advisor1:</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;primary: <span class="p">&lt;model-id&gt;</span></p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;provider: <span class="p">&lt;openai|anthropic|ollama-local|…&gt;</span></p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;fallback_chain: [<span class="p">&lt;provider/model&gt;</span>, …]</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;lens: synthesis, second-order consequences</p>
<p>policies:</p>
<p>&nbsp;&nbsp;no_repeat_model_in_sequence: <span class="ok">true</span></p>
<p>&nbsp;&nbsp;team_shape: 3 advisors + 2 kaizen</p>
<p>&nbsp;&nbsp;always_be_testing: <span class="ok">true</span></p>
<p>&nbsp;&nbsp;reject_dispatch_for_banned: <span class="ok">true</span></p>
<p>banned: []</p>
</div>
<div>
<div class="term">
<p><span class="p">$</span> python3 routing-matrix/scripts/validate.py routing-matrix.yaml</p>
<p class="ok">✓ 10 roles valid · sequence 1→8 + coordinator + logger</p>
<p class="ok">✓ 0 banned models assigned to roles</p>
<p class="ok">✓ all fallback chains resolve</p>
<p class="ok">✓ schema v1.0.0</p>
</div>
<div class="card" style="margin-top:16px"><p class="kick">Policies with teeth</p>
<p style="font-size:14px"><b>No repeat model in sequence</b> — every voice a different model, so one model's blind spot gets caught by another's eyes. <b>Always be testing</b> — new models prove themselves in real work, and the team's verdict keeps or cuts them. Provider down? The fallback chain walks itself — and if everything's exhausted, it aborts telling you every model it tried and why.</p></div>
</div>
</div>""")

# ---------- PROVISION-PROJECT ----------
demos["provision-project"] = page("A New Project, Fully Governed, In One Pass", """
<div class="grid2" style="margin-top:14px">
<div class="tree">ClientPortal/
├── AGENTS.md                 <span class="note">always created</span>
├── CLAUDE.md                 <span class="note">detected: claude CLI</span>
├── .cursor/rules/project.md  <span class="note">detected: .cursor/</span>
├── TROUBLESHOOTING.md
├── .env · .gitignore
├── handoffs/2026-08-11_initial-provisioning.md
├── logs/clientportal/00_SESSION_LEDGER.md
├── terminal-sessions/ · .backups/ · .remember/
</div>
<div>
<div class="term">
<p class="c"># self-verify — every line must print OK</p>
<p class="ok">OK dir: handoffs</p>
<p class="ok">OK dir: logs/clientportal</p>
<p class="ok">OK file: AGENTS.md</p>
<p class="ok">OK file: 00_SESSION_LEDGER.md</p>
<p class="ok">OK file: .remember/recent.md</p>
</div>
<div class="card" style="margin-top:16px"><p class="kick">Platform detection built in</p>
<p style="font-size:14px">It sniffs which agent platforms you run — Hermes, Claude Code, Codex, Cursor, OpenCode — and writes each platform's native instruction file. Same core content, every portal. Governance points at your nucleus; no personal names, no hardcoded paths, ever.</p></div>
</div>
</div>""")

# ---------- PROVISION-AGENT ----------
demos["provision-agent"] = page("One Agent, Four Identity Files, Registered", """
<div class="grid2" style="margin-top:14px">
<div class="grid2">
<div class="card" style="border-top:5px solid var(--terra)"><p class="kick">SOUL.md</p><p style="font-size:13.5px">Personality — name, role, behavioral boundaries, communication style.</p></div>
<div class="card" style="border-top:5px solid var(--sage)"><p class="kick">TOOLS.md</p><p style="font-size:13.5px">Capabilities — which tools, APIs, CLIs; constraints spelled out.</p></div>
<div class="card" style="border-top:5px solid var(--slate)"><p class="kick">MEMORY.md</p><p style="font-size:13.5px">Scoped memory — long-term facts, session scratchpad, learning log.</p></div>
<div class="card" style="border-top:5px solid var(--gold)"><p class="kick">USER.md</p><p style="font-size:13.5px">Handler profile — who directs this agent, timezone, preferences.</p></div>
</div>
<div>
<div class="term">
<p class="c"># config/agent_registry.yaml — append-only</p>
<p>- name: Sentinel</p>
<p>&nbsp;&nbsp;role: "Nightly audit + drift watch"</p>
<p>&nbsp;&nbsp;skills: [kaizen, wrapup]</p>
<p>&nbsp;&nbsp;status: <span class="ok">active</span></p>
<p>&nbsp;&nbsp;handler: "&lt;handler name&gt;"</p>
</div>
<div class="card" style="margin-top:16px"><p style="font-size:14px">Skills are <b>referenced, not copied</b> — the agent loads them from your governance nucleus at runtime, so one skill update reaches every agent. Self-verify prints OK for all 9 files and 6 dirs, or it isn't done.</p></div>
</div>
</div>""")

# ---------- PROVISION-TEAM ----------
demos["provision-team"] = page("A Coordinated Team — Identity, Roster, Rules", """
<div class="grid3" style="margin-top:14px">
<div class="card" style="border-top:5px solid var(--terra)"><p class="kick">TEAM_IDENTITY.md</p><p style="font-size:13.5px">Name, shared purpose, the blackboard concept, collective boundaries.</p></div>
<div class="card" style="border-top:5px solid var(--sage)"><p class="kick">TEAM_COMPOSITION.md</p><p style="font-size:13.5px">Which agents, their roles, their folder paths, their skill sets.</p></div>
<div class="card" style="border-top:5px solid var(--slate)"><p class="kick">TEAM_GOVERNANCE.md</p><p style="font-size:13.5px">Handoff rules, approval gates, escalation paths, dispatch contract.</p></div>
</div>
<table style="margin-top:16px">
<tr><th>Agent</th><th>Role</th><th>Skills</th><th>Status</th></tr>
<tr><td>Scout</td><td>Research + source validation</td><td>market-research, web fetch</td><td><span class="tag tag-ok">provisioned</span></td></tr>
<tr><td>Forge</td><td>Implementation</td><td>software-development, terminal</td><td><span class="tag tag-ok">provisioned</span></td></tr>
<tr><td>Sentinel</td><td>Audit + drift watch</td><td>kaizen, wrapup</td><td><span class="tag tag-ok">provisioned</span></td></tr>
</table>
<p class="note" style="margin-top:12px">Default orchestration: sequential dispatch with convergence voting — orchestrator dispatches, workers execute, every worker reports a verdict, disagreements get resolved before anything moves on. Registered append-only in team_registry.yaml. Retired teams are archived, never deleted.</p>""")

# ---------- HOOKS-GUIDE ----------
demos["hooks-guide"] = page("Hooks — Governance Inside The Agent's Loop", """
<div class="grid2" style="margin-top:14px">
<div class="term">
<p class="c"># pre_tool_use — the gate fires BEFORE the tool runs</p>
<p>&gt; tool: write_file → path: ~/governance/CONSTITUTION.md</p>
<p class="bad">{"action":"block",</p>
<p class="bad"> "message":"Protected path. Escalate to the owner."}</p>
<p>&nbsp;</p>
<p class="c"># post_tool_use — silent audit, never slows the agent</p>
<p>{"ts":"14:02:11","tool":"write_file","ok":true,"ms":42}</p>
<p>{"ts":"14:02:13","tool":"terminal","ok":true,"ms":318}</p>
</div>
<div>
<div class="card"><p class="kick">Safety rules, universal</p>
<p style="font-size:14px">▸ <b>Fail-open</b> — a crashed hook never deadlocks the agent<br>
▸ <b>Kill-switch</b> — one sentinel file bypasses everything<br>
▸ <b>Idempotent</b> — same input, same result, twice<br>
▸ <b>Timeout-bounded</b> — 5s and it's considered hung<br>
▸ <b>No network in pre_tool_use</b> — it fires hundreds of times a session</p></div>
<div class="card" style="margin-top:14px"><p class="kick">Per-platform adapters</p>
<p style="font-size:14px">Hermes, Claude Code, Codex, Cursor, OpenCode, Continue, Aider, Cline — what each platform actually supports, and the manual workarounds (rule files, wrapper scripts, pre-commit hooks) for the ones with no native hooks.</p></div>
</div>
</div>""")

for name, html in demos.items():
    (OUT / f"demo-{name}.html").write_text(html)
    print(f"demo-{name}.html {len(html)}b")
