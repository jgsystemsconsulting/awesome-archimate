# Spec and assessment: awesome-acceptability-assessment (P4)

Date: 2026-09-18
Package: P4

## Problem

sindresorhus/awesome list PR is deferred because the acceptability gate was never assessed.

## Research

Primary sources consulted this session:

- https://github.com/sindresorhus/awesome/blob/main/awesome.md (contribution guidelines; create-list guidance)
- https://github.com/sindresorhus/awesome/blob/main/pull_request_template.md
- https://github.com/sindresorhus/awesome (README list structure)

research: local assessment with official awesome contribution docs (URLs above)

## Assessment criteria (from awesome contribution guidance)

1. List must be useful and focused; not a dumping ground.
2. Descriptions must be clear and not promotional fluff.
3. Table of contents and consistent formatting.
4. Links must work; dead links fail review.
5. Prefer established resources; avoid low-quality or spam.
6. Naming: Awesome X pattern; avoid trademark abuse.
7. Review bandwidth: maintainers are slow; list must be high quality before PR.
8. Badge and LICENSE expectations for listed projects.

## Awesome ArchiMate against the bar

| Criterion | Status | Notes |
|---|---|---|
| Focus | PASS | ArchiMate-only curated index; 8 sections, 17 entries |
| Format | PASS | Family entry format with tags and year; Contents present |
| Links | PASS at launch | lychee on README; P5 now covers landing too |
| Naming | PASS | Awesome ArchiMate matches Awesome X |
| Badge | PASS | awesome.re badge already on README |
| Licence | PASS | CC0-1.0 list; upstream keep own licences |
| Depth | BORDERLINE | 17 entries is thin vs many listed awesome lists; reviewers may ask for more breadth before accepting |
| Freshness process | PASS | weekly lychee + monthly freshness report |
| CONTRIBUTING | PASS | inclusion bar and tag vocabulary exist |
| Self-promotion | PASS | editorial neutrality cited |

## Decision

**Go, with prerequisites (not PR-now).**

Do **not** open the sindresorhus/awesome PR in this package. Prerequisites before a future PR:

1. Grow curated entry count past the thin-list risk (target roughly 30+ high-quality entries across the eight sections without lowering the inclusion bar).
2. One clean full-sweep lychee run (README + landing) with zero open broken-link issues.
3. Confirm list still matches awesome.md formatting conventions after growth (TOC, descriptions, no marketing fluff).
4. Re-read the current PR template on sindresorhus/awesome the week of submission (templates change).

**No-go** only if the project abandons public awesome-list distribution. That is not the case.

## DISTRIBUTION.md update

Update the sindresorhus/awesome row: deferred with decision date 2026-09-18 and the go-with-prerequisites note above.

## Non-goals

- Opening the PR in this package
- Org catalogue work (P3)
- Community directory scatter-posts
