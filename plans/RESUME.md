# Resume plan: continue from here

[Plans index](README.md) · [Latest review](REVIEW-2026-09-25-round3.md) · [Progress](PROGRESS.md) · [Runbook](RUNBOOK.md)

Written 2026-09-25, after the third implementation round (Waves A and B).
It picks up exactly where work stopped. The
[round-3 review](REVIEW-2026-09-25-round3.md) records what was built and
why; the [first review](REVIEW-2026-09-25.md) covers Sep 24–25 before that.
This file says what to do next and in what order. When this plan is
superseded, replace it and add a new review file rather than editing history.

## Where things stand

| ID | Last commit | Built | Next agent task | Waiting on the owner |
|---|---|---|---|---|
| P0 Nurse Handoff | `8ab0cce` (loop) | tickets 001–008 of 12 | the loop continues with 009 | G1 release gate when `DONE` appears |
| P1 NurseBench | `053d96f` | M0; Track 1 spec, calculators, 150 items, task, scorer, report; Track 4 spec draft, rules, sampler | P1-M2-6 Track 4 task and scorer (Wave C) | D-3, API keys, M1-5 hand items, calculator sign-off, Q-10–Q-25, Track 4 spec and rule review |
| P2 Charge Assign | `6b08d18` | rubric, calculator, 50 scenarios, H1–H5, M1, S1–S4, baselines, benchmark results | P2-M4-1 floor map, M4-2 reasons, M5-1 replanning (Wave C) | M1-4 spot-check, M2-2 review, M3-4 results and limitations, Q015–Q027 |
| P3 Dysphagia | `b1228b1` | spec, Questionnaire, page, 15 fixtures, CQL library with ELM build and fixture tests | P3-M4-1..3 HAPI on the portable JDK, PlanDefinition, `$apply` fixture runner (Wave C) | Q019, Q020–Q022, M2-4 wording, CQL review |
| P4 Grounded Handoff | `bfe05aa` | spec, citation check, Synthea pin, overlay, fact sheet, value fidelity, omission check | P4-M1-1b/2b/4b HAPI loading (Wave D, after P3-M4-1); M3-4 citation view, M5-4 Provenance | Q021–Q031, inventory review, model and budget |
| P5 Stroke Agent | `29cccc1` | digest, specs, sampler, gold, segmenter, date checks, packets C01–C20, measure engine | P5-M5-1 router, M5-2 review page (Wave C) | P5-M2-4 review of 20 packets, M4-2 engine review, D-7, Q016–Q023 |

## Start of the next session

1. Say: **"Resume the Nursing OS portfolio from plans/RESUME.md."** The
   startup hook and project resolver route this to the hub.
2. Resolve the project, then read this file,
   [PROGRESS.md](PROGRESS.md) and the round-3 review's findings:
   `node C:/Users/14087/.agent-memory/project-system/project-memory.cjs boot "resume nursing os portfolio" --owner --json`
3. Confirm the six repos are clean and synced with GitHub:
   ```bash
   cd C:/Users/14087/Desktop && for r in Nursing_OS_Project nursebench charge-assign dysphagia-screen-fhir grounded-handoff stroke-abstraction-agent; do git -C $r fetch -q origin; echo "$r dirty=$(git -C $r status --porcelain | wc -l) head=$(git -C $r rev-parse --short HEAD) remote=$(git -C $r rev-parse --short origin/main)"; done
   ```
4. Check the loop:
   `powershell -NoProfile -File C:/Users/14087/Desktop/loops/controller.ps1 status`.
   If a hub ticket is running, do not edit the hub until it finishes.
5. Check what the owner answered since this plan. Look for changed rows in
   each repo's `memory/QUESTIONS.md` and new owner entries in the hub's
   `memory/DECISIONS.md`. Apply the answers before starting new agent work.
   An answer that changes a reading (for example P3-Q019, P1-Q-16/Q-17) is
   a small code change plus its test; do it first.
6. Check CI on GitHub for the round-3 commits (not observed; round-3
   finding 1). Check usage: the weekly limit resets **Sep 27, 5am
   (Pacific)**. Run at most **three agents at once**.

## Owner queue, in priority order

### Tier 1: needed for NurseBench v0.1 (due Oct 31)

1. **D-3.** Choose the model roster (3 frontier + 1 open-weights) and a hard
   API budget cap. Set the API keys as user environment variables, never in a
   repo. Needed by about **Oct 25** for P1-M1-8.
