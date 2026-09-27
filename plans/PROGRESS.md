# Portfolio progress

[Plans index](README.md) · [Master plan](MASTER-PLAN.md) · [Runbook](RUNBOOK.md) · [Resume plan](RESUME.md) · [Session log](SESSION-LOG.md)

This file records **milestone-level** state across all six projects.
Task-level state lives in each repo's own `TASKS.md`; for P0 that is the hub
[`TASKS.md`](../TASKS.md). Update this file at the end of every work session
([RUNBOOK §6](RUNBOOK.md#6-updating-progress)). Tick a box only when its
acceptance criteria were checked in that session.

Last updated: 2026-09-27 by Claude Code

## Dashboard

Status values: `not-started` · `in-progress` · `blocked` · `review` (waiting on an owner gate) · `done`

| ID | Project | Current milestone | Status | Next action | Target |
|---|---|---|---|---|---|
| P0 | Nurse Handoff | v0.1.0 released 2026-09-26; M2 v0.2 rules (tickets 101–110) | blocked | The loop has been blocked since 07:00 UTC 2026-09-27 (the Codex sandbox refuses the Store `pwsh.exe`); owner: apply a fix from the checklist, then Q-002/Q-003 | v0.2 ~Oct 9 |
| P1 | NurseBench | M1 harness and items ready; Tracks 4, 2 and 5 drafted with specs, data, scorers and tools; Track 2 reply task and Track 5 checklist grader built; hostile-input hardening | review | Owner: set the four API keys (D-3 go), then the smoke and full runs; RN review of drafts | v0.1 Oct 31 |
| P2 | Charge Assign | M1–M4 done (delegated reviews); M5 replanning and review packet ready | review | Owner: blinded charge-nurse review (M5-3), RN read | Feb 2027 |
| P3 | Dysphagia Screen FHIR | M1–M4 done; HAPI CI green; v0.1.0 prepared | review | Owner: RN re-read, then tag v0.1.0 and go public | Mar 2027 |
| P4 | Grounded Handoff | M1–M3 done; first model run (25 patients, 4 arms, `claude-sonnet-5` and `claude-haiku-4-5`), judge on 8 handoffs | in-progress | Judge the primary and loop-on arms for the headline; owner: support labels and ratings (packets ready) | Apr – mid-May 2027 |
| P5 | Stroke Abstraction Agent | M1–M3 and M5 done; real 60-chart run (98.8% element accuracy, 99.1% measure agreement); real-data metrics (P5-M6-2b) | in-progress | Rerun with extraction prompt 0.2; owner: blind abstraction, engine review, RN review | mid-May – Jun 2027 |

All five separate repositories now exist privately, are registered for project
recall, and have reviewed work pushed to `main`. Parallel technical work does
not complete clinical milestones or change release targets. Native repository
handoffs contain the check evidence and task-level state.

## Owner gates and decisions

- [x] **G0** Employer policy: outside work is permitted off shift; the employer is never named or used (owner, 2026-09-24)
- [x] **D-1** Separate repos: decided by the owner on 2026-09-24
- [ ] **D-2** Nurse Handoff ends at v0.2; roadmap v0.3+ goes to P4, at the P0 v0.2 release
- [ ] **D-3** NurseBench model roster and API budget cap, by ~Oct 25 (roster and USD 100 cap recommended as a delegated decision, 2026-09-27; the owner's API keys are the go)
- [x] **D-4** New repos stay private until ready, then go public at release (owner, 2026-09-24)
- [ ] **D-5** Loop enrollment for new repos (recommended: no)
- [ ] **D-6** CAHIMS and NCA-GENL dates confirmed
- [x] **D-7** P5 orchestration: the `claude-cli` extractor (delegated agent decision under the owner's 2026-09-26 delegation)
- [x] **D-8** Build later projects alongside NurseBench instead of in sequence: yes. The owner asked for parallel work on all projects (2026-09-24). Release targets are unchanged.
- [x] **D-9** Clinical input delegated to agents (owner, 2026-09-24). Agent drafts carry provenance, and the owner signs off as RN before each release ([RUNBOOK §1](RUNBOOK.md#1-roles-and-the-authorship-boundary))
- [x] Morse Fall Scale dropped; no permission email (owner, 2026-09-24)
- [ ] LLM API keys set as user environment variables (never in a repo)

## Tooling (RGB, checked 2026-09-24)

- [x] Python 3.11, uv, Node 24, Git
- [x] Portable Temurin 21.0.12.1+1 and Maven 3.9.16; P2/P4 builds verified; no global PATH change
- [x] HAPI on the portable JDK for P3 and P4 (owner decision 2026-09-25); Docker Desktop is only a fallback
- [x] Project-local SUSHI 3.20.1 in P3, pinned by npm lockfile; no global installation
- [x] GitHub CLI `gh` 2.101.0, per-user install, logged in (2026-09-27)

## Milestones

### P0 Nurse Handoff ([plan](projects/P0-nurse-handoff.md))
- [x] M1 v0.1 build: tickets 001–015 (001–008 by the loop through `8ab0cce`; 009–015 in a direct Claude session, `e8dee59`; validator repair `e2ecbe4`)
- [x] G1 v0.1 release: reviewed, `v0.1.0` tagged, "v0.1 released" ticked, `DONE` deleted, pushed (2026-09-26, owner instruction)
- [ ] M2 v0.2 rules: tickets 101–110
- [ ] G2 v0.2 release: `v0.2.0` tagged; D-2 recorded
- [ ] M3 portfolio polish: LICENSE, DISCLAIMER, CHANGELOG, CI, write-up

### P1 NurseBench ([plan](projects/P1-nursebench.md))
- [x] M0 scaffolding: repo, schema, mock-model Inspect task, canary, split, CI (Oct 11); wording finalized under D-9, RN-reviewed 2026-09-24
- [ ] M1 Track 1 protocol math: 150 items, real runs (Oct 31)
- [ ] v0.1.0 released and public; hub README row added
- [ ] M2 Track 4 NIHSS (Nov 30)
- [ ] M3 Track 2 escalation red-team, grader kappa reported (Dec 31)
- [ ] M4 Track 5 discharge education (Jan 31)
- [ ] v1.0.0 released with write-up

### P2 Charge Assign ([plan](projects/P2-charge-assign.md))
- [x] M1 domain, generator, acuity rubric (M1-4 spot-check as a delegated agent review, 2026-09-27)
- [x] M2 hard constraints with ConstraintVerifier tests, CI (M2-2 as a delegated agent review)
- [x] M3 soft constraints, baselines, benchmark (M3-4 results and limitations drafted under delegation)
- [ ] v0.1.0 released
- [x] M4 floor-map UI and explanations (M4-3 wording review delegated; owner RN read pending)
- [ ] M5 replanning demo, blinded charge-nurse review
- [ ] v1.0.0 released with write-up

### P3 Dysphagia Screen FHIR ([plan](projects/P3-dysphagia-screen-fhir.md))
- [x] M1 clinical spec, terminology, guideline wording (agent-drafted under D-9, RN-reviewed 2026-09-24)
- [x] M2 Questionnaire (FSH, SUSHI, LHC-Forms) (M2-4 wording check as a delegated agent review; owner RN re-read before release)
- [x] M3 CQL library, 12–15 fixtures passing (`b1228b1`; CQL agent-drafted under D-9, owner review pending)
- [x] M4 PlanDefinition, `$apply` on local HAPI (`81bc905`; HAPI on the portable JDK, owner decision 2026-09-25)
- [ ] v0.1.0 released
- [ ] M5 CI with HAPI in Docker, README, demo
- [ ] v1.0.0 released with write-up

### P4 Grounded Handoff ([plan](projects/P4-grounded-handoff.md))
- [x] M1 HAPI, Synthea, nursing overlay (`8f32925`; US Core 6.1.0 report in docs/us-core-validation.md)
- [x] M2 SMART launch and bundle view (`821c693`; local pinned SMART launcher v2, owner question P4-Q041)
- [x] M3 fact sheet, cited generation, citation UI (first model run `23f5068`, 2026-09-27)
- [ ] M4 three-layer verifier, omission checklist (agent parts done 2026-09-27; owner labels M4-4 and release M4-6 open)
- [ ] v0.1.0 released
- [ ] M5 evaluation on 25 patients, ablations, Provenance
- [ ] v1.0.0 released with write-up

### P5 Stroke Abstraction Agent ([plan](projects/P5-stroke-abstraction-agent.md))
- [x] M1 measure digest (Specs Manual v2026B1; agent-drafted under D-9, RN-reviewed 2026-09-24)
- [x] M2 60 synthetic chart packets (C01–C20 validated by an agent under delegation; owner review pending)
- [x] M3 segmenter, extractors, evidence verifier (D-7 claude-cli extractor; verified in the real run, 2026-09-27)
- [ ] M4 measure engine, end-to-end run (real 60-chart run done 2026-09-27; owner engine review M4-2 and release M4-4 open)
- [ ] v0.1.0 released
- [x] M5 review queue and router (`b739469`; thresholds are placeholders pending P5-Q024)
- [ ] M6 evaluation, kappa, cost per chart
- [ ] v1.0.0 released with write-up

### Portfolio close-out
- [ ] Hub README lists all six projects with release links and headline results
- [ ] Six write-ups published
- [ ] Résumé lines filled from real results only

## Hours

Hours are the owner's actual time, logged per session. Agents never estimate or fill them in.
Estimates come from the research plans.

| ID | Estimate | Actual |
|---|---|---|
| P0 | ~6 | not logged |
| P1 | ~110 | not logged |
| P2 | ~45 | not logged |
| P3 | ~40 | not logged |
| P4 | ~60 | not logged |
| P5 | ~70 | not logged |

## Session log

One row per session, in [SESSION-LOG.md](SESSION-LOG.md).
