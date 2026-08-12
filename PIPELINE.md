# SkillManager_Public

**Public skill release pipeline for the IncredAgents / My AI Freedom Systems ecosystem.**

This project is the staging ground for every agent skill we release publicly —
whether given away free or sold — through
[github.com/MyAiFreedomSystems](https://github.com/MyAiFreedomSystems).

A skill earns its place here when it is:

1. **Useful to others** — solves a real problem for someone who is not us.
2. **Standalone** — works without our private files, accounts, brand assets, or machine setup.
3. **Clean** — contains no personal names, local paths, machine details, credentials, or client data.

## How it works

The agent skill [`skills/package-public-skill`](skills/package-public-skill/SKILL.md)
runs the release pipeline end to end:

```
candidate skill → evaluate → scrub personal data → write README + CHANGELOG + LICENSE
              → build themed web page → package .skill zip → stage in releases/
```

- **Evaluate** — is it genuinely useful and standalone? If not, it stays private.
- **Scrub** — `scripts/scrub_personal.py` scans every file for personal paths,
  emails, hostnames, tokens, and client identifiers. Nothing ships with findings unresolved.
- **Document** — every release gets a README (from the house template), a
  Keep-a-Changelog CHANGELOG, and a LICENSE chosen per release (free or paid —
  the owner decides; the site never promises either).
- **Web page** — every release gets a landing page built from
  `skills/package-public-skill/assets/site-template/`, which matches the IncredAgents
  theme used across our other skill sites (navy + cream + gold, Georgia italic
  headings, Yellowtail script accent).
- **Package** — validated and zipped as `<skill-name>.skill`, staged under `releases/`
  ready for GitHub.

## Repo layout

```
SkillManager_Public/
├── README.md                     ← you are here
├── CHANGELOG.md                  ← pipeline + release history
├── registry/
│   └── pipeline.md               ← candidate queue: private skill → release status
├── releases/                     ← staged, scrubbed, packaged skills ready for GitHub
├── skills/
│   └── package-public-skill/     ← the agent skill that runs the pipeline
└── site/                         ← public landing page for the skills program (traffic driver)
```

## The landing site

`site/` is the public-facing page for the whole skills program — the traffic
destination every skill's README and social post points back to. Run it locally:

```bash
cd site
npm run dev            # serves on http://localhost:7100/ (override with --port/--host)
```

## Rules of the house

- **Never fabricate.** No invented quotes, testimonials, endorsements, names,
  numbers, or screenshots. Every word attributed to a person must be their real
  words from a real source. If we don't have it, we ask for it — we never mock
  it up. (Learned the hard way in v7.)
- **No personal data ships.** Not a name, not a path, not a client. Scrub or don't ship.
- **Never overwrite. Always version.** Every design or content iteration gets a
  new version number: snapshot the current state into `versions/v<N>/` BEFORE
  changing anything, bump the version, log it in the CHANGELOG. No exceptions.
- **Free by default.** A skill is listed as paid only by explicit decision, recorded in `registry/pipeline.md`.
- **One theme.** All skill web pages use the shared template. Consistency is the brand.
- **Changelog or it didn't happen.** Every release, every version bump, logged.
