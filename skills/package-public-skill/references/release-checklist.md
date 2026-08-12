# Release Checklist

Run top to bottom before any skill is declared public-ready.

## Standalone
- [ ] Works without the owner's accounts, subscriptions, or logged-in sessions
- [ ] Works without private brand assets (or bundles generic replacements)
- [ ] No references to other private skills, folders, or internal tooling
- [ ] Install + first success achievable in under 10 minutes by a stranger

## Scrub
- [ ] `scrub_personal.py` exits 0
- [ ] No owner name, username, home path, hostname, or machine detail anywhere
- [ ] No client names, client data, or customer-identifying examples
- [ ] No credentials, tokens, or API keys (checked scripts AND docs AND examples)
- [ ] Comments and docstrings also clean (they ship too)

## Documentation
- [ ] README.md filled from the house template; no `{{PLACEHOLDER}}` left
- [ ] CHANGELOG.md present; first public entry dated; Keep-a-Changelog format
- [ ] LICENSE present; owner confirmed the license choice
- [ ] SKILL.md frontmatter: `name` + complete `description` with trigger phrases

## Web page
- [ ] Built from `assets/site-template/`, tokens replaced
- [ ] Palette/fonts untouched (navy `#1B3A5C`, cream `#FAFAF8`, gold `#D9A441`)
- [ ] Repo link points at the intended GitHub URL
- [ ] Page loads with `npm run dev` and looks right at mobile width

## Package & stage
- [ ] `<skill-name>.skill` zip built from the scrubbed folder
- [ ] Everything staged under `releases/<skill-name>/`
- [ ] `registry/pipeline.md` status updated
- [ ] Project `CHANGELOG.md` entry added
- [ ] Owner confirmed: free or paid, and the GitHub repo name
