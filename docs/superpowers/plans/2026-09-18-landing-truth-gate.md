# Landing Truth Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `scripts/check_release.py` exit 1 whenever the landing page's version, sweep, or entries chip, or its eight section-index anchors, disagrees with RELEASE-INFO.txt and README.md.

**Architecture:** Extend `scripts/check_release.py` in place with one contiguous module-level region inserted between the existing SPDX header scan and the `if scanned < 1:` line. Four small helpers (`read_source`, `landing_chip`, `curated_walk`, `github_slug`), two constants (`CURATED_SECTIONS`, `ENTRY_RX`), all new failures appended to the existing `fails` list. The existing print/exit block, success line, REQUIRED check, and SCAN_GLOBS stay untouched. validate.yml keeps its single `python scripts/check_release.py` call.

**Tech Stack:** Python 3.12 standard library only (pathlib, re, subprocess, sys). Verification runs the gate itself plus temporary in-tree mutations restored with `git checkout`.

**Spec:** docs/superpowers/specs/2026-09-18-landing-truth-gate.md

research: skipped (local file assertions only; no external API)

## Global Constraints

- Stdlib only. validate.yml has no pip install step; any import outside `pathlib`, `re`, `subprocess`, `sys` breaks CI (R8).
- validate.yml, links.yml, and every other workflow file are untouched. No new CI file, no requirements.txt (R8).
- Failure style unchanged: accumulate into `fails`, print `RELEASE GATE FAILED:` with indented `  - ` lines, `sys.exit(1)` (R7).
- Success line unchanged: `release gate: PASS (scanned {N} files)` with N the existing SCAN_GLOBS file count (R7).
- `CURATED_SECTIONS` is exactly, in order: `("Specifications and standards", "Certification", "The Archi tool", "Plugins and collaboration", "Books", "Example models", "TOGAF alignment", "Communities")`. Hardcoded on purpose (spec Design approach 5).
- Version compares against RELEASE-INFO.txt bare `Version:` field only, never `Tag:` (`v0.1.0`) (R1, R2).
- Sweep comes from the README badge alt text `Last full sweep: YYYY-MM`, never the shield URL path (`2026--09`) (R3).
- PR template change is limited to extending the existing version-bearing list with `docs/index.html` on one line (R9). The gate, not the template, is the enforcement.
- All commands run from the repo root in Git Bash; `python` is on PATH (validate.yml uses the same command).
- No em dash anywhere in the diff (repo rule, PR template). Commit messages follow the repo's plain conventional style.
- Zero-match or multi-match on any source regex (chip, Version field, sweep badge, section-index list) is a named fail, never first-match-wins (R6).

## Codebase context

From docs/superpowers/context/2026-09-18-landing-truth-gate-context.md (CONTEXT_COMPLETE):

- `scripts/check_release.py` is 62 lines, flat and procedural: REQUIRED file list, tracked-path scan, forbidden-content scan over `SCAN_GLOBS` (line 34, already includes `docs/**/*.html`), SPDX header scan, then the single `if fails:` print/exit block at lines 57-61. The insertion region for this plan is between the SPDX loop (ends line 52) and `if scanned < 1:` (line 54).
- `docs/index.html` lines 428-441 hold the three chips as `<dt>version</dt><dd>0.1.0</dd>`, `<dt>sweep</dt><dd>2026-09</dd>`, `<dt>entries</dt><dd>17</dd>` inside `dl.chips`. Lines 450-459 hold one `<ul class="section-index">` with eight `<li><a href="...README.md#slug">` items whose fragments already match the curated slugs in README heading order.
- RELEASE-INFO.txt line 2 is `Version: 0.1.0` (bare); line 4 is `Tag: v0.1.0`. README.md line 6 is the badge `![Last full sweep: 2026-09](https://img.shields.io/badge/last%20full%20sweep-2026--09-brightgreen)`.
- README curated bullets total 17: Specifications 3, Certification 2, The Archi tool 2, Plugins and collaboration 4, Books 1, Example models 3, TOGAF alignment 1, Communities 1. A naive `^- [` count reads 29 because the Contents TOC adds 12 link bullets; meta headings (Install, Usage, Support, Version, Contributing, Contents) are never counted. The Install section contains the README's only fenced code block (```bash, lines 80-82).
- GitHub slugs of the eight curated headings: `specifications-and-standards`, `certification`, `the-archi-tool`, `plugins-and-collaboration`, `books`, `example-models`, `togaf-alignment`, `communities`.
- CONTRIBUTING.md entry format (lines 28-36): `- [Name](https-url) - Description with inline-code tags (YYYY).` ending in a parenthesized year and a period.
- PR template line 26: `- [ ] If this changes version-bearing files (CHANGELOG.md, RELEASE-INFO.txt, CITATION.cff), they are updated together` (R9 target).

