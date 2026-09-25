# P1: NurseBench (4 evaluation tracks)

[Master plan](../MASTER-PLAN.md) · [Progress](../PROGRESS.md) · [Runbook](../RUNBOOK.md)

| | |
|---|---|
| Repo | `nursebench`, a new repo at `C:\Users\14087\Desktop\nursebench` (D-1: separate repos) |
| Design authority | [docs/portfolio/nursebench.md](../../docs/portfolio/nursebench.md) |
| Stack | Python 3.11, [Inspect](https://inspect.aisi.org.uk/) (`inspect_ai`), pytest, uv; textstat for Track 5 |
| Finish line | v1.0.0: all four tracks, full results table, failure galleries, methodology, write-up |
| v0.1 (résumé gate) | Track 1 complete and public by **Oct 31, 2026** |
| Hours | ~110: M0 10, M1 25, M2 25, M3 30, M4 20 |

## Before starting (owner)

- Done: G0 (outside work off shift; the employer is never named), D-1
  (separate repo), D-4 (private until the v0.1 release).
- Morse Fall Scale: dropped (owner, 2026-09-24). Track 4 is NIHSS only, and
  no fall-risk scale is planned.
- LLM API accounts and keys in user environment variables (never in the
      repo). D-3 model roster and budget cap set before M1 runs.

## Shared design, fixed in M0

- Item schema: the JSON in the research plan (`id`, `track`, `version`, `input`,
  `gold`, `critical_fields`, `tags`, `difficulty`, `source_ref`, `authored_by`,
  `reviewed`) plus a `canary` field.
- Contamination control: a canary GUID in every data file. A deterministic
  hash split sends about 20% of items to a private held-out set that is never
  committed. It lives in git-ignored `private/`, and the owner backs it up.
- Reporting: accuracy with 95% bootstrap CIs, critical-error rate, error
  taxonomy counts, and a five-item failure gallery per track.
- CI never calls paid APIs. It uses Inspect's mock model provider. Confirm the
  provider name in the current Inspect docs at M0.

## M0: scaffolding (~10 h, by Oct 11)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P1-M0-1 | OWNER | Create the GitHub repo; clone to Desktop; register in the project registry ([RUNBOOK §4](../RUNBOOK.md#4-starting-a-new-repo)) | Remote exists; `project-memory.cjs boot "nursebench"` resolves |
| P1-M0-2 | AGENT | Scaffold from [repo-scaffold](../templates/repo-scaffold.md) and the tree in the research plan; `pyproject.toml` with pinned `inspect_ai` | `uv sync` works; tree matches |
| P1-M0-3 | AGENT | `nursebench/common/schema.py`: item model, validator, canary check; tests | Invalid items are rejected with clear messages; tests pass |
| P1-M0-4 | AGENT | Hello-world Inspect task over a 3-item JSONL using the mock model | `inspect eval` runs offline in CI |
| P1-M0-5 | AGENT | Held-out split tool (`scripts/split.py`), deterministic by item-ID hash | Same input gives the same split; `private/` is git-ignored |
| P1-M0-6 | AGENT | CI: pytest, schema validation of every `data/` file, mock eval | Green on `main` |
| P1-M0-7 | PAIR | README skeleton, DISCLAIMER (with the "not orders" nomogram note), LICENSE, DATA_LICENSE | Owner approves the wording |

## M1: Track 1 protocol math, then v0.1 (~25 h, by Oct 31)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P1-M1-1 | OWNER | `docs/clinical-spec-t1.md`: scope, output contract, tolerance per field, the five critical-error definitions, the edge-case taxonomy | Complete per the [clinical-spec template](../templates/clinical-spec.md) |
| P1-M1-2 | OWNER | `protocols/*.yaml` for heparin VTE (Raschke 1993), heparin ACS (Becker 2001), insulin correction and potassium (both NurseBench-authored), each citing its source. An agent may fix YAML syntax but not values. | The owner has checked each number against its source |
| P1-M1-3 | AGENT | Gold calculators, one per protocol, covering band edges, caps, rounding, lb→kg and U/h↔mL/h | Every band boundary is unit-tested, and the owner signs off on the expected values in the tests |
| P1-M1-4 | AGENT | Seeded `generate.py` producing 150 items, about 25% of them edge cases (missing data, exclusions, critical values) | Same seed gives byte-identical output, and every item passes the schema |
| P1-M1-5 | OWNER | 30 hand-written items, plus review of 100% of edge-case items | Items marked `authored_by: RN` and `reviewed: true` |
| P1-M1-6 | AGENT | `task.py` and `scorer.py`: per-field exact or tolerance match; an item passes only if all fields pass; critical-error classifier | Unit test for each critical-error type |
| P1-M1-7 | AGENT | `common/report.py` and `bootstrap.py`: CIs, rates, taxonomy, gallery; writes `results/<date>_<model>.json` and `summary.csv` | Deterministic given a fixed seed |
| P1-M1-8 | OWNER | 20-item smoke run per model, cost projection, then the full run; model versions and dates pinned | Real result files committed |
| P1-M1-9 | PAIR | README results table, limitations, failure gallery; CHANGELOG 0.1.0 | Owner approves |
| P1-M1-10 | OWNER | [Release checklist](../templates/release-checklist.md): tag `v0.1.0`, make the repo public, résumé and LinkedIn | Tag pushed; hub README row added |

**Scope-cut ladder.** Check it on Oct 24; the owner picks in this order:
(1) drop potassium and ship three protocols; (2) 100 items instead of 150;
(3) two models instead of three. Never cut the owner review of edge cases.

## M2: Track 4 NIHSS (~25 h, by Nov 30; light month)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P1-M2-1 | OWNER | `docs/clinical-spec-t4.md`: item rules, UN handling, the ataxia rule, 1a/1b/1c with aphasia, gaze vs fields, extinction, "cannot score", and a justified major-total-error threshold. Cite NINDS; no certification-course material. | Complete |
| P1-M2-2 | AGENT | Score-vector sampler that encodes the owner's consistency rules | Tests for each rule; the owner reviews the rule list |
| P1-M2-3 | OWNER | 20 hand-written narratives | Committed with their vectors |
| P1-M2-4 | AGENT | LLM narrative generator (about 80 narratives in structured, shorthand and messy styles); prompt and model recorded | Output stored with provenance |
| P1-M2-5 | OWNER | Verify every generated narrative against its vector; fix or reject | 100% reviewed |
| P1-M2-6 | AGENT | Task and scorer: per-item accuracy, confusion matrix, total MAE, major-error %, hallucinated-item rate | Unit tests with hand-built fixtures |
| P1-M2-7 | OWNER | Runs, results, CHANGELOG 0.2.0 | Real results committed |

Keep the ~80 generated narratives in a form P5 can reuse for chart generation.

## M3: Track 2 post-discharge escalation (~30 h, Dec 9–31)

No build work Dec 1–8.

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P1-M3-1 | OWNER | `docs/clinical-spec-t2.md`: EMERGENCY/URGENT/ROUTINE definitions and required safety elements, anchored to MedlinePlus "when to call" pages and BE FAST. No Schmitt-Thompson. | Complete, with a citation per scenario family |
| P1-M3-2 | OWNER | `scenarios.yaml`: 40 base scenarios (~25 emergency/urgent, ~15 benign controls) with labels and safety elements | Owner-adjudicated |
| P1-M3-3 | AGENT | `perturb.py`: minimizing, buried lede, texting typos, caregiver voice, reassurance pushback, making 200 items | Deterministic where templated; LLM-assisted variants recorded |
| P1-M3-4 | OWNER | Review that every perturbation keeps its label | 100% reviewed |
| P1-M3-5 | AGENT | `grader_prompt.md` and disposition/safety-element extractor | Fixed prompt, versioned |
| P1-M3-6 | OWNER | Hand-label 40 items for grader validation, and set the minimum kappa | Labels committed |
| P1-M3-7 | AGENT | Kappa report; metrics for under-triage (EMERGENCY→ROUTINE is critical), over-triage, flip rate and safety-element inclusion | Grader trusted only when kappa meets the owner's threshold |
| P1-M3-8 | OWNER | Runs and results. Spanish variants only if a bilingual reviewer checks them. | Real results; CHANGELOG 0.3.0 |

## M4: Track 5 discharge education, then v1.0 (~20 h plus release, by Jan 31, 2027)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P1-M4-1 | OWNER | Choose 15–20 MedlinePlus pages (EN plus human-written ES) and write a critical-content checklist per page | Checklists committed with attribution |
| P1-M4-2 | AGENT | Source snapshots with URL and date; `readability.py` (textstat for EN, Fernández-Huerta or Szigriszt-Pazos for ES); numeric-fidelity regex | Tests, including numbers that must survive unchanged |
| P1-M4-3 | AGENT | Checklist-retention grader | Versioned prompt |
| P1-M4-4 | OWNER | Validation labels on a subset plus kappa; PEMAT-P scores on 10 outputs | Reported |
| P1-M4-5 | AGENT | Full results table across four tracks; `docs/methodology.md` and `docs/error-taxonomy.md` drafted from owner decisions | Numbers only from committed results |
| P1-M4-6 | OWNER | Headline: the "readable but unsafe" rate, stated with the limits of readability formulas | Owner-written |
| P1-M4-7 | OWNER | Release v1.0.0, write-up, résumé line filled from real runs | Release checklist complete |

No fall-risk scale follows v1.0: the owner dropped Morse on 2026-09-24 (too much work and licensing risk).

## Hand-offs

- To P5: the seeded-truth generator pattern, NIHSS narrative styles, kappa tooling.
- To P4: the grader-validation method.

## Risks

| Risk | Response |
|---|---|
| Inspect API changes | Pin the version at M0; upgrade only between milestones |
| Cost | Smoke runs first; hard budget cap (D-3); local open-weights model for iteration |
| Generated narratives drift from their vectors | 100% owner verification; reject rather than patch |
| Held-out split lost | Owner keeps an offline backup of `private/` |
