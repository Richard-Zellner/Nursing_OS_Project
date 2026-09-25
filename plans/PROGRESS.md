# Portfolio progress

[Plans index](README.md) · [Master plan](MASTER-PLAN.md) · [Runbook](RUNBOOK.md) · [Resume plan](RESUME.md) · [Latest review](REVIEW-2026-09-25-round3.md)

This file records **milestone-level** state across all six projects.
Task-level state lives in each repo's own `TASKS.md`; for P0 that is the hub
[`TASKS.md`](../TASKS.md). Update this file at the end of every work session
([RUNBOOK §6](RUNBOOK.md#6-updating-progress)). Tick a box only when its
acceptance criteria were checked in that session.

Last updated: 2026-09-25 by Claude Code (round 3: Waves A and B; see REVIEW-2026-09-25-round3.md)

## Dashboard

Status values: `not-started` · `in-progress` · `blocked` · `review` (waiting on an owner gate) · `done`

| ID | Project | Current milestone | Status | Next action | Target |
|---|---|---|---|---|---|
| P0 | Nurse Handoff | M1 v0.1 build (001–008 done) | in-progress | The loop continues with ticket 009 | v0.1 ~Sep 26, v0.2 ~Oct 9 |
| P1 | NurseBench | M1 Track 1 harness built (calculators, 150 items, task, scorer, report); M2 Track 4 spec draft, rules and sampler | review | Owner: D-3 models and budget, 30 hand items (M1-5), calculator sign-off (M1-3), Q-10–Q-25; then P1-M1-8 runs. Agent next: P1-M2-6 Track 4 scorer | v0.1 Oct 31 |
| P2 | Charge Assign | M1–M3 built: calculator, 50 scenarios, H1–H5, M1 and S1–S4, baselines, benchmark results | review | Owner: spot-check 5 scenarios (M1-4), constraint review (M2-2), read results and write limitations (M3-4), Q015–Q027. Agent next: P2-M4-1/2 floor map and reasons, M5-1 replanning | Feb 2027 |
| P3 | Dysphagia Screen FHIR | M3 done: CQL library compiled to ELM, all 15 fixtures pass | review | Owner: P3-Q019 gating, M2-4 wording, CQL review, Q020–Q022; M4 HAPI and `$apply` need Docker | Mar 2027 |
| P4 | Grounded Handoff | M1 built except HAPI loading; fact sheet, value-fidelity verifier (layer 2) and omission check built | in-progress | Owner: Q021–Q031, inventory and verifier-doc review. Agent next: P4-M3-4 citation view, M5-4 Provenance; HAPI and SMART need Docker; generation needs a model decision | Apr – mid-May 2027 |
| P5 | Stroke Abstraction Agent | Sampler, gold, segmenter, date checks; chart packets C01–C20; shared measure engine | review | Owner: review the 20 packets (P5-M2-4), engine paths (M4-2), D-7, Q016–Q023. Agent next: P5-M5-1 router, M5-2 review page | mid-May – Jun 2027 |

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
- [x] **D-8** Build later projects alongside NurseBench instead of in sequence: yes. The owner asked for parallel work on all projects (2026-09-24). Release targets are unchanged.
- [x] **D-9** Clinical input delegated to agents (owner, 2026-09-24). Agent drafts carry provenance, and the owner signs off as RN before each release ([RUNBOOK §1](RUNBOOK.md#1-roles-and-the-authorship-boundary))
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
- [ ] M1 v0.1 build: tickets 004–015 (001–008 done by the loop, through `8ab0cce`)
- [ ] G1 v0.1 release: reviewed, `v0.1.0` tagged, "v0.1 released" ticked, `DONE` deleted, pushed
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
- [ ] M1 domain, generator, acuity rubric
- [ ] M2 hard constraints with ConstraintVerifier tests, CI
- [ ] M3 soft constraints, baselines, benchmark
- [ ] v0.1.0 released
- [ ] M4 floor-map UI and explanations
- [ ] M5 replanning demo, blinded charge-nurse review
- [ ] v1.0.0 released with write-up

### P3 Dysphagia Screen FHIR ([plan](projects/P3-dysphagia-screen-fhir.md))
- [x] M1 clinical spec, terminology, guideline wording (agent-drafted under D-9, RN-reviewed 2026-09-24)
- [ ] M2 Questionnaire (FSH, SUSHI, LHC-Forms)
- [x] M3 CQL library, 12–15 fixtures passing (`b1228b1`; CQL agent-drafted under D-9, owner review pending)
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
- [x] M1 measure digest (Specs Manual v2026B1; agent-drafted under D-9, RN-reviewed 2026-09-24)
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

Append one row per session, newest last. Loop runs log in `memory/LOG.md`, not here.

| Date | Who | Project | Work done | Verification | Next |
|---|---|---|---|---|---|
| 2026-09-24 | Claude Code (owner request) | all | Created `plans/`: master plan, six project plans, progress file, runbook, templates | Links checked; `tests/verify.ps1` run | Owner: review, decide D-1, commit and push `plans/` before the next loop unit |
| 2026-09-24 | Claude Code (owner decision) | all | Owner chose separate repos (D-1); recorded in DECISIONS/ACTIVE-DECISIONS; plans committed and pushed | `tests/verify.ps1` run | P1: G0 policy check, create `nursebench` repo |
| 2026-09-24 | Claude Code (owner decision) | all | G0 satisfied (outside work off shift; employer never named); D-4 private until ready; Morse email made optional; employer name removed from the overview | `tests/verify.ps1` run | P1: create private `nursebench` repo |
| 2026-09-24 | Claude Code (owner decision) | all | Git history rewritten to remove the employer name (only one overview line changed in 3 commits) and force-pushed; Morse dropped from NurseBench | History diff checked; `tests/verify.ps1` run | P1: create private `nursebench` repo |
| 2026-09-24 | Codex (owner-delegated setup) | P1 | Created private repo, cloned to Desktop, registered project recall, and pushed the starter scaffold; P1-M0-1 and P1-M0-2 complete | GitHub API confirms private and remote main matches; locked dependency sync, package imports/compilation, Inspect CLI, Git ignores, all 39 task IDs and 13 local links checked | P1-M0-3 schema/validator; remaining M0 tasks and owner wording review stay open |
| 2026-09-24 | Codex + three subagents (owner-requested parallel round) | P0–P5 | Six scoped assignments reviewed by parent; P0 loader, P1 schema/split/offline eval/full CI, P2 domain, P3 SUSHI build, P4 citation existence, P5 exact evidence spans; four remaining repos created privately and registered | Parent reran 206 tests plus builds/CLI checks; all five separate repos passed Windows/Linux CI; P4 Java-selector failure corrected and green run observed; links, task IDs, exclusions and Git state checked | P0 ticket 005 under existing loop allowance; P1 wording review; owner clinical inputs and P3 HAPI dependency gate further clinical work |
| 2026-09-24 | Claude Code (owner request) | all | Dashboard fixes (D-8 wording, hours "not logged"); D-9 clinical-drafting delegation recorded | `tests/verify.ps1` run | Draft the clinical inputs |
| 2026-09-25 | Claude Code + five subagents (D-9) | P1–P5 | Drafted the blocking clinical inputs: P1 M0-7, Track 1 spec, 4 protocols; P2 rubric and constraint spec; P3 spec, terminology, 15 fixtures; P4 overlay and handoff spec; P5 measure digest, truth vector, fixture spec. Parent reviewed each; owner RN sign-off recorded (owner-stated). Source checks stay open in each repo's QUESTIONS.md. Menon citation corrected in the hub | Real runs: P1 86 pytest + validate + mock eval; P2 Maven 6 tests; P3 SUSHI 0 errors, 8 tests; P4 Maven BUILD SUCCESS; P5 69 pytest + verify-evidence. All five pushed; working trees clean | Agent tasks: P1-M1-3, P2-M1-4, P3-M2-2, P4-M1-2, P5-M2-2. Owner: D-7, Docker install, source checks |
| 2026-09-25 | Claude Code + five subagents | P1–P5 | Implementation round 2: P1 calculators and 150 items (bfffb2f); P2 acuity calculator, 50 scenarios, H1–H5 (68c3e17); P3 Questionnaire, LHC-Forms page, 15 fixture responses (765e202); P4 Synthea pin, inventory, overlay generator (aacdfda); P5 sampler, gold outcomes, segmenter, date checks (48b993c). Parent reviewed each diff, reran checks, fixed two stale README lines | Parent reruns: P1 420 pytest + validate + mock eval; P2 Maven 69 tests; P3 SUSHI 0/0, 71 tests; P4 Maven 47 tests; P5 344 pytest + both verify-evidence fixtures. Signed-off clinical docs unchanged in every repo | Owner reviews listed in the dashboard; weekly usage limit reached during the round |
| 2026-09-25 | Claude Code (owner request) | all | Full review and record: [REVIEW-2026-09-25.md](REVIEW-2026-09-25.md) (timeline, decisions, per-project state, 11 findings) and [RESUME.md](RESUME.md) (owner queue in 3 tiers, agent waves A/B, blockers, brief template) | Read-only audit of 6 repos: all clean and synced; 1,005 tests at last parent reruns; 58 open questions (31 source checks, 27 owner decisions or reviews) | Owner Tier 1 items; then Wave A (P1-M1-6/7, P3-M3-3/4, P2-M3-1..3) |
| 2026-09-25 | Claude Code + three subagents | P1–P3 | Wave A of RESUME.md: P1-M1-6/7 Track 1 task, scorer, bootstrap and report (a513968); P2-M3-1..3 M1 and S1–S4, baselines, real benchmark over 50 scenarios (6b08d18); P3-M3-3/4 CQL library with pinned Maven ELM build and fixture tests (b1228b1). Parent reviewed each diff against the spec and reran checks. New owner questions: P1 Q-16–Q-17, P2 Q021–Q027, P3 Q021–Q022 | Parent reruns: P1 629 pytest + validate + mock eval + mock Track 1 report (refused for results/); P2 Maven 107 tests (1 skipped: on-demand benchmark); P3 npm verify incl. Maven 55 JUnit tests. P3 `npm run verify` now needs JDK 21 | Wave B running: P4-M3-2/M4-2/M4-5, P5-M2-3 (20 packets) + M4-1, P1-M2-1/2 |
| 2026-09-25 | Claude Code + three subagents | P1, P4, P5 | Wave B of RESUME.md: P4-M3-2 fact sheet, M4-2 value fidelity, M4-5 omission check (bfe05aa); P5-M2-3a packets C01–C20 and M4-1 shared measure engine (29cccc1); P1-M2-1 Track 4 spec draft (D-9) and M2-2 rules and sampler (053d96f). Round recorded in [REVIEW-2026-09-25-round3.md](REVIEW-2026-09-25-round3.md); RESUME.md refreshed with Waves C and D. New owner questions: P1 Q-18–Q-25, P4 Q027–Q031, P5 Q020–Q023 | Parent reruns: P4 Maven 106 tests; P5 536 pytest + verify-evidence + packet regeneration check + all 20 case evidence files consistent; P1 756 pytest + validate + mock eval. CI runs not observed (no gh CLI) | Owner Tier 1 and the P5-M2-4 packet review; then Wave C (P1-M2-6, P2-M4-1/2 + M5-1, P5-M5-1/2) |
