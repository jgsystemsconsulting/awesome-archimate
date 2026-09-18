---
date: 2026-09-18
project: awesome-archimate
mode: light
rounds: 1
input_digest: 8a3ea4ff516a56bc6463b3584dba699a2b60b3a44e07f706b728d1b2c68092a9
open_objections: []
---

# Work packages: awesome-archimate (2026-09-18, light mode, round 1)

First package-loop run. Trigger state: post-release v0.1.0 (2026-09-17) plus
taste-skill landing audit (2026-09-18). Lens wave found 9 raw candidates; merge
unions left 6 packages; triage graded all 6 PASS with zero critical defects.
Dependency order: P2, P1, P3, P4, P5, P6. P6 is independent and can run any time.

One escalated conflict (X1) is a human fork at the proposal stop: whether the
chrome nits (favicon, woff2 preload, nav touch targets, dead IE shim) belong
inside P1 or stay as backlog rows b-01 through b-04.

## P2: landing-truth-gate

| Field | Value |
|---|---|
| id | P2 |
| name | landing-truth-gate |
| size | M |
| deps | none |
| status | done |
| promoted_ids | [] |
| corroboration | 3 (value, risk, cohesion) |
| first_prompt | `/superpowers-process full landing truth gate` |

**Problem.** The product is a dual surface: canonical README list plus the
docs/index.html router. Version, sweep, and entry chips and the eight
section-index anchors are hand-copied into the landing with no check against
README/RELEASE-INFO. scripts/check_release.py only asserts docs/index.html
exists, and links.yml lychee scopes README.md only. A release bump or heading
rename desyncs Pages silently while CI stays green.

**Evidence.**

- docs/index.html:L429-440, `<dt>version</dt><dd>0.1.0</dd>` through `<dt>entries</dt><dd>17</dd>` (hardcoded chips, accurate 2026-09-18)
- docs/index.html:L450-458, section-index anchor links to README headings
- scripts/check_release.py:L11-19, REQUIRED list checks file existence only
- .github/workflows/links.yml:L28, `args: --no-progress --max-retries 3 --include-fragments=anchor-only README.md`
- RELEASE-INFO.txt:L2, `Version: 0.1.0`
- README.md:L6, sweep badge `last full sweep-2026--09`
- DESIGN.md:L9, README stays canonical deep list

**In scope.** Extend check_release.py (or a sibling gate run by validate.yml) to
assert landing chips match RELEASE-INFO version, README sweep badge, and README
curated entry count; assert section-index href fragments match the live README
heading anchors; document the single write path so maintainers know chips and
anchors are gated, not freehand.

**Out of scope.** Entry-row mirroring on the landing; lychee args and PR fail
policy (P5 owns links.yml); copy rewrites (P1); favicon and font chrome; README
entry content changes; distribution channel submissions; Path N Next export.

**Why now.** Every entry add and release desyncs Pages silently; the gate must
land before P1 copy edits and P3 distribution traffic depend on a router that
can go quietly wrong.

**Triage notes.** PASS. Overlap with P5 split on evidence: P2 keeps chip, count,
and fragment assertions in the release gate; links.yml changes cede to P5.

## P1: landing-visitor-copy

| Field | Value |
|---|---|
| id | P1 |
| name | landing-visitor-copy |
| size | S |
| deps | P2 |
| status | done |
| promoted_ids | [b-01, b-02, b-03, b-04] |
| corroboration | 2 (value, cohesion) |
| first_prompt | `/superpowers-process full landing visitor copy` |

**Problem.** The landing is the only surface most newcomers see before the
README, but the copy uses maintainer jargon: nav label "Hero", duplicate
full-list CTA labels ("Full list" vs "Open full list on GitHub"), "Evidence"
and "Sections" headings, and maintainer-only sentence tails (FAMILY.md registry
detail at L442, "the landing does not mirror entry rows" at L449). Same file
carries the contested chrome nits (X1).

**Evidence.**

- docs/index.html:L406, `<a href="#hero">Hero</a>`
- docs/index.html:L411, nav `<a class="nav-full" ...>Full list</a>`
- docs/index.html:L421, hero `<a class="primary" ...>Open full list on GitHub</a>`
- docs/index.html:L427, `<h2 id="evidence-heading">Evidence</h2>`
- docs/index.html:L442, family paragraph with FAMILY.md sentence tail
- docs/index.html:L449, mirror-note sentence
- DESIGN.md:L8-9, primary actions contract
- DESIGN.md:L23, "The list is the product. Chrome exists to route attention."
- DESIGN.md:L112, touch targets 44px minimum on primary actions

**In scope.** Rename nav and section labels to visitor language (brand or Top
for the first item, plain names for headings); one shared label for the
full-list intent across nav and hero; drop or shorten maintainer-only sentence
tails, keeping a short family pointer; optional merge of hero claim and support
into one line of at most 20 words. Contested per X1: favicon, woff2 preload,
nav touch targets, dead IE shim (b-01..b-04 if the fork keeps them out).

**Out of scope.** Entry-row mirroring; visual redesign and token changes;
Path N Next; chip and anchor sync automation (P2); README entries and badges;
CI refactors; og:image (pilot-optional per DESIGN.md); distribution work.

**Why now.** Post-v0.1.0 the landing is the submitted homepage router; every
growth channel sends people through this copy first. Runs after P2 so copy
edits land once the gate catches drift.

**Triage notes.** PASS. Chrome-nit items stay in in_scope pending the X1 fork;
all items live in the single file docs/index.html, so size stays S either way.

## P3: org-catalogue-entry

