# Context: landing-visitor-copy (2026-09-18)

## Context brief

**Primary question.** What exact visitor-facing strings and head/chrome items in docs/index.html must change for taste-audit should-fixes with X1 chrome included?

**Success criteria C1-C4.** Met in round 1.

**Out of scope.** Chip dd values, chip dt names, section-index structure/href fragments, check_release.py logic, lychee, distribution.

**Ruling X1.** Parent package drain includes chrome nits in P1 (favicon, woff2 preload, nav touch targets, remove main{display:block}). Promote backlog b-01..b-04 into this package.

**Workspace baseline.** HEAD b93a41e (P2 Done on feat/landing-truth-gate).

## Findings

1. Nav labels L406-411: Hero, Evidence, Sections, Curation, Contribute, Full list.
2. Hero L418-421: h1 Awesome ArchiMate; claim; support; CTA "Open full list on GitHub".
3. Headings: Evidence L427, Sections L448, Curation L465, Contribute L472.
4. Family prose L442 FAMILY.md tail; mirror prose L449 "does not mirror entry rows".
5. Head: no rel=icon, no preload; fonts local woff2 already.
6. Nav a padding space-2/space-1 (~35px); primary already min-height 44px (DESIGN primary-only 44px).
7. main{display:block} L169-171 IE shim.
8. P2 gate: keep dt names version/sweep/entries, dd values, ul.section-index eight li href fragments unchanged. Display text of section-index links and in-page #ids may change if href and id stay paired.
9. DESIGN tokens/light/self-host fonts bind; no CDN.

## Synthesis

Copy changes (visitor language):
- Nav first link: "Top" or "Awesome ArchiMate" (not Hero); keep href #hero or rename id+href together to #top.
- One full-list CTA label on nav and hero (pick "Open full list" or "Full list on GitHub", use both places).
- Headings: Evidence -> Status (or fold chips without h2 jargon); Sections -> Browse sections (or keep Sections as plain); optional.
- Family: short "Part of the awesome-mbse list family." drop FAMILY.md tail.
- Sections intro: drop "the landing does not mirror entry rows."
- Optional merge claim+support to one <=20 word line.

Chrome (X1 include):
- Add favicon (simple SVG data URI or link to monogram under docs/).
- Preload IBMPlexSans-Regular and SemiBold woff2.
- Raise .site-nav a min-height/padding to 44px touch.
- Remove main{display:block} only.

Must not: change chip structure, dd values, section-index hrefs/class/li count; add CDN fonts; touch check_release.py.

## Evidence index

| loc | kind |
|---|---|
| docs/index.html:3-421 | code |
| docs/index.html:147-171 | code |
| docs/index.html:406-472 | code |
| DESIGN.md:51,112,148 | doc |
| scripts/check_release.py:65,161 | code |
| docs/superpowers/packages/...:P1 X1 | doc |
