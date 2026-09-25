# Resume plan: continue from here

[Plans index](README.md) · [Review 2026-09-25](REVIEW-2026-09-25.md) · [Progress](PROGRESS.md) · [Runbook](RUNBOOK.md)

Written 2026-09-25, after the second implementation round. It picks up exactly
where work stopped. The [review](REVIEW-2026-09-25.md) records what exists and
why. This file says what to do next and in what order. When this plan is
superseded, replace it and add a new review file rather than editing history.

## Where things stand

| ID | Last commit | Built | Next agent task | Waiting on the owner |
|---|---|---|---|---|
| P0 Nurse Handoff | `8ab0cce` (loop) | tickets 001–008 of 12 | the loop continues with 009 | G1 release gate when `DONE` appears |
| P1 NurseBench | `bfffb2f` | M0; Track 1 spec, protocols, calculators, 150 items | P1-M1-6 task and scorer, then M1-7 report | D-3, API keys, M1-5 hand items, calculator sign-off, Q-10–Q-15 |
| P2 Charge Assign | `68c3e17` | rubric, spec, calculator, 50 scenarios, H1–H5 | P2-M3-1 medium and soft constraints, M3-2 baselines, M3-3 benchmark | spot-check 5 scenarios, M2-2 constraint review, Q015–Q020 |
| P3 Dysphagia | `765e202` | spec, Questionnaire, page, 15 fixture responses | P3-M3-3 CQL library, M3-4 CQL tests | Q019 gating, Q020 and M2-4 wording, Docker |
| P4 Grounded Handoff | `aacdfda` | spec, citation check, Synthea pin, overlay | P4-M3-2 fact sheet, M4-2 value fidelity, M4-5 omissions | Q021–Q026, inventory review, Docker |
| P5 Stroke Agent | `48b993c` | digest, specs, sampler, gold outcomes, segmenter, date checks | P5-M2-3 template chart generator (first 20), M4-1 measure engine | D-7, Q016–Q019 |

## Start of the next session

1. Say: **"Resume the Nursing OS portfolio from plans/RESUME.md."** The
   startup hook and project resolver route this to the hub.
2. Resolve the project, then read this file,
   [PROGRESS.md](PROGRESS.md) and the review's findings:
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
6. Check usage. The weekly limit resets **Sep 27, 5am (Pacific)**. Run at
   most **three agents at once**.

## Owner queue, in priority order

### Tier 1: needed for NurseBench v0.1 (due Oct 31)

1. **D-3.** Choose the model roster (3 frontier + 1 open-weights) and a hard
   API budget cap. Set the API keys as user environment variables, never in a
   repo. Needed by about **Oct 25** for P1-M1-8.
2. **P1-M1-5.** Write the 30 hand-written items, and review the 44 generated
   edge-case items (`reviewed: true` once reviewed).
   - These are meant to be RN-authored, which is why they are not delegated.
   - If you prefer, delegate them under D-9. They would then count as
     agent-drafted and RN-reviewed, not RN-authored.
3. **P1 calculator sign-off (P1-M1-3).** Check the derived expected values
   listed in `nursebench/memory/HANDOFF.md`. Answer Q-10 to Q-15:
   - Q-13 decides the held-out size (currently 12%).
   - The others confirm conservative readings.

### Tier 2: unblocks the other repos

4. **Install Docker Desktop with WSL2.** Needed for P3 M4 (`$apply`) and all
   HAPI loading in P4. Set a WSL memory cap in `%UserProfile%\.wslconfig`,
   and stop Qwen while HAPI runs.
5. **D-7.** Choose how P5 is orchestrated: Claude Agent SDK, `claude -p`
   scripts, or Java. The choice also needs a model and budget, like D-3.
6. **P3-Q019:** should a blank exclusion hide the water trial? This is the
   current literal spec reading; the alternative shows the trial unless an
   exclusion is answered "Yes".
   **P3-Q020 and P3-M2-4:** check the Questionnaire wording. Open it with
   `npm run site`.