| Field | Value |
|---|---|
| id | P3 |
| name | org-catalogue-entry |
| size | S |
| deps | P1, P2 |
| status | done |
| promoted_ids | [] |
| corroboration | 1 (value) |
| first_prompt | `/superpowers-process full org catalogue entry` |

**Problem.** The only planned growth channel still open after v0.1.0 is the org
catalogue entry on labs.jgsystemsconsulting.com. Repo, Releases, Pages, and
About are already submitted, so discovery stays capped until the catalogue
routes EA/MBSE practitioners to the list.

**Evidence.**

- docs/DISTRIBUTION.md:L13, org catalogue row, status planned
- docs/DISTRIBUTION.md:L9-11, GitHub surfaces submitted
- README.md:L3-4, stated goal
- DESIGN.md:L7-8, primary users

**In scope.** Publish the awesome-archimate entry on the org catalogue
alongside the other awesome-mbse spokes; point catalogue traffic at the list
with an accurate one-line description; update DISTRIBUTION.md from planned to
submitted when live.

**Out of scope.** sindresorhus/awesome PR (P4 gates it); community directory
posts; marketplace work (ledger N/A); landing HTML redesign.

**Why now.** Next named channel in the ledger; goes live only after the landing
router is trustworthy (P2 gate, P1 copy).

**Triage notes.** PASS, no defects. External-site work (labs site content), so
the SP run covers the entry change plus the ledger update.

## P4: awesome-acceptability-assessment

| Field | Value |
|---|---|
| id | P4 |
| name | awesome-acceptability-assessment |
| size | S |
| deps | none |
| status | done |
| promoted_ids | [] |
| corroboration | 1 (value) |
| first_prompt | `/superpowers-process full awesome acceptability assessment` |

**Problem.** The external channel with the widest reach (sindresorhus/awesome) is
deferred solely because the acceptability gate is unassessed. Without a
concrete go/no-go on membership bar, review bandwidth, and naming, the list
cannot pursue or permanently close its largest distribution payoff.

**Evidence.**

- docs/DISTRIBUTION.md:L14, deferred row naming the unassessed gate
- README.md:L1, Awesome badge already claimed
- README.md:L3-4, stated goal

**In scope.** Written acceptability assessment against the sindresorhus/awesome
membership bar, naming, and review expectations; explicit go/no-go plus any
prerequisite README fixes; DISTRIBUTION.md note update with decision date.

**Out of scope.** Opening the awesome PR before a pass decision; org catalogue
work; community directory posts.

**Why now.** Pure gate-assessment debt; resolves or closes the biggest external
payoff without blocking landing fixes. Independent, can run in parallel with
P2/P1.

**Triage notes.** PASS, no defects.

## P5: link-check-product-surface

| Field | Value |
|---|---|
| id | P5 |
| name | link-check-product-surface |
| size | S |
| deps | none |
| status | done |
| promoted_ids | [] |
| corroboration | 1 (risk) |
| first_prompt | `/superpowers-process full landing link check coverage` |

**Problem.** The product is a curated link list, but CI only lychee-scans
README.md, never docs/index.html, and PR runs set fail: false so broken
product-surface links merge with only an advisory warning. Visitors hit rot
before maintainers do.

**Evidence.**

- .github/workflows/links.yml:L28-29, README-only args and `fail: false`
- .github/workflows/links.yml:L31-38, advisory-only warning step on PRs
- docs/index.html:L411, L451-458, landing hrefs outside lychee scope

**In scope.** Add docs/index.html to lychee args (or equivalent landing href
check); tighten PR policy so product-surface link failures are visible as
blocking or required status without weakening the scheduled report-issue
behavior; keep action refs SHA-pinned.

**Out of scope.** Stale workflow heuristics; chip and anchor sync (P2 owns the
gate assertions); distribution submissions.

**Why now.** Without landing coverage, P2 can prove anchors match README while
outbound landing URLs rot uncaught; link integrity is the core failure mode of
an awesome list.

**Triage notes.** PASS. Overlap with P2 split: P5 owns links.yml (args and fail
policy); gate-side fragment and count assertions stay in P2.

## P6: pin-validate-setup-python

| Field | Value |
|---|---|
| id | P6 |
| name | pin-validate-setup-python |
| size | S |
| deps | none |
| status | done |
| promoted_ids | [] |
| corroboration | 1 (risk) |
| first_prompt | `/superpowers-process full pin validate setup python` |

**Problem.** validate.yml is the only workflow that runs the release gate, yet
it pulls actions/setup-python@v5 by mutable tag while the other three workflows
pin full commit SHAs per the repo's stated supply-chain hardening. A retagged
major can change the Python runner under the gate without a reviewable diff.

**Evidence.**

- .github/workflows/validate.yml:L19-24, `uses: actions/setup-python@v5`
- .github/workflows/links.yml:L2-7, SHA-pinning policy comment
- .github/workflows/lint.yml:L23, SHA-pinned checkout with version comment

**In scope.** Resolve setup-python v5 to a full commit SHA and pin it with a
version comment matching sibling workflows; confirm validate still runs
check_release.py on push and PR to main.

**Out of scope.** check_release.py logic; new CI jobs; Dependabot or Renovate
policy.

**Why now.** Broken-window supply-chain exception on the sole release-gate
workflow; tiny fix, lands before larger CI work copies validate as the
pattern. Independent.

**Triage notes.** PASS, no defects.

## Conflict X1 (human fork)

P1 scope: value lens excluded the chrome nits (favicon, woff2 preload, nav
touch targets, IE shim) as no-payoff polish; cohesion lens included them as one
landing subsystem with the copy work. Triage did not resolve it. Resolve at the
proposal stop: "include chrome in P1" promotes b-01..b-04 into P1
(promoted_ids); "copy only" leaves them as backlog rows.
