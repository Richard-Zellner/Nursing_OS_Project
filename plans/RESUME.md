# Resume plan: continue from here

[Plans index](README.md) · [Latest review](REVIEW-2026-09-25-round4.md) · [Progress](PROGRESS.md) · [Runbook](RUNBOOK.md)

Written 2026-09-25 (evening, Pacific), after the fourth implementation
round: Waves C and D and Nurse Handoff tickets 009–015.
- The [round-4 review](REVIEW-2026-09-25-round4.md) records what was built.
- [Round 3](REVIEW-2026-09-25-round3.md) and the
  [first review](REVIEW-2026-09-25.md) cover the earlier work.
- This file says what to do next. When it is superseded, replace it and
  add a new review file rather than editing history.

**The owner queue is now the bottleneck.** Almost every remaining agent task
waits for an owner review, answer, decision or release. Wave E below is the
small set of agent work that does not.

## Where things stand

| ID | Last commit | Built | Next agent task | Waiting on the owner |
|---|---|---|---|---|
| P0 Nurse Handoff | `e2ecbe4` | v0.1 build complete (tickets 001–015); `DONE` present; controller baseline and trusted acceptance PASS (2026-09-26 07:00 UTC) | none until v0.2 | **G1 release**; Q-002 |
| P1 NurseBench | `db23296` | Track 1 harness plus pre-run check and cost projection; Track 4 spec draft, rules, sampler, scorer; Track 2 spec draft, private scenarios, perturbations, triage metrics, kappa gate; Track 5 tools; v0.1 README drafts | none unblocked | D-3 (fill `config/runs.toml` from the template), API keys, M1-5, calculator sign-off, Q-10–Q-48, README draft approval |
| P2 Charge Assign | `f5bbd5c` | M1–M3 built with benchmark results; floor map (now port 8084), reasons, replanning; blinded review packet generator; README draft | none unblocked | M1-4, M2-2, M3-4 results and limitations, M4-3 wording, README draft approval, Q015–Q036 |
| P3 Dysphagia | `cf47395` | M1–M4 built; manual "HAPI $apply fixtures" workflow; README and CHANGELOG drafts | none (P3-M5-1 ticks after one green manual run) | run the workflow once (Actions, route `java`), M2-4 wording, CQL and action wording, README approval, Q019–Q028, v0.1.0 release |
| P4 Grounded Handoff | `6abcd99` | M1–M2 done; fact sheet; verifiers 1–2; omissions; citation view; Provenance export; evaluation harness; README draft | none unblocked | Q021–Q047, doc and README reviews, model and budget |
| P5 Stroke Agent | `0e9877c` | packets C01–C20, engine, router, review page, metric code, end-to-end runner with a pluggable extractor, extractor contract, README draft | none unblocked | **P5-M2-4 packet review**, M4-2 engine review, D-7 (implement against docs/extractor-contract.md), price table, README approval, Q016–Q033 |

## Start of the next session

1. Say: **"Resume the Nursing OS portfolio from plans/RESUME.md."**
2. Resolve the project, then read this file,
   [PROGRESS.md](PROGRESS.md) and the round-4 review's findings:
   `node C:/Users/14087/.agent-memory/project-system/project-memory.cjs boot "resume nursing os portfolio" --owner --json`
3. Confirm the six repos are clean and synced with GitHub:
   ```bash
   cd C:/Users/14087/Desktop && for r in Nursing_OS_Project nursebench charge-assign dysphagia-screen-fhir grounded-handoff stroke-abstraction-agent; do git -C $r fetch -q origin; echo "$r dirty=$(git -C $r status --porcelain | wc -l) head=$(git -C $r rev-parse --short HEAD) remote=$(git -C $r rev-parse --short origin/main)"; done
   ```
4. Check the loop:
   `powershell -NoProfile -File C:/Users/14087/Desktop/loops/controller.ps1 status`.
   - Expect `DONE` to be honoured (state `done`) or waiting.
   - If it says `repair` again, read `reason` and fix the cause before anything else.
   - Do not edit the hub while a run is active.
   - If Codex is down and hub work is needed, pause with a session-owned `STOP` and remove it after pushing.
