# Nurse Handoff — task ledger

One ticket per loop iteration. A **ticket** is a bold-numbered item like
`**001 Skeleton.**`; take the first unchecked ticket whose "Blocked by"
tickets are all checked. Tick it only when its acceptance criteria are met
and verified in the same run. Add follow-up tickets in place rather than
leaving notes. The Definition of Done boxes are ticked when the ticket
named in parentheses is done. Human-only steps are in the last section
and are never ticked by the agent.

**Rule 0.** If the `HOST-VERIFY` line at the top of the prompt says
`fail`, the only unit of work this run is to make `tests/verify.ps1` pass
on the host; untick the ticket it names if its work was incomplete. Take a
new ticket only when the host result is `pass`.

Verification for every ticket:
`nurse-handoff/.venv/Scripts/python.exe -m pytest -q nurse-handoff` and
`powershell -NoProfile -ExecutionPolicy Bypass -File tests/verify.ps1`.
Bare `python` does not resolve inside the sandbox; always use the venv path.
The rules text and ticket definitions are protected; maintain assigned
checkboxes. Propose new work or ticket splits in `memory/QUESTIONS.md`.
Ticket 107 explicitly deletes its placeholder; ticket 110 adds the v0.2
Definition of Done. Tickets 103 and 106 may append their new fields in a
v0.2 extension section of PATIENT-SCHEMA.md, preserving the v0.1 text.

## v0.1 — Deterministic handoff

- [x] **001 Skeleton.** Create `nurse-handoff/` with the structure in spec §9:
  `README.md` (the §15 opening plus a usage stub), `requirements.txt`
  (`pytest` only), `nurse_handoff/__init__.py` (version `0.1.0`),
  `nurse_handoff/__main__.py` (prints usage and exits 2 when no path given),
  empty `data/` and `tests/` with `tests/__init__.py`, and a `conftest.py`
  that adds the package to `sys.path`. Acceptance:
  `.venv/Scripts/python.exe -m nurse_handoff` from inside `nurse-handoff/`
  prints usage and exits 2; `.venv/Scripts/python.exe -m pytest -q` runs and
  reports no tests collected (pytest exit code 5 is acceptable here and only
  here). Blocked by: none.

- [x] **002 Schema document in code.** Create `nurse_handoff/schema.py`
  holding the field lists from `docs/PATIENT-SCHEMA.md`: `REQUIRED_FIELDS`,
  `IMPORTANT_FIELDS` (with their warning text), `OPTIONAL_FIELDS`, and the
  expected type per field. Acceptance: a test asserts the three required
  fields and six important fields match the docs. Blocked by: 001.

- [x] **003 Four synthetic patients.** Write `data/simple_patient.json`,
  `data/chf_patient.json` (spec §3 extended per §11-B), `data/incomplete_patient.json`,
  `data/complex_patient.json` per spec §11. Acceptance: each parses with
  `json.load`; a test checks IDs are `SYNTH-001` to `SYNTH-004`, no key named
  `name`, `dob`, `mrn`, or `facility` exists, and patient C lacks
  `code_status`, `mobility`, `respiratory`. Blocked by: 001.

- [x] **004 Loader.** `loader.py`: `load_patient(path) -> dict`. Raises
  `PatientFileError` (message `file not found: <path>` or
  `invalid JSON in <path>: <json error>`) for missing or malformed files.
  Rejects a top-level non-object. Acceptance: `tests/test_loader.py` covers
  valid load, missing file, invalid JSON, non-object. Blocked by: 001, 003.

- [x] **005 Validator.** `validator.py`: `validate(record) -> list[str]`
  returning one `"<field> is required"` per missing required field in schema
  order, plus `"<field> must be <type>"` for type errors (spec
  `PATIENT-SCHEMA.md` §Type errors). Empty string counts as missing.
  Acceptance: `tests/test_validator.py` covers each required field missing,
  all three missing at once (three messages, ordered), wrong-type age, and a
  clean record returning `[]`. Blocked by: 002.

