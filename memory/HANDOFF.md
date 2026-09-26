# Handoff

## Nurse Handoff — v0.1 ready for human release

Tickets 009-015 were completed in a direct owner-requested Claude Code session
during the Codex outage (not by the loop), in ledger order, one at a time, each
verified with `tests/verify.ps1` before its tick and LOG line.

- 009: `render_handoff` checked on all four patients and a required-only
  record; hand-authored snapshots compared byte for byte.
- 010-012: `rules.py` with `check_oxygen`, `check_iv_access`,
  `check_mobility`, and `check_important_fields`; `tests/test_rules.py`.
- 013: `collect_warnings`, `render_warnings`, and the CLI (exit 0/1/2, UTF-8
  LF bytes); subprocess tests in `tests/test_cli.py`.
- 014: all 17 spec section 12 bullets map to named tests; `data/` scan.
- 015: full `nurse-handoff/README.md`; hub `README.md` status updated.

Repair (2026-09-25, same direct session): the controller's independent
check (`.loop/trusted-acceptance.py`) rejected `DONE` because `validate`
accepted `age: -1` and `medications_of_note: [17]`. `validate` now reports
`age must be a non-negative integer` and `<list> must be a list of strings`,
as PATIENT-SCHEMA.md requires; tests added in `test_validator.py` and
`test_cli.py`. The trusted check passes on a copy of the project.

Verification: pytest 242 passed; `tests/verify.ps1` passed. Every v0.1
Definition of Done box is ticked and `DONE` exists.

Review (2026-09-26): `validate` also rejects a patient_id that is not
`SYNTH-###` (schema type column); pytest 244 passed.

Open questions: Q-003 (newline in list items, whitespace-only strings,
UTF-8 BOM); Q-002, now only the empty optional strings part
(`mobility: ""` renders `Mobility: ` with trailing whitespace); negative age
is fixed. Decide whether it blocks tagging.

Human action: answer Q-002, then `git tag v0.1.0` and push. Tick "v0.1
released" and delete `DONE` to unblock v0.2 (ticket 101).
