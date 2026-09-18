# Maturity bar: awesome list spokes

This repository must stay at the family maturity bar before growth-channel work
(especially a sindresorhus/awesome PR). The bar is **two gates**, both green:

1. **Release Repo Standard (RR-B)** for packaging: Pages landing, release gate,
   DISTRIBUTION, public identity, Install/Usage/Support/Version shell as needed.
2. **Sindresorhus Awesome readiness (SA-*)** for meta-list shape: theme blurb,
   Contents rules, awesome-lint clean, CC0 detectible LICENSE, logo when practical,
   and real 30-day age (never faked).

## Always-required lint

**awesome-lint must pass on every push and PR to main.**

- CI job: `.github/workflows/lint.yml` runs `npx awesome-lint@2.3.0 README.md`.
- A failing awesome-lint run blocks merge. Do not disable or soften this check.
- Local check before push:

```bash
npx awesome-lint@2.3.0 README.md
python scripts/check_release.py
python ~/.zcode/skills/sindresorhus-awesome-ready/tools/audit.py --repo . --gh --lint
```

## SA decision vocabulary

| Decision | Meaning |
|---|---|
| NO-GO | Any SA FAIL remains |
| WAIT | No FAIL; SA-AGE under 30 days and/or manual submit steps remain |
| GO-IF-MANUAL-CLEAR | No FAIL; age PASS; lint PASS; only submit-day manual steps left |

WARNs are always printed and should be fixed when cheap (logo, licence sidebar).
They do not alone force NO-GO.

## Age integrity

Do not backdate commits, rewrite history, or change file mtimes to invent 30 days
of maturity. SA-AGE is calendar truth.

## Re-run on sibling spokes

Use the skill prompt in
`docs/superpowers/prompts/awesome-spoke-maturity.md`
(or `~/.zcode/skills/sindresorhus-awesome-ready/templates/maturity-prompt.md`)
against each `awesome-*` repo until that spoke matches this bar.
