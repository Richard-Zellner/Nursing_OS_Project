# Resume plan

[Plans index](README.md) · [Progress](PROGRESS.md) · [Session log](SESSION-LOG.md) · [Runbook](RUNBOOK.md)

Current as of the end of 2026-09-27. History lives in the [session log](SESSION-LOG.md). Keep this file short and
current: replace it, don't append to it.

## Where things stand

All six repos are clean, pushed and green on CI.

| ID | Built | State |
|---|---|---|
| P0 Nurse Handoff | v0.1.0 released; v0.2 tickets 101–103 accepted | The Codex loop runs tickets 104–110 on its own. It was fixed on 2026-09-27: the worker now runs without WindowsApps on PATH (`loops/supervisor.py` `worker_env`). |
| P1 NurseBench | Track 1 harness and 180 items; Tracks 4, 2 and 5 with specs, data, scorers, tasks and tools; NIHSS sampler; 240 Track 2 items (60 held out); Track 5 language check; narrative generator (built, not run) | Waiting for the owner's D-3 go (four API keys), then the smoke and full runs. |
| P2 Charge Assign | solver, baselines, benchmark, floor map (WCAG AA), reasons, replanning, blinded review packet, hardened API | Done until the owner's blinded review. |
| P3 Dysphagia | spec 0.2, CQL, HAPI `$apply` (220/220 on GitHub), accessible form, third-party notices; v0.1.0 prepared | Done until the owner's RN re-read, then release. |
| P4 Grounded Handoff | FHIR load (US Core 0 errors), fact sheet, three verifier layers, view, SMART launch, export, harness; model runs with prompts v1 and v2; judge on 13 patients per arm (not validated); blinded rating packet; P4-Q056 post-hoc re-reading | One stopped task to finish (below); then the owner's labels and ratings. |
| P5 Stroke Agent | 60 cases, engine, router, review page, metrics, runner, D-7 extractor; three real 60-chart runs (98.8%, 99.1% and 99.6% element accuracy; same-prompt runs agree on 99.1% of values); run comparison tool | Waiting for the owner's blind abstraction; the open-weights run needs PC time. |

The owner's delegation (hub DECISIONS, 2026-09-26 and 2026-09-27) lets agents answer questions and give approvals as
"delegated agent decisions". It never covers RN attestation, human measurement, the owner's first-person writing,
releases or visibility.

## What's next

**Agent work, unblocked:**
1. **P4:** finish recording the same-prompt repeat of the v2 run, with no new model calls. All 25 handoffs are
   generated and parked, unverified, in the git-ignored `grounded-handoff/output/stopped-2026-09-27-v2-repeat/`. The
   steps are in P4's HANDOFF, and the analysis plan is in P4's DECISIONS (2026-09-27).
2. **P4-M5-4b:** the model's Device and AI Provenance in the export.
3. **P0:** check each loop acceptance, and keep hub edits between runs.
4. **Loops:** `test_nursing_ticket_001_skeleton_is_valid` fails because its fixture predates the newer verifier checks.
   This is not a loop fault.
5. **P5-M6-3:** the open-weights comparison, only when the owner frees the PC. The local Qwen llama-server is on
   127.0.0.1:65060 and needs about 15–19 GB of RAM.
6. **Optional model work:** the P4 judge on v2 and on patients 14–25; a Haiku and citations-off judge.

