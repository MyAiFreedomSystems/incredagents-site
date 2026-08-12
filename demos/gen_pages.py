#!/usr/bin/env python3
"""Generate the 14 per-skill mini pages from content mined out of the real
SKILL.md files. Reuses site/styles.css classes (skill-hero, truth-grid,
terminal, voice-grid, cta-band, footer)."""
import pathlib

SITE = pathlib.Path(__file__).parent.parent / "site"
ORG = "https://github.com/MyAiFreedomSystems"
PACK = f"{ORG}/incredagents"

def T(words):
    """word spans with stagger; tuple item marks script accent"""
    out = []
    i = 0
    for w in words:
        if isinstance(w, tuple):
            out.append(f'<span class="w script-accent" style="--i:{i}">{" ".join(x for x in w if x)}</span>')
        else:
            out.append(f'<span class="w" style="--i:{i}">{w}</span>')
        i += 1
    return " ".join(out)

def section(eyebrow, h2, lead, inner):
    return f"""
<section class="section-light">
  <p class="eyebrow">{eyebrow}</p>
  <h2>{h2}</h2>
  <p class="section-lead">{lead}</p>
  {inner}
</section>"""

def truth(cards):
    items = "".join(
        f'<article class="truth-card reveal"{f" style=\"--d:{d}s\"" if d else ""}><h3>{h}</h3><p>{p}</p></article>'
        for (h, p, d) in cards)
    return f'<div class="truth-grid">{items}</div>'

def term(title, lines, foot=None):
    body = "".join(f"<p>{l}</p>" for l in lines)
    f = f'<p class="term-foot">{foot}</p>' if foot else ""
    return f"""
  <div class="terminal reveal">
    <div class="term-bar">
      <span class="term-dot td-gold"></span><span class="term-dot"></span><span class="term-dot"></span>
      <span class="term-title">{title}</span>
    </div>
    <div class="term-body">{body}</div>
    {f}
  </div>"""

PROMPT = '<span class="prompt">$</span>'
C = lambda s: f'<span class="term-comment"># {s}</span>'

PACK_INSTALL = term("your machine — three commands", [
    f"{PROMPT} git clone https://github.com/MyAiFreedomSystems/incredagents.git",
    f"{PROMPT} cd incredagents",
    f"{PROMPT} python3 onboard.py",
], "One installer wires in the whole mod pack and asks only for the keys each skill needs.")

def standalone_install(repo):
    return term("your machine — one command", [
        f"{PROMPT} git clone https://github.com/MyAiFreedomSystems/{repo}.git",
        C("drop the folder in your agent's skills directory. done."),
    ])

LOGO_ALIAS = {"harvest-testimonials":"skill-harvest.svg","graphic-testimonials":"skill-graphic.svg",
 "testimonial-display":"skill-display.svg","logo-theme-manager":"skill-theme.svg"}

def page(p):
    p["logo"] = LOGO_ALIAS.get(p["slug"], f"skill-{p['slug']}.svg")
    sections = "".join(section(*s) for s in p["sections"])
    install = p.get("install", "")
    install_sec = section("Get started", p["install_h2"], p["install_lead"], install) if install else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{p['name']} · IncredAgents Skills</title>
<meta name="description" content="{p['meta']}">
<link rel="icon" type="image/png" href="../assets/incredagents-logo.png">
<link rel="stylesheet" href="../styles.css">
</head>
<body>

<nav>
  <a class="nav-brand" href="../index.html"><img class="brand-logo" src="../assets/incredagents-logo.png" alt="IncredAgents logo">IncredAgents</a>
  <div class="nav-links">
    <a href="../index.html#skills">All Skills</a>
    <a class="nav-cta" href="{p['github']}">GitHub</a>
  </div>
</nav>

<header class="skill-hero">
  <img class="skill-badge reveal" src="../assets/{p['logo']}" alt="{p['name']} logo">
  <p class="eyebrow eyebrow-gold reveal">{p['kicker']}</p>
  <h1 class="skill-title">{p['title']}</h1>
  <p class="skill-sub reveal" style="--d:.4s">{p['sub']}</p>
  <figure class="skill-art reveal" style="--d:.25s">
    <img src="../assets/{p['art']}" alt="{p['art_alt']}">
  </figure>
  <div class="hero-actions reveal" style="--d:.5s">
    <a class="btn btn-pulse" href="{p['github']}">Get It On GitHub →</a>
    <a class="btn ghost" href="../index.html#skills">Back To All Skills</a>
  </div>
</header>
{sections}
{install_sec}
<div class="cta-band">
  <h2>{p['cta_h2']}</h2>
  <p>{p['cta_p']}</p>
  <a class="btn" href="{p['github']}">Get {p['name']} On GitHub →</a>
</div>

<footer>
  <img class="foot-brand-logo" src="../assets/incredagents-logo.png" alt="IncredAgents logo">
  <span class="foot-brand">IncredAgents</span>
  <p>Built by <a href="https://github.com/MyAiFreedomSystems">My AI Freedom Systems</a></p>
  <p class="foot-eco"><a href="https://freedomaios.com"><img class="foot-logo foot-logo-v2" src="../assets/freedomaios-logo.png" alt="FreedomAIOS logo — Take the road less traveled">Part of the FreedomAIOS ecosystem</a></p>
  <p style="margin-top:8px;">Every skill is scrubbed of personal data before it ships. Every word attributed to a person is their real words, from a real source.</p>
  <p class="site-version">Site v15</p>
</footer>