- [x] **006 Overview section.** `generator.py`: `render_overview(record)
  -> str` producing the `NURSING HANDOFF` header, underline, blank line, the
  age/code-status line (em dash U+2014, `Code status: Not documented` when
  missing), and `Primary problem:` line, exactly per `docs/OUTPUT-FORMAT.md`.
  Acceptance: tests for present and missing code status; byte-exact
  comparison. Blocked by: 005.

- [ ] **007 Assessment section.** `render_assessment(record) -> str` with
  Neuro, Cardiac, Respiratory, Mobility, Diet lines. Respiratory follows the
  rendering table in `PATIENT-SCHEMA.md` exactly, including the `false`
  case. Acceptance: one test per row of the respiratory table; a test that
  the string `Room air` never appears for any of the four patients or for a
  record with `respiratory` absent. Blocked by: 006.

- [ ] **008 List sections.** `render_list_section(title, items) -> str` and
  its use for ACCESS, MEDICATIONS OF NOTE, THIS SHIFT, PENDING. `None`
  (missing) renders `Not documented`; `[]` renders `None`; otherwise `- item`
  lines in input order. Acceptance: tests for all three states and for
  section order in `render_handoff`. Blocked by: 006.

- [ ] **009 Missing-data pass.** `render_handoff(record) -> str` assembles
  all sections with exactly one blank line between them and a single
  trailing LF. Run it against all four patients and a record containing only
  the three required fields. Acceptance: no exception for any of them; the
  minimal record renders `Not documented` for every optional line; snapshot
  tests for patients A and B stored under `tests/snapshots/` and compared
  byte for byte. Blocked by: 007, 008.

- [ ] **010 Rule 1 oxygen.** `rules.py`: `check_oxygen(record) -> list[str]`
  emitting the exact spec wording when `oxygen` is `true` and `device` or
  `flow_lpm` is missing. `oxygen` absent or `false` emits nothing.
  Acceptance: `tests/test_rules.py` cases: device missing, flow missing, both
  missing, both present, oxygen false, respiratory absent. Blocked by: 005.

- [ ] **011 Rule 2 IV access.** `check_iv_access(record)`: any medication
  containing the word-bounded token `IV` with `access` missing or empty →
  spec wording. `"IVF"` or `"Ivabradine"` must not trigger. Acceptance: tests
  for hit, no meds, meds without IV, false positives, access present.
  Blocked by: 010.

- [ ] **012 Rule 3 mobility and Rule 4 pending.** `check_mobility(record)`
  with spec wording. Rule 4 is a rendering rule already covered by 008;
  add a test that a missing `pending_tasks` renders `Not documented` and
  produces the important-field warning, and that `[]` renders `None` with
  no warning. Blocked by: 011.

- [ ] **013 Warnings block and CLI.** `rules.py`: `collect_warnings(record)
  -> list[str]` = important-field warnings (schema order, `⚠ ` prefix) then
  rule warnings, with the mobility de-duplication from `OUTPUT-FORMAT.md`.
  `__main__.py`: load → validate (print ERRORs to stderr, exit 1) → render
  handoff → print WARNINGS block (`None` when empty) → exit 0; file/JSON
  errors exit 2. Acceptance: subprocess tests running the CLI on all four
  patients and on a missing file, checking stdout, stderr, and exit codes;
  patient B produces `WARNINGS` / `None`; patient D produces both rule
  warnings. Blocked by: 009, 012.

- [ ] **014 Test coverage audit.** Walk spec §12 and confirm every listed
  test exists by name in `tests/`; add any missing. Add
  `tests/test_no_real_data.py` that scans `data/` for the forbidden keys and
  for anything matching a date-of-birth pattern. Acceptance: every §12
  bullet maps to a named test; `pytest -q` passes. Blocked by: 013.

- [ ] **015 README complete.** `nurse-handoff/README.md`: §15 opening,
  install (`python -m venv .venv`, `pip install -r requirements.txt`), usage,
  sample output for patient B, the known-vs-unknown principle with the
  `oxygen: false` vs `respiratory: null` example, the four patients table,
  the rules list, how to run tests, roadmap, disclaimer. Update the hub
  `README.md` status to "v0.1 ready for release". Acceptance: every section
  present; `verify.ps1` passes. Blocked by: 014.

### Definition of Done — v0.1 (agent ticks these; DONE file when all ticked)

