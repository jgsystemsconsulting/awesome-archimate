# landing-visitor-copy (P1) design

Package P1 from `docs/superpowers/packages/2026-09-18-awesome-archimate-packages.md`, with chrome nits b-01..b-04 promoted into scope by the X1 ruling ("include chrome"). Baseline: HEAD b93a41e, P2 done, `scripts/check_release.py` green.

## Problem

The landing is the first surface newcomers see, and its copy speaks maintainer shorthand: the first nav link is "Hero", the Evidence heading are internal vocabulary, two different labels name the same full-list link, and two sentences explain repo plumbing (FAMILY.md registry rules, entry-row mirroring) that visitors cannot act on. The same file carries four chrome nits: no favicon, no font preload, nav links under the 44px touch minimum, and a dead IE shim.

## Codebase context

Single-file change. `docs/index.html` holds all copy, inline CSS, and four self-hosted `@font-face` rules pointing at `docs/fonts/*.woff2` (Regular, Medium, SemiBold, Mono; OFL). `scripts/check_release.py` is the P2 truth gate: it regexes the chips (`<dt>version|sweep|entries</dt>` with exact `<dd>` values `0.1.0`, `2026-09`, `17`) and the `ul.section-index` block (exactly one list, 8 `li`, each with one href whose fragment must equal the GitHub slug of the eight curated section titles). None of the copy this spec changes is gate input except by accident, and the constraints below keep it that way.

## Research

research: skipped (local copy and chrome only; no external API)

## Decisions

All forks were locked before authoring: X1 resolved to include chrome; copy direction (nav not "Hero", visitor-language Evidence heading, one shared CTA label, drop the two maintainer tails) was fixed in the package. Exact strings below are this spec's picks; no open questions remain.

### Copy changes (docs/index.html)

| Line | Current | New | Why this string |
|---|---|---|---|
| 406 | `<a href="#hero">Hero</a>` | `<a href="#hero">Top</a>` | Shortest honest label for a same-page jump. "Awesome ArchiMate" as a nav item duplicates the h1 directly below it. Keeps `id="hero"`, href, and the three `#hero` CSS selectors untouched. |
| 407 | `<a href="#evidence">Evidence</a>` | `<a href="#evidence">Status</a>` | Must match the renamed heading or wayfinding breaks. `id="evidence"`, `aria-labelledby`, and href stay as-is. |
| 411 | `>Full list</a>` | `>Open full list</a>` | One shared label with the hero CTA. |
| 421 | `>Open full list on GitHub</a>` | `>Open full list</a>` | Same label as nav. "GitHub" stays on the page in the href, the support sentence, and the target URL, so nothing is lost. |
| 427 | `<h2 id="evidence-heading">Evidence</h2>` | `<h2 id="evidence-heading">Status</h2>` | The chips report version, sweep date, entry count: that is status. "Status" is visitor language; folding the chips into prose was rejected because the P2 gate greps chip markup. |
| 442 | `Part of the awesome-mbse list family; registry and family rules live in FAMILY.md in the jgsystemsconsulting/awesome-mbse repository.` | `Part of the awesome-mbse list family.` | Family pointer kept, registry plumbing dropped per lock. |
| 449 | `Eight README anchors. Open a section on GitHub; the landing does not mirror entry rows.` | `Eight README anchors. Open a section on GitHub.` | Mirror sentence deleted per lock; the rest of the line is untouched. |

Nav labels "Sections", "Curation", "Contribute" and all hero claim/support prose stay unchanged: the locks cover only the rows above, and the claim-plus-support merge in the package is marked optional, so it is skipped.

### Chrome changes (X1 promotion, same file)

1. **Favicon.** Inline SVG data URI in `<head>`, no new tracked asset:

   ```html
   <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%23157adb'/%3E%3Ctext x='16' y='22' font-family='sans-serif' font-size='17' font-weight='600' fill='%23ffffff' text-anchor='middle'%3EA%3C/text%3E%3C/svg%3E">
   ```

   `#157adb` is the sRGB approximation of the accent token (`oklch(0.58 0.17 253)`); at 16px the approximation is fine and tokens stay untouched. Percent-encode `<`, `>`, and `#` inside the URI. Fallback if the encoded URI misbehaves in review: write a tiny `docs/favicon.svg` with the same monogram and link it instead (the dispatch allows one optional asset under `docs/`).

2. **Font preload.** Two links in `<head>`, placed before `<style>`:

   ```html
   <link rel="preload" href="fonts/IBMPlexSans-Regular.woff2" as="font" type="font/woff2" crossorigin>
   <link rel="preload" href="fonts/IBMPlexSans-SemiBold.woff2" as="font" type="font/woff2" crossorigin>
   ```

   `crossorigin` is mandatory even same-origin: fonts always fetch in CORS mode, and a preload without it double-downloads. Per lock only Regular and SemiBold preload; Medium and Mono keep loading via `@font-face` alone.

3. **Nav touch targets.** Replace the `.site-nav a` padding rule with:

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

   `min-height: 44px` is the contract (DESIGN.md L112 extended to nav anchors by this package's X1 include ruling (b-03)); padding-block drops from `space-2` to `space-1` so the bar grows by roughly 8px, not 16px. The flex centering keeps label text vertically centered at the taller height.

4. **Dead IE shim.** Delete the `main { display: block; }` rule (lines 169-171) and nothing else. Every browser that can render this page ships `main` as block by default.

## Constraints

- P2 gate inputs are frozen: chip `dt` names (`version`, `sweep`, `entries`), `dd` values (`0.1.0`, `2026-09`, `17`), exactly one `ul.section-index`, exactly 8 `li`, and all 8 href fragments (`specifications-and-standards`, `certification`, `the-archi-tool`, `plugins-and-collaboration`, `books`, `example-models`, `togaf-alignment`, `communities`). Section-index link display text and class also stay unchanged per lock.
- No CDN fonts; `@font-face` src URLs keep pointing at `docs/fonts/`.
- No design-token, spacing-scale, or color changes beyond the nav padding edit above.
- No em dashes in any copy string.
- `python scripts/check_release.py` must PASS after all edits.
- Only `docs/index.html` changes by default; the favicon fallback route may add one `docs/favicon.svg`.

## Out of scope

Entry-row mirroring, token or visual redesign, `og:image`, README entries and badges, `check_release.py` logic, lychee, distribution, Path N Next, and the optional hero claim-plus-support merge.

## Verification

1. `python scripts/check_release.py` prints `release gate: PASS`.
2. Grep checks on `docs/index.html`: no `>Hero<`, no `>Evidence<` display text (`id="evidence"` and `href="#evidence"` legitimately remain), `>Full list<` gone, both full-list links read `Open full list`, family paragraph is one sentence, `mirror entry rows` gone, `main {` rule gone, two preload links present with `crossorigin`.
3. Browser smoke: favicon renders in the tab; devtools network shows each preloaded font fetched exactly once; every nav link's computed height is at least 44px; all anchors scroll to the right sections; page renders identically apart from the intended string and chrome changes.
4. Em-dash scan over the changed lines comes back clean.

## Open questions

None. X1, label direction, and guardrails were locked before authoring; exact strings are pinned in the Decisions table.
