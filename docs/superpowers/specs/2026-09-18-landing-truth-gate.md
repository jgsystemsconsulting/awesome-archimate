# Spec: landing-truth-gate (package P2)

Date: 2026-09-18
Package: P2 of the package-loop cut
Status: drafted (Superpowers step 1)

## Problem

The landing page (docs/index.html) states three facts about the list: version (0.1.0), sweep month (2026-09), and curated entry count (17). It also links eight README section anchors. All four are hand-written. None is checked anywhere. scripts/check_release.py only confirms docs/index.html exists; its only HTML content scan is the private-key regex. A maintainer can bump RELEASE-INFO.txt, add a curated row, or rename a section and leave the landing stale, and CI stays green. The landing then misstates the release.

## Goals

1. scripts/check_release.py fails (exit 1) whenever any landing chip disagrees with its source of truth.
2. scripts/check_release.py fails whenever a section-index anchor fragment is not the GitHub slug of its README section heading, or the anchor set drifts from the eight curated sections.
3. The gate extends the existing script and runs through the existing validate.yml step. One CI path, no new workflow.
4. Failure output keeps the established shape: accumulate into `fails`, print `RELEASE GATE FAILED:` with indented `- ` lines, `sys.exit(1)`.

## Non-goals

- P1 visitor copy changes on the landing.
- P5 lychee arguments, links.yml changes, or any PR-blocking link policy. Lychee stays README-only advisory.
- P3 org catalogue and P4 awesome assessment.
- P6 setup-python version pin.
- Path N Next.
- Mirroring entry rows onto the landing. The landing links sections; it does not copy rows.
- README inclusion-bar content changes.
- Full entry-grammar enforcement (tag vocabulary, cardinality, 140-char limit). The gate checks only the shape it needs to count rows unambiguously.
- Checking the README `## Version` section, CITATION.cff, or CHANGELOG mirrors. RELEASE-INFO.txt `Version:` is the only version source this gate reads.
- Any PR template change beyond an optional one-line hygiene note if it costs nothing (see Requirements R9).

## Codebase context

From docs/superpowers/context/2026-09-18-landing-truth-gate-context.md (CONTEXT_COMPLETE, round 1; context log graded 12 claims, synthesis lists 11 findings):

- scripts/check_release.py (62 lines, stdlib only) builds a `REQUIRED` file list, scans tracked paths and globs (`SCAN_GLOBS`, line 34, already includes `docs/**/*.html`), and reports through a single `fails` list, `RELEASE GATE FAILED:` header, `sys.exit(1)`. validate.yml calls it as `python scripts/check_release.py` on Python 3.12 with no install step, so the script must stay stdlib-only.
- docs/index.html lines 428-441 hold the three chips as `<dt>version</dt><dd>0.1.0</dd>`, `<dt>sweep</dt><dd>2026-09</dd>`, `<dt>entries</dt><dd>17</dd>` inside `dl.chips`. Lines 450-459 hold the eight section-index `<li><a href="...README.md#slug">` items.
- Version source of truth: RELEASE-INFO.txt line 2, `Version: 0.1.0` (bare form). Line 4 is `Tag: v0.1.0`. The chip must never be compared to the Tag field.
- Sweep source of truth: README.md line 6 badge alt text, `![Last full sweep: 2026-09](https://img.shields.io/badge/last%20full%20sweep-2026--09-brightgreen)`. The shield URL path double-escapes the hyphen (`2026--09`), so the alt text is the parse target, not the URL. No machine source for sweep exists today.
- Entry count source of truth: bullets under the eight curated `##` headings only (Specifications and standards, Certification, The Archi tool, Plugins and collaboration, Books, Example models, TOGAF alignment, Communities) that match the count grammar (a CONTRIBUTING.md entry-shape subset: link, hyphen separator, description, year-last). Today that count is 17. A naive `^- [` count reads 29 because the Contents TOC contributes 12 link bullets (8 curated anchors plus 4 meta anchors).
- Section-index source of truth: the eight curated `##` headings in README.md, slugified the way GitHub does. Contents also lists Install, Usage, Support, Version, and README carries a Contributing heading outside Contents; none of these is a landing target.
- GitHub slugs of the eight headings: specifications-and-standards, certification, the-archi-tool, plugins-and-collaboration, books, example-models, togaf-alignment, communities. The landing hrefs already match, in README heading order.

## Requirements / acceptance criteria

All criteria are testable by running `python scripts/check_release.py` from the repo root on Python 3.12 with no third-party packages installed.

R1. Version chip check. The gate parses RELEASE-INFO.txt for the `Version:` field (regex anchored so it cannot match `Tag:`), parses the landing `<dt>version</dt>` chip `<dd>` text (stripped), and appends a fail when they differ. Given the current tree, the gate exits 0. Changing the chip `<dd>` to any other value produces a fail line naming both values, and exit 1.