<script>
const io = new IntersectionObserver((entries) => {{
  entries.forEach((e) => {{
    if (e.isIntersecting) {{ e.target.classList.add("in"); io.unobserve(e.target); }}
  }});
}}, {{ threshold: 0.15 }});
document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
</script>

</body>
</html>
"""

PAGES = []

# ================= STANDALONE SKILLS =================

PAGES.append({
 "slug":"harvest-testimonials","name":"Harvest-Testimonials",
 "github":f"{ORG}/harvest-testimonials","kicker":"Standalone Skill",
 "title":T(["The","praise","is","already","out","there.",("Go",),"get","it."]),
 "sub":"Your clients are saying nice things on YouTube, Facebook, LinkedIn, Skool, and your own blog — right now. This skill finds every word, with names, photos, and source links, and pulls it in. Nothing invented. Nothing shipped on a hunch.",
 "meta":"Find the testimonials you have already earned across YouTube, blogs, and social communities — exact words, real names, source links.",
 "art":"matt-davis-testimonial.jpeg",
 "art_alt":"A real client Facebook post this skill surfaced — exact words, real name, real source",
 "sections":[
  ("Where it hunts","Your proof is scattered. It isn't anymore.",
   "YouTube channels, blog testimonial sections, and the login-gated communities where clients actually talk — each source gets the tool that can actually reach it.",
   truth([
    ("YouTube, Minus The Grind.","Every video listed, auto-captions pulled and cleaned, names and roles read from the titles where spelling is reliable. Face frames extracted at three timestamps per video, so you pick the shot with eye contact.",0),
    ("The Open Web.","Blog and site testimonial sections get fetched and read — with a hard warning baked in: theme filler exists, and every person gets verified as a real client before anything moves forward.",0.1),
    ("Behind The Login.","Skool, Facebook, LinkedIn, Instagram — reached through your own logged-in browser session. It never touches your credentials, respects rate limits, and a captcha means stop and tell you, not push through.",0.2),
   ])),
  ("The gate","Nothing Reaches Design Unqualified.",
   "Every candidate — from every source — runs a gauntlet before a pixel gets designed.",
   truth([
    ("A Script Catches The Mechanical Failures.","Missing source link, anonymous author, placeholder patterns, duplicates, quotes too short or too long — rejected by code, not by vibe.",0),
    ("A Rubric Catches The Judgment Failures.","Survivors get scored 0–100 on specificity, verifiability, and whether this person could actually be your client. 70+ ships. 40–69 goes to you with reasons attached. Under 40 is gone.",0.1),
    ("No Screenshot, No Permalink, No Chance.","Every social capture requires proof of provenance — a screenshot of the comment and its author, plus the source link. This rule exists because a fake once shipped. It will not happen twice.",0.2),
   ])),
  ("First thing it does","Dedupe. Before Anything Else.",
   "It lists the testimonials you already have and skips those people. You will never get served the same praise twice.",
   term("the first pass — before any fetching",[
     f"{PROMPT} list existing cards + site alt texts → skip those people",
     C("users hate duplicate proof. so it never happens."),
     f"{PROMPT} <span class='block-cursor'></span>",
   ])),
 ],
 "install":standalone_install("harvest-testimonials"),
 "install_h2":"Two Minutes To Your First Harvest.",
 "install_lead":"Clone it, tell your agent where your clients talk, and watch qualified proof pile up.",
 "cta_h2":"The kind words exist. Go collect them.",
 "cta_p":"Every day they sit unharvested is a day your sales page argues alone.",
})

PAGES.append({
 "slug":"graphic-testimonials","name":"Graphic-Testimonials",
 "github":f"{ORG}/graphic-testimonials","kicker":"Standalone Skill",
 "title":T(["Their","words.","Your","brand.",("Minutes.","","","")]),
 "sub":"Feed it a quote, a name, a role, and a photo. Get back a branded 1080×1080 card — recolored to your exact palette, circular portrait, ready to post — wired into your page. Canva if you have it. Its own template if you don't.",
 "meta":"Turn harvested testimonials into branded card images — Canva or standalone HTML template, recolored to your brand, with circular client photos.",
 "art":"card-matthew-davis.png",
 "art_alt":"A real branded testimonial card produced by this skill — real condensed words, real client, navy and gold brand",
 "sections":[
  ("Two ways in","Canva If You Have It. Its Own Template If You Don't.",
   "No Canva account? Nothing stops. The bundled HTML template renders the same card through headless Chrome — stars, quote, script name, circular photo — driven by your brand config.",
   truth([
    ("Your Canva Template, Respected.","It duplicates your template and edits the copy — it never touches your original. Transactions, not guesswork: element IDs come from the API response, and unusable cards get renamed, never deleted.",0),
    ("Recolored To Your Exact Brand.","A post-process script corner-samples the background and blends to your hex while preserving the anti-aliasing — no jagged edges, no close-enough blue.",0.1),
    ("Faces Baked In, Circles Done Right.","Client photos composited as clean circles with your ring color. Fair warning: re-exporting from Canva loses the face — the skill tells you so, and re-runs the step.",0.2),
   ])),
  ("The hard rules","Real Clients. Versioned Files. No Exceptions.",
   "Every name and quote traces back to a source — this skill sits downstream of a qualification gate, and it acts like it.",
   truth([
    ("Nothing Ships Unsourced.","Real, verifiable clients only. If a name can't be traced, it doesn't become a card.",0),
    ("Never Overwrite Your Originals.","Files are versioned. Your Canva template is duplicated, never edited. What you had before the skill ran, you still have.",0.1),
    ("Ranked By What You're Selling.","Cards get wired into your page with the stories that match the offer first — overflow goes under its own subheading, not deleted.",0.2),
   ])),
 ],
 "install":standalone_install("graphic-testimonials"),
 "install_h2":"From Quote To Card Tonight.",
 "install_lead":"Clone it, hand it harvested material, and get back cards worth posting.",
 "cta_h2":"Your next card is one command away.",
 "cta_p":"Pair it with Harvest-Testimonials and the whole pipeline runs itself.",
})

PAGES.append({
 "slug":"testimonial-display","name":"Testimonial-Display",
 "github":f"{ORG}/testimonial-display","kicker":"Standalone Skill",
 "title":T(["Proof","belongs","where","the",("objection","","",""),"lives."]),
 "sub":"You have the testimonials. This skill answers the only question that matters: where on the page does each one go so it builds trust instead of becoming decoration nobody reads?",
 "meta":"Place testimonials where they build trust and lift conversion — pattern library, relevance matching, and hard trust rules.",
 "art":"demo-testimonial-display.png",
 "art_alt":"The skill's real demo file — interleaved singles and a wall-of-love grid with fictional filler clearly marked",
 "sections":[
  ("The core method","Relevance Matching. Never Random Placement.",
   "Every testimonial gets tagged by the objection it answers — then placed at the exact section of your page arguing that same point.",
   truth([
    ("Tag The Objection.","Each quote answers something — 'was skeptical it'd work for a small shop,' 'setup took one afternoon.' The skill reads each one and names what it kills.",0),
    ("Map The Page.","Your setup section argues 'this won't be hard.' Your pricing section raises 'is it worth it?' Every section is making an argument — whether you placed proof there or not.",0.1),
    ("Match Quote To Argument.","The setup testimonial goes in the setup section. The ROI quote sits beside pricing. Leftovers go to the wall near the close — never forced where they don't belong.",0.2),
   ])),
  ("Ten patterns, one guide","The Right Pattern For Your Page Type.",
   "Long-form sales letter, SaaS homepage, e-commerce product page, agency site, landing page — each gets its own placement recipe from the pattern library.",
   truth([
    ("Sales Pages.","Featured single near the top, singles interleaved at relevance points, wall of love near the close to catch 'does this work for people like me?'",0),
    ("Product + Agency Pages.","Star-rating snippets beside every CTA. Photo and video proof in the description zone. No sliders above the fold — ever.",0.1),
    ("A Working Demo Ships In The Repo.","Three core patterns rendered as a self-contained HTML file — with fictional filler visibly marked as fictional, because placeholder quotes never ship to production.",0.2),
   ])),
  ("Non-negotiables","Trust Rules With Teeth.",
   "Real names, real photos, real sources — and the slider rules most sites get wrong.",
   truth([
    ("Real Only, Linked Where Public.","No invented quotes, no merged people, no stripped context. Condensed quotes get marked as edited. Verifiability is what makes proof credible.",0),
    ("No Auto-Play Traps.","Sliders get visible pause controls, keyboard operation, reduced-motion respect, and a no-JS fallback. WCAG isn't a suggestion here.",0.1),
    ("Fast Or It Doesn't Count.","Lazy-loaded images, explicit dimensions so walls don't shift the layout, and plain CSS grid over heavyweight masonry libraries.",0.2),
   ])),
 ],
 "install":standalone_install("testimonial-display"),
 "install_h2":"Place Your Proof Like It Matters.",
 "install_lead":"Clone it, hand it your page and your quotes, and get a placement plan with the rules enforced.",
 "cta_h2":"Stop decorating. Start converting.",
 "cta_p":"The quotes you already have are worth more in the right position.",
})

PAGES.append({
 "slug":"logo-theme-manager","name":"Logo-Theme-Manager",
 "github":f"{ORG}/logo-theme-manager","kicker":"Standalone Skill",
 "title":T(["One","file","rules","your","whole",("brand.","","","")]),
 "sub":"AI site builders scatter hex codes across pages and paste logos into random folders. Then the brand changes and updating the site becomes a scavenger hunt. This skill ends that — one token file, one manifest, one command to replace everything.",
 "meta":"Build a true token-based theme system and a sha256-tracked logo manifest — replace every logo and favicon across every project in one command.",
 "art":"demo-logo-theme-manager.png",
 "art_alt":"The skill's integrity check output — OK, DRIFTED, and MISSING per file — plus the one-command replace",
 "sections":[
  ("The problem it kills","The Rebrand Scavenger Hunt Is Over.",
   "Some files get replaced, some don't, and nobody notices the missed ones until a customer does. This skill makes that failure structurally impossible.",
   truth([
    ("One Token File.","Every color, font, radius, and the logo itself live in a single theme.css as CSS variables. Pages consume tokens — inline hex codes are treated as bugs and hunted down with grep.",0),
    ("A Manifest With Fingerprints.","Every copy of your logo and favicon set — across the project and its clones — crawled, cataloged, and sha256-fingerprinted. The crawler finds files you forgot existed.",0.1),
    ("Check Proves It. Replace Fixes It.","--check prints OK, MISSING, or DRIFTED per file and fails the build if anything's wrong. --replace regenerates the whole set — transparent master, four PNG sizes, multi-size favicon — and writes it over every location in one command.",0.2),
   ])),
  ("Details that matter","Built For The Real World.",
   "Dry-run by default. Explicit background keying when your logo isn't on white. Git commits if you ask — never pushes. And honest fallbacks when the environment is constrained.",
   truth([
    ("Nothing Writes Without A Preview.","--dry-run shows exactly what a replace would touch before it touches anything.",0),
    ("The Full Identity Set.","favicon.ico, 32px, apple-touch-180, 192, 512 — generated, not hand-cropped — plus Organization JSON-LD so search engines get the canonical logo.",0.1),
    ("No Pillow? It Tells You The Path.","Constrained agents get the manual route spelled out — and the skill never claims a replace it couldn't execute.",0.2),
   ])),
 ],
 "install":standalone_install("logo-theme-manager"),
 "install_h2":"Your Next Rebrand Takes One Command.",
 "install_lead":"Clone it, crawl your project once, and never hunt a stray hex code again.",
 "cta_h2":"Make your brand change-proof.",
 "cta_p":"The next logo swap is either one command or a scavenger hunt. Pick.",
})

# ================= MOD PACK SKILLS =================

def pack_page(slug, **kw):
    kw.setdefault("github", f"{PACK}/tree/main/{slug}")
    kw.setdefault("kicker", "Inside The IncredAgents Mod Pack")
    kw.setdefault("install", PACK_INSTALL)
    return {"slug": slug, **kw}

PAGES.append(pack_page(
 "goal", name="Goal",
 title=T(["Vague","goals","die.",("This",),"one","has","a","budget."]),
 sub="Type /goal and your objective gets forced through a real plan — definition of done with no vibe words, acceptance criteria you can check, a hard turn budget — before a single action runs. State persists in SQLite. Completion requires an evidence audit.",
 meta="Structured goal execution for agents: forced planning, SQLite-persisted state, turn budgets, and an anti-vaporware completion audit.",
 art="demo-goal.png",
 art_alt="A real /goal plan file with definition of done, acceptance criteria checklist, and live status with turn budget",
 sections=[
  ("The two-phase law","Planned Before Executed. Every Time.",
   "Skipping the plan is how agents burn 500 turns on an unbounded task with a vibe-word definition of done. This skill makes that impossible.",
   truth([
    ("No Vibe Words Allowed.","'Clean,' 'polished,' 'feels nice' — banned from the definition of done. If a small evaluator can't judge it from the transcript, it doesn't count.",0),
    ("Out Of Scope Is Load-Bearing.","At least two explicit non-goals, written down. Scope creep dies in the plan file, not in your budget.",0.1),
    ("A Hard Turn Budget.","Light tasks: 15–25 turns. Heavy: 60–100. Cap at 100. Hit the budget and it pauses and reports — it never quietly burns on.",0.2),
   ])),
  ("While it runs","State That Survives. Oversight That Doesn't Sleep.",
   "Goal state persists in SQLite across turns and sessions. A heartbeat monitors the agent's vitals every 60 seconds. You get a notification the moment a goal launches.",
   truth([
    ("Pause, Resume, Clear, Complete.","/goal status shows elapsed time, tokens, and what's still unverified. Pause and resume across sessions — it re-reads the plan first.",0),
    ("It Stops And Asks.","Destructive action? Missing credential? It stops, names exactly what it needs, and waits. No silent improvisation with your stuff.",0.1),
    ("Archive, Never Delete.","Files, database rows, records — cleared goals get archived with why, not deleted. Your history stays auditable.",0.2),
   ])),
  ("The anti-vaporware gate","'Done' Requires Evidence.",
   "Before /goal complete, every requirement gets mapped to real, current evidence — files inspected, commands run, results read. Memory is not evidence. Anything missing means work continues, not a victory lap.",
   term("the completion audit — every step, or it isn't done",[
     f"{PROMPT} restate objective → map every requirement to evidence",
     f"{PROMPT} inspect real files, command output, test results",
     f"{PROMPT} python3 goal/scripts/goal.py complete",
     C("only after the audit passes. then the ledger gets the receipt."),
   ])),
 ],
 install_h2="Give Your Agent A Finish Line.",
 install_lead="Ships in the mod pack. One installer wires it in.",
 cta_h2="Stop hoping it finished. Know.",
 cta_p="Your next goal comes with a plan, a budget, and receipts.",
))

PAGES.append(pack_page(
 "kaizen", name="Kaizen",
 title=T(["One","percent","better.",("Every",),"session."]),
 sub="The forty-year-old Toyota discipline, wired into your agent's daily work: leave every artifact better than it was found, standardize before improving, name the waste out loud. Small, held every day, compounds — 1% a day is 37× in a year.",
 meta="Continuous improvement as an agent discipline — leave every artifact better, name muda/mura/muri, verify with its own eyes.",
 art="demo-kaizen.png",
 art_alt="A session improvement log naming the three wastes — muda, mura, muri — with the cuts made",
 sections=[
  ("The posture","Small Is Not Weak.",
   "Big swings collapse under their own weight. Kaizen is the opposite: improve the thing a little today, a little more tomorrow, and let the math compound.",
   truth([
    ("Leave It Better Than Found.","Every file your agent touches comes back one clearer sentence, one less dead line better. Scoped, never an unsolicited rewrite — but present.",0),
    ("Standardize Before Improving.","If the current way lives only in tribal memory, it gets written down first. No baseline means no way to tell a step forward from a regression.",0.1),
    ("Many Cycles Beat One Big Reveal.","Ten-minute iterations you can react to produce better work than two-hour builds you have to rework. The cycle is the unit of progress.",0.2),
   ])),
  ("The vocabulary","It Names The Three Wastes.",
   "Muda — effort producing no value. Mura — quality that swings session to session. Muri — overburden, including a fifty-page document where one page closes the decision. Named waste gets cut; unnamed waste repeats.",
   truth([
    ("Go And See.","Before recommending a change, it reads the actual file. Before claiming a tool can't do something, it verifies. No diagnosing from memory.",0),
    ("It Uses Its Own Eyes.","Ship a visible artifact and it screenshots the result itself — then reports what it saw. You confirm what it saw; you don't do the seeing.",0.1),
    ("Spirit Over Letter.","It honors the outcome you're reaching for, and proposes a better mechanism before executing — instead of building the letter of your request and missing the point.",0.2),
   ])),
 ],
 install_h2="Install The Discipline, Not The Hype.",
 install_lead="Ships in the mod pack. Load it at session start and the baseline starts rising.",
 cta_h2="Compounding beats swinging.",
 cta_p="Every session leaves your system one notch stronger — or it doesn't. This makes it the first one.",
))

PAGES.append(pack_page(
 "wrapup", name="Wrapup",
 title=T(["Sessions","end","with",("evidence.","","",""),"Not","'done.'"]),
 sub="Every session closes with a faithful record — what was delivered, what failed, what's still owed — pushed to the destinations you configured, with a returned link or path for each one. A failed destination blocks SHIP and says why.",
 meta="End-of-session close that produces a faithful, evidence-backed record and delivers it to your configured destinations.",
 art="demo-wrapup.png",
 art_alt="A wrapup evidence table — destination, type, format, pushed status, and the link proving each one",
 sections=[
  ("Fidelity first","The Failures Make It In.",
   "No smoothing over abandoned approaches or unresolved blockers. The summary reflects what actually happened — because a record you can't trust is worse than none.",
   truth([
    ("A Four-Line Checklist, All YES.","Accurate goal. What actually happened, failures included. Every claim backed by evidence in the transcript. No PII or secrets. One NO and the draft gets fixed before anything ships.",0),
    ("Evidence Over Claims.","Completion is proven with returned links, file paths, and API confirmations — never with the word 'done.' If a push couldn't be verified, the table says so.",0.1),
    ("The Transcript Gets Saved First.","Before any summarizing, the raw record is exported and verified non-empty — so the source of truth exists even if everything after fails.",0.2),
   ])),
  ("Your setup, not its assumptions","Destinations Come From Your Config.",
   "File archives, Notion, NotebookLM, Obsidian, webhooks — enabled means pushed, disabled means untouched. Nothing is hard-coded, nothing is assumed.",
   truth([
    ("Three Questions At Setup.","Where should transcripts go? Which services? What format per destination? Answered once, written to config, respected forever.",0),
    ("Zero-Config Fallback.","No config at all? Every session still lands in a dated markdown log — date, goal, accomplished, decisions, open threads, lessons learned.",0.1),
    ("It Audits Its Own Shortcuts.","Skipped verification, unverified completion claims, steps done out of order — found and recorded honestly, so patterns surface instead of repeating silently.",0.2),
   ])),
 ],
 install_h2="Close Every Session Like It Matters.",
 install_lead="Ships in the mod pack. The installer asks the three setup questions and wires it in.",
 cta_h2="Get receipts for your agent's work.",
 cta_p="The next session ends with a record you can verify — or it doesn't end.",
))

PAGES.append(pack_page(
 "graphics", name="Graphics",
 title=T(["One","skill.","Eight","styles.","You","pick","by",("looking.",)]),
 sub="Every visual asset — infographics, banners, diagrams, logos, mockups, posters — enters through one door. Eight curated styles shown as real examples you point at, an ask-first discipline before anything generates, and a pipeline with safety guarantees built in.",
 meta="One entry point for every visual asset — eight curated styles, an example-led picker, and a safe generation pipeline.",
 art="demo-graphics.png",
 art_alt="The skill's real example brief — eight styles rendered as actual generated examples you pick by looking",
 sections=[
  ("The picker","You Choose With Your Eyes, Not Adjectives.",
   "When /graphics fires, the first thing that opens is the example brief — every style rendered as a real generated image. You point at the one you want. No describing 'modern but playful' into the void.",
   truth([
    ("Eight Styles, A Through H.","Classic infographic, central metaphor, hub-and-spoke wheel, isometric pillars, course banner, whiteboard explainer, technical diagram, typography image. Each with its own recipe.",0),
    ("Every Ratio Previewed.","Square, landscape, wide, social cover — the same prompt shown across aspect ratios before you commit.",0.1),
    ("Ask-First, Always.","Describe the image without picking and it proposes a style — then asks. Nothing generates until you've seen the plan.",0.2),
   ])),
  ("The consolidation","Ten Old Skills. One Door.",
   "This skill replaced an entire drawer of one-off image skills — infographic, visual-assets, image-pipeline, diagram, banner, and more. Every prompt template, parameter, and safety guarantee moved inside, so there's exactly one place to get it right.",
   truth([
    ("One Canonical Prompt Per Style.","Each style carries its canonical recipe — see it, adapt it, know exactly what will be asked of the engine.",0),
    ("Credentials Checked Before Generating.","A pre-flight check runs at invocation — missing keys get named, and a direct-API fallback exists when the tool wrapper drops the ball.",0.1),
    ("No Substitute Artifacts.","Ask for an image, get an image. It never hands you an HTML mockup or a description and calls it done.",0.2),
   ])),
 ],
 install_h2="Every Visual, One Entry Point.",
 install_lead="Ships in the mod pack with all eight style recipes included.",
 cta_h2="Stop prompt-gambling. Pick by looking.",
 cta_p="The next asset starts with examples, not adjectives.",
))

PAGES.append(pack_page(
 "pre-build-sop", name="Pre-Build-SOP",
 title=T(["No","code","until","six","steps","are",("done.","","","")]),
 sub="Agents default to writing code immediately — pattern-matched from memory, never looking at real inputs, patching bugs forever. This skill replaces that reflex with a gate: six preparation steps, completed and approved, before a single line gets written.",
 meta="Forced preparation before any build — task and spirit, real research, real inputs, named failure modes, approved plan.",
 art="demo-pre-build-sop.png",
 art_alt="A prep report with all six steps checked and the no-code rule enforced",
 sections=[
  ("The gate","Reading Is Allowed. Building Is Not.",
   "Until all six steps complete and you approve the plan: no code, no scaffolding, no installs, no architecture decisions. Searching, querying APIs by hand, inspecting real data — allowed.",
   truth([
    ("Task And Spirit, Stated Separately.","What you're building — and the outcome you're actually reaching for — in two sentences. When they point different directions, the gap surfaces before it gets expensive.",0),
    ("Real Research, Dated Sources.","A dedicated research pass on current practitioner consensus — official docs read directly, known failure modes named, anything unverifiable flagged. Generalities get sent back.",0.1),
    ("Real Inputs, Actually Opened.","The real data file. The real API response. The actual page. Edge cases found in the data, not imagined — three null fields discovered beats thirty bugs patched.",0.2),
   ])),
  ("The discipline","Eight Ways It Will Break, Written Down First.",
   "Before the plan, the agent names at least eight failure modes it expects in production. Can't name eight? The research wasn't thorough enough — go back.",
   truth([
    ("Failure Modes Before Architecture.","Rate limits, maintenance pages returning HTML, oversized records — named while they're cheap.",0),
    ("The Plan Gets Approved, Then Executed.","Presented, questioned, approved. After approval: action, not re-confirmation.",0.1),
    ("Adjacent Work Gets Done, Not Deferred.","Surface a dependency bug during prep and it gets named in the plan and executed — not parked for a 'version two' that never comes.",0.2),
   ])),
 ],
 install_h2="Put The Gate Before The Build.",
 install_lead="Ships in the mod pack. It activates on any word that means building.",
 cta_h2="Cheap prep beats expensive patching.",
 cta_p="The next build starts with six steps — or with bugs.",
))

PAGES.append(pack_page(
 "moe-build-team", name="Moe-Build-Team",
 title=T(["The","team","builds.","The","orchestrator","just","holds",("the","door."),]),
 sub="A panel of specialist voices — each with a lens the orchestrator doesn't have — researches, plans, and converges before anything reaches you. The orchestrator routes work and holds the process. It never touches the artifact.",
 meta="Multi-model build team orchestration — lineup approval, team-defined goals, converged plans, and a read-only audit logger.",
 art="demo-moe-build-team.png",
 art_alt="A build team lineup table — role, model, provider — with the dispatch order and logger audit trail",
 sections=[
  ("The order","The Lineup Is The Only Thing You See First.",
   "No goal definition. No research findings. No status paragraphs. A compact table — role, model, provider — and your approval. Then the team works.",
   truth([
    ("The Team Defines The Goal.","Not the orchestrator. The team writes the plan too — the orchestrator that produces a plan has already failed, and the protocol says so in those words.",0),
    ("Every Voice Has A Lens You Need.","Advisor sees strategic risk. Builder catches implementation traps. Linter finds structural flaws. QA verifies against observable criteria. Kaizen audits every decision against the goal.",0.1),
    ("Converged Or It Doesn't Ship.","Plans reach you as a brief only after the team converges — you review, you approve, then execution begins without re-confirmation theater.",0.2),
   ])),
  ("The guardrails","A Logger That Never Decides. Modes For Real Budgets.",
   "Every dispatch, completion, failure, and decision lands in a read-only audit trail — timestamped, structured, and out of the convergence vote entirely.",
   truth([
    ("The Logger Records, Never Rules.","Session header on dispatch, timeline events as they happen, footer at the end. It never edits a file or makes a recommendation.",0),
    ("Multi-Model When You Can.","Different model families per role produce genuinely different lenses — blind spots in one architecture get caught by another.",0.1),
    ("Graceful Tiers When You Can't.","One provider available? Separate instances with role-specific prompts preserve independent reasoning. The multi-lens chain survives the budget.",0.2),
   ])),
 ],
 install_h2="Assemble The Panel.",
 install_lead="Ships in the mod pack. Pair it with Routing-Matrix to fill the lineup.",
 cta_h2="Six lenses beat one pair of eyes.",
 cta_p="The next build gets a team that has to agree — before you see anything.",
))

PAGES.append(pack_page(
 "routing-matrix", name="Routing-Matrix",
 title=T(["Every","task","routed","to","the","right",("model.","","","")]),
 sub="A fill-in-the-blanks YAML that maps your models onto agent roles — with fallback chains, provider lanes, ban lists, and policies that force perspective diversity. Ships as a template: the structure and governance are pre-built, you fill in your models.",
 meta="Multi-model routing configuration — roles, fallback chains, provider lanes, and diversity policies, as a fillable YAML template.",
 art="demo-routing-matrix.png",
 art_alt="A routing matrix YAML with role assignments, fallback chains, and policies — plus the validator passing",
 sections=[
  ("The structure","Ten Roles. One Sequence. Zero Guesswork.",
   "Orchestrator, three advisors with distinct lenses, builder, QA, linter, two kaizen passes, and a logger — each with a primary model, a provider lane, and an ordered fallback chain.",
   truth([
    ("Fallbacks That Walk Themselves.","Provider down, rate-limited, context window too small — the dispatcher walks the chain in order. Everything exhausted? It aborts with a list of every model tried and why each failed.",0),
    ("Every Provider Lane.","OpenAI, Anthropic, Google, DeepSeek, OpenRouter, local Ollama, Apple Silicon MLX, or your own custom lane — the matrix doesn't care where the model lives.",0.1),
    ("A Validator, Not A Prayer.","A script checks your filled matrix against the schema — missing fields, duplicate roles, malformed chains, banned models accidentally assigned. Green or it doesn't route.",0.2),
   ])),
  ("The policies","Diversity Is Enforced, Not Hoped For.",
   "The default policies exist because one model reviewing its own work is how blind spots ship.",
   truth([
    ("No Repeats In Sequence.","No model may hold two consecutive roles — every voice in the chain sees with different training data.",0),
    ("Always Be Testing.","New models prove themselves in real work alongside the team — never synthetic benchmarks. The team's convergence verdict keeps them or cuts them.",0.1),
    ("Bans With Teeth.","Name a banned model in a dispatch and the dispatch gets rejected — not silently substituted with something else.",0.2),
   ])),
 ],
 install_h2="Fill In Your Models. Run The Validator.",
 install_lead="Ships in the mod pack as a ready template with commented examples.",
 cta_h2="Stop letting one model grade its own homework.",
 cta_p="Copy the template, fill the blanks, validate — the matrix does the rest.",
))

PAGES.append(pack_page(
 "provision-project", name="Provision-Project",
 title=T(["A","new","project,","fully","governed,","in","one",("pass.",)]),
 sub="Say the word and a complete agent-ready workspace appears — canonical folder structure, governance files, session ledger, initial handoff — with native instruction files for every agent platform it detects on your machine.",
 meta="Provision an agent-ready project workspace with governance files, platform detection, and self-verifying scaffolding.",
 art="demo-provision-project.png",
 art_alt="A provisioned project tree with platform instruction files and the self-verify output printing OK",
 sections=[
  ("What lands","The Whole Scaffold, Not A Folder.",
   "Handoffs, session ledger, memory stub, troubleshooting file, environment and gitignore — the structure every project should have had from day one, there from minute one.",
   truth([
    ("It Detects Your Platforms.","Hermes, Claude Code, Codex, Cursor, OpenCode — whichever it finds, it writes that platform's native instruction file. Same core content, every portal.",0),
    ("Governance Points Home.","Every file references your governance nucleus — no personal names, no hardcoded paths, no duplicated rules rotting in project folders.",0.1),
    ("The First Handoff Exists Immediately.","Date, what was done, what's pending, open questions — written at provisioning, so the next session starts oriented.",0.2),
   ])),
  ("The guarantees","It Verifies Itself, Line By Line.",
   "A self-check runs at the end — every directory and file must print OK, or the job isn't reported done.",
   truth([
    ("Already Provisioned? It Refuses.","Run it twice on the same folder and it stops instead of clobbering your work.",0),
    ("Agents On Arrival.","Pass an agents list and each one gets provisioned into the project automatically — identity, skills, ledger stub.",0.1),
    ("A Dispatch Contract, Declared.","Orchestrator dispatches, workers execute, every worker reports a verdict, disagreements get resolved before anything moves on.",0.2),
   ])),
 ],
 install_h2="Stand Up Your Next Project Properly.",
 install_lead="Ships in the mod pack. Set GOVERNANCE_HOME once and every project inherits your rules.",
 cta_h2="Minute-one structure beats week-two cleanup.",
 cta_p="The next project starts governed — or starts over.",
))

PAGES.append(pack_page(
 "provision-agent", name="Provision-Agent",
 title=T(["An","agent","with","a","soul,","not","a",("folder.",)]),
 sub="One command and a fully provisioned agent identity appears — personality, capabilities, memory structure, and a profile of the human who directs it — registered in your governance nucleus and verified file by file.",
 meta="Provision a named agent with identity overlays, scoped skills, tool constraints, and memory structure.",
 art="demo-provision-agent.png",
 art_alt="The four agent identity files — SOUL, TOOLS, MEMORY, USER — plus the registry entry",
 sections=[
  ("The four files","Identity Is Four Documents Deep.",
   "SOUL.md carries the personality — role, boundaries, communication style. TOOLS.md spells out exactly which tools and APIs it may touch. MEMORY.md scaffolds long-term facts, session scratchpad, and learning log. USER.md profiles the human in charge.",
   truth([
    ("Scoped, Not Omnipotent.","Tool constraints are declared up front — what this agent may use, and what stays out of reach.",0),
    ("Skills Are Referenced, Never Copied.","The agent loads skills from your governance nucleus at runtime. Update a skill once and every agent gets the improvement.",0.1),
    ("You Get Asked, Not Guessed.","Missing a name, role, or handler? It asks once. It never provisions a guessed identity.",0.2),
   ])),
  ("The discipline","Registered. Verified. Append-Only.",
   "The agent lands in your registry with its role, skills, and handler — and the registry never deletes. Retired agents get archived, so your history stays whole.",
   truth([
    ("Casing Is Load-Bearing.","Sentinel, not sentinel. The name you give is the name it keeps — everywhere.",0),
    ("Self-Verify Or It Isn't Done.","Nine files and six directories must each print OK before it reports ready.",0.1),
    ("No Follow-Up Homework.","It hands you the path and the bound skills — next steps live in the agent's handoff, not in a chore list for you.",0.2),
   ])),
 ],
 install_h2="Stand Up An Agent That Knows Who It Is.",
 install_lead="Ships in the mod pack. Builds on Provision-Project's scaffold.",
 cta_h2="Folders don't do work. Identities do.",
 cta_p="The next agent arrives with a soul, a scope, and a paper trail.",
))

PAGES.append(pack_page(
 "provision-team", name="Provision-Team",
 title=T(["A","crew","with","rules,","not","a","group",("chat.",)]),
 sub="Multiple agents become one coordinated team — with a shared identity, a written roster, governance for how work changes hands, and a dispatch contract everyone observes. Registered, verified, archived never deleted.",
 meta="Provision a multi-agent team with identity, composition, governance, and orchestration protocol.",
 art="demo-provision-team.png",
 art_alt="The three team files plus a roster table showing provisioned agents and their skills",
 sections=[
  ("The three files","A Team Is Three Documents.",
   "TEAM_IDENTITY.md — name, shared purpose, collective boundaries. TEAM_COMPOSITION.md — who's on the team, their roles, their skills. TEAM_GOVERNANCE.md — handoff rules, approval gates, escalation paths.",
   truth([
    ("Composition Is Never Guessed.","Every member must already be a provisioned agent — the team assembles identities, it doesn't invent them.",0),
    ("Orchestration Isn't Reinvented.","The default contract — sequential dispatch, convergence voting, orchestrator resolves disagreements — is referenced, not rebuilt per team.",0.1),
    ("Custom Rules Get Written Down.","Need something beyond the standard contract? It goes in the governance file as a documented decision — never improvised mid-run.",0.2),
   ])),
  ("The guarantees","Same Discipline As Everything Else We Ship.",
   "Self-verifying. Append-only registry. No duplicated governance. And no chore lists handed back to you.",
   truth([
    ("It Refuses To Clobber.","A folder that already has team files is already a team — it stops instead of overwriting.",0),
    ("Every Line Prints OK.","Seven files and four directories verified before it reports ready.",0.1),
    ("Archived, Never Deleted.","Retired teams stay in the registry as archived. Your organizational memory survives reorganizations.",0.2),
   ])),
 ],
 install_h2="Turn Your Agents Into A Team.",
 install_lead="Ships in the mod pack. Provision the agents first, then assemble.",
 cta_h2="Coordination is a document, not a hope.",
 cta_p="The next multi-agent job starts with a roster and rules.",
))

PAGES.append(pack_page(
 "hooks-guide", name="Hooks-Guide",
 title=T(["Rules","that","fire","inside","the","agent's",("loop.","","","")]),
 sub="A hook intercepts your agent at the exact moment it matters — before a tool call, after it, at session start, at compaction — and returns allow, block, or modify. Governance without modifying a single line of the agent's source code.",
 meta="Agent lifecycle hooks across platforms — pre-flight gates, audit logging, compaction survival, with per-platform adapters.",
 art="demo-hooks-guide.png",
 art_alt="A pre-tool-use hook blocking a protected write, plus a silent audit log and the universal safety rules",
 sections=[
  ("The interception points","Six Moments Where Rules Can Live.",
   "Before any tool call. After it completes. Session start. Session end. Compaction. Error. Each one is a chance to enforce, log, or save state — and this guide maps all six to real use.",
   truth([
    ("The Gate.","Pre-tool-use hooks block writes to protected paths, banned commands, and out-of-scope actions — with a human-readable reason, not a silent failure.",0),
    ("The Ledger.","Post-tool-use hooks serialize every call — tool, input, exit status, milliseconds — to an audit log. And they never fail, because a logger that breaks the agent is worse than none.",0.1),
    ("The Survivor.","Compaction-survival patterns keep hook state alive when context gets compressed — persistent filenames, checkpoint directories, re-injection on the first post-compaction call.",0.2),
   ])),
  ("The safety rules","A Broken Hook Must Never Break The Agent.",
   "Fail-open on exceptions. A kill-switch sentinel file that bypasses everything. Idempotent. Five-second timeout. No network calls in pre-tool-use — it fires hundreds of times a session.",
   truth([
    ("Per-Platform Truth.","Hermes, Claude Code, Codex, Cursor, OpenCode, Continue, Aider, Cline — what each platform actually supports, not what their marketing implies.",0),
    ("Workarounds For The Rest.","No native hooks? Rule files, wrapper scripts, pre-commit hooks, post-hoc audit — the guide tells you which fallback each platform gets.",0.1),
    ("Battle-Tested Patterns Included.","Pre-dispatch validation, post-converge logging, compaction survival — with working code, not pseudocode.",0.2),
   ])),
 ],
 install_h2="Put Your Rules Where They Can't Be Ignored.",
 install_lead="Ships in the mod pack. Reference it the next time you need a gate, a log, or a checkpoint.",
 cta_h2="Governance inside the loop beats policy docs.",
 cta_p="The next rule you write will actually fire.",
))

# write all pages
(SITE / "skills").mkdir(exist_ok=True)
for p in PAGES:
    out = SITE / "skills" / f"{p['slug']}.html"
    out.write_text(page(p))
    print(f"skills/{p['slug']}.html")
print(f"total {len(PAGES)} pages")
