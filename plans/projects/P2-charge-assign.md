# P2: Charge Assign (acuity-based assignment optimizer)

[Master plan](../MASTER-PLAN.md) · [Progress](../PROGRESS.md) · [Runbook](../RUNBOOK.md)

| | |
|---|---|
| Repo | `charge-assign`, a new repo at `C:\Users\14087\Desktop\charge-assign` |
| Design authority | [docs/portfolio/charge-assign.md](../../docs/portfolio/charge-assign.md) |
| Stack | JDK 21, Maven, Timefold Solver 2.x Community (Apache-2.0), started from the timefold-quickstarts Employee Scheduling example |
| v0.1 | after M3: solver, baselines and a benchmark results table |
| Finish line | v1.0.0: UI, explanations, replanning demo, blinded charge-nurse review, write-up |
| Window | Feb 2027, ~45 h |

## Before starting

- Owner: JDK 21 and Maven installed by the end of January. Neither was on RGB
  on 2026-09-24. Verify with `java -version` and `mvn -v`.
- M1 task: pin the current Timefold 2.x release from Maven Central and use only
  the 2.x quickstart. Ignore tutorials written for 1.x.
- Owner: plan how to recruit 2–3 charge nurses for the blinded review
  (off-duty, synthetic scenarios only, no employer channels or material).
  Start asking in January.

## M1: domain, generator, acuity rubric (~10 h)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P2-M1-1 | OWNER | `docs/acuity-rubric.md`: point values for each factor, citing Perroca and Sir et al. 2015 as inspiration and not copying SNCT | Complete |
| P2-M1-2 | OWNER | `docs/clinical-spec.md`: every hard/medium/soft constraint in plain language; the ratio table from CA Title 22 §70217 with citation; charge-nurse cap; incompatible-pair policy; soft weights | Every constraint has a stated rationale |
| P2-M1-3 | AGENT | Scaffold (repo template plus quickstart base); domain model with `Nurse`, `Patient` (planning entity, variable = nurse) and `UnitConfig` | Builds under `mvn verify` |
| P2-M1-4 | AGENT | Seeded scenario generator: 24–32 beds, 5–8 RNs, varied census and acuity, 50 scenarios saved as JSON | Same seed gives the same file; the owner spot-checks 5 for realism |

## M2: hard constraints (~10 h)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P2-M2-1 | AGENT | Constraints for ratio cap by unit type, required competency, charge-nurse load cap, orientee only with preceptor (shared geography), incompatible pairs | One `ConstraintVerifier` test per constraint, covering pass and violation |
| P2-M2-2 | OWNER | Review each constraint against the clinical spec | Signed off in `memory/DECISIONS.md` |
| P2-M2-3 | AGENT | GitHub Actions CI running `mvn verify` | Green |

## M3: soft constraints, baselines, benchmark, then v0.1 (~10 h)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P2-M3-1 | AGENT | Medium: max acuity per nurse. Soft: acuity balance (squared deviation), geography (halls/spread), continuity weighted by acuity (Jiang 2023), admit/discharge spread. Weights come from the spec. | `ConstraintVerifier` test for each |
| P2-M3-2 | AGENT | Baselines: round-robin by room, and greedy "highest acuity to lightest load" | Unit tests |
| P2-M3-3 | AGENT | Benchmark runner over the 50 scenarios: violations (must be 0), acuity spread (max−min, SD), halls per nurse, continuity %, solve time | `results/summary.csv` generated |
| P2-M3-4 | OWNER | Read the results; write limitations (unvalidated rubric; preferences and politics are invisible to the model) | README results section |
| P2-M3-5 | OWNER | Release v0.1.0 | Release checklist |

## M4: floor-map UI and explanations (~8 h)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P2-M4-1 | AGENT | Unit floor-map grid colored by nurse, and per-nurse load bars (adapted from the quickstart page) | Renders for any generated scenario |
| P2-M4-2 | AGENT | Timefold score analysis turned into plain-language reasons ("Room 12 → Ana: continuity kept; adds one hall") | One reason per assignment |
| P2-M4-3 | OWNER | Review the explanation wording as a charge nurse would read it | Approved |

## M5: replanning, blinded review, v1.0 (~7 h)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P2-M5-1 | AGENT | Replanning demo: a 1500 admission, existing assignments pinned (`@PlanningPin`), a soft penalty per reassignment | Test shows only the minimum reassignments |
| P2-M5-2 | AGENT | Blinded review packet: 5 scenarios × 3 anonymized assignments (optimizer, greedy, round-robin), randomized order, answer key kept separately | Packet reproducible from a seed |
| P2-M5-3 | OWNER | Run the review with 2–3 charge nurses; record rankings and quotes (with their permission) | Raw responses stored; summary in README |
| P2-M5-4 | PAIR | README positioning (Epic Assignment Wizard, iQueue and TeleTracking contrast; humble prototype framing), demo GIF, CHANGELOG | Owner approves |
| P2-M5-5 | OWNER | Release v1.0.0, write-up, résumé line from real numbers | Release checklist |

If reviewer recruitment slips, release v1.0 without the review, state that
in the limitations, and add the review in v1.1. Never substitute the owner's
own ranking and call it a blinded review.

## Risks

| Risk | Response |
|---|---|
| Timefold 2.x API differs from examples | Pin the version and use only the 2.x quickstart source |
| Slow solves on large scenarios | Termination limit in config; report solve time honestly |
| Constraint weights feel arbitrary in an interview | Every weight has a rationale line in the clinical spec |
