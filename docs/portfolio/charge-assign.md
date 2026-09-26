# Acuity-based assignment optimizer (project 11)

A Timefold (Java) solver that builds a charge nurse's shift assignment — CA ratios, competencies, isolation, geography, continuity, balanced acuity — benchmarked against round-robin and a greedy heuristic. \~45 h.

## Design

The solver treats the assignment like a charge nurse does, under explicit hard and soft rules, and explains every choice in plain language.

**Stack.** [Timefold Solver](https://timefold.ai/license) Community edition (Apache-2.0), the maintained fork of Red Hat's OptaPlanner. It runs on JDK 21, and you'd start from the Employee Scheduling example in [timefold-quickstarts](https://github.com/TimefoldAI/timefold-quickstarts) (Spring Boot or Quarkus). The 2.x line is current as of Sept 2026 and deprecated much of the 1.x API. Pin the version from Maven Central when you start, and ignore 1.x-era tutorials.

**Domain model:**

- **Nurse:** competencies (tele, stroke, chemo), orientee/preceptor pairing, charge flag, float/agency flag, prior-shift patients.
- **Patient** (planning entity; the planning variable is the assigned nurse): room, hall/pod coordinates, acuity points, isolation type, tele required, expected admit/discharge/transfer, sitter need.
- **Unit config:** unit type → ratio cap, room map, incompatible-pair rules.

**Acuity rubric** (yours, in `docs/acuity-rubric.md`). Points for:

- ADL dependence
- fall precautions
- isolation
- titrated drips
- q1–2h assessments / neuro checks
- wound/drain care
- behavioral needs
- blood products
- admit/discharge workload
- telemetry

Cite Perroca and Sir et al. 2015 as inspiration. Don't copy the NHS Safer Nursing Care Tool (licensed) or vendor tools.

| Level | Constraint | Notes |
| --- | --- | --- |
| Hard | Ratio cap by unit type | CA Title 22 §70217: med-surg 1:5, telemetry 1:4, step-down 1:3, "at all times" |
| Hard | Required competency | e.g., tele patient → tele-competent RN |
| Hard | Charge nurse load cap | Configurable, often 0–2 patients; the charge nurse covers breaks under §70217 |
| Hard | Orientee load only with preceptor pairing | Paired nurses share geography |
| Hard | Incompatible pairs | Configurable unit policy, e.g., neutropenic precautions vs infectious isolation |
| Medium | Max acuity points per nurse | Keeps the heaviest assignment survivable |
| Soft | Balance acuity | Minimize squared deviation from the unit mean |
| Soft | Geography | Minimize halls / room spread per nurse |
| Soft | Continuity | Same nurse as prior shift, weighted higher for high-acuity patients (Jiang et al. 2023) |
| Soft | Spread admits and discharges | Penalize >1 expected admit per nurse |

Use Timefold's HardMediumSoftScore, and give every constraint its own ConstraintVerifier unit test.

**Baselines:** round-robin by room number, and a greedy "highest acuity to lightest load" heuristic that mimics the whiteboard method.

**Replanning demo.** A 1500 admission arrives. Re-solve with existing assignments pinned (`@PlanningPin`) plus a soft penalty per reassignment, and show that only the minimum moves.

**UI.** Adapt the quickstart's web page:

- a unit floor-map grid colored by nurse
- per-nurse load bars
- Timefold's score analysis rendered as plain-language reasons ("Room 12 → Ana: continuity kept; adds one hall")

## Build plan

1. **M1 (\~10 h):** domain model, scenario generator (24–32 beds, 5–8 RNs, varied census and acuity, 50 seeded scenarios), acuity rubric doc.
2. **M2 (\~10 h):** hard constraints, ConstraintVerifier tests, CI.
3. **M3 (\~10 h):** soft constraints, both baselines, benchmark runner, results table.
4. **M4 (\~8 h):** floor-map UI and plain-language explanations.
5. **M5 (\~7 h):** replanning demo, blinded charge-nurse review, README, demo GIF, write-up.

## Evaluation

The optimizer has to beat the whiteboard on balance and continuity with zero rule violations.

**Per-scenario metrics:**

- ratio and competency violations (must be 0)
- acuity spread (max−min and SD)
- halls per nurse
- continuity %
- reassignments on replan
- solve time

**Blinded review.** Two or three charge nurses rank three anonymized assignments (optimizer, greedy, round-robin) for five synthetic scenarios. Report their preferences and quote their comments. This is the part no software engineer can fake. Use synthetic scenarios only, never a real census.

**Positioning line for the README:**

- Epic's Assignment Wizard suggests a shift assignment plan for the charge nurse to review (EpicShare, "Balance nursing workloads", accessed 2026-09-26).
- LeanTaaS iQueue for Inpatient Flow (LeanTaaS acquired Hospital IQ in January 2023) and TeleTracking (Capacity IQ) forecast capacity and staffing.
- Corrected 2026-09-26 from the vendors' own public pages (Charge Assign P2-Q035); the earlier text called the Epic tool a manual aid and put Hospital IQ under TeleTracking.
- This prototype solves the per-shift constrained assignment itself.

Keep it humble: this is a prototype, not a product.

**Limitations to state:** the acuity rubric is unvalidated, and real assignments involve preferences and politics the model can't see.

**Résumé line:** "Built an acuity-based nurse assignment optimizer (Java, Timefold) enforcing CA Title 22 ratios, competencies and isolation rules; reduced acuity spread \[x\]% vs round-robin across \[n\] synthetic scenarios; charge nurses preferred it in \[k/m\] blinded comparisons."