5. Apply owner answers first. Look for changed rows in each repo's
   `memory/QUESTIONS.md` and new owner entries in hub `memory/DECISIONS.md`.
6. Check CI on GitHub (not observed in rounds 3–4) and usage. The weekly
   limit resets **Sep 27, 5am (Pacific)**. Run at most **three agents at once**.

## Owner queue, in priority order

### Tier 1: releases that are ready, and NurseBench v0.1 (due Oct 31)

1. **P0 Nurse Handoff G1.** Once the controller honours `DONE`, follow
   [P0 plan § G1](projects/P0-nurse-handoff.md#p0-g1-v01-release-gate-owner):
   review, answer Q-002 (empty optional strings), tag `v0.1.0`, tick "v0.1
   released", delete `DONE`, commit and push.
2. **D-3.** Choose the model roster (3 frontier + 1 open-weights) and a hard
   API budget cap. Set the API keys as user environment variables. Needed by
   about **Oct 25** for P1-M1-8.
3. **P1-M1-5:** the 30 hand-written items, and review of the 44 edge-case
   items.
4. **P1 calculator sign-off (P1-M1-3)** and **Q-10 to Q-17**. Q-16 and Q-17
   decide how the scorer reads format failures and critical errors; answer
   them before the smoke run.
5. **NurseBench Q-29 and Q-30 (licensing).** Stay with public-domain
   MedlinePlus summaries, ask Ebix for consent, or allow other federal
   sources. Also decide on the one A.D.A.M.-cited value in the signed-off
   Track 1 spec.
6. **Back up `nursebench/private/`.** It holds the only copy of the 40
   Track 2 scenarios (Q-37 decides whether any stay held out).

### Tier 2: reviews that unblock agent work

7. **P5-M2-4:** review the 20 chart packets with the form in
   `stroke-abstraction-agent/data/review/P5-M2-4/`. The other 40 cases wait
   for this. Then review the engine paths (M4-2) and answer Q020–Q026
   (router thresholds Q024; review-log policy Q026).
8. **D-7:** P5 orchestration (Claude Agent SDK, `claude -p` scripts, or
   Java), plus a model and budget.
9. **P3 v0.1.0:**
   - M2-4 wording (`npm run site`);
   - read the CQL and the new action wording (Q024);
   - Q019–Q023;
   - then release (M4-4).

   To run HAPI: `npm run test:hapi`, with JAVA_HOME set and at least 6 GiB free.
10. **P2:**
    - M1-4 spot-check;
    - M2-2 constraint review;
    - M3-4 results and limitations;
    - M4-3 reason wording (open the page with `java -jar target/quarkus-app/quarkus-run.jar`);
    - Q015–Q030. Q026 asks whether the baselines are fair.
11. **P4:**
    - Q021–Q039: example.org code systems Q032, code-status category Q033, the export rules and AI tag Q036–Q037;
    - review the inventory, the verifier doc, the US Core report and the handoff-view doc.
12. **P1 drafts:**
    - Track 4 spec and rule list (Q-18–Q-28);
    - Track 2 spec and scenarios (Q-31–Q-38);
    - Track 5 tool choices (Q-39–Q-43; cmudict licence Q-43).

### Tier 3: before any release, or when convenient

13. **Source checks (31 rows).** Clear before each repo's first public release:
    - P1: Q-2, Q-3, Q-4, Q-5, Q-7
    - P2: Q006–Q009, Q013
    - P3: Q007, Q013–Q018
    - P4: Q006, Q015–Q017, Q019, Q020 (Q007 now has validator evidence)
    - P5: Q007–Q012, Q015
14. **NurseBench README:** write "Why a nurse built it" in your own words.
15. **Remaining decisions:** D-2 (at v0.2), D-5 and D-6.
16. **Optional:**
    - install the GitHub CLI (`winget install GitHub.cli`) so agents can check CI;
    - GitHub Support purge of pre-scrub SHAs;
    - noreply email on the two oldest hub commits;
    - Docker Desktop, only if the Java HAPI route ever fails.

## Agent queue

Run at most three agents at once. The parent reviews each diff, reruns
verification, commits and pushes, then updates PROGRESS.md. Two agents must
never work in the same repo at the same time.

### Wave E: done 2026-09-26 except E4

E1 `0585cc7`, E2 `791ff72` and E3 `821c693` landed (see the PROGRESS session log). E4 stays parked until CI
can be observed. After Wave E there is no unblocked agent work left; every next step waits on an owner item
above.

| Agent | Repo | Tasks | Acceptance | Notes |
|---|---|---|---|---|
| E4 | P3 | **P3-M5-1** CI job running HAPI (Java route or the pinned `docker-compose.yml` service) against all fixtures | Green on GitHub | Only once CI can be observed (the GitHub CLI installed, or the owner checks Actions). |

### Wave F: done 2026-09-26 (owner asked for five agents in parallel)

One agent per repo drafted the PAIR READMEs and CHANGELOGs for owner approval and built the remaining
model-free code: P1 pre-run check and cost projection; P2 review packet generator; P3 manual HAPI workflow
(`hapi-fixtures.yml`, route `java`); P4 evaluation harness; P5 end-to-end runner and extractor contract. Commits
and checks are in the PROGRESS session log. Nothing was ticked on the owner's behalf. After Wave F, the only
agent work left needs an owner action first.

### Wave E as planned (for reference)

| Agent | Repo | Tasks | Acceptance | Notes |
|---|---|---|---|---|
| E1 | P1 | **P1-M3-7** triage metrics (under-triage with EMERGENCY→ROUTINE critical, over-triage, flip rate, safety-element inclusion) and Cohen's kappa code, from spec §9 | Tests with synthetic labels; report section like Track 4's | The grader (M3-5) needs D-3 and the labels (M3-6) are human; the grader stays untrusted until kappa meets the owner's minimum (Q-36). Optionally switch Track 1 to the shared JSON parser with no behaviour change. |
| E2 | P5 | **P5-M6-2** metrics code: evidence validity, the automation-vs-accuracy curve across router thresholds, cost and latency fields | Tests on the extractor-output fixtures; never reported as results | Human–human and human–pipeline kappa need the owner's blind abstraction (M6-1). |
| E3 | P4 | Rerun `HandoffViewHapiTest` when at least 6 GiB is free; then **P4-M2-1/2** SMART EHR launch against the local HAPI (pinned local launcher, or stop and report if that is not feasible offline) | Launch completes; backend fetches the listed resources, paging with `_offset` (HAPI stops paging at 3,000) | Only one HAPI at a time; never stop other apps to free RAM. |
| E4 | P3 | **P3-M5-1** CI job running HAPI (Java route or the pinned `docker-compose.yml` service) against all fixtures | Green on GitHub | Only once CI can be observed (the GitHub CLI installed, or the owner checks Actions). |

### Blocked until an owner action

| Work | Unblocked by |
|---|---|
| P0 v0.2 tickets 101–110 | G1: "v0.1 released" ticked and `DONE` deleted |
| P1-M1-8 runs, then M1-9; P1-M2-4, M3-5, M4-3 (model work) | D-3, API keys, Q-16/Q-17 |
| P1-M4-2 snapshots, then M4-3 | The owner's Track 5 page list (M4-1) and Q-29 |
| P2-M5-2 blinded review packet | The owner's M3-4 read of the results |
| P4-M3-3 generation, M4-3 judge, M5-1/2 evaluation, M5-4b model Device | A model and budget decision |
| P5-M2-5 remaining 40 charts | P5-M2-4 review of the first 20 |
| P5-M3-3 extractors, M4-3 end to end, M6-3 | D-7 plus a model and budget decision |
| Every kappa, rating, blinded review or blind abstraction | The owner or named human reviewers ([RUNBOOK §1](RUNBOOK.md#1-roles-and-the-authorship-boundary)) |

## Agent brief template

```text
You are implementing <task IDs> in the owner's private repo C:\Users\14087\Desktop\<repo>
(<project>, P<n> of the Nursing OS portfolio). Work ONLY inside that repo; do not edit
C:\Users\14087\Desktop\Nursing_OS_Project. Do NOT commit, push or tag — the parent reviews and commits.
Environment: Windows 11, PowerShell 7 primary (Git Bash available). <JDK/Node/uv/HAPI notes for the repo>.
Read first: AGENTS.md, TASKS.md, memory/HANDOFF.md, recent memory/DECISIONS.md, memory/QUESTIONS.md,
the signed-off clinical docs, and the plan at ..\Nursing_OS_Project\plans\projects\<plan>.md.
Rules: signed-off clinical docs are not edited — implement the most conservative reading of any
ambiguity, note it in code, and add a QUESTIONS row. New clinical content follows D-9 (provenance line,
Owner RN review: pending). Generated data items are authored_by: agent, reviewed: false. Human-measurement
tasks stay human. No paid model calls. Only public-domain sources (no A.D.A.M. encyclopedia content).
No new dependencies unless needed (explain). Keep CI green. Tick only verified tasks; rewrite HANDOFF
(≤40 lines); append DECISIONS. Never name the owner's employer. HAPI: check free RAM (≥6 GiB), never stop
other processes, one server at a time, always stop it. Save work as you go; if a usage limit stops you,
you will be resumed from your transcript.
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
| P3 | JAVA_HOME as above; `npm ci --ignore-scripts`; `npm run verify`. With HAPI: `.\scripts\hapi\hapi.ps1 test` (about 2 minutes) |
| P4 with HAPI | `.\scripts\hapi\hapi.ps1 start`; `.\scripts\smart\smart.ps1 start`; `.\mvnw.cmd -B -ntp verify "-Dgroundedhandoff.hapi.required=true"`; `.\scripts\smart\smart.ps1 stop`; `.\scripts\hapi\hapi.ps1 stop` (cohort already loaded; a full `hapi.ps1 test` reloads for about 25 minutes) |
| P5 | `uv sync --locked`; `uv run --locked pytest -q`; `uv run --locked verify-evidence tests/fixtures/mechanical-valid.json`; `uv run --locked python -m stroke_abstraction.packets --check`; `uv run --locked python -m stroke_abstraction.extractor_fixtures --check` |

Test counts at this checkpoint (after Wave F):
- hub: 242
- P1: 1684 locally (1665 + 19 skipped without `private/`)
- P2: 131 (2 opt-in skips)
- P3: 90 Node + 56 JUnit (1 HAPI skip; 86 with HAPI)
- P4: 191 (11 skipped without HAPI and the launcher)
- P5: 966

## Operating rules for resumed work

- **Hub edits:** commit and push them right away. Check `controller.ps1
  status` first. The controller's trusted acceptance check is the truth for
  P0.
- **Owner-only actions:** never record an owner review, tick an owner task,
  answer an owner question or release anything on the owner's behalf. The
  only exception is applying an owner's explicit statement, quoted in
  DECISIONS.
- **Human judgments stay human.** Agents prepare packets and forms only.
- **Paid runs:** a 20-item smoke run and a cost projection against the
  budget cap come first.
- **Sources:** public domain or properly licensed only. MedlinePlus
  health-topic summaries are fine. The A.D.A.M. encyclopedia is not.
- **Held-out data** stays in Git-ignored `private/` until the owner decides.
- **After each wave:** update PROGRESS and the session log, and add a hub LOG
  line. After a large round, write a new review and refresh this plan.
- **Line endings:** hub files are LF. Python's `write_text` on Windows
  writes CRLF, so normalize before committing.
- **Limits:** if a usage limit stops agents, resume them with SendMessage.
  Never restart them from scratch.

## Calendar check

| Date | Milestone | Status |
|---|---|---|
| ~Sep 26 | P0 Nurse Handoff v0.1 | Build complete; owner G1 release |
| Oct 11 | P1 M0 | Done early |
| ~Oct 25 | D-3 needed for P1 runs | Open |
| Oct 31 | NurseBench v0.1 public | Harness ready; needs D-3, M1-5, the calculator sign-off, Q-16/Q-17, Q-29, then the runs |
| November | Light month (NCA-GENL); P1 Track 4 | Spec, rules, sampler and scorer drafted; owner review and narratives remain |
| Dec 1–8 | No build work (CAHIMS) | Planned |
| Dec | P1 Track 2 | Spec, draft scenarios and perturbations drafted early |
| Jan 31, 2027 | NurseBench v1.0 | Planned |
| Feb–Jun 2027 | P2–P5 releases | P3 v0.1 is technically ready now; release targets unchanged |
