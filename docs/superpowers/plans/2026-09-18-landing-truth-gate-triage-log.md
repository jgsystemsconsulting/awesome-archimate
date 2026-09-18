# ARL triage log: landing-truth-gate (plan)

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| Restore checks require clean tree while script stays dirty | R1 | R1 | Genuine | M1: Mutation discipline and restore steps demanded no modified tracked files while Tasks 1-3 keep scripts/check_release.py uncommitted. Fixed: expect only in-progress task files modified. |
| R8 git log -3 workflows check weak | R1 | R1 | Advisory-skipped | Cheap note deferred; non-blocking. |
| landing_chip name unescaped | R1 | R1 | Advisory-skipped | Cheap: re.escape(name) applied. |
| heading startswith vs exact equality | R1 | R1 | Advisory-skipped | Cheap: stripped == "## " + title for presence hits. |
| print/exit cite 57-62 | R1 | R1 | Advisory-skipped | Cheap: 57-61. |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| restore clean-tree expectation | saboteur | MAJ | Genuine | Fixed (Round 1) |
| R8 / re.escape / heading / cite | saboteur, auditor | ADV | Advisory-skipped | Fixed cheap where cheap |

Fixes applied: 1 MAJOR + advisories
Inflation rate: 0% (0 of 1 CRITICAL+MAJOR triaged FP/Design)
Validation: SKIP

## Round 2 Summary (confirmation)

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| restore expectation L64 | parent confirm | — | resolved by this change | Confirmed: porcelain now allows in-progress task files |

Fixes applied: 0
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 1 genuine MAJOR + advisories
Document is ready.