## File structure

- Modify: `scripts/check_release.py` (one growing region; ~85 added lines across Tasks 1-3)
- Modify: `.github/PULL_REQUEST_TEMPLATE.md` (one line, Task 4)
- No new files. No test files are committed; the mutation probes below are run in the working tree and reverted with `git checkout` before any commit.

## Acceptance coverage (R1-R10)

| Req | Covered by |
|---|---|
| R1 version chip | Task 1 (check + bump mutation) |
| R2 tag immunity | Task 1 (v0.1.0 chip mutation must fail) |
| R3 sweep chip | Task 1 (check + stale mutation + duplicate-badge probe) |
| R4 entries chip and curated count | Task 2 (walk, grammar fail, integer parse, meta immunity) |
| R5 section index and headings | Task 3 (li count, fragment order, heading presence, duplicate) |
| R6 fail-not-raise | Guards in Tasks 1-3 code; Task 4 (unreadable source, ambiguous chip probes) |
| R7 output style | Insertion point before print/exit; Task 4 (exact success-line check) |
| R8 one CI path, stdlib | Task 4 (import scan, workflow untouched) |
| R9 PR template one-liner | Task 4 |
| R10 mutation acceptance | Tasks 1-3 mutation steps; mapping re-checked in Task 4 |

## Mutation discipline

Every mutation below is temporary. Mutate, run the gate, observe the expected output, then restore with the exact `git checkout -- <file>` (or `mv` back) command given, and confirm `git status --porcelain` shows only the in-progress task files modified (typically `scripts/check_release.py`; after Task 4 Step 1 also `.github/PULL_REQUEST_TEMPLATE.md`) before moving on. Never commit a mutated tree. Each task's commit step runs only after all its restores are verified.

---

### Task 1: Version and sweep chip checks

**Files:**
- Modify: `scripts/check_release.py` (insert after the SPDX header scan block, before `if scanned < 1:`)

**Interfaces:**
- Consumes: existing `fails` list, `re`, `pathlib` (already imported).
- Produces: module-level helpers `read_source(path) -> str | None` and `landing_chip(html, name) -> str | None`; module-level source strings `release_info`, `readme`, `html` (each `str` or `None`). Tasks 2 and 3 reuse all of these.

**Model:** flash

- [ ] **Step 1: Record the pre-change baseline**

```bash
python --version
python scripts/check_release.py
echo "exit=$?"
git status --porcelain
```

Expected: Python 3.12.x; output exactly one line `release gate: PASS (scanned N files)`; exit=0. Write down N (it includes docs/superpowers markdown; that is fine, it must not change). Working tree clean apart from possibly untracked docs/superpowers files.

- [ ] **Step 2: Insert the Task 1 block**

In `scripts/check_release.py`, between the end of the SPDX header scan loop (`fails.append(f"SPDX missing: {path}")`) and the line `if scanned < 1:`, insert:

```python

# --- landing truth gate (P2): landing chips and section index vs sources ---

def read_source(path):
    try:
        return pathlib.Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        fails.append(f"unreadable source file: {path}")
        return None


def landing_chip(html, name):
    hits = re.findall(rf"<dt>{re.escape(name)}</dt>\s*<dd>([^<]*)</dd>", html)
    if len(hits) != 1:
        fails.append(f"landing chip missing or ambiguous: {name}")
        return None
    return hits[0].strip()


release_info = read_source("RELEASE-INFO.txt")
readme = read_source("README.md")
html = read_source("docs/index.html")

if release_info is not None:
    version_hits = re.findall(r"(?m)^Version: (\S+)\s*$", release_info)
    if len(version_hits) != 1:
        fails.append(
            f"RELEASE-INFO Version field missing or ambiguous: {len(version_hits)} matches"
        )
    else:
        chip_version = landing_chip(html, "version") if html is not None else None
        if chip_version is not None and chip_version != version_hits[0]:
            fails.append(
                f"landing version chip {chip_version} != RELEASE-INFO Version {version_hits[0]}"
            )

if readme is not None:
    sweep_hits = re.findall(r"!\[Last full sweep: (\d{4}-\d{2})\]", readme)
    if len(sweep_hits) != 1:
        fails.append(f"README sweep badge missing or ambiguous: {len(sweep_hits)} matches")
    else:
        chip_sweep = landing_chip(html, "sweep") if html is not None else None
        if chip_sweep is not None and chip_sweep != sweep_hits[0]:
            fails.append(
                f"landing sweep chip {chip_sweep} != README sweep badge {sweep_hits[0]}"
            )
```

Note the version regex: the `(?m)^Version: ` prefix cannot match the `Tag:` line, and the trailing `\s*` absorbs a Windows CR, which is why this is the only multiline `$` use. Sweep parses the alt-text bracket only; the shield URL inside `(...)` never matches.

- [ ] **Step 3: Clean run passes**

```bash
python scripts/check_release.py
echo "exit=$?"
```

Expected: `release gate: PASS (scanned N files)` with the same N as Step 1; exit=0.

- [ ] **Step 4: Mutation R10a, bump version chip**

```bash
sed -i 's|<dd>0.1.0</dd>|<dd>0.2.0</dd>|' docs/index.html
python scripts/check_release.py
echo "exit=$?"
```

Expected: `RELEASE GATE FAILED:` containing the line `  - landing version chip 0.2.0 != RELEASE-INFO Version 0.1.0`; exit=1; no Traceback.

- [ ] **Step 5: Restore**

```bash
git checkout -- docs/index.html
git status --porcelain
```

Expected: only in-progress task files modified (e.g. `scripts/check_release.py`); mutated source files restored.

- [ ] **Step 6: Mutation R2, tag-shaped chip must fail**

```bash
sed -i 's|<dd>0.1.0</dd>|<dd>v0.1.0</dd>|' docs/index.html
python scripts/check_release.py
echo "exit=$?"
```

Expected: fail line `  - landing version chip v0.1.0 != RELEASE-INFO Version 0.1.0`; exit=1. If the gate wrongly compared against `Tag:`, the chip `v0.1.0` would match and the run would pass, so this failing proves the Tag line is never read.

- [ ] **Step 7: Restore**

```bash
git checkout -- docs/index.html
git status --porcelain
```

- [ ] **Step 8: Mutation R10b, stale sweep chip**

```bash
sed -i 's|<dd>2026-09</dd>|<dd>2026-08</dd>|' docs/index.html
python scripts/check_release.py
echo "exit=$?"
```

Expected: fail line `  - landing sweep chip 2026-08 != README sweep badge 2026-09`; exit=1.

- [ ] **Step 9: Restore**

```bash
git checkout -- docs/index.html
git status --porcelain
```

- [ ] **Step 10: Probe R3, ambiguous sweep source**

```bash
sed -i '6a ![Last full sweep: 2026-09](https://img.shields.io/badge/last%20full%20sweep-2026--09-brightgreen)' README.md
python scripts/check_release.py
echo "exit=$?"
```

Expected: fail line `  - README sweep badge missing or ambiguous: 2 matches`; exit=1.

- [ ] **Step 11: Restore**

```bash
git checkout -- README.md
git status --porcelain
```

- [ ] **Step 12: Commit**

```bash
git add scripts/check_release.py
git commit -m "feat: gate landing version and sweep chips against sources"
```

---

### Task 2: Curated entry count and entries chip check

**Files:**
- Modify: `scripts/check_release.py` (insert immediately after the Task 1 block, still before `if scanned < 1:`)

**Interfaces:**
- Consumes: `fails`, `re`, `readme`, `html` from Task 1; `landing_chip`.
- Produces: `CURATED_SECTIONS` (module-level tuple), `ENTRY_RX` (compiled pattern), `curated_walk(readme) -> tuple[int, dict[str, int]]` (count, exact-`## ` heading hit tally keyed by curated title), and module-level `curated_count: int | None` and `heading_hits: dict[str, int]`. Task 3 consumes `heading_hits` and `CURATED_SECTIONS`.

