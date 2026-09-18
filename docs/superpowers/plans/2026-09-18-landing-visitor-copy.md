# Landing Visitor Copy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite the landing copy in `docs/index.html` from maintainer shorthand to visitor language, and fix four chrome defects (missing favicon, missing font preloads, sub-44px nav touch targets, dead IE shim) in the same file.

**Architecture:** Single-file edit, no build step, no new tracked assets by default. Seven exact string replacements from the spec Decisions table, three new `<head>` lines, one CSS rule replacement, one CSS rule deletion. `scripts/check_release.py` is the truth gate after every task; the markup it greps (evidence chips and the section index) is never touched.

**Tech Stack:** Static HTML with inline CSS, self-hosted IBM Plex woff2 fonts, Python 3 gate script, Git Bash grep.

**Spec:** `docs/superpowers/specs/2026-09-18-landing-visitor-copy.md`

**Research:** skipped (local copy and chrome only; no external API)

research: skipped (local copy and chrome only; no external API)

**Baseline:** HEAD `b93a41e`, P2 merged, gate green. Line numbers cited below are HEAD line numbers. Task 2 Step 1 inserts three lines in `<head>`, which shifts later line numbers, so anchor every edit on the exact strings shown, never on line numbers.

## Global Constraints

- Gate inputs are frozen: chip `dt` names `version`, `sweep`, `entries`; `dd` values `0.1.0`, `2026-09`, `17`; exactly one `ul.section-index`; exactly 8 `li`; all 8 href fragments (`specifications-and-standards`, `certification`, `the-archi-tool`, `plugins-and-collaboration`, `books`, `example-models`, `togaf-alignment`, `communities`).
- Section-index link display text and class stay unchanged.
- Nav labels `Sections`, `Curation`, `Contribute` and all hero claim/support prose stay unchanged; the optional hero claim-plus-support merge is skipped per lock.
- Keep `id="hero"`, `id="evidence"`, `id="evidence-heading"`, `aria-labelledby="evidence-heading"`, and every href unchanged.
- No CDN fonts; `@font-face` src URLs keep pointing at `fonts/*.woff2` relative to `docs/`.
- No design-token, spacing-scale, or color changes beyond the nav padding edit in Task 2.
- No em dashes in any copy string.
- `python scripts/check_release.py` must PASS after every task.
- Only `docs/index.html` changes by default; the Task 2 fallback route may add one `docs/favicon.svg`.

## Codebase context

`docs/index.html` (493 lines at HEAD) is the whole page: copy, one inline `<style>` block, and four self-hosted `@font-face` rules pointing at `docs/fonts/IBMPlexSans-Regular.woff2`, `IBMPlexSans-Medium.woff2`, `IBMPlexSans-SemiBold.woff2`, and `IBMPlexMono-Regular.woff2` (vendored, OFL). `scripts/check_release.py` regexes the evidence chips (`<dt>version|sweep|entries</dt>` with exact `<dd>` values `0.1.0`, `2026-09`, `17`) and the `ul.section-index` block (exactly one list, 8 `li`, one href each, fragment equals the GitHub slug of the eight curated section titles). None of the strings this plan edits is gate input; the greps in each task prove it. Run all commands from the repo root: `C:/Users/gower/OneDrive/Documents/GitHub/awesome-archimate`. A no-match `grep` exits 1 in bash; for the expect-no-output checks that exit code is the pass condition, not a failure.

---

### Task 1: Visitor copy replacements

**Files:**
- Modify: `docs/index.html:406-407` (nav labels), `:411` (nav full-list link), `:421` (hero CTA), `:427` (Evidence heading), `:442` (family paragraph), `:449` (sections intro)

**Interfaces:**
- Consumes: nothing; first task on a clean `b93a41e` tree.
- Produces: nav links labeled `Top` and `Status`; both full-list links labeled `Open full list`; `<h2>` reading `Status`; one-sentence family paragraph; two-sentence sections intro. Task 3's grep battery depends on these exact strings.

**Model:** flash

- [ ] **Step 1: Confirm the old copy is present (failing state)**

