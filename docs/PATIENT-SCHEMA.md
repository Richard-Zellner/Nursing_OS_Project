# Patient record schema (v0.1)

One JSON object per patient. Unknown keys are ignored with no error. Every
field except the three required ones may be absent or `null`; both mean
**not documented** and render identically.

| Field | Type | Class | `null`/absent means | Renders when missing |
|---|---|---|---|---|
| `patient_id` | string, `SYNTH-###` | required | ERROR, stop | — |
| `age` | integer ≥ 0 | required | ERROR, stop | — |
| `primary_problem` | string | required | ERROR, stop | — |
| `code_status` | string | important | not documented | `Code status: Not documented` + warning |
| `neuro` | string | important | not documented | `Neuro: Not documented` + warning |
| `cardiac` | string | optional | not documented | `Cardiac: Not documented` |
| `respiratory` | object or null | important | not documented | `Respiratory: Not documented` + warning |
| `respiratory.oxygen` | boolean | — | not documented | see below |
| `respiratory.device` | string | — | not documented | see Rule 1 |
| `respiratory.flow_lpm` | number | — | not documented | see Rule 1 |
| `mobility` | string | important | not documented | `Mobility: Not documented` + warning (Rule 3) |
| `diet` | string | optional | not documented | `Diet: Not documented` |
| `access` | list of strings | important | not documented | `ACCESS` section shows `Not documented` + warning |
| `medications_of_note` | list of strings | optional | not documented | section shows `Not documented` |
| `recent_events` | list of strings | optional | not documented | section shows `Not documented` |
| `pending_tasks` | list of strings | important | not documented | `Not documented` + warning (Rule 4) |

## Respiratory rendering

| `oxygen` | `device` | `flow_lpm` | Renders |
|---|---|---|---|
| `true` | present | present | `Respiratory: 2 L/min nasal cannula` |
| `true` | missing or `null` | any | `Respiratory: Supplemental oxygen (device not documented)` + Rule 1 warning |
| `true` | present | missing | `Respiratory: nasal cannula (flow not documented)` + Rule 1 warning |
| `false` | — | — | `Respiratory: No supplemental oxygen documented` |
| missing | — | — | `Respiratory: Not documented` |
| whole object `null` | | | `Respiratory: Not documented` + important-field warning |

Never render the words "Room air" unless the input contains them (for
example in a future `respiratory.note` field). `oxygen: false` is a
documented fact; `oxygen` absent is an unknown. Keep them distinct in code
(`is None` checks, not truthiness).

## Lists

- Missing or `null` list → `Not documented`.
- Empty list `[]` → `None` (explicitly documented as nothing).
- Non-empty → one `- item` line per entry, in input order, no sorting.

## Type errors

A field of the wrong type (for example `age: "seventy"`, `access: "20G"`)
is a validation ERROR in v0.1: `ERROR: age must be an integer`. Do not
coerce.