**Model:** flash

- [ ] **Step 1: Insert the Task 2 block**

Immediately after the sweep check added in Task 1, before `if scanned < 1:`, insert:

```python

CURATED_SECTIONS = (
    "Specifications and standards", "Certification", "The Archi tool",
    "Plugins and collaboration", "Books", "Example models", "TOGAF alignment",
    "Communities",
)
ENTRY_RX = re.compile(r"^- \[[^\]]+\]\(https?://[^)\s]+\)\s+-\s+.+\(\d{4}\)\.$")


def curated_walk(readme):
    """Count grammar-valid bullets under curated headings and tally exact ## hits."""
    count = 0
    heading_hits = {title: 0 for title in CURATED_SECTIONS}
    current = None
    in_fence = False
    for raw in readme.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        stripped = line.strip()
        if stripped.startswith("## ") and not stripped.startswith("###"):
            # Exact presence uses stripped == "## " + title for curated titles only
            current = stripped[3:].strip()
            if stripped == "## " + current and current in heading_hits:
                heading_hits[current] += 1
            continue
        if current in heading_hits and line and re.match(r"^[-*] \[", line):
            probe = "- " + line[2:] if line.startswith("* ") else line
            if ENTRY_RX.match(probe):
                count += 1
            else:
                fails.append(f"curated entry malformed in {current}: {line[:60]}")
    return count, heading_hits


curated_count = None
heading_hits = {}
if readme is not None:
    curated_count, heading_hits = curated_walk(readme)

chip_entries = landing_chip(html, "entries") if html is not None else None
if chip_entries is not None:
    if not re.fullmatch(r"[0-9]+", chip_entries):
        fails.append(f"landing entries chip not an integer: {chip_entries}")
    elif curated_count is not None and int(chip_entries) != curated_count:
        fails.append(f"landing entries chip {chip_entries} != curated count {curated_count}")
```

