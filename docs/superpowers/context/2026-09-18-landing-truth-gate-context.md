# Context: landing-truth-gate (2026-09-18)

## Context brief

**Primary question.** What must change so docs/index.html chips (version, sweep, entry count) and the eight section-index anchors cannot drift from RELEASE-INFO.txt / README.md without CI failing?

**Sub-questions.**

1. How does scripts/check_release.py work today (REQUIRED list, fail model, invocation)?
2. Where and how are chips and section-index anchors authored in docs/index.html?
3. What are the single sources of truth for version, sweep date, curated entry count, and section heading anchors?
4. How are curated entries marked in README so a count is unambiguous?
5. How is validate.yml wired, and what can host a new assertion without inventing a second CI path?
6. What constraints or contradictions would make a naive gate wrong (entry count scope, lychee ownership, P5 boundary)?

**Success criteria (decision-bearing).**

- C1: Locate the current release-gate implementation and its CI entry point.
- C2: Locate every hardcoded chip value and every section-index href in docs/index.html.
- C3: Identify the authoritative sources for version, sweep, curated entry count, and README section heading anchors.
- C4: Identify how curated entries are marked in README so a count is unambiguous.
- C5: Identify existing conventions the gate should match (fail list style, validate.yml Python setup, link-check ownership boundary with P5).
- C6: Surface gotchas that would make a wrong gate (counting meta sections, badge parse fragility, fragment slug rules).

**Out of scope.** Visitor copy rewrites (P1); lychee args and PR fail policy (P5); org catalogue and sindresorhus assessment (P3/P4); setup-python pin (P6); Path N Next; entry-row mirroring onto the landing; README inclusion-bar content changes.

**Budget.** Round cap 3. Round 1 reached CONTEXT_COMPLETE.

**Workspace baseline.** HEAD 51082134d30023988967fc9c4003bb2d21eb4628. Porcelain fingerprint sha256 a943b791de3bfb9072ae32ec8cd64db72f8361288c47815b59ac7090816d25fd (untracked docs/superpowers/ only at gate start).

## Findings

Round 1 graded 12 claims: 8 CORROBORATED, 4 SINGLE-SOURCE, 0 CONFLICTED, 0 STALE. See the context log for the full table.

1. **Gate existence-only (CORROBORATED, C1).** scripts/check_release.py REQUIRED includes docs/index.html and only runs `is_file()`. Content scan of HTML is private-key regex only. validate.yml invokes `python scripts/check_release.py` after setup-python 3.12.
2. **Three chips hardcoded (CORROBORATED, C2).** docs/index.html L429-440: version 0.1.0, sweep 2026-09, entries 17. No generator.
3. **Eight section-index anchors hardcoded (CORROBORATED, C2).** docs/index.html L451-458 full GitHub blob URLs with README heading slugs matching Contents L16-23.
4. **Version SoT = RELEASE-INFO.txt Version field (SINGLE-SOURCE, C3).** L2 `Version: 0.1.0`. Mirrors exist in README Version, CITATION.cff, CHANGELOG. Gate reads none today. Tag field is `v0.1.0` (do not compare chip to Tag).
5. **Sweep has no machine SoT (CORROBORATED, C3/C6).** Literals only: README.md L6 badge alt `2026-09` and landing chip. Shield URL path uses escaped `2026--09`. RELEASE-INFO has Built timestamp, not sweep.
6. **Curated entry count = 17 under eight headings (CORROBORATED, C4).** Grammar from CONTRIBUTING entry format under Specs..Communities. Raw `^- [` count is 29 = 12 Contents TOC + 17 curated (naive proxy flagged SINGLE-SOURCE, unusable).
7. **Fail convention (CORROBORATED, C5).** Accumulate `fails`, print `RELEASE GATE FAILED:` plus indented `-` lines, `sys.exit(1)`.
8. **P5 lychee boundary (CORROBORATED, C5).** links.yml README-only, fail:false advisory. Must not own landing truth or block-merge link policy.
9. **Meta gotchas (CORROBORATED, C6).** Contents mixes 8 curated + 4 meta anchors; body also has Contributing (not in Contents) plus Install/Usage/Support/Version. Heading-scan or full-Contents count breaks.
10. **Tag vs bare version (SINGLE-SOURCE, C6).** RELEASE-INFO Tag `v0.1.0` vs Version `0.1.0`; chip uses bare.
11. **SCAN_GLOBS pattern (SINGLE-SOURCE, C5).** scripts/check_release.py L34 already globs docs HTML; extend this script rather than a second path.

## Synthesis

Extend **scripts/check_release.py** in place (sole validate.yml caller). Do not add a second workflow for P2. Assertions to add:

| Check | Expected source | Landing parse |
|---|---|---|
| version chip | RELEASE-INFO.txt `Version:` field (bare, not Tag) | `<dt>version</dt>` sibling `<dd>` text |
| sweep chip | README.md L6 badge alt `Last full sweep: YYYY-MM` (not shield path) | `<dt>sweep</dt>` sibling `<dd>` |
| entries chip | count of grammar-valid curated bullets under the eight section headings only | `<dt>entries</dt>` sibling `<dd>` integer |
| section-index | exactly eight `<ul class="section-index">` links whose `#fragment` equals GitHub-slug of each curated `##` heading in order (or set-equal to Contents' first eight curated anchors) | href fragments |

Gotchas the implementer must bake in:

- Do not count all `^- [` lines (29). Use entry grammar under Specs..Communities only (17 today).
- Do not slug every `##` heading: Contributing and meta sections are not landing targets.
- Prefer badge **alt text** for sweep (`2026-09`), not the double-hyphen shield path.
- Compare version to RELEASE-INFO **Version**, never **Tag**.
- Lychee/P5 stays out of this package: no links.yml changes here.
- Keep existing fail-list + exit-1 style; append new messages into `fails`.
- Optional maintainer note: document the write path (update RELEASE-INFO / README badge / curated rows, then refresh chips and section-index together). PR template version-bearing list omits docs/index.html today; gate is the enforcement, template update is optional hygiene inside this package if cheap.

Open questions for design (not blocking CONTEXT_COMPLETE): whether section-index must preserve display label text as well as fragment; whether validate.yml needs any change (no: keep one run line).

## Evidence index

| loc | kind |
|---|---|
| scripts/check_release.py:9-62 | code |
| scripts/check_release.py:11-19 | code |
| scripts/check_release.py:34 | code |
| scripts/check_release.py:57-61 | code |
| .github/workflows/validate.yml:15-24 | config |
| .github/workflows/links.yml:27-38 | config |
| docs/index.html:428-458 | code |
| README.md:6 | doc |
| README.md:14-27 | doc |
| README.md:29-68 | doc |
| README.md:70-108 | doc |
| RELEASE-INFO.txt:1-4 | doc |
| CONTRIBUTING.md:28-69 | doc |
| CONTRIBUTING.md:139-146 | doc |
| CITATION.cff:4-19 | doc |
| .github/PULL_REQUEST_TEMPLATE.md:11,26 | doc |

## Round summary

Round 1: fixes_applied=0, coverage=6/6, verdict=CONTEXT_COMPLETE, next=converged
