# Show HN Launch Kit — Pre-Flight Check

Everything needed to launch Pre-Flight Check on Hacker News. Written so Tina
only has to copy, paste, and be present for two hours.

---

## The post

**Title** (exact — HN titles must be plain, no adjectives):

```
Show HN: Pre-Flight Check – a skill that stops your AI agent shipping unverified work
```

**URL:**

```
https://github.com/MyAiFreedomSystems/pre-flight-check
```

**Text:** leave empty. URL posts perform better for tools; the story goes in
the first comment.

## The first comment (post this yourself, immediately after submitting)

```
I built this after my agent embarrassed me in front of a client.

It delivered a landing page and told me it was "verified and ready to
publish." I forwarded it to the client. She wrote back with a screenshot:
at her laptop's window width, the hero image was sitting on top of the
headline. The agent had tested desktop and phone widths, declared victory,
and stopped. Her screen was 690px — right in the gap between the two
breakpoints, a width nobody checked.

That bug was my fault, not the model's. I never made "done" mean anything.
So I wrote the gate I should have given it: before an agent may call any
work done, it has to run the check — trace every name, number, and quote to
a real source (or delete it), fetch every link, screenshot the page at one
width inside every breakpoint gap and one pixel either side of each
breakpoint, verify overlaps with geometry instead of eyeballs, and report
honestly what passed, what failed, and what it didn't check.

It's a SKILL.md file, so it works in Claude Code, Cursor, Codex, and
anything else that speaks the Agent Skills standard. No dependencies, no
service, no signup. npx skills add MyAiFreedomSystems/pre-flight-check.

The part that surprised me: the biggest failure mode it catches isn't
visual. It's fabricated content — testimonials, statistics, "facts" the
agent invented to fill a gap. Gate 1 (truth check) fires more often than
every other gate combined.

Happy to answer questions about the breakpoint-sweep method or the
geometry-based overlap checks — those two took the longest to get right.
```

## Timing

- Post **Tuesday, Wednesday, or Thursday, between 8:00 and 10:00 AM Eastern**.
- Do not post on a weekend or Monday morning.
- Clear two hours after posting. The first two hours decide everything.

## The two-hour reply playbook

- Reply to **every** comment, fastest to the earliest ones. HN weights early
  discussion heavily.
- Answer like a builder, not a marketer. "Yes, that breaks when X — here's
  how the gate handles it" beats "great question!"
- Criticism is a gift. "You're right, that's a hole — gate 3 doesn't cover
  PDFs yet" builds more trust than defending.
- If someone posts a better approach: "That's smart — want to open an issue?"
  turns a critic into a contributor.
- Never argue about whether the problem is real. Someone always says "just
  review your agent's work yourself." One calm reply ("the whole point is I
  shouldn't have to") and move on.

## What NOT to do

- No adjectives in the title. No "awesome", no "powerful", no "free".
- No "free forever" — it isn't necessarily.
- No vote rings. Do not ask anyone to upvote. HN detects it and kills the
  post, sometimes the account.
- No link-shorteners, no UTM parameters.
- Don't cross-post the link anywhere during the first two hours — split
  attention kills momentum.
- Don't edit the title after posting.

## After the post

- If it lands on the front page: add nothing, keep replying. Resist editing
  the README mid-flight.
- If it sinks with <5 points: that's normal (most Show HNs do). Wait 2+ weeks,
  improve the repo, then it's eligible for a repost under HN's rules.
- Either way: screenshot the thread for the changelog and the site.

## What I need from Tina

1. **Your HN account** — the post has to come from a human's account with
   some history. A brand-new account posting its own project gets flagged.
2. **One morning** — the two-hour window above.
3. **A decision on the screenshot** — optionally attach the "before" image
   (the 690px overlap) to the README before launch. Real failure evidence is
   the strongest asset this repo has.

## Deferred directory submissions — revisit dates

- **hesreallyhim/awesome-claude-code** (47k★): hard rule — repo must be 14+
  days old with active development, or 100+ stars. First commits were
  2026-08-10/11 → eligible **2026-08-25**. Must be submitted by a human via
  their web issue form, not the gh CLI.
- **VoltAgent/awesome-agent-skills**: rejects brand-new skills ("give your
  skill time to mature and gain users"). Revisit when the repos have real
  stars/installs — check again mid-September.
