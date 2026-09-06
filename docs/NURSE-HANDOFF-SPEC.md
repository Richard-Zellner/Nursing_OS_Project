# Nurse Handoff — Specification (v0.1)

Source of truth for the `nurse-handoff/` project. When code and this file
disagree, this file wins. Companion documents: `PATIENT-SCHEMA.md` (fields)
and `OUTPUT-FORMAT.md` (exact report layout).

## Mission

Build a small, deterministic application that converts structured synthetic
patient information into a concise nursing shift-handoff report.

The application must:

1. organize patient information consistently
2. identify important missing information
3. never invent undocumented information
4. handle incomplete records without crashing
5. produce an output that a nurse can quickly scan

Educational project. Synthetic patient data only. Not for clinical use.

## 1. The problem

Nurses preparing for handoff assemble information from many places: patient
overview, diagnosis, code status, assessment findings, oxygen requirements,
mobility, IV access, medications, recent events, abnormal findings, pending
tests, and tasks for the next shift. The question this project explores:

> How can structured patient information be transformed into a consistent,
> concise nursing handoff without losing important information or
> fabricating missing information?

## 2. Scope

### v0.1 WILL

Take a JSON patient record and: validate it, organize it, identify missing
important fields, generate a readable handoff, and produce warnings.

### v0.1 WILL NOT

No AI, speech-to-text, Epic integration, FHIR, databases, authentication,
real patient data, web interfaces, or cloud hosting.

## 3. Example input

```json
{
  "patient_id": "SYNTH-001",
  "age": 72,
  "code_status": "Full Code",
  "primary_problem": "CHF exacerbation",

  "neuro": "Alert and oriented x4",
  "cardiac": "Normal sinus rhythm",
  "respiratory": {
    "oxygen": true,
    "device": "nasal cannula",
    "flow_lpm": 2
  },

  "mobility": "1-person assist",
  "diet": "Cardiac diet",

  "access": [
    "20G peripheral IV, left forearm"
  ],

  "medications_of_note": [
    "Furosemide 40 mg IV BID"
  ],

  "recent_events": [
    "Furosemide given at 1800",
    "900 mL urine output this shift"
  ],

  "pending_tasks": [
    "Morning BMP",
    "Daily weight"
  ]
}
```

## 4. Expected output

```text
NURSING HANDOFF
---------------

72-year-old — Full Code
Primary problem: CHF exacerbation

ASSESSMENT
Neuro: Alert and oriented x4
Cardiac: Normal sinus rhythm
Respiratory: 2 L/min nasal cannula
Mobility: 1-person assist
Diet: Cardiac diet

ACCESS
- 20G peripheral IV, left forearm

MEDICATIONS OF NOTE
- Furosemide 40 mg IV BID

THIS SHIFT
- Furosemide given at 1800
- 900 mL urine output this shift

PENDING
- Morning BMP
- Daily weight
```

## 5. Core design rule: known vs unknown

**Known:** `"oxygen": false` means the patient is documented as not
receiving supplemental oxygen.

**Unknown:** `"respiratory": null` (or the key absent) means respiratory
status was not provided.

These are not the same thing. The program must never convert unknown
information into assumed information.

- `Respiratory: Not documented` is acceptable.
- `Respiratory: Room air` is NOT acceptable unless the input says so.

> Missing data should remain missing.

## 6. Validation

Before generating the handoff, validate the record.

Required fields in v0.1: `patient_id`, `age`, `primary_problem`.

If one is missing (absent, `null`, or empty string):

```text
ERROR: primary_problem is required
```

The program stops with a non-zero exit code and prints no handoff. If
several required fields are missing, print one ERROR line per field, in the
order above.

## 7. Important-but-optional fields

Missing values in these fields must not stop generation but must create
warnings: `code_status`, `neuro`, `respiratory`, `mobility`, `access`,
`pending_tasks`.

```text
WARNINGS
--------
⚠ Code status not documented
WARNING: Mobility status not documented.
```

The report is still generated. The block header is `WARNINGS` with an
underline, exactly as in `OUTPUT-FORMAT.md`; the earlier draft's
`HANDOFF WARNINGS` wording is superseded.

```text
ERROR    → cannot safely generate report
WARNING  → generate report, but tell the user information is missing
```

## 8. Clinical consistency rules (deterministic, intentionally simple)

### Rule 1 — Oxygen

If `respiratory.oxygen` is `true` but `device` or `flow_lpm` is missing:

```text
WARNING: Supplemental oxygen documented but device/flow information is incomplete.
```

### Rule 2 — IV medication

