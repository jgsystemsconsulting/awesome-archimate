# Context log: landing-truth-gate

| Finding | First seen | Last seen | Verdict | Rationale |
|---|---|---|---|---|
| Landing is checked for existence only; no chip or anchor validation | R1 | R1 | CORROBORATED | scripts/check_release.py REQUIRED list includes docs/index.html (L15) with an is_file check only (L17-19); the only content scan of docs html is the private-key regex (L31-44). Invoked by .github/workflows/validate.yml L24 with setup-python 3.12 (L19-22). Two code sites. |
| Three evidence chips hardcoded in the landing | R1 | R1 | CORROBORATED | docs/index.html L429-440: three chip nodes carry literals version 0.1.0, sweep 2026-09, entries 17. Static file; no workflow generates it (validate.yml runs check_release.py only, links.yml runs lychee only). |
| Eight section-index anchors hardcoded in the landing | R1 | R1 | CORROBORATED | docs/index.html L451-458 hardcode eight README URLs with slugs; L449 states "Eight README anchors"; slugs match README.md Contents L16-23. Code plus agreeing doc. |
| Version SoT is the RELEASE-INFO.txt Version field; no code parses it | R1 | R1 | SINGLE-SOURCE | RELEASE-INFO.txt L2 "Version: 0.1.0". Mirrors: README.md L107-108, CITATION.cff L4 and L19, CHANGELOG.md L9. All doc sites; no code reads the field (gate checks existence only). SoT named: RELEASE-INFO.txt. |
| Sweep date has no machine-readable SoT; exists only as literals | R1 | R1 | CORROBORATED | README.md L6 badge and docs/index.html L433-436 chip both carry 2026-09 as literals; RELEASE-INFO.txt has a Built timestamp (L3) but no sweep field; CONTRIBUTING.md L88 mentions the sweep concept only. Doc plus code site. |
| Curated entry count is 17 under eight section headings | R1 | R1 | CORROBORATED | README.md L31-68 recounted: 17 grammar-valid entries across 8 headings (3+2+2+4+1+3+1+1). CONTRIBUTING.md Entry format (L28-69) defines the grammar. Landing chip agrees (docs/index.html L438-439). Code plus doc. |
| Raw "- [" line count 29 is a naive proxy for the entry count | R1 | R1 | SINGLE-SOURCE | README.md only: 29 lines match `^- [`, decomposing as 12 Contents links (L16-27) + 17 curated entries. Recount verified this round. A gate must count grammar-valid entries under the eight headings, not raw lines. |
| Fail convention: accumulate list, print, exit 1 | R1 | R1 | CORROBORATED | scripts/check_release.py accumulates `fails` (L9; appends at L19, 29, 44, 50, 52, 55) then prints "RELEASE GATE FAILED:" and sys.exit(1) (L57-61). CONTRIBUTING.md L4: "CI gates enforce most of it". Two code loci plus doc. |
| P5 boundary: lychee owns README link checking, advisory on PRs | R1 | R1 | CORROBORATED | .github/workflows/links.yml L28 scopes lychee to README.md with --include-fragments=anchor-only, L29 fail: false, L31-38 advisory warning only. CONTRIBUTING.md L139-146 restates. The landing's outbound anchors are not covered by lychee. |
| Meta gotcha: Contents mixes curated and meta anchors; extra headings exist | R1 | R1 | CORROBORATED | README.md Contents L16-27 = 8 curated + 4 meta anchors (Install, Usage, Support, Version); further non-section headings at L70 (Contributing), L75 (Install), L84 (Usage), L93 (Support), L105 (Version); badge text is URL-escaped (2026--09). docs/index.html L449 asserts the count of eight. Naive heading or line counts break. |
| Tag form v0.1.0 vs bare 0.1.0 both exist in the SoT file | R1 | R1 | SINGLE-SOURCE | RELEASE-INFO.txt L2 "Version: 0.1.0" and L4 "Tag: v0.1.0". Landing chip and README use the bare form. Single artifact. |
| SCAN_GLOBS is a reusable scan-list pattern | R1 | R1 | SINGLE-SOURCE | scripts/check_release.py L34 defines SCAN_GLOBS; only site in the repo. Single code site. |

## Round 1

- Claims graded: 12. CORROBORATED 8, SINGLE-SOURCE 4, CONFLICTED 0, STALE 0. Verdict values CONFLICTS_OPEN, GAPS_REMAIN, and TRIAGE_ABORTED were not triggered this round.
- read_errors: none. Every cited path was re-read while grading; all quotes matched current file contents.
- Reframes against the merge: the sweep claim was upgraded to CORROBORATED after verifying the landing chip (docs/index.html L434-435) as a second, code site; the merge had it doc-only. The 29-vs-17 tension was reconciled without a CONFLICTED row: the raw `^- [` count is exactly 29, decomposing as 12 Contents links + 17 curated entries, so both numbers are correct for their own metric. Row split accordingly: grammar-valid count CORROBORATED, naive proxy SINGLE-SOURCE and flagged as unusable in the gate.
- Coverage: C1 met (gate implementation and CI entry point located). C2 met (all three chip values and all eight section-index hrefs located). C3 met (version SoT: RELEASE-INFO.txt Version field, SINGLE-SOURCE, named; sweep: no SoT exists, literals only; curated count: entry grammar under the eight headings; anchors: README Contents slugs). C4 met (curated entries marked by the CONTRIBUTING entry grammar: one line per entry, tags in sentence, year token last, under the eight section headings). C5 met (fail-list convention, validate.yml Python 3.12 setup and invocation line, lychee/P5 advisory boundary). C6 met (meta anchor mix, raw-line counting trap, badge URL-escaped text, GitHub slug forms).
- No criterion unmet; decision-bearing claims are CORROBORATED or SINGLE-SOURCE with the SoT named.

## Converged: Round 1

Track 1: Merged verdict CONTEXT_COMPLETE.