- [x] four synthetic patients exist (003)
- [x] patient JSON loads correctly (004)
- [x] required fields are validated (005)
- [ ] missing information is preserved as unknown (007, 009)
- [ ] handoff is generated (009)
- [ ] basic clinical rules run (010–012)
- [ ] warnings are shown (013)
- [ ] `pytest -q` passes with zero failures (014)
- [ ] README explains the project (015)
- [ ] no real patient information is used (014)

When all ten are ticked and pytest passed this run: create `DONE`, state
"v0.1 ready for human release" in `memory/HANDOFF.md`, and stop.

## v0.2 — More clinical validation rules

Blocked by: the human ticking "v0.1 released" below and deleting `DONE`.
Each ticket adds one deterministic rule in `rules.py`, its tests, a line in
the README rules list, and (if needed) new synthetic patients numbered
`SYNTH-005` onward. Rules must be simple, explainable in one sentence, and
never infer clinical facts. Do not touch v0.3+ (web, FHIR, LLM).

- [ ] **101 Version bump.** `__init__.py` to `0.2.0-dev`; README "Version
  history" section. Blocked by: v0.1 released.
- [ ] **102 Rule 5 code status.** Missing `code_status` also emits
  `WARNING: Code status not documented; confirm before handoff.` in addition
  to the important-field glyph line (do not de-duplicate this one; it is
  intentionally loud). Blocked by: 101.
- [ ] **103 Rule 6 telemetry without rhythm.** New optional field
  `monitoring` (string). If it contains the token `telemetry` and `cardiac`
  is missing → `WARNING: Telemetry documented but no cardiac rhythm
  documented.` Update `PATIENT-SCHEMA.md`. Blocked by: 101.
- [ ] **104 Rule 7 diuretic without output.** If any medication contains
  `furosemide`, `bumetanide`, or `torsemide` (case-insensitive) and no
  `recent_events` entry contains `urine output` or `UO` → `WARNING: Diuretic
  listed but no urine output documented this shift.` Blocked by: 101.
- [ ] **105 Rule 8 NPO conflict.** If `diet` contains `NPO` and any
  `pending_tasks` entry contains `meal` or `tray` → `WARNING: NPO diet
  documented but a meal-related task is pending.` Blocked by: 101.
- [ ] **106 Rule 9 fall risk without mobility.** New optional field
  `fall_risk` (boolean). If `true` and `mobility` missing → `WARNING: Fall
  risk documented but mobility status not documented.` Blocked by: 101.
- [ ] **107 Rule 10 access without IV meds.** Informational only, no
  warning: nothing. (Placeholder to remind the agent that not every
  mismatch deserves a warning; delete this ticket with a DECISIONS.md note
  explaining why.) Blocked by: 101.
- [ ] **108 Patients E and F.** `SYNTH-005` exercising rules 6–9 all at
  once; `SYNTH-006` a clean telemetry patient producing no warnings.
  Snapshot tests for both. Blocked by: 102–106.
- [ ] **109 Rule registry.** Refactor `rules.py` so every rule is a function
  registered in an ordered `RULES` list with an id and one-line description;
  `python -m nurse_handoff --rules` prints the list. Blocked by: 108.
- [ ] **110 README and v0.2 Definition of Done.** Document all rules;
  update version to `0.2.0`; add a v0.2 Definition of Done block modeled on
  v0.1 and tick what applies. Blocked by: 109.

## Human checklist (agent never ticks these)

- [ ] Re-run `powershell -File ..\loops\setup.ps1` after a Python upgrade or if the Nursing venv is missing; the controller checks it and reports a blocker when setup is needed.
- [ ] Create the GitHub repository and push `main` after 001 lands (Q-001).
- [ ] Review and commit between iterations. Edits to protected files (AGENTS.md, PROMPT.md, loop.sh, tests/verify.ps1, docs/NURSE-HANDOFF-SPEC.md) are captured in the next pre-run snapshot; commits remain a human review choice.
- [ ] After the v0.1 DONE file appears: review, `git tag v0.1.0`, push.
- [ ] v0.1 released (tick this, then delete `DONE` to unblock v0.2).
- [ ] After v0.2 DONE: review, `git tag v0.2.0`, decide on v0.3.
