# Portfolio progress

[Plans index](README.md) · [Master plan](MASTER-PLAN.md) · [Runbook](RUNBOOK.md)

This file records **milestone-level** state across all six projects.
Task-level state lives in each repo's own `TASKS.md`; for P0 that is the hub
[`TASKS.md`](../TASKS.md). Update this file at the end of every work session
([RUNBOOK §6](RUNBOOK.md#6-updating-progress)). Tick a box only when its
acceptance criteria were checked in that session.

Last updated: 2026-09-24 by Claude Code (initial plan)

## Dashboard

Status values: `not-started` · `in-progress` · `blocked` · `review` (waiting on an owner gate) · `done`

| ID | Project | Current milestone | Status | Next action | Target |
|---|---|---|---|---|---|
| P0 | Nurse Handoff | M1 v0.1 build (tickets 004–015) | in-progress | The loop takes ticket 004 after the daily run limit resets | v0.1 ~Sep 26, v0.2 ~Oct 9 |
| P1 | NurseBench | M0 scaffolding | not-started | Owner: create the private `nursebench` repo | M0 Oct 11, v0.1 Oct 31 |
| P2 | Charge Assign | — | not-started | Install JDK 21 + Maven in January | Feb 2027 |
| P3 | Dysphagia Screen FHIR | — | not-started | Install Docker Desktop in February | Mar 2027 |
| P4 | Grounded Handoff | — | not-started | Waits on P3's HAPI setup | Apr – mid-May 2027 |
| P5 | Stroke Abstraction Agent | — | not-started | Waits on P1 and P3 | mid-May – Jun 2027 |

## Owner gates and decisions

- [x] **G0** Employer policy: outside work is permitted off shift; the employer is never named or used (owner, 2026-09-24)
- [x] **D-1** Separate repos: decided by the owner on 2026-09-24
- [ ] **D-2** Nurse Handoff ends at v0.2; roadmap v0.3+ goes to P4, at the P0 v0.2 release
- [ ] **D-3** NurseBench model roster and API budget cap, by ~Oct 25
- [x] **D-4** New repos stay private until ready, then go public at release (owner, 2026-09-24)
- [ ] **D-5** Loop enrollment for new repos (recommended: no)
- [ ] **D-6** CAHIMS and NCA-GENL dates confirmed
- [ ] **D-7** P5 orchestration choice, at P5 M3
- [ ] **D-8** Run P2 in parallel with P1 (recommended: no)
- [ ] (Optional) Morse Fall Scale permission email, only if fall-risk scoring is wanted in NurseBench v1.1
- [ ] LLM API keys set as user environment variables (never in a repo)

## Tooling (RGB, checked 2026-09-24)

- [x] Python 3.11, uv, Node 24, Git
- [ ] JDK 21 and Maven, for P2 (by end of January) and P3's cql-to-elm
- [ ] Docker Desktop with WSL2, for P3 (by end of February) and P4
- [ ] SUSHI (`npm install -g fsh-sushi`), for P3
- [ ] GitHub CLI `gh` (optional; repos can be created on github.com)

## Milestones

### P0 Nurse Handoff ([plan](projects/P0-nurse-handoff.md))
- [ ] M1 v0.1 build: tickets 004–015 (001–003 done, `916b48b`)
- [ ] G1 v0.1 release: reviewed, `v0.1.0` tagged, "v0.1 released" ticked, `DONE` deleted, pushed
- [ ] M2 v0.2 rules: tickets 101–110
- [ ] G2 v0.2 release: `v0.2.0` tagged; D-2 recorded
- [ ] M3 portfolio polish: LICENSE, DISCLAIMER, CHANGELOG, CI, write-up

### P1 NurseBench ([plan](projects/P1-nursebench.md))
- [ ] M0 scaffolding: repo, schema, mock-model Inspect task, canary, split, CI (Oct 11)
- [ ] M1 Track 1 protocol math: 150 items, real runs (Oct 31)
- [ ] v0.1.0 released and public; hub README row added
- [ ] M2 Track 4 NIHSS (Nov 30)
- [ ] M3 Track 2 escalation red-team, grader kappa reported (Dec 31)
- [ ] M4 Track 5 discharge education (Jan 31)
- [ ] v1.0.0 released with write-up

### P2 Charge Assign ([plan](projects/P2-charge-assign.md))
- [ ] M1 domain, generator, acuity rubric
- [ ] M2 hard constraints with ConstraintVerifier tests, CI
- [ ] M3 soft constraints, baselines, benchmark
- [ ] v0.1.0 released
- [ ] M4 floor-map UI and explanations
- [ ] M5 replanning demo, blinded charge-nurse review
- [ ] v1.0.0 released with write-up

### P3 Dysphagia Screen FHIR ([plan](projects/P3-dysphagia-screen-fhir.md))
- [ ] M1 clinical spec, terminology, guideline wording
- [ ] M2 Questionnaire (FSH, SUSHI, LHC-Forms)
- [ ] M3 CQL library, 12–15 fixtures passing
- [ ] M4 PlanDefinition, `$apply` on local HAPI
- [ ] v0.1.0 released
- [ ] M5 CI with HAPI in Docker, README, demo
- [ ] v1.0.0 released with write-up

### P4 Grounded Handoff ([plan](projects/P4-grounded-handoff.md))
- [ ] M1 HAPI, Synthea, nursing overlay
- [ ] M2 SMART launch and bundle view
- [ ] M3 fact sheet, cited generation, citation UI
- [ ] M4 three-layer verifier, omission checklist
- [ ] v0.1.0 released
- [ ] M5 evaluation on 25 patients, ablations, Provenance
- [ ] v1.0.0 released with write-up

### P5 Stroke Abstraction Agent ([plan](projects/P5-stroke-abstraction-agent.md))
- [ ] M1 measure digest
- [ ] M2 60 synthetic chart packets (first 20 hand-validated)
- [ ] M3 segmenter, extractors, evidence verifier
- [ ] M4 measure engine, end-to-end run
- [ ] v0.1.0 released
- [ ] M5 review queue and router
- [ ] M6 evaluation, kappa, cost per chart
- [ ] v1.0.0 released with write-up

### Portfolio close-out
- [ ] Hub README lists all six projects with release links and headline results
- [ ] Six write-ups published
- [ ] Résumé lines filled from real results only

## Hours

Hours are the owner's actual time, logged per session. Estimates come from the research plans.

| ID | Estimate | Actual |
|---|---|---|
| P0 | ~6 | 0 |
| P1 | ~110 | 0 |
| P2 | ~45 | 0 |
| P3 | ~40 | 0 |
| P4 | ~60 | 0 |
| P5 | ~70 | 0 |

## Session log

Append one row per session, newest last. Loop runs log in `memory/LOG.md`, not here.

| Date | Who | Project | Work done | Verification | Next |
|---|---|---|---|---|---|
| 2026-09-24 | Claude Code (owner request) | all | Created `plans/`: master plan, six project plans, progress file, runbook, templates | Links checked; `tests/verify.ps1` run | Owner: review, decide D-1, commit and push `plans/` before the next loop unit |
| 2026-09-24 | Claude Code (owner decision) | all | Owner chose separate repos (D-1); recorded in DECISIONS/ACTIVE-DECISIONS; plans committed and pushed | `tests/verify.ps1` run | P1: G0 policy check, create `nursebench` repo |
| 2026-09-24 | Claude Code (owner decision) | all | G0 satisfied (outside work off shift; employer never named); D-4 private until ready; Morse email made optional; employer name removed from the overview | `tests/verify.ps1` run | P1: create private `nursebench` repo |