If any entry in `medications_of_note` contains the token `IV` (word-bounded,
case-sensitive) and `access` is missing or an empty list:

```text
WARNING: IV medication listed but no vascular access documented.
```

### Rule 3 — Mobility

If `mobility` is missing:

```text
WARNING: Mobility status not documented.
```

### Rule 4 — Pending tasks

If `pending_tasks` is missing, do NOT assume there are none. The `PENDING`
section body reads `Not documented`, never `None`, and the important-field
warning fires. An explicit empty list `[]` is a documented "nothing
pending" and renders as `None` with no warning. (The earlier draft's
inline `Pending tasks: Not documented` form is superseded by the section
layout in `OUTPUT-FORMAT.md`.)

## 9. Project structure

```text
nurse-handoff/
├── README.md
├── requirements.txt          (pytest only)
├── nurse_handoff/
│   ├── __init__.py
│   ├── __main__.py           (CLI entry so `python -m nurse_handoff` works)
│   ├── loader.py             reads the patient file
│   ├── validator.py          checks required fields
│   ├── rules.py              looks for problems, returns warnings
│   └── generator.py          creates the handoff text
├── data/
│   ├── simple_patient.json
│   ├── chf_patient.json
│   ├── incomplete_patient.json
│   └── complex_patient.json
└── tests/
    ├── test_loader.py
    ├── test_validator.py
    ├── test_generator.py
    └── test_rules.py
```

Separation of responsibilities: loader → validator → rules → generator.

## 10. CLI

```bash
python -m nurse_handoff data/chf_patient.json
```

Prints the handoff, then a `WARNINGS` block (`None` when there are no
warnings). Exit code 0 on success, 1 on validation ERROR, 2 on file or JSON
errors. Exact layout: `OUTPUT-FORMAT.md`.

## 11. Synthetic test patients

- **A — simple_patient.json.** Routine med-surg patient. Every field
  present, no oxygen, no warnings. Tests basic formatting.
- **B — chf_patient.json.** The example above, extended with telemetry,
  oxygen, IV diuretic, intake and output, daily weight, pending labs. Tests a
  realistic handoff. No warnings expected.
- **C — incomplete_patient.json.** Deliberately omits code status,
  mobility, and the respiratory assessment. Report still generates with
  warnings.
- **D — complex_patient.json (contradictory).** Includes
  `"respiratory": {"oxygen": true, "device": null, "flow_lpm": null}` and an
  IV medication with no access. Expected: both rule warnings.

All patient IDs use the `SYNTH-###` form. No names, dates of birth, MRNs,
or facility names anywhere.

## 12. Tests

Loader: valid JSON loads; nonexistent file gives useful error; invalid JSON
gives useful error.

Validator: missing patient ID fails; missing age fails; missing primary
problem fails.

Generator: age appears; diagnosis appears; oxygen information appears
correctly; medications appear; pending tasks appear.

Missing data: missing optional field does not crash; unknown data displays
"Not documented"; unknown oxygen status does NOT become "Room air".

Rules: oxygen without device warns; IV medication without access warns;
missing mobility warns.

## 13. Definition of Done (v0.1)

- repository exists on GitHub (human step)
- four synthetic patients exist
- patient JSON loads correctly
- required fields are validated
- missing information is preserved as unknown
- handoff is generated
- basic clinical rules run
- warnings are shown
- `pytest` passes
- README explains the project
- no real patient information is used

Then `python -m nurse_handoff data/chf_patient.json` prints a complete,
readable handoff. Tag `v0.1.0` (human step). Do not add features before the
release.

## 14. Roadmap (do not build ahead)

```text
v0.1  Deterministic handoff
v0.2  More clinical validation rules            ← loop may proceed here after v0.1
v0.3  Simple web interface                      ← human decision required
v0.4  FHIR resources
v0.5  LLM handoff generation
v0.6  Deterministic evaluation of AI output
```

Eventual research question: can an AI-generated nursing handoff be
automatically checked against the source clinical record to detect
omissions, hallucinations, and changes in clinical meaning?

## 15. README opening (use verbatim in nurse-handoff/README.md)

> **Nurse Handoff** is an educational prototype exploring how structured
> clinical information can be converted into a standardized nursing
> shift-report summary.
>
> Nursing handoff requires clinicians to synthesize information scattered
> throughout the medical record. This project explores a deterministic
> approach to organizing that information while explicitly preserving
> missing or unknown data.
>
> The initial version intentionally does not use artificial intelligence.
> Its primary design principle is: *the system may organize documented
> information, but it must not invent undocumented information.*
>
> All patient records included in this repository are synthetic and the
> software is not intended for clinical use.