Design notes baked in: `splitlines()` handles CRLF so no multiline `$` anchor is used here; the Contents TOC is skipped because Contents is not in `CURATED_SECTIONS`; the Install ```bash fence is toggled out; a bullet under a curated heading that breaks the grammar fails by name and does not increment the count; `[0-9]+` (not `\d`) rejects signs, underscores, and non-ASCII digits.

- [ ] **Step 2: Clean run passes with count 17**

```bash
python scripts/check_release.py
echo "exit=$?"
```

Expected: `release gate: PASS (scanned N files)`, same N; exit=0. If this fails with an entries mismatch or a malformed-entry line, the walk or grammar is wrong: fix before continuing. The current 17 curated bullets all satisfy `ENTRY_RX`.

- [ ] **Step 3: Mutation R10c, entries chip 16**

```bash
sed -i 's|<dd>17</dd>|<dd>16</dd>|' docs/index.html
python scripts/check_release.py
echo "exit=$?"
```

Expected: fail line `  - landing entries chip 16 != curated count 17`; exit=1.

- [ ] **Step 4: Restore**

```bash
git checkout -- docs/index.html
git status --porcelain
```

- [ ] **Step 5: Mutation R10d, valid 18th curated bullet, chip untouched**

```bash
python - <<'PY'
from pathlib import Path
p = Path("README.md")
t = p.read_text(encoding="utf-8")
anchor = "- [Archi forum](https://forum.archimatetool.com/)"
i = t.index(anchor)
j = t.index("\n", i)
row = "\n- [Mutation forum](https://example.com/forum) - Temporary mutation row for gate verification `ArchiMate-general` `Archi` `community` (2026)."
p.write_text(t[:j] + row + t[j:], encoding="utf-8", newline="")
PY
python scripts/check_release.py
echo "exit=$?"
```

Expected: fail line `  - landing entries chip 17 != curated count 18`; exit=1. The inserted row is grammar-valid, so no malformed-entry line appears.

- [ ] **Step 6: Restore**

```bash
git checkout -- README.md
git status --porcelain
```

- [ ] **Step 7: Probe R4, malformed curated bullet fails by name and changes nothing**

```bash
python - <<'PY'
from pathlib import Path
p = Path("README.md")
t = p.read_text(encoding="utf-8")
anchor = "- [ArchiMate Certification](https://www.opengroup.org/certifications/archimate)"
i = t.index(anchor)
j = t.index("\n", i)
row = "\n- [Broken row] - missing url and year"
p.write_text(t[:j] + row + t[j:], encoding="utf-8", newline="")
PY
python scripts/check_release.py
echo "exit=$?"
```

Expected: exactly one new fail line, `  - curated entry malformed in Certification: - [Broken row] - missing url and year`; exit=1. No entries-chip line: the malformed bullet does not increment the count, so chip 17 still equals count 17.

- [ ] **Step 8: Restore**

```bash
git checkout -- README.md
git status --porcelain
```

- [ ] **Step 9: Probe R4, non-integer chip is a named fail, not a traceback**

```bash
sed -i 's|<dd>17</dd>|<dd>about 17</dd>|' docs/index.html
python scripts/check_release.py
echo "exit=$?"
```

Expected: fail line `  - landing entries chip not an integer: about 17`; exit=1; no Traceback.

- [ ] **Step 10: Restore**

```bash
git checkout -- docs/index.html
git status --porcelain
```

- [ ] **Step 11: Probe R4, meta-section bullet is invisible to the count**

```bash
python - <<'PY'
from pathlib import Path
p = Path("README.md")
t = p.read_text(encoding="utf-8")
anchor = "- Bug or dead link:"
i = t.index(anchor)
j = t.index("\n", i)
row = "\n- [Fake support](https://example.com) - Temporary meta-section row `ArchiMate-general` `community` (2026)."
p.write_text(t[:j] + row + t[j:], encoding="utf-8", newline="")
PY
python scripts/check_release.py
echo "exit=$?"
```

Expected: `release gate: PASS (scanned N files)`; exit=0. Support is not curated, so the bullet neither counts nor fails.

- [ ] **Step 12: Restore**

```bash
git checkout -- README.md
git status --porcelain
```

- [ ] **Step 13: Commit**

```bash
git add scripts/check_release.py
git commit -m "feat: gate landing entries chip against curated README count"
```

---

### Task 3: Section index and curated heading checks

**Files:**
- Modify: `scripts/check_release.py` (insert immediately after the Task 2 block, still before `if scanned < 1:`)

**Interfaces:**
- Consumes: `fails`, `re`, `html`, `heading_hits`, `CURATED_SECTIONS` from Tasks 1-2.
- Produces: `github_slug(title) -> str`. Nothing later consumes it; this task completes the gate.

**Model:** flash

- [ ] **Step 1: Insert the Task 3 block**

Immediately after the entries-chip check added in Task 2, before `if scanned < 1:`, insert:

```python

def github_slug(title):
    return re.sub(r"[^\w\s-]", "", title.lower()).strip().replace(" ", "-")


for title, hits in heading_hits.items():
    if hits == 0:
        fails.append(f"curated heading missing from README: {title}")
    elif hits > 1:
        fails.append(f"curated heading duplicated in README ({hits}x): {title}")

if html is not None:
    blocks = re.findall(r'<ul class="section-index">(.*?)</ul>', html, re.DOTALL)
    if len(blocks) != 1:
        fails.append(f"landing section-index list missing or ambiguous: {len(blocks)} found")
    else:
        lis = re.findall(r"<li\b[^>]*>.*?</li>", blocks[0], re.DOTALL)
        if len(lis) != 8:
            fails.append(f"section-index li count {len(lis)} != 8")
        else:
            fragments = []
            for li in lis:
                hrefs = re.findall(r'href="[^"#]*#([^"]+)"', li)
                if len(hrefs) != 1:
                    fails.append(f"section-index li href missing or ambiguous: {li[:60]}")
                    fragments = None
                    break
                fragments.append(hrefs[0])
            if fragments is not None:
                expected = [github_slug(t) for t in CURATED_SECTIONS]
                for got, want in zip(fragments, expected):
                    if got != want:
                        fails.append(f"section-index fragment mismatch: {got} != {want}")