```bash
grep -nE '>Hero</a>|>Evidence</a>|>Full list</a>|>Open full list on GitHub</a>|>Evidence</h2>|list family;|does not mirror entry rows' docs/index.html
```

Expected: exactly 7 matching lines, numbered 406, 407, 411, 421, 427, 442, 449. Any other count means the working tree drifted from `b93a41e`; stop and reconcile before editing.

- [ ] **Step 2: Replace the two nav labels and the nav full-list link**

Find (lines 406-407):

```html
      <a href="#hero">Hero</a>
      <a href="#evidence">Evidence</a>
```

Replace:

```html
      <a href="#hero">Top</a>
      <a href="#evidence">Status</a>
```

Find (line 411):

```html
      <a class="nav-full" href="https://github.com/jgsystemsconsulting/awesome-archimate/blob/main/README.md">Full list</a>
```

Replace:

```html
      <a class="nav-full" href="https://github.com/jgsystemsconsulting/awesome-archimate/blob/main/README.md">Open full list</a>
```

Keep the three nav links at lines 408-410 (`Sections`, `Curation`, `Contribute`) untouched.

- [ ] **Step 3: Replace the hero CTA label**

Find (line 421):

```html
        <a class="primary" href="https://github.com/jgsystemsconsulting/awesome-archimate/blob/main/README.md">Open full list on GitHub</a>
```

Replace:

```html
        <a class="primary" href="https://github.com/jgsystemsconsulting/awesome-archimate/blob/main/README.md">Open full list</a>
```

The href is unchanged; the word "GitHub" stays on the page in the href, the support sentence, and the target URL.

- [ ] **Step 4: Rename the Evidence heading**

Find (line 427):

```html
        <h2 id="evidence-heading">Evidence</h2>
```

Replace:

```html
        <h2 id="evidence-heading">Status</h2>
```

`id="evidence-heading"` and the section's `aria-labelledby="evidence-heading"` stay untouched, so the nav label `Status` matches the heading.

- [ ] **Step 5: Shorten the family paragraph**

Find (line 442):

```html
        <p class="family">Part of the awesome-mbse list family; registry and family rules live in FAMILY.md in the jgsystemsconsulting/awesome-mbse repository.</p>
```

Replace:

```html
        <p class="family">Part of the awesome-mbse list family.</p>
```

- [ ] **Step 6: Shorten the sections intro**

Find (line 449):

```html
        <p class="muted prose">Eight README anchors. Open a section on GitHub; the landing does not mirror entry rows.</p>
```

Replace:

```html
        <p class="muted prose">Eight README anchors. Open a section on GitHub.</p>
```

- [ ] **Step 7: Verify the copy greps**

```bash
grep -nE '>Hero<|>Evidence<|>Full list<|Open full list on GitHub' docs/index.html
# expect: no output
grep -c '>Open full list</a>' docs/index.html
# expect: 2
grep -nE 'FAMILY\.md|list family;|does not mirror' docs/index.html
# expect: no output
grep -n 'awesome-mbse list family' docs/index.html
# expect: 1 line ending in "list family.</p>"
```

- [ ] **Step 8: Run the release gate**

```bash
python scripts/check_release.py
```

Expected: stdout includes `release gate: PASS`.

- [ ] **Step 9: Commit**

```bash
git add docs/index.html
git commit -m "feat(pages): replace maintainer shorthand with visitor copy"
```

---

### Task 2: Chrome fixes (favicon, font preloads, nav touch targets, IE shim)

**Files:**
- Modify: `docs/index.html:12-13` (head insert point), `:150-156` (`.site-nav a` rule), `:168-171` (`main` rule and surrounding blank line)
- Create (fallback only, see Step 8): `docs/favicon.svg`

**Interfaces:**
- Consumes: gate green after Task 1.
- Produces: exactly one `rel="icon"` link, exactly two `rel="preload" ... crossorigin` links, a `.site-nav a` rule with `min-height: 44px`, and no `main {` rule. Task 3's battery counts these.

**Model:** flash

- [ ] **Step 1: Insert the favicon and the two font preloads in `<head>`**

Find (lines 12-13):

