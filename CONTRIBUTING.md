# Contributing to Awesome ArchiMate

Thanks for helping keep this the best-curated ArchiMate index anywhere. Read this
before opening a PR: CI gates enforce most of it.

The fastest path: open an issue, or open a pull request that edits `README.md` directly.

## Inclusion bar

An entry is accepted only if **all** hold:

1. **On-topic**: genuinely about ArchiMate (any version), the Archi tool and its
   plugins, or enterprise architecture modeling practice around them.
2. **Substantive**: it teaches, demonstrates, specifies, or provides something usable.
   Not a stub. Not pure vendor marketing.
3. **Live**: the link resolves right now.
4. **Active or foundational**: maintained (commit within 24 months) or foundational
   value: a formal specification, certification program, or other canonical reference
   whose value does not depend on recent commits.
5. **Not duplicative**: not already listed (see the canonical-URL rule below).
6. **Legally linkable**: publicly accessible. We link, we never re-host model files,
   PDFs, or proprietary content.

Tie-breakers (nice-to-have, not gates): has a real openable model (`has-model`),
recently updated, from a recognized source (The Open Group, a university, an
established practitioner).

## Entry format

One line per entry, **hyphen separator** (` - `, never an en/em dash: awesome-lint
rejects those), tags as **inline code spans inside the sentence before the year
token**, year parenthesized as the last token:

```markdown
- [Resource Name](https://example.com) - One-line factual description `ArchiMate3` `Archi` `has-model` `tutorial` (2024).
```

- **Description:** factual, one line, **at most 140 characters** (measured from the
  first character after ` - ` to the last character before the first tag, excluding
  the link markup and tags). No hype.
- **`has-model`** means: a directly downloadable, non-paywalled `.archimate` file or
  ArchiMate Exchange Format model that opens in a named tool, or a repository or
  collection whose documented contents include at least one such file. Screenshots,
  papers describing a model, and access-gated or request-only files do not qualify.

## Tag vocabulary, cardinality and order

Tags appear in this fixed order, drawn **only** from this vocabulary:

`language -> method -> tool -> has-model -> type -> spec/standard -> paid -> year`

| Axis | Cardinality | Values |
| ------ | ------------- | -------- |
| language | exactly 1 | `ArchiMate3` (3.x, including 3.2) · `ArchiMate4` · `ArchiMate-general` (version-agnostic: methodology, books, both-version docs; not a lazy default) |
| method | 0 or 1 | `TOGAF` |
| tool | 0 or more | `Archi` · `other-tool` |
| has-model | 0 or 1 | `has-model` |
| type | 0 or 1 | `tutorial` · `course` · `book` · `paper` · `blog` · `docs` · `video` · `tool` · `plugin` · `certification` · `example` · `community` · `mcp` |
| spec/standard | 0 or 1 | `spec` · `standard` |
| paid | 0 or 1 | `paid` |
| year | exactly 1 | `(YYYY)` after the tags, not a code span (see The year rule) |

- `other-tool` graduates to its own tag once 3 or more entries share it.
- The type tag is **required unless `spec` or `standard` is present**: a pure
  specification row carries its language tag plus `spec` or `standard` only.
- Type value notes: `certification` marks a certification program or registry page;
  `example` marks a collection or repository of example models; `community` marks a
  forum or community hub; `docs` marks a wiki or documentation home, not a single
  blog post.
- For an Open Group normative document use `spec` or `standard` and omit `paper`.

## The year rule (`YYYY`)

`(YYYY)` = the year of the resource's **most recent author-published version**:

- a paper → its publication year;
- a repo → its latest tagged release, or the latest default-branch commit if untagged;
- a course → its current cohort year.

**Trivial edits (typo fixes) don't count.** Examples:

- A 2019 paper with a 2024 typo-fix commit → `(2019)`.
- A repo whose latest release tag is `v2.1` from 2023 → `(2023)`.

### Spoke addendum: undated pages

A web page with no visible publication or revision date takes the year it was last
verified during a sweep. This sentence is spoke-only; it is not part of the hub year rule.

## Canonical-URL rule (dedupe)

Before deciding "is this a duplicate", canonicalize both URLs: force `https`, lowercase
the host, strip a trailing slash, drop the query string and fragment unless they're
semantically required. If the canonical forms match, it's a duplicate.

## Editorial neutrality

This list is maintained by JG Systems Consulting Ltd. Current position: JGS sells no
ArchiMate-niche product, so no product disclosure applies today. The rules that hold:

- JGS products are listed by the **same inclusion bar** as everything else.
- Every JGS entry sits next to **at least 1 genuine competing or alternative entry**.
- **A superior competing tool is listed above a JGS one.** Neutrality is enforced by
  this rule, not by tone.

If JGS ships an ArchiMate-niche product, this section gains the product disclosure
before any JGS entry is listed.

## Local checks

Run from the repository root before opening a PR:

```bash
npx awesome-lint@2.3.0 README.md
npx markdownlint-cli2 "README.md" "CONTRIBUTING.md"
```

### Link check

`lychee` is a native binary, not an npm package. Install it once with your platform
package manager (`scoop`, `winget`, or `choco` on Windows, `brew` on macOS, `pacman`,
`zypper`, `snap`, or `apk` on Linux), then run from the repository root:

```bash
lychee --no-progress --max-retries 3 --include-fragments anchor-only README.md
```

Export `GITHUB_TOKEN` (for example `GITHUB_TOKEN=$(gh auth token)`) to avoid GitHub
rate limiting on `github.com` links. Third-party sites sometimes return transient
timeouts or 429s; retry before treating a failure as a broken link.

## Maintenance

Three workflows in `.github/workflows/` run on a fixed cadence. This section states
what each does.

### Link scan (weekly)

`links.yml` runs lychee every Monday at 18:00 UTC, on every pull request, and on
manual dispatch. PR runs are advisory: a PR with broken links gets a warning but is
never blocked by it. Scheduled and manual runs create or update a "Link Checker
Report" issue when the check exits nonzero; a clean run leaves that issue untouched.
Fragment checking (`--include-fragments anchor-only`) validates that every
table-of-contents anchor resolves.

### Freshness report (monthly)

`stale.yml` runs on the first day of each month at 06:00 UTC, or on manual dispatch.
It collects the `github.com` repository URLs from README.md and lists repos with no
push in the last 24 months. The report is advisory: an entry past the window can
still be valid under the foundational-value exception (criterion 4 of the Inclusion
bar). The "Freshness report" issue is refreshed on every run, including months with
no stale entries.

### Lint gates (every PR and push to main)

`lint.yml` runs `awesome-lint@2.3.0` on README.md, and `markdownlint` on README.md
and CONTRIBUTING.md, on every pull request targeting main and every push to main.
These gates block merge on failure. The local markdownlint command above installs an
unpinned npx package and may differ from the version CI runs; the pinned
`awesome-lint@2.3.0` matches CI exactly.