```

Design notes baked in: fragments compare as an ordered list against the `CURATED_SECTIONS` tuple order (not a set, not README document order); the expected slugs come from the tuple, so a README-only rename cannot hide; the heading check requires exact stripped-line equality `## <title>`, counted outside fences.

- [ ] **Step 2: Clean run passes**

```bash
python scripts/check_release.py
echo "exit=$?"
```

Expected: `release gate: PASS (scanned N files)`, same N; exit=0.

- [ ] **Step 3: Mutation R10e, delete one section-index li**

```bash
python - <<'PY'
from pathlib import Path
p = Path("docs/index.html")
t = p.read_text(encoding="utf-8")
i = t.index('<li><a href="https://github.com/jgsystemsconsulting/awesome-archimate/blob/main/README.md#books">')
j = t.index("</li>", i) + len("</li>")
end = j + 1 if t[j:j + 1] == "\n" else j
p.write_text(t[:i] + t[end:], encoding="utf-8", newline="")
PY
python scripts/check_release.py
echo "exit=$?"
```

Expected: fail line `  - section-index li count 7 != 8`; exit=1.

- [ ] **Step 4: Restore**

```bash
git checkout -- docs/index.html
git status --porcelain
```

- [ ] **Step 5: Mutation R10f, alter one fragment by one character**

```bash
sed -i 's|README.md#books">|README.md#book">|' docs/index.html
python scripts/check_release.py
echo "exit=$?"
```

Expected: fail line `  - section-index fragment mismatch: book != books`; exit=1. Only that one line: the other seven fragments still match.

- [ ] **Step 6: Restore**

```bash
git checkout -- docs/index.html
git status --porcelain
```

- [ ] **Step 7: Mutation R10g, rename a curated heading in README only**

```bash
sed -i 's|## Communities|## Community|' README.md
python scripts/check_release.py
echo "exit=$?"
```

Expected: exit=1 with both fail lines (order as implemented):

```text
  - landing entries chip 17 != curated count 16
  - curated heading missing from README: Communities
```

The entries line appears because the renamed section drops its bullet from the curated count. No fragment-mismatch line: the landing fragments and the tuple still agree, which is exactly the point of tuple-driven expectations.

- [ ] **Step 8: Restore**

```bash
git checkout -- README.md
git status --porcelain
```

- [ ] **Step 9: Probe R5, duplicate curated heading**

```bash
python - <<'PY'
from pathlib import Path
p = Path("README.md")
t = p.read_text(encoding="utf-8")
i = t.index("## Books")
j = t.index("\n", i)
p.write_text(t[:j + 1] + "## Books\n" + t[j + 1:], encoding="utf-8", newline="")
PY
python scripts/check_release.py
echo "exit=$?"
```

Expected: fail line `  - curated heading duplicated in README (2x): Books`; exit=1.

- [ ] **Step 10: Restore**

```bash
git checkout -- README.md
git status --porcelain
```

- [ ] **Step 11: Commit**

```bash
git add scripts/check_release.py
git commit -m "feat: gate landing section index against curated README slugs"
```

---

### Task 4: Acceptance sweep, R9 template line, final verification

**Files:**
- Modify: `.github/PULL_REQUEST_TEMPLATE.md` (line 26, one line)
- Verify only: `scripts/check_release.py`, `.github/workflows/validate.yml`

**Interfaces:**
- Consumes: the completed gate from Tasks 1-3.
- Produces: nothing; this is the acceptance gate.

**Model:** flash

- [ ] **Step 1: R9, extend the version-bearing list in the PR template**

Find the line containing `version-bearing files` (currently line 26):

```bash
grep -n "version-bearing files" .github/PULL_REQUEST_TEMPLATE.md
```

Change exactly that line from:

```markdown
- [ ] If this changes version-bearing files (CHANGELOG.md, RELEASE-INFO.txt, CITATION.cff), they are updated together
```

to:

```markdown
- [ ] If this changes version-bearing files (CHANGELOG.md, RELEASE-INFO.txt, CITATION.cff, docs/index.html), they are updated together
```

```bash
sed -i 's|(CHANGELOG.md, RELEASE-INFO.txt, CITATION.cff)|(CHANGELOG.md, RELEASE-INFO.txt, CITATION.cff, docs/index.html)|' .github/PULL_REQUEST_TEMPLATE.md
git diff --stat
```