R2. Tag immunity. Setting the version chip to `v0.1.0` while RELEASE-INFO.txt still says `Version: 0.1.0` fails. The gate never reads the `Tag:` line.

R3. Sweep chip check. The gate parses README.md for exactly one badge alt of the form `Last full sweep: YYYY-MM`, parses the landing `<dt>sweep</dt>` chip `<dd>`, and fails on mismatch or on a missing/ambiguous (zero or multiple) source match on either side. The shield URL (with `2026--09`) is not parsed.

R4. Entries chip check. The gate counts curated bullets in README.md under the eight curated `##` headings. Under a curated heading, every non-blank, non-heading line that looks like a list item (after optional leading whitespace, starts with `- ` or `* ` followed by `[`) must match the count grammar defined in the Design approach or the gate appends a fail naming the section and the first 60 characters of the line. Only grammar-valid lines increment the count. The landing `<dt>entries</dt>` chip text, after strip, must match `re.fullmatch(r"[0-9]+", text)` then `int(text)`; anything else (signs, underscores, non-ASCII digits, empty) appends a named fail (no traceback). The gate fails when the integer differs from the curated count. List items under meta sections (Install, Usage, Support, Version, Contributing, Contents) neither change the expected count nor fail the gate.

R5. Section-index check. Expected fragments are the GitHub slugs of the eight titles in the module-level `CURATED_SECTIONS` tuple, in tuple order (not README document order). The gate requires exactly one `<ul class="section-index">` block in the landing HTML (zero or multiple is a fail). Inside that block it requires exactly eight `<li>` children; each `<li>` must contain exactly one `<a href="...#fragment">`. It fails when the ordered fragments do not equal the eight expected slugs, or when any title in `CURATED_SECTIONS` lacks an exact `## <title>` line in README (stripped line equality `## ` + title, not prefix match). Duplicate exact `## <title>` lines for the same curated title are a fail.

R6. Missing or unparseable landing structures (no chip match, ambiguous chip match, no or multiple section-index lists, non-integer entries chip, unreadable source files after REQUIRED passed) produce explicit fail lines appended to `fails`, not a Python traceback. The script never raises past its own failure collection for these inputs.

R7. Style preservation. New failures are appended to the existing `fails` list before the existing print/exit block. The output format `RELEASE GATE FAILED:` plus indented `- ` lines and `sys.exit(1)` is unchanged. On a clean tree the success line still prints exactly: `release gate: PASS (scanned {N} files)` with N the existing SCAN_GLOBS count.

R8. validate.yml is untouched. No second workflow, no new CI file, no requirements.txt. The script remains import-free of anything outside the standard library.

R9. Optional, only if trivial: add `docs/index.html` to the version-bearing file list in .github/PULL_REQUEST_TEMPLATE.md so the write path is visible to contributors. If it is not a two-line edit, skip it and note the skip in the PR description. The gate, not the template, is the enforcement.

R10. Mutation acceptance (for the verification step, not committed): each of these alone must produce exit 1 with a named fail line: bump the version chip; set the sweep chip to a stale month; change the entries chip to 16; append a valid 18th curated bullet without touching the chip; delete one section-index `<li>`; alter one fragment by one character; rename a curated `##` heading in README only.

## Design approach

Extend scripts/check_release.py in place, after the forbidden-content scan and before the `if fails:` block. Keep the script's flat, procedural style. Two small helpers, no classes, no config.

1. Source reads. Read README.md, RELEASE-INFO.txt, docs/index.html once each with `pathlib.Path(...).read_text(encoding="utf-8")`. Wrap each read: a missing file is already covered by the REQUIRED check, but a read error here should append a fail and skip the dependent checks rather than crash.

2. Chip extraction helper. One function, `landing_chip(html, name)`, using `re.findall(rf"<dt>{name}</dt>\s*<dd>([^<]*)</dd>", html)`. Exactly one match is required; zero or more than one appends `landing chip missing or ambiguous: <name>`. Strip the captured text before comparing.

3. Version source. Prefer splitlines walk: for each `line.strip()`, if it starts with `Version: ` take the remainder stripped as the value. Collect all such values; require exactly one. Equivalent: `re.findall(r"(?m)^Version: (\S+)\s*$", release_info)` (the trailing `\s*` absorbs a Windows CR so this is the one allowed multiline `$` use). The literal `Version:` prefix cannot match the `Tag:` line. Zero or multiple is a fail.

4. Sweep source. `re.findall(r"!\[Last full sweep: (\d{4}-\d{2})\]", readme)`. This matches the alt text only; the shield URL path is inside `(...)` and never matches the bracket group. Exactly one match required.