**Owner work** (the private checklist on the owner's Desktop has the details):
1. **NurseBench D-3 go:** set the four API keys by about Oct 25 for v0.1 on Oct 31.
2. **Questions:**
   - hub Q-002/Q-003;
   - NurseBench Q-50, Q-51, Q-55 (the narrative model) and Q-56;
   - the Dysphagia dentures question;
   - Stroke Agent P5-Q035.
3. **RN review of agent drafts** in every repo. They are marked "Owner RN review: pending".
4. **Human measurement:**
   - the Charge Assign blinded review;
   - the Grounded Handoff labels and ratings (packets ready);
   - the Stroke Agent blind abstraction;
   - the NurseBench grader labels and PEMAT-P.
5. **First-person writing and releases:**
   - "Why a nurse built it" in each README;
   - releases and visibility (Dysphagia v0.1.0 is ready).

## Start a session

1. Say **"Resume the Nursing OS portfolio from plans/RESUME.md."**
2. Boot: `node ~/.agent-memory/project-system/project-memory.cjs boot "resume nursing os portfolio" --owner --json`
3. Check that all six repos are clean and synced:
   ```bash
   cd ~/Desktop && for r in Nursing_OS_Project nursebench charge-assign dysphagia-screen-fhir grounded-handoff stroke-abstraction-agent; do git -C $r fetch -q origin; echo "$r dirty=$(git -C $r status --porcelain | wc -l) head=$(git -C $r rev-parse --short HEAD) remote=$(git -C $r rev-parse --short origin/main)"; done
   ```
4. Check the loop with `powershell -NoProfile -File "$HOME\Desktop\loops\controller.ps1" status` (PowerShell), and don't
   edit the hub during a run. The controller runs every 4 hours on the hour (03, 07, 11, 15, 19 and 23 UTC).
5. Check CI with `gh run list --repo Richard-Zellner/<repo>`. In an older shell, `gh` may not be on PATH; it is in
   `%LOCALAPPDATA%\Microsoft\WinGet\Packages\GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe\bin\`.
6. Apply any new owner answers in each repo's `memory/QUESTIONS.md` first.

## How agent work runs

- **One agent per repo,** up to five in parallel when the owner asks.
- **Agents commit locally and never push.** The parent reruns verification, pushes, checks CI, then records the round
  in [SESSION-LOG.md](SESSION-LOG.md).
- **Brief each agent with:**
  - the repo;
  - the owner's instruction, quoted;
  - the limits above;
  - the environment (JDK, ports, the RAM guard);
  - the verification commands below;
  - a token cap for any model run.
- **Tell agents:**
  - not to spawn helpers or worktrees;
  - to write commit messages and docs with file tools, never through shell quoting. A quoting slip once ran
    `npm version`.
- **An independent review after each round pays off.** On 2026-09-27 reviews found real bugs in P1, P2, P4 and P5, and
  the P3 HAPI workflow caught a server-only failure.
- **CI runs on Windows and Linux.** Tests must write files with explicit bytes or newlines.

## Verification

| Repo | Command (from the repo root) |
|---|---|
| Hub | `powershell -NoProfile -ExecutionPolicy Bypass -File tests/verify.ps1` |
| P1 | `uv sync --locked`; `uv run --locked pytest -q` (again with `private/t2_escalation/` hidden); `uv run --locked python -m nursebench.validate`; hello_world mock eval with `scripts/check_mock_eval.py` |
| P2, P4 | `$env:JAVA_HOME="$env:USERPROFILE\.local\share\nursing-os-tools\jdk21\jdk-21.0.12.1+1"; $env:Path="$env:JAVA_HOME\bin;$env:Path"; .\mvnw.cmd -B -ntp verify` |
| P3 | JAVA_HOME as above; `npm ci --ignore-scripts`; `npm run verify`; HAPI through the `hapi-fixtures.yml` workflow (`gh workflow run hapi-fixtures.yml -f route=java`) or locally with `.\scripts\hapi\hapi.ps1 test` |
| P4 with servers | `hapi.ps1 start`; `smart.ps1 start`; `mvnw verify "-Dgroundedhandoff.hapi.required=true"`; stop both |
| P5 | `uv sync --locked`; `uv run --locked pytest -q`; `verify-evidence tests/fixtures/mechanical-valid.json`; `packets --check`; `extractor_fixtures --check` |

**Local servers** (one HAPI at a time; never stop other programs; stop what you start):

| Port | Server |
|---|---|
| 8080 | P3 HAPI |
| 8081 | P4 app |
| 8082 | P4 HAPI |
| 8083 | P4 SMART launcher |
| 8084 | P2 app |
| 65060 | the owner's local Qwen (start only with the owner's OK) |

## Rules

- **Evidence:** results come only from real runs, with the model ID and date. Mock and smoke runs never go in
  `results/`, and neither does an unrecorded run.
- **Sources:** public domain or properly licensed only. No A.D.A.M. encyclopedia content (NurseBench Q-29).
- **Held-out data:** it stays in Git-ignored `private/`, backed up in `%USERPROFILE%\Documents\Nursing-OS-backups\`.
- **Hub edits:** commit and push them promptly, between loop runs. Hub files use LF line endings.
- **The employer is never named** (G0).

## Calendar

| Date | Milestone |
|---|---|
| Oct 9 | Nurse Handoff v0.2 (loop) |
| ~Oct 25 | D-3 keys needed for the NurseBench runs |
| Oct 31 | NurseBench v0.1 public |
| Nov | Track 4 (light month: NCA-GENL) |
| Dec 1–8 | No build work (CAHIMS) |
| Jan 31, 2027 | NurseBench v1.0 |
| Feb–Jun 2027 | P2–P5 releases (P3 v0.1 is ready early) |