```html
  <meta property="og:type" content="website">
  <style>
```

Replace:

```html
  <meta property="og:type" content="website">
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%23157adb'/%3E%3Ctext x='16' y='22' font-family='sans-serif' font-size='17' font-weight='600' fill='%23ffffff' text-anchor='middle'%3EA%3C/text%3E%3C/svg%3E">
  <link rel="preload" href="fonts/IBMPlexSans-Regular.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="fonts/IBMPlexSans-SemiBold.woff2" as="font" type="font/woff2" crossorigin>
  <style>
```

Notes: `<`, `>`, and `#` are percent-encoded inside the data URI. `crossorigin` is mandatory even same-origin because fonts always fetch in CORS mode; a preload without it double-downloads. Per lock, only Regular and SemiBold preload; Medium and Mono keep loading via `@font-face` alone. `#157adb` is the sRGB approximation of the accent token `oklch(0.58 0.17 253)`; tokens stay untouched.

- [ ] **Step 2: Verify the head additions**

```bash
grep -c 'rel="icon"' docs/index.html
# expect: 1
grep -c 'rel="preload"' docs/index.html
# expect: 2
grep -c 'crossorigin' docs/index.html
# expect: 2
```

- [ ] **Step 3: Raise the nav touch targets**

Find (lines 150-156):

```css
    .site-nav a {
      font-size: var(--text-meta);
      font-weight: 500;
      color: var(--color-text-muted);
      text-decoration: none;
      padding: var(--space-2) var(--space-1);
    }
```

Replace:

```css
    .site-nav a {
      font-size: var(--text-meta);
      font-weight: 500;
      color: var(--color-text-muted);
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      min-height: 44px;
      padding: var(--space-1) var(--space-1);
    }
```

`min-height: 44px` is the contract; padding-block drops from `space-2` to `space-1` so the bar grows by roughly 8px instead of 16px. The inline-flex centering keeps label text vertically centered at the taller height.

- [ ] **Step 4: Delete the dead IE shim**

Find (lines 168-173):

```css
    /* Main sections */
    main {
      display: block;
    }

    section {
```

Replace:

```css
    /* Main sections */
    section {
```

Delete the `main` rule and the blank line after it, nothing else. The `/* Main sections */` comment stays; every browser that can render this page ships `main` as block by default.

- [ ] **Step 5: Verify the CSS changes**

```bash
grep -n 'main {' docs/index.html
# expect: no output
grep -c 'min-height: 44px' docs/index.html
# expect: 2 (the nav anchor rule and the existing .primary rule)
grep -c 'padding: var(--space-1) var(--space-1)' docs/index.html
# expect: 1
grep -n 'padding: var(--space-2) var(--space-1)' docs/index.html
# expect: no output
```

- [ ] **Step 6: Run the release gate**

```bash
python scripts/check_release.py
```

Expected: stdout includes `release gate: PASS`.

- [ ] **Step 7: Commit**

```bash
git add docs/index.html
git commit -m "feat(pages): add favicon, font preloads, and 44px nav targets"
```

- [ ] **Step 8: Fallback only, if Task 3's smoke shows a broken tab icon**

