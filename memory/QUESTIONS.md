# Questions for the human

Append-only. The loop adds rows with status `open`; the human answers by
filling the Answer cell and setting status `answered`. Never delete rows.
HANDOFF.md lists only the ids that are still open.

| Id | Date | Question | Status | Answer |
|---|---|---|---|---|
| Q-001 | 2026-09-04 | Create the GitHub repository and push `main` after Ticket 001 lands, or wait until v0.1 DONE? | answered | 2026-09-24: Owner requested the public GitHub repository now and automatic controller commits/pushes after verification. |
| Q-002 | 2026-09-25 | Validation edge cases found after v0.1 tickets 009-015 (pre-existing ticket 005 behavior, not changed): `validate` accepts a negative `age` although PATIENT-SCHEMA.md says integer >= 0 (renders `-3-year-old`), and accepts empty strings in optional text fields such as `mobility: ""`, which render `Mobility: ` with trailing whitespace against OUTPUT-FORMAT.md. Should v0.2 add a ticket making negative age an ERROR and treating empty optional strings as not documented (or as an ERROR), and should this block tagging v0.1.0? | open | |
