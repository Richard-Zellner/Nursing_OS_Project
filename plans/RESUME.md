# Resume plan

[Plans index](README.md) · [Progress](PROGRESS.md) · [Session log](SESSION-LOG.md) · [Runbook](RUNBOOK.md)

Current as of 2026-09-27. History lives in the [session log](SESSION-LOG.md) and the review files. Keep this file short
and current: replace it, don't append to it.

## Where things stand

| ID | Built | Next | Needs the owner |
|---|---|---|---|
| P0 Nurse Handoff | v0.1.0 released (tag `v0.1.0`) | v0.2 tickets 101–110, run by the Codex loop (blocked 07:00–13:15 UTC 2026-09-27; fixed by running the worker without WindowsApps on PATH, see `loops/supervisor.py` `worker_env`) | Q-002/Q-003 input handling for v0.2 |
| P1 NurseBench | Track 1 harness and items; Track 4, 2 and 5 specs, data, scorers and tools; NIHSS sampler (P1-M2-2); Track 2 reply task and 240 phrasing variants (P1-M3-3; 60 held out); Track 5 task with a language check; narrative generator built (not run, Q-55); recommended D-3 roster and cap | smoke and full runs after the D-3 go | the four API keys (the D-3 go), Q-50, Q-51, Q-55, RN review, label review of the variants, grader labels, PEMAT-P |
| P2 Charge Assign | solver, baselines, benchmark results, floor map, reasons, replanning, review packet | polish | the blinded charge-nurse review, RN read |
| P3 Dysphagia | spec 0.2, CQL, HAPI `$apply` (178 tests), HAPI CI green; v0.1.0 prepared | polish | RN re-read, dentures question, then tag v0.1.0 and go public |
| P4 Grounded Handoff | FHIR load (US Core 0 errors), fact sheet, three verifier layers, view, SMART launch, export, harness; first model run (25 patients, 4 arms; loop cut value errors per handoff 1.48 → 0.04) | judge the primary and loop-on arms for the headline; prompt v2 (P4-Q055) | support labels and ratings (packets ready), A-13 and RN review |
| P5 Stroke Agent | 60 cases, engine, router, review page, metrics, runner, D-7 extractor; real 60-case runs with prompts 0.1 and 0.2 (element accuracy 98.8% and 99.1%); real-data metrics | open-weights comparison (P5-M6-3): the local Qwen llama-server listens on 127.0.0.1:65060 when started and needs about 15–19 GB of RAM, so run it when nothing else is heavy; a repeat run would measure run-to-run variation | P5-Q035 (GWTG login), RN review, blind abstraction, engine review |

The owner's delegation (hub DECISIONS, 2026-09-26 and 2026-09-27) lets agents answer questions and give approvals as
"delegated agent decisions". It never covers:
- RN attestation;
- human measurement;
- the owner's first-person writing;
- releases and visibility.

The owner's own to-do list is a private checklist on the owner's Desktop.

## Start a session

1. Say **"Resume the Nursing OS portfolio from plans/RESUME.md."**
2. Boot: `node ~/.agent-memory/project-system/project-memory.cjs boot "resume nursing os portfolio" --owner --json`
3. Check that all six repos are clean and synced:
   ```bash
   cd ~/Desktop && for r in Nursing_OS_Project nursebench charge-assign dysphagia-screen-fhir grounded-handoff stroke-abstraction-agent; do git -C $r fetch -q origin; echo "$r dirty=$(git -C $r status --porcelain | wc -l) head=$(git -C $r rev-parse --short HEAD) remote=$(git -C $r rev-parse --short origin/main)"; done
   ```
4. Check the loop with `powershell -NoProfile -File "$HOME\Desktop\loops\controller.ps1" status` (PowerShell), and don't edit
   the hub during a run. The controller runs every 4 hours on the hour (03, 07, 11, 15, 19 and 23 UTC).
5. Check CI with `gh run list --repo Richard-Zellner/<repo>`. `gh` is installed per-user and logged in.
6. Apply any new owner answers in each repo's `memory/QUESTIONS.md` first.

## How agent work runs

- **One agent per repo.** Several can run in parallel if the owner asks; the owner asked for five on 2026-09-27.
- **Agents commit locally and never push.** The parent reruns verification, pushes, checks CI, then records the round
  in [SESSION-LOG.md](SESSION-LOG.md).
- **Brief each agent with:**
  - the repo;
  - the owner's instruction, quoted;
  - the limits above;
  - the environment (JDK, HAPI ports and the RAM guard);
  - the verification commands below;
  - "local commits only".
- **CI runs on Windows and Linux.** Tests must write files with explicit bytes or newlines; a Windows-only pass once
  hid a Linux failure.

## Verification

| Repo | Command (from the repo root) |
|---|---|
| Hub | `powershell -NoProfile -ExecutionPolicy Bypass -File tests/verify.ps1` |
| P1 | `uv sync --locked`; `uv run --locked pytest -q` (again with `private/t2_escalation/` hidden); `uv run --locked python -m nursebench.validate`; hello_world mock eval with `scripts/check_mock_eval.py` |
| P2, P4 | `$env:JAVA_HOME="$env:USERPROFILE\.local\share\nursing-os-tools\jdk21\jdk-21.0.12.1+1"; $env:Path="$env:JAVA_HOME\bin;$env:Path"; .\mvnw.cmd -B -ntp verify` |
| P3 | JAVA_HOME as above; `npm ci --ignore-scripts`; `npm run verify`; with HAPI, `.\scripts\hapi\hapi.ps1 test` |
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

## Rules

- **Evidence:** results come only from real runs, with the model ID and date. Mock and smoke runs never go in `results/`.
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