Expected: a one-line change in `.github/PULL_REQUEST_TEMPLATE.md` only. This fits R9's two-line bar, so it ships; if it had grown beyond that, the instruction is to skip and note the skip in the PR description.

- [ ] **Step 2: R7, clean run, exact success line**

```bash
python scripts/check_release.py
echo "exit=$?"
```

Expected: output is exactly one line, `release gate: PASS (scanned N files)`, where N equals the Task 1 Step 1 baseline number; exit=0.

- [ ] **Step 3: Probe R6, ambiguous chip is a named fail**

```bash
python - <<'PY'
from pathlib import Path
p = Path("docs/index.html")
t = p.read_text(encoding="utf-8")
i = t.index("<dt>entries</dt>")
j = t.index("</dd>", i) + len("</dd>")
block = t[t.rindex('<div class="chip">', 0, i):j]
p.write_text(t[:j] + "\n          " + block + t[j:], encoding="utf-8", newline="")
PY
python scripts/check_release.py
echo "exit=$?"
```

Expected: fail line `  - landing chip missing or ambiguous: entries`; exit=1; no Traceback.

- [ ] **Step 4: Restore**

```bash
git checkout -- docs/index.html
git status --porcelain
```

- [ ] **Step 5: Probe R6, unreadable source is a named fail**

```bash
mv RELEASE-INFO.txt RELEASE-INFO.txt.hold
python scripts/check_release.py
echo "exit=$?"
mv RELEASE-INFO.txt.hold RELEASE-INFO.txt
git status --porcelain
```

Expected while the file is moved: exit=1 with fail lines including `  - required file missing: RELEASE-INFO.txt` and `  - unreadable source file: RELEASE-INFO.txt`, and no Traceback anywhere in the output. After the `mv` back: mutated file restored; only in-progress task files still modified.

- [ ] **Step 6: R8, stdlib and single-CI-path checks**

```bash
grep -E '^(import|from) ' scripts/check_release.py
ls requirements.txt 2>/dev/null
git log --oneline -3 -- .github/workflows/
python scripts/check_release.py >/dev/null; echo "exit=$?"
```

Expected: imports are exactly `pathlib`, `re`, `subprocess`, `sys` (nothing outside the standard library); no requirements.txt printed; no new commits under `.github/workflows/` from this branch's work; exit=0.

- [ ] **Step 7: R10 completeness re-check**

Confirm all seven mutations were exercised and each produced exit 1 with a named fail line:

| R10 mutation | Task/step |
|---|---|
| bump version chip | Task 1, Step 4 |
| stale sweep chip | Task 1, Step 8 |
| entries chip 16 | Task 2, Step 3 |
| valid 18th bullet, chip untouched | Task 2, Step 5 |
| delete one section-index li | Task 3, Step 3 |
| fragment one-character change | Task 3, Step 5 |
| rename curated README heading | Task 3, Step 7 |

If any row is missing from the executed history, run that step now before committing.

- [ ] **Step 8: Commit**

```bash
git add .github/PULL_REQUEST_TEMPLATE.md
git commit -m "docs: list docs/index.html as version-bearing in PR template"
git status --porcelain
git log --oneline -5
```

Expected: clean tree (untracked docs/superpowers files allowed); four commits from this plan on top of the starting HEAD.

---

## Self-review record

- Spec coverage: R1-R10 each map to a task step in the table above; nothing in Requirements, Non-goals, or Edge cases is unassigned. Non-goals respected: no visitor copy edits, no lychee or links.yml work, no workflow change, no entry mirroring, no tag-vocabulary or 140-char enforcement, no README Version section, CITATION.cff, or CHANGELOG reads.
- Placeholder scan: every code step contains the full code; every verification step contains the exact command and expected output. Nothing is deferred and no step says "add this later".
- Type and name consistency: `read_source`, `landing_chip`, `curated_walk`, `github_slug`, `CURATED_SECTIONS`, `ENTRY_RX`, `release_info`, `readme`, `html`, `curated_count`, `heading_hits` are each defined once (Tasks 1-2) and used with the same names afterwards.
