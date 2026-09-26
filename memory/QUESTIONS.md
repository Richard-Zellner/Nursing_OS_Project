# Questions for the human

Append-only. The loop adds rows with status `open`; the human answers by
filling the Answer cell and setting status `answered`. Never delete rows.
HANDOFF.md lists only the ids that are still open.

| Id | Date | Question | Status | Answer |
|---|---|---|---|---|
| Q-001 | 2026-09-04 | Create the GitHub repository and push `main` after Ticket 001 lands, or wait until v0.1 DONE? | answered | 2026-09-24: Owner requested the public GitHub repository now and automatic controller commits/pushes after verification. |
| Q-002 | 2026-09-25 | Validation edge cases found after v0.1 tickets 009-015 (pre-existing ticket 005 behavior, not changed): `validate` accepts a negative `age` although PATIENT-SCHEMA.md says integer >= 0 (renders `-3-year-old`), and accepts empty strings in optional text fields such as `mobility: ""`, which render `Mobility: ` with trailing whitespace against OUTPUT-FORMAT.md. Should v0.2 add a ticket making negative age an ERROR and treating empty optional strings as not documented (or as an ERROR), and should this block tagging v0.1.0? | open | |
| Q-003 | 2026-09-26 | Edge cases found in the parent review (behaviour unspecified; not changed): (a) a list item containing a newline, e.g. `pending_tasks: ["line one\nline two"]`, renders a second line without the `- ` prefix, breaking one line per entry; (b) whitespace-only strings (`primary_problem: "   "`, `mobility: "  "`) are accepted and render trailing whitespace, like the empty strings in Q-002; (c) a file saved with a UTF-8 BOM is rejected as invalid JSON (exit 2). Options: reject in validation, normalise when rendering, or accept as is. Decide whether any of these block the v0.1.0 tag. | open | |