Skip this step when the data-URI favicon renders. If it misbehaves, write `docs/favicon.svg` with the same monogram:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#157adb"/><text x="16" y="22" font-family="sans-serif" font-size="17" font-weight="600" fill="#ffffff" text-anchor="middle">A</text></svg>
```

Then swap the link. Find (the full icon line inserted in Step 1):

```html
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%23157adb'/%3E%3Ctext x='16' y='22' font-family='sans-serif' font-size='17' font-weight='600' fill='%23ffffff' text-anchor='middle'%3EA%3C/text%3E%3C/svg%3E">
```

Replace:

```html
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
```

Re-run `python scripts/check_release.py` (expect `release gate: PASS`), then commit:

```bash
git add docs/favicon.svg docs/index.html
git commit -m "fix(pages): swap data-URI favicon for favicon.svg asset"
```

This is the only sanctioned new asset, and it is one file under `docs/`.

---

### Task 3: Verification battery and browser smoke

**Files:**
- Read-only: `docs/index.html`, plus `docs/favicon.svg` if the Task 2 fallback ran

**Interfaces:**
- Consumes: the final strings produced by Tasks 1 and 2.
- Produces: a verification record in the execution summary (gate output, grep results, smoke checklist). No file writes.

**Model:** standard

- [ ] **Step 1: Run the full grep battery**

```bash
grep -nE '>Hero<|>Evidence<|>Full list<' docs/index.html
# expect: no output
grep -n 'Open full list on GitHub' docs/index.html
# expect: no output
grep -c '>Open full list</a>' docs/index.html
# expect: 2
grep -nE 'FAMILY\.md|list family;|does not mirror|mirror entry rows' docs/index.html
# expect: no output
grep -n 'awesome-mbse list family' docs/index.html
# expect: 1 line, "Part of the awesome-mbse list family.</p>"
grep -n 'main {' docs/index.html
# expect: no output
grep -c 'rel="icon"' docs/index.html
# expect: 1
grep -c 'rel="preload"' docs/index.html
# expect: 2
grep -c 'crossorigin' docs/index.html
# expect: 2
grep -c 'min-height: 44px' docs/index.html
# expect: 2
grep -c 'README.md#' docs/index.html
# expect: 8 (gate input untouched)
grep -c '<dt>' docs/index.html
# expect: 3 (gate input untouched)
```

Note: `id="evidence"`, `href="#evidence"`, and `id="evidence-heading"` legitimately remain; the battery greps `>Evidence<` display text only.

- [ ] **Step 2: Confirm the frozen anchors survived**

```bash
grep -c 'href="#hero"' docs/index.html
# expect: 1
grep -c 'id="hero"' docs/index.html
# expect: 1
grep -c 'href="#evidence"' docs/index.html
# expect: 1
grep -c 'id="evidence-heading"' docs/index.html
# expect: 1
grep -c 'aria-labelledby="evidence-heading"' docs/index.html
# expect: 1
grep -n '<a href="#sections">Sections</a>\|<a href="#curation">Curation</a>\|<a href="#contribute">Contribute</a>' docs/index.html
# expect: 3 lines, unchanged
```

- [ ] **Step 3: Em-dash scan**

```bash
python -c "import pathlib; print(pathlib.Path('docs/index.html').read_text(encoding='utf-8').count(chr(0x2014)))"
```

Expected: `0`.

- [ ] **Step 4: Run the release gate**

```bash
python scripts/check_release.py
```

Expected: stdout includes `release gate: PASS`.

- [ ] **Step 5: Browser smoke (manual, all five checks)**

Serve the page so the relative font URLs resolve:

```bash
python -m http.server 8000 --directory docs
```

Open `http://localhost:8000/` and check each item:

1. The tab shows the blue rounded "A" favicon. If it is broken or blank, run Task 2 Step 8, then repeat this smoke.
2. Devtools Network, font filter: `IBMPlexSans-Regular.woff2` and `IBMPlexSans-SemiBold.woff2` each appear exactly once. A duplicate or cancelled request means `crossorigin` is missing or mismatched.
3. Inspect each of the six nav links: computed height is at least 44px and the label is vertically centered.
4. Click every nav link: `Top` scrolls to the h1, `Status` to the chips section, `Sections`, `Curation`, and `Contribute` to their sections, and `Open full list` navigates to the GitHub README.
5. Everything else renders as at `b93a41e` apart from the intended changes: hero claim and support text unchanged, chip values `0.1.0` / `2026-09` / `17` unchanged, all 8 section rows and their labels unchanged, contribute links unchanged, footer unchanged.

Stop the server with Ctrl+C when done.

- [ ] **Step 6: Close out**

```bash
git status --short
git log --oneline -3
```

Expected: no `docs/index.html` entry in the status output (untracked `docs/superpowers/` planning files may appear); the log ends with the Task 1 and Task 2 commit messages, plus the fallback commit if it ran. If the fallback ran after the smoke, re-run the Step 1 battery, Step 3 scan, and Step 4 gate once more and record the results in the execution summary.