2. **P1-M1-5.** Write the 30 hand-written items, and review the 44 generated
   edge-case items (`reviewed: true` once reviewed). Delegation under D-9 is
   possible, but then they count as agent-drafted and RN-reviewed.
3. **P1 calculator sign-off (P1-M1-3)** and questions **Q-10 to Q-17**.
   Q-13 decides the held-out size. **Q-16 and Q-17** fix how the scorer
   reads format failures and critical errors; answer them before the smoke
   run.

### Tier 2: unblocks the other repos

4. **Docker Desktop: now a fallback only.** Owner decision 2026-09-25: Wave C
   first tries running HAPI on the portable JDK 21 (C1). Install Docker Desktop
   with WSL2 only if that route fails; then set a WSL memory cap in
   `%UserProfile%\.wslconfig`. Either way, stop Qwen while HAPI runs.
   **Also:** the Nurse Handoff loop's ticket 009 run on Sep 25, 23:00 UTC failed
   with `401 Unauthorized` (Codex API key rejected). Fix the Codex login, or the
   loop keeps retrying without progress.
5. **P5-M2-4:** review the 20 chart packets with the form in
   `stroke-abstraction-agent/data/review/P5-M2-4/`. The other 40 cases wait
   for this. Also answer Q020–Q023 (Q023: C14's discharge medicines after
   comfort measures).
6. **D-7.** Choose how P5 is orchestrated: Claude Agent SDK, `claude -p`
   scripts, or Java, plus a model and budget.
7. **P3:** Q019 (blank-exclusion gating), Q020–Q022 and M2-4 wording
   (`npm run site`); read the CQL (`input/cql/DysphagiaScreenLogic.cql`).
8. **P2:** spot-check 5 scenarios (M1-4), review H1–H5 (M2-2), read
   `results/summary.csv` and write the limitations (M3-4), and answer
   Q015–Q027. Q026 asks whether the hard-aware baselines are a fair
   comparison.
9. **P4:** answer Q021–Q031 and review `docs/synthea-inventory.md` and
   `docs/fact-sheet-and-verifiers.md`.
10. **P1 Track 4:** review the spec and the rule list (§5.4) and answer
    Q-18–Q-25; this is the remaining acceptance step for P1-M2-2.

### Tier 3: before any release, or when convenient

11. **Source checks (31 rows).** Clear these before each repo's first public
    release (paywalls, member logins, reCAPTCHA):
    - P1: Q-2, Q-3, Q-4, Q-5, Q-7
    - P2: Q006–Q009, Q013
    - P3: Q007, Q013–Q018
    - P4: Q006, Q007 (needs HAPI), Q015–Q017, Q019, Q020
    - P5: Q007–Q012, Q015
