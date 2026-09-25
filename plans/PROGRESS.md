# Portfolio progress

[Plans index](README.md) · [Master plan](MASTER-PLAN.md) · [Runbook](RUNBOOK.md)

This file records **milestone-level** state across all six projects.
Task-level state lives in each repo's own `TASKS.md`; for P0 that is the hub
[`TASKS.md`](../TASKS.md). Update this file at the end of every work session
([RUNBOOK §6](RUNBOOK.md#6-updating-progress)). Tick a box only when its
acceptance criteria were checked in that session.

Last updated: 2026-09-24 by Codex (owner-requested parallel work and independent review)

## Dashboard

Status values: `not-started` · `in-progress` · `blocked` · `review` (waiting on an owner gate) · `done`

| ID | Project | Current milestone | Status | Next action | Target |
|---|---|---|---|---|---|
| P0 | Nurse Handoff | M1 v0.1 build (004 complete) | in-progress | Ticket 005 validator; loop eligible after the daily run limit resets | v0.1 ~Sep 26, v0.2 ~Oct 9 |
| P1 | NurseBench | M0 technical work complete; wording review open | review | Owner P1-M0-7 README/disclaimer review, then Track 1 spec and protocols | M0 Oct 11, v0.1 Oct 31 |
| P2 | Charge Assign | M1 domain scaffold and M2 CI complete | in-progress | Owner acuity rubric and clinical constraints spec before generator/solver work | Feb 2027 |
| P3 | Dysphagia Screen FHIR | M2-1 authoring foundation complete | in-progress | Owner M1 wording, sources, terminology and clinical spec; no Questionnaire/CQL/HAPI yet | Mar 2027 |
| P4 | Grounded Handoff | M1 scaffold portion and M4-1 complete | in-progress | P3 HAPI setup and owner overlay/handoff spec; citation existence is mechanical only | Apr – mid-May 2027 |
| P5 | Stroke Abstraction Agent | Scaffold and M3-4a exact-span checks complete | in-progress | Owner measure digest/date rules, clinical spec and D-7; P1/P3 dependencies remain | mid-May – Jun 2027 |

All five separate repositories now exist privately, are registered for project
recall, and have reviewed work pushed to `main`. Parallel technical work does
not complete clinical milestones or change release targets. Native repository
handoffs contain the check evidence and task-level state.

## Owner gates and decisions

- [x] **G0** Employer policy: outside work is permitted off shift; the employer is never named or used (owner, 2026-09-24)
- [x] **D-1** Separate repos: decided by the owner on 2026-09-24
- [ ] **D-2** Nurse Handoff ends at v0.2; roadmap v0.3+ goes to P4, at the P0 v0.2 release
- [ ] **D-3** NurseBench model roster and API budget cap, by ~Oct 25
- [x] **D-4** New repos stay private until ready, then go public at release (owner, 2026-09-24)
- [ ] **D-5** Loop enrollment for new repos (recommended: no)
- [ ] **D-6** CAHIMS and NCA-GENL dates confirmed
- [ ] **D-7** P5 orchestration choice, at P5 M3
- [x] **D-8** Owner requested parallel work on all projects with subagents and parent review (2026-09-24); independent technical tasks advanced, clinical gates remain
- [x] Morse Fall Scale dropped; no permission email (owner, 2026-09-24)
- [ ] LLM API keys set as user environment variables (never in a repo)

## Tooling (RGB, checked 2026-09-24)

- [x] Python 3.11, uv, Node 24, Git
- [x] Portable Temurin 21.0.12.1+1 and Maven 3.9.16; P2/P4 builds verified; no global PATH change
- [ ] Docker Desktop with WSL2, for P3 (by end of February) and P4
- [x] Project-local SUSHI 3.20.1 in P3, pinned by npm lockfile; no global installation
- [ ] GitHub CLI `gh` (optional; repos can be created on github.com)

## Milestones

### P0 Nurse Handoff ([plan](projects/P0-nurse-handoff.md))
- [ ] M1 v0.1 build: tickets 004–015 (001–004 done; loader accepted in `15e9a17`)
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
| 2026-09-24 | Claude Code (owner decision) | all | Git history rewritten to remove the employer name (only one overview line changed in 3 commits) and force-pushed; Morse dropped from NurseBench | History diff checked; `tests/verify.ps1` run | P1: create private `nursebench` repo |
| 2026-09-24 | Codex (owner-delegated setup) | P1 | Created private repo, cloned to Desktop, registered project recall, and pushed the starter scaffold; P1-M0-1 and P1-M0-2 complete | GitHub API confirms private and remote main matches; locked dependency sync, package imports/compilation, Inspect CLI, Git ignores, all 39 task IDs and 13 local links checked | P1-M0-3 schema/validator; remaining M0 tasks and owner wording review stay open |
| 2026-09-24 | Codex + three subagents (owner-requested parallel round) | P0–P5 | Six scoped assignments reviewed by parent; P0 loader, P1 schema/split/offline eval/full CI, P2 domain, P3 SUSHI build, P4 citation existence, P5 exact evidence spans; four remaining repos created privately and registered | Parent reran 206 tests plus builds/CLI checks; all five separate repos passed Windows/Linux CI; P4 Java-selector failure corrected and green run observed; links, task IDs, exclusions and Git state checked | P0 ticket 005 under existing loop allowance; P1 wording review; owner clinical inputs and P3 HAPI dependency gate further clinical work |