7. **P2:** spot-check 5 of the 50 scenarios (P2-M1-4), review H1–H5 against
   the spec (P2-M2-2), and answer Q015–Q020.
8. **P4:** answer Q021–Q026 and review `docs/synthea-inventory.md`. Its
   provenance says pending.
9. **P5:** answer Q016–Q019.

### Tier 3: before any release, or when convenient

10. **Source checks (31 rows).** Clear these before each repo's first public
    release. Each needs a source an agent could not open (paywalls, member
    logins, reCAPTCHA):
    - P1: Q-2, Q-3, Q-4, Q-5, Q-7
    - P2: Q006–Q009, Q013
    - P3: Q007, Q013–Q018
    - P4: Q006, Q007 (needs HAPI), Q015–Q017, Q019, Q020
    - P5: Q007–Q012, Q015
11. **NurseBench README:** write "Why a nurse built it" in your own words.
12. **P0 G1 release gate:** when `DONE` appears in the hub, follow
    [P0 plan § G1](projects/P0-nurse-handoff.md#p0-g1-v01-release-gate-owner):
    review, tag `v0.1.0`, tick "v0.1 released", delete `DONE`, commit and push.
13. **Remaining decisions:** D-2 (at the v0.2 release), D-5 and D-6.
14. **Optional:**
    - ask GitHub Support to purge the pre-scrub SHAs (listed in hub
      DECISIONS)
    - change the author email on the two oldest hub commits to the noreply
      address (needs a force-push)

## Agent queue, in waves

Run one wave at a time, at most three agents at once. The parent reviews each
diff, reruns verification, commits and pushes, then updates PROGRESS.md.

### Wave A: next session (no owner dependency)

| Agent | Repo | Tasks | Acceptance | Notes |
|---|---|---|---|---|
| A1 | P1 | **P1-M1-6** `task.py` and `scorer.py`, then **P1-M1-7** `report.py` and `bootstrap.py` | A unit test for each critical-error type and for the format-failure path; deterministic CIs; report written from mock results | Critical path for Oct 31. No paid calls: test with synthetic model outputs and the mock model. |
| A2 | P3 | **P3-M3-3** CQL library with ELM compiled in the Maven build (portable JDK), then **P3-M3-4** CQL tests against all 15 fixtures | Every fixture matches `docs/fixtures.md` | Pin the CQL version and translator. E12 and E13 go straight to the CQL (P3-Q019). No HAPI needed. |
| A3 | P2 | **P2-M3-1** M1 and S1–S4 with ConstraintVerifier tests for spec cases 24–36, **P2-M3-2** baselines, **P2-M3-3** benchmark over 50 scenarios | Tests pass; `results/summary.csv` produced by a real benchmark run | Soft scores need ×100 scaling or BigDecimal (spec Appendix B). |

### Wave B: after Wave A lands

| Agent | Repo | Tasks | Acceptance | Notes |
|---|---|---|---|---|
| B1 | P4 | **P4-M3-2** fact-sheet builder, **P4-M4-2** value-fidelity verifier (layer 2), **P4-M4-5** omission check | Tests with seeded mismatches and every manifest state | Deterministic; works on overlay output without HAPI or an LLM |
| B2 | P5 | **P5-M2-3** template-based chart-packet generator for C01–C20 only, then **P5-M4-1** measure engine that reuses `gold.py` paths | 20 packets with their truth vectors; one test per algorithm path | No LLM. Stop after 20 packets for the owner's validation (P5-M2-4) before generating the other 40. |
| B3 | P1 | **P1-M2-1** Track 4 NIHSS clinical spec under D-9 (provenance pending), then **P1-M2-2** score-vector sampler | Spec complete; sampler tests | November is a light month. Optional if usage is tight. |

### Blocked until an owner action

| Work | Unblocked by |
|---|---|
| P1-M1-8 model runs, then M1-9 results | D-3, API keys, the owner's go-ahead after the 20-item smoke run |
| P3-M4-1 to M4-3 HAPI and `$apply`; P3-M5-1 CI | Docker Desktop |
| P4-M1-1b, 2b, 4b HAPI loading and US Core validation; P4-M2 SMART launch | Docker Desktop, then P3-M4-1 |
| P4-M3-3 LLM generation; P4-M4-3 judge | A model and budget decision (as for D-3) |
| P5-M3-3 extractors, then M4-3 end-to-end | D-7 and a model and budget decision |
| P5-M2-5 remaining 40 charts | Owner validation of the first 20 (P5-M2-4) |
| Every kappa, rating, blinded review or blind abstraction | The owner or named human reviewers ([RUNBOOK §1](RUNBOOK.md#1-roles-and-the-authorship-boundary)) |

## Agent brief template

Use this for every agent. It carries the rules that kept the last two rounds
clean.

```text
You are implementing <task IDs> in the owner's private repo C:\Users\14087\Desktop\<repo>
(<project>, P<n> of the Nursing OS portfolio). Work ONLY inside that repo; do not edit
C:\Users\14087\Desktop\Nursing_OS_Project. Do NOT commit, push or tag — the parent reviews and commits.
Read first: AGENTS.md, TASKS.md, memory/HANDOFF.md, recent memory/DECISIONS.md, memory/QUESTIONS.md,
the signed-off clinical docs, and the plan at ..\Nursing_OS_Project\plans\projects\<plan>.md.
Rules: signed-off clinical docs are not edited — implement the most conservative reading of any
ambiguity, note it in code, and add a QUESTIONS row. New clinical content follows D-9 (provenance line,
Owner RN review: pending). Generated data items are authored_by: agent, reviewed: false. No paid model
calls. No new dependencies unless needed (explain). Tick only verified tasks; rewrite HANDOFF (≤40 lines);
append DECISIONS. Verification (must pass): <command from the table below>.
Report back concisely: files changed, coverage, test counts, ambiguities logged, verification results.
```

## Verification commands

| Repo | Command (from the repo root) |
|---|---|
| Hub | `powershell -NoProfile -ExecutionPolicy Bypass -File tests/verify.ps1` |
| P1 | `uv sync --locked`; `uv run --locked pytest -q`; `uv run --locked python -m nursebench.validate`; mock eval: `uv run --locked inspect eval nursebench/hello_world.py --model mockllm/model --log-dir <fresh %TEMP% dir> --display none`, then `uv run --locked python scripts/check_mock_eval.py <dir>`. Delete the dir afterwards. |
| P2, P4 | PowerShell: `$env:JAVA_HOME='C:\Users\14087\.local\share\nursing-os-tools\jdk21\jdk-21.0.12.1+1'; $env:Path="$env:JAVA_HOME\bin;$env:Path"; .\mvnw.cmd -B -ntp verify` |
| P3 | `npm ci --ignore-scripts`; `npm run verify` |
| P5 | `uv sync --locked`; `uv run --locked pytest -q`; `uv run --locked verify-evidence tests/fixtures/mechanical-valid.json` |

Test counts at this checkpoint: hub 54, P1 420, P2 69, P3 71, P4 47, P5 344.

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
- **Limits:** if a usage limit stops agents, resume them from their
  transcripts with SendMessage. Never restart them from scratch; their
  partial work is on disk.

## Calendar check

| Date | Milestone | Status |
|---|---|---|
| Oct 11 | P1 M0 | Done early (Sep 24–25) |
| ~Oct 25 | D-3 needed for P1 runs | Open |
| Oct 31 | NurseBench v0.1 public | On track if Tier 1 owner items and Wave A land in the next ~3 weeks |
| November | Light month (NCA-GENL); only P1 Track 4 | Planned |
| Dec 1–8 | No build work (CAHIMS) | Planned |
| Jan 31, 2027 | NurseBench v1.0 | Planned |
| Feb–Jun 2027 | P2–P5 releases | Ahead of schedule because of parallel work (D-8); release targets unchanged |