5. Curated sections. A module-level ordered tuple `CURATED_SECTIONS` is exactly these eight titles in this order: `("Specifications and standards", "Certification", "The Archi tool", "Plugins and collaboration", "Books", "Example models", "TOGAF alignment", "Communities")`. Hardcoded on purpose: it is the contract between README, landing, and gate, and a rename should fail loudly until all three move. Expected section-index order is this tuple order.

6. Slug helper. GitHub slug rule: lowercase; drop characters other than word characters, spaces, and hyphens; replace spaces with hyphens. Implemented with two `re` calls, roughly `re.sub(r"[^\w\s-]", "", title.lower()).strip().replace(" ", "-")`. Every current title is plain words, so this is exact for the known set and conservative for future ones.

7. Entry count. Walk `readme.splitlines()`. Maintain a fence flag: a line whose stripped form starts with triple backticks toggles in/out of a fenced code block; while inside a fence, ignore heading and bullet rules. Outside fences, track the most recent top-level heading: a line whose stripped form matches `## ` + title but not `###` (title extract = `line.lstrip()[3:].strip()` when the stripped line starts with `## ` and not `###`). Current section is curated when that title is in `CURATED_SECTIONS`. Inside a curated section, any non-blank non-heading line that after optional leading whitespace matches `^[-*] \[` is a list item under scrutiny: apply count grammar to the fully stripped line (`line.strip()`), fail if it does not match, else increment. Count grammar: `^- \[[^\]]+\]\(https?://[^)\s]+\)\s+-\s+.+\(\d{4}\)\.$` after normalizing a leading `* ` to `- ` for the check only (or accept both markers in the pattern). Tag vocabulary and the 140-character limit stay out. The sum is the expected entries value.

   Using `splitlines()` with strip helpers sidesteps the `\r\n` pitfall that a `(?m)...$` regex would hit on Windows checkouts.

8. Section index. `blocks = re.findall(r'<ul class="section-index">(.*?)</ul>', html, re.DOTALL)`; require `len(blocks) == 1`. In that block, `lis = re.findall(r'<li\b[^>]*>.*?</li>', block, re.DOTALL)` (or equivalent non-greedy li parse); require `len(lis) == 8`. For each li, require exactly one `href` with a `#fragment` and collect fragments in order. Compare the eight fragments to `[slug(t) for t in CURATED_SECTIONS]`. Separately, for each title in `CURATED_SECTIONS`, count README lines outside fenced code blocks (same fence toggle as step 7) where `line.strip() == "## " + title`; require count exactly 1.

9. Failure messages follow the existing lowercase, file-scoped voice, e.g. `landing version chip 0.2.0 != RELEASE-INFO Version 0.1.0`, `landing entries chip 16 != curated count 17`, `section-index fragment mismatch: <slug> != <expected>`, `curated heading missing from README: <title>`.

Rough size: about 60-80 added lines, no new dependencies, validate.yml untouched.

## Edge cases and gotchas

From context C6 and the reads above; the implementer bakes each of these in:

- Never count all `^- [` lines: 29 today, because the Contents TOC contributes 12. Scope by current `##` heading.
- Never compare the version chip to the `Tag:` field (`v0.1.0`). Bare `Version:` only.
- Sweep comes from the badge alt text (`2026-09`), never the shield URL path (`2026--09`, double hyphen).
- Contributing, Install, Usage, Support, and Version are meta headings: no anchors expected, no bullets counted. Contributing is not even in Contents.
- Contents TOC lines are themselves `- [` bullets in the Contents section; the heading-scope walk skips them because Contents is not a curated section.
- A bullet under a curated heading that breaks the grammar must fail, not just be excluded from the count, or a malformed row could silently change the total.
- Zero-match or multi-match on any source regex (chip, Version field, sweep badge, section-index list) is a fail with a named message. Silent first-match-wins hides duplication.
- Exactly one section-index list, exactly eight `<li>` children, ordered fragments equal to `CURATED_SECTIONS` slugs in tuple order (not a set compare; not README document order if it ever diverges).
- Entries chip integer parse is fail-not-raise: non-integer text is a named fail.
- List markers under curated headings: both `- [` and `* [` (with optional indent) are scrutinized; neither escapes.
- Heading extract and presence use exact `## <title>` line equality; fenced code blocks are skipped.
- Stdlib only. validate.yml has no pip install step; adding a dependency would break CI.
- CRLF: parse via `splitlines()` plus `rstrip()`, not multiline `$` anchors, so a Windows checkout does not produce phantom failures.
- Future section rename: the maintainer must move README heading plus TOC, landing section-index, and `CURATED_SECTIONS` together. The gate fails on any partial move; that is intended friction.
- Known labels: chip and anchor display text is not gated. Fragments and numbers are truth; wording is P1 territory.

## Research

research: skipped (local file assertions only; no external API)
