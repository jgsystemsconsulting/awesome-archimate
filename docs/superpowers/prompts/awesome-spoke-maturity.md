# Prompt: bring an awesome-* spoke to family maturity

Copy everything below the line into a new agent chat with the target repo open.

---

Repo: <path-or-name of this awesome-* repo>

Goal: Match the maturity bar of awesome-requirements-engineering (and awesome-archimate packaging): RR-B packaging + SA (sindresorhus/awesome) readiness, with awesome-lint always green in CI.

Do not ask permission for reversible steps. Only stop for irreversible/out-of-repo side effects.

## Definition of done

1. DESIGN_BRIEF.md + DESIGN.md exist if a Pages landing is in scope (minimal-technical, Path S).
2. docs/index.html GitHub Pages landing (or confirm N/A only if family explicitly defers Pages): sticky nav, hero + one CTA, real evidence chips, section index to README anchors, curation/contribute/footer, self-hosted fonts.
3. scripts/check_release.py (or family gate) asserts landing chips + section anchors cannot drift; fonts required if landing exists.
4. CI:
   - awesome-lint on README.md is **blocking** on push/PR to main (full SHA action pins).
   - lychee covers README.md and docs/index.html when landing exists; PR fails on broken product-surface links.
5. docs/MATURITY.md exists and states the dual gate (RR-B + SA) and that awesome-lint must always pass.
6. .gitignore includes SA/local audit noise (see below).
7. SA auditor clean except honest SA-AGE WAIT if under 30 days:
   `python ~/.zcode/skills/sindresorhus-awesome-ready/tools/audit.py --repo . --gh --lint`
   - 0 FAIL, WARNs fixed when cheap (logo, CC0 sidebar detection, licence prose).
   - Never fake age (no backdated commits, no mtime tricks).
8. README SA shape:
   - Theme blurb (not "Curated list of...").
   - Contents: no Contributing/Footnotes; if Install/Usage/Support/Version are ## headings, they appear in Contents (awesome-lint).
   - No ## Licence heading; prefer licence enquiry on Pages/Release/DISTRIBUTION.
   - Awesome badge; CONTRIBUTING.md; public topics awesome + awesome-list; default branch main.
9. DISTRIBUTION.md updated for Pages/public/Releases/catalogue/awesome deferred-or-ready status.
10. On main; feature branches deleted; push origin main when auth allows; release tag if version bump warranted.

## Process

1. Survey repo vs awesome-requirements-engineering gold sample.
2. Run SA auditor --gh --lint; list FAIL/WAIT/WARN with ids.
3. Fix FAILs and WARNs (cheap first). Keep SA-AGE as WAIT if under 30 days.
4. Ensure .github/workflows/lint.yml runs awesome-lint and fails the job on lint errors.
5. Add docs/MATURITY.md (copy bar from awesome-requirements-engineering).
6. Add gitignore entries below if missing.
7. Local verify: awesome-lint, check_release.py, SA auditor.
8. Commit on a feature branch or main per repo practice; FF-merge; delete branch; push origin main.
9. Report final SA decision + remaining WAIT only.

## .gitignore entries to ensure



## Skills / tools

- sindresorhus-awesome-ready (audit.py + SA standard)
- release-repo-standard when packaging gaps remain
- Family gold: awesome-requirements-engineering, awesome-archimate

## Explicit bans

- Do not open sindresorhus/awesome PR unless user says go-now and SA-AGE PASS with 0 FAIL.
- Do not disable awesome-lint in CI.
- Do not fake the 30-day age gate.