12. **NurseBench README:** write "Why a nurse built it" in your own words.
13. **P0 G1 release gate:** when `DONE` appears in the hub, follow
    [P0 plan § G1](projects/P0-nurse-handoff.md#p0-g1-v01-release-gate-owner).
14. **Remaining decisions:** D-2 (at the v0.2 release), D-5 and D-6.
15. **Optional:** GitHub Support purge of pre-scrub SHAs; noreply author
    email on the two oldest hub commits (force-push); install the GitHub CLI
    (`winget install GitHub.cli`) so agents can check CI.

## Agent queue, in waves

Run one wave at a time, at most three agents at once. The parent reviews each
diff, reruns verification, commits and pushes, then updates PROGRESS.md.
Waves C and D have no owner dependency, but they build on drafts that are
still pending owner review; keep every reading easy to change. Wave C has four
agents: start C1–C3, then C4 when the first one finishes.

### Wave C: next session

| Agent | Repo | Tasks | Acceptance | Notes |
|---|---|---|---|---|
| C1 | P3 | **P3-M4-1** HAPI FHIR JPA server on the portable JDK 21 (no Docker), **P3-M4-2** PlanDefinition and ActivityDefinitions, **P3-M4-3** `$apply` fixture runner | HAPI starts locally with Clinical Reasoning; resources load; `$apply` matches the expected actions for all 15 fixtures | Owner decision 2026-09-25. Pin the HAPI starter version; embedded H2; a start/stop script and a JVM heap cap; record free RAM and stop Qwen first. Check that the pinned HAPI's CQL engine matches the Library (CQL 1.5, cqframework 5.3.0) and keep the Library as CQL text (round-3 finding). Keep a `docker-compose.yml` with the same pinned version only for GitHub CI (P3-M5-1). If the Java route cannot work, stop and report why; do not install Docker. |
| C2 | P1 | **P1-M2-6** Track 4 task and scorer: per-item accuracy, confusion matrix, total MAE, major-error %, hallucinated-item rate | Unit tests with hand-built fixtures; mock-model run only | Use the Track 4 spec draft and `rules.py`; no narratives (M2-3 is owner-written, M2-4 needs a model decision). Reuse `nursebench/common/report.py`. |
| C3 | P2 | **P2-M4-1** floor-map grid and load bars, **P2-M4-2** plain-language reasons, **P2-M5-1** replanning demo | Renders for any scenario; one reason per assignment; test shows minimum reassignments | Timefold Community lacks `SolutionManager.analyze`: build reasons from the plain-Java replay. Wording stays agent-drafted for owner review (M4-3). |
| C4 | P5 | **P5-M5-1** router with confidence and conflict thresholds, **P5-M5-2** local review page with accept/override and a decision log | Configurable and tested; works locally | No LLM: drive both from synthetic extractor outputs derived from C01–C20 truth vectors with seeded noise, clearly marked as fixtures. |

### Wave D: after Wave C lands

| Agent | Repo | Tasks | Acceptance | Notes |
|---|---|---|---|---|
| D0 | P4 | **P4-M1-1b**, **2b**, **4b**: load the Synthea and overlay bundles into the same Java-run HAPI and validate against US Core 6.1.0 | Patients queryable; validator results recorded | Only after C1 works. Reuse P3's start script (copied, with a note of its origin). Loading must keep resource ids (round-3 P4 finding). |
| D1 | P4 | **P4-M3-4** handoff view with clickable citations, **P4-M5-4** DocumentReference plus Provenance output | Works on the demo patient from overlay files; Provenance validates structurally | No HAPI, no LLM: use a hand-written demo handoff that passes layers 1–2. |
| D2 | P1 | **P1-M3-1** Track 2 spec under D-9 (provenance pending), then the deterministic part of **P1-M3-3** `perturb.py` | Spec complete with citations; templated perturbations tested | MedlinePlus and BE FAST only; no Schmitt-Thompson. M3-2 scenarios are owner-adjudicated; LLM-assisted variants wait for a model decision. |
| D3 | P1 | **P1-M4-2** `readability.py` and the numeric-fidelity regex | Tests, including numbers that must survive unchanged | Source snapshots wait for the owner's page list (P1-M4-1). Optional if usage is tight. |

### Blocked until an owner action

| Work | Unblocked by |
|---|---|
| P1-M1-8 model runs, then M1-9 results | D-3, API keys, Q-16/Q-17, the owner's go-ahead after the 20-item smoke run |
| P1-M2-4 narrative generator; P1-M3-5 grader; P1-M4-3 checklist grader | D-3 (models and budget) |
| P4-M2 SMART launch | P4 HAPI loading (Wave D0), which needs P3-M4-1 (Wave C1) |
| Docker Desktop install | Only if the Java HAPI route in C1 fails |
| P4-M3-3 LLM generation; P4-M4-3 judge; P4-M5 evaluation | A model and budget decision (as for D-3) |
| P5-M3-3 extractors, then M4-3 end-to-end; P5-M6 | D-7 and a model and budget decision |
| P5-M2-5 remaining 40 charts | Owner review of the first 20 (P5-M2-4) |
| P2-M5-2 blinded review packet | Owner's M3-4 read of the results (so the packet uses accepted settings) |
| Every kappa, rating, blinded review or blind abstraction | The owner or named human reviewers ([RUNBOOK §1](RUNBOOK.md#1-roles-and-the-authorship-boundary)) |

## Agent brief template

Use this for every agent. It carries the rules that kept the last three
rounds clean.

```text
You are implementing <task IDs> in the owner's private repo C:\Users\14087\Desktop\<repo>
(<project>, P<n> of the Nursing OS portfolio). Work ONLY inside that repo; do not edit
C:\Users\14087\Desktop\Nursing_OS_Project. Do NOT commit, push or tag — the parent reviews and commits.
Environment: Windows 11, PowerShell 7 primary (Git Bash available). <JDK/Node/uv notes for the repo>.
Read first: AGENTS.md, TASKS.md, memory/HANDOFF.md, recent memory/DECISIONS.md, memory/QUESTIONS.md,
the signed-off clinical docs, and the plan at ..\Nursing_OS_Project\plans\projects\<plan>.md.
Rules: signed-off clinical docs are not edited — implement the most conservative reading of any
ambiguity, note it in code, and add a QUESTIONS row. New clinical content follows D-9 (provenance line,
Owner RN review: pending). Generated data items are authored_by: agent, reviewed: false. Human-measurement
tasks stay human. No paid model calls. No new dependencies unless needed (explain). Keep CI green.
Tick only verified tasks; rewrite HANDOFF (≤40 lines); append DECISIONS. Never name the owner's employer.
Save work as you go; if a usage limit stops you, you will be resumed from your transcript.
Verification (must pass): <command from the table below>. Baseline test count: <n>.
Report back concisely: files changed, coverage, test counts, ambiguities logged, verification results.
```

## Verification commands

| Repo | Command (from the repo root) |
|---|---|
| Hub | `powershell -NoProfile -ExecutionPolicy Bypass -File tests/verify.ps1` |
| P1 | `uv sync --locked`; `uv run --locked pytest -q`; `uv run --locked python -m nursebench.validate`; mock eval: `uv run --locked inspect eval nursebench/hello_world.py --model mockllm/model --log-dir <fresh %TEMP% dir> --display none`, then `uv run --locked python scripts/check_mock_eval.py <dir>`. Delete the dir afterwards. |
| P2, P4 | PowerShell: `$env:JAVA_HOME='C:\Users\14087\.local\share\nursing-os-tools\jdk21\jdk-21.0.12.1+1'; $env:Path="$env:JAVA_HOME\bin;$env:Path"; .\mvnw.cmd -B -ntp verify` |
| P2 benchmark | `.\mvnw.cmd -B -ntp test -Dtest=BenchmarkRunnerTest "-Dcharge.benchmark=true"` (about 4 minutes; rewrites `results/`) |
| P3 | Set JAVA_HOME as for P2, then `npm ci --ignore-scripts`; `npm run verify` (SUSHI, Node tests and the Maven CQL build) |
| P5 | `uv sync --locked`; `uv run --locked pytest -q`; `uv run --locked verify-evidence tests/fixtures/mechanical-valid.json`; `uv run --locked python -m stroke_abstraction.packets --check` |

Test counts at this checkpoint: hub 54, P1 756, P2 107 (1 skipped),
P3 78 Node + 55 JUnit, P4 106, P5 536.

## Operating rules for resumed work

- **Hub edits:** commit and push them right away. The loop will not start
  while the hub has uncommitted changes. Check `controller.ps1 status` first.
- **Owner-only actions:** never record an owner review, tick an owner task,
  or answer an owner question on the owner's behalf. The only exception is
  applying an owner's explicit statement, quoted in DECISIONS.
- **Human judgments:** human-measurement tasks stay human. Agents prepare
  packets and forms only.
- **Paid runs:** a 20-item smoke run and a cost projection against the
  budget cap come first.
- **After each wave:** update the PROGRESS dashboard and session log, and add
  a hub LOG line. After a large round, write a new review file and refresh
  this plan.
- **Line endings:** hub files are LF. Python's `write_text` on Windows
  writes CRLF; normalize before committing.
- **Limits:** if a usage limit stops agents, resume them from their
  transcripts with SendMessage. Never restart them from scratch; their
  partial work is on disk.

## Calendar check

| Date | Milestone | Status |
|---|---|---|
| Oct 11 | P1 M0 | Done early (Sep 24–25) |
| ~Oct 25 | D-3 needed for P1 runs | Open |
| Oct 31 | NurseBench v0.1 public | On track: the harness is built; needs D-3, M1-5, the calculator sign-off, Q-16/Q-17, then the runs |
| November | Light month (NCA-GENL); only P1 Track 4 | Track 4 spec, rules and sampler drafted early; owner review and narratives remain |
| Dec 1–8 | No build work (CAHIMS) | Planned |
| Jan 31, 2027 | NurseBench v1.0 | Planned |
| Feb–Jun 2027 | P2–P5 releases | Ahead of schedule (D-8); release targets unchanged |
