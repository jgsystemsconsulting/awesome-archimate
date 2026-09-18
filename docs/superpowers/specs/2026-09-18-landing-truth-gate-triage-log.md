# ARL triage log: landing-truth-gate

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| section-index re.search first-match (L87/L103) | R1 | R1 | Genuine | C1: Design used re.search while edge case required multi-match fail. Fixed: findall, len==1, eight li. |
| entries chip int parse traceback (L53) | R1 | R1 | Genuine | C2: int() of non-integer chip raised vs R6. Fixed: fullmatch [0-9]+ then int, named fail. |
| fragment-less ninth link silent pass (L87) | R1 | R1 | Genuine | M1: count li not only fragment hrefs. Fixed in R5/step 8. |
| only column-0 `- [` scrutinized (L53) | R1 | R1 | Genuine | M2: * [ and indented markers escaped. Fixed in R4/step 7. |
| order README vs CURATED_SECTIONS (L55) | R1 | R1 | Advisory-skipped | Cheap: pinned tuple order in R5/Design. |
| fence-blind heading walk (L83) | R1 | R1 | Advisory-skipped | Cheap: fence toggle in step 7 and presence count. |
| CURATED_SECTIONS "e.g." (L79) | R1 | R1 | Advisory-skipped | Cheap: exact eight-title contract. |
| ## title extract undefined | R1 | R1 | Advisory-skipped | Cheap: line.strip() == "## " + title. |
| success line string unstated (R7) | R1 | R1 | Advisory-skipped | Cheap: quoted exact success print. |
| Version re.search vs exactly-one (L75) | R1 | R1 | Advisory-skipped | Cheap: findall / splitlines walk. |
| int() laxity vs digits-only | R2 | R2 | Advisory-skipped | Cheap: fullmatch [0-9]+. |
| CRLF ban vs Version regex | R2 | R2 | Advisory-skipped | Cheap: note \s* absorbs CR / prefer splitlines. |
| presence count fence skip | R2 | R2 | Advisory-skipped | Cheap: same fence toggle on presence. |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| section-index re.search | saboteur, auditor | CRIT | Genuine | Fixed (Round 1) |
| entries chip int parse | saboteur, auditor | CRIT | Genuine | Fixed (Round 1) |
| fragment-less ninth link | saboteur | MAJ | Genuine | Fixed (Round 1) |
| bullet marker scope | saboteur | MAJ | Genuine | Fixed (Round 1) |
| order / e.g. / extract / success / Version / fence | various | ADV | Advisory-skipped | Fixed cheap (Round 1) |

Fixes applied: 4 CRITICAL/MAJOR + advisories
Inflation rate: 0% (0 of 4 CRITICAL+MAJOR triaged FP/Design)
Validation: SKIP

## Round 2 Summary (confirmation wave)

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| L53 entries/markers | saboteur, new_hire, auditor | — | resolved by this change | Confirmed |
| L87 section-index | saboteur, new_hire, auditor | — | resolved by this change | Confirmed |
| int laxity / CRLF / fence presence | saboteur, auditor | ADV | Advisory-skipped | Fixed cheap (Round 2) |

Fixes applied: 0 CRITICAL/MAJOR (confirmation only; cheap ADV)
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 4 genuine CRIT/MAJOR + advisories
Document is ready.
