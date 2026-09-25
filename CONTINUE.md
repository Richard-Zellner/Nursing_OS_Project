# Continue here

A one-page reference for picking the Nursing OS portfolio back up, for the
owner and for any agent session. Stable facts live here. What's current lives
in [plans/RESUME.md](plans/RESUME.md) (what to do next) and
[plans/PROGRESS.md](plans/PROGRESS.md) (dashboard).

**Current checkpoint:** 2026-09-25, recorded in
[plans/REVIEW-2026-09-25.md](plans/REVIEW-2026-09-25.md). When a new review
and resume plan replace these, update this line.

## How to resume

1. Tell Claude Code (or Codex): **"Resume the Nursing OS portfolio from plans/RESUME.md."**
2. The agent resolves the project, checks that all six repos are clean and in
   sync with GitHub, and checks the Nurse Handoff loop.
3. It applies any answers you have written in a repo's `memory/QUESTIONS.md`.
   Then it runs the next agent wave in RESUME.md, at most three agents at
   once.
4. Your own to-do list is the **Owner queue** in RESUME.md. Tier 1 comes first.

## Where everything is

All six folders are on the Desktop (`C:\Users\14087\Desktop\`). GitHub owner: `Richard-Zellner`.

| ID | Project | Folder | GitHub | Plan |
|---|---|---|---|---|
| Hub | Portfolio hub and plans | `Nursing_OS_Project` | public | [plans/](plans/README.md) |
| P0 | Nurse Handoff (loop-driven) | `Nursing_OS_Project/nurse-handoff` | public (in hub) | [P0](plans/projects/P0-nurse-handoff.md) |
| P1 | NurseBench | `nursebench` | private until release | [P1](plans/projects/P1-nursebench.md) |
| P2 | Charge Assign | `charge-assign` | private until release | [P2](plans/projects/P2-charge-assign.md) |
| P3 | Dysphagia Screen FHIR | `dysphagia-screen-fhir` | private until release | [P3](plans/projects/P3-dysphagia-screen-fhir.md) |
| P4 | Grounded Handoff | `grounded-handoff` | private until release | [P4](plans/projects/P4-grounded-handoff.md) |
| P5 | Stroke Abstraction Agent | `stroke-abstraction-agent` | private until release | [P5](plans/projects/P5-stroke-abstraction-agent.md) |

Every repo uses the same files:

| File | Holds |
|---|---|
| `AGENTS.md` | Rules for agents working in that repo |
| `TASKS.md` | Task state (task IDs match the plan) |
| `memory/HANDOFF.md` | What happened last and what comes next |
| `memory/QUESTIONS.md` | Questions for you. Write your answer in the Answer cell and set Status to `answered`. |
| `memory/DECISIONS.md` | Append-only record of decisions |
| `docs/clinical-spec*.md` | Clinical content, with a provenance line on line 1 |

Hub-only files:
- [plans/MASTER-PLAN.md](plans/MASTER-PLAN.md): finish line and calendar
- [plans/RUNBOOK.md](plans/RUNBOOK.md): how the work is done
- [plans/templates/release-checklist.md](plans/templates/release-checklist.md): what every release needs
- [TASKS.md](TASKS.md): the Nurse Handoff ticket ledger

## Rules that always apply

- **Employer.** Never named, referenced or used anywhere. Work happens outside
  shift hours (G0).
- **Visibility.** New repos stay private until their release (D-4). The hub is
  public, so never put personal details in it.
- **Clinical content.** Agents draft it under D-9. Line 1 of each file reads
  `Provenance: agent-drafted … Owner RN review: pending.` until you sign
  off, and then `Owner RN review: YYYY-MM-DD.`
  - Generated items stay `authored_by: agent`, `reviewed: false` until you
    review them.
  - Public wording says "RN-reviewed", never "RN-authored", for
    agent-drafted content.
- **Human judgments stay human.** Kappa labels, usefulness and safety
  ratings, PEMAT-P, the blinded charge-nurse review and the blind abstraction
  are yours or other named reviewers'.
- **Evidence.** Results come only from real runs, with the model ID and date.
  Every paid run starts with a 20-item smoke run against the budget cap.
- **Hub edits.** Commit and push hub edits right away. The Nurse Handoff loop
  waits while the hub has uncommitted changes.
- **Usage.** Run at most three agents at once. If a usage limit stops them,
  resume them rather than restarting.

## Decisions so far

| Decided | Still open |
|---|---|
| D-1 separate repos · G0 employer rule · D-4 private until release · Morse dropped · D-8 parallel work · D-9 agent-drafted clinical content · RN sign-off for round 1 | D-2 Nurse Handoff ends at v0.2 · **D-3 NurseBench models and budget (needed ~Oct 25)** · D-5 loop for new repos · D-6 exam dates · **D-7 Stroke Agent orchestration** |

The details are in [memory/DECISIONS.md](memory/DECISIONS.md) and the
[master plan](plans/MASTER-PLAN.md#open-owner-decisions).

## Commands

Check that every repo is clean and in sync (Git Bash):

```bash
cd C:/Users/14087/Desktop && for r in Nursing_OS_Project nursebench charge-assign dysphagia-screen-fhir grounded-handoff stroke-abstraction-agent; do git -C $r fetch -q origin; echo "$r dirty=$(git -C $r status --porcelain | wc -l) head=$(git -C $r rev-parse --short HEAD) remote=$(git -C $r rev-parse --short origin/main)"; done
```

Nurse Handoff loop status (PowerShell):

```powershell
powershell -NoProfile -File C:/Users/14087/Desktop/loops/controller.ps1 status
```

Tests: each repo's command is in its `AGENTS.md` and in the table in
[RESUME.md](plans/RESUME.md#verification-commands).

- **Java repos (P2, P4):** use the portable JDK first:
  ```powershell
  $env:JAVA_HOME='C:\Users\14087\.local\share\nursing-os-tools\jdk21\jdk-21.0.12.1+1'; $env:Path="$env:JAVA_HOME\bin;$env:Path"
  ```
- **Dysphagia Questionnaire:** open it in a browser with `npm run site` in
  `dysphagia-screen-fhir`, then go to http://127.0.0.1:8123/site/.

## Tools on this PC

- Installed: Python 3.11, uv, Node 24 and Git. JDK 21 and Maven are a
  portable copy that is not on PATH.
- SUSHI (the FHIR build tool) is installed inside `dysphagia-screen-fhir`
  only.
- Missing: **Docker Desktop**, which the FHIR server work in P3 and P4 needs;
  also the GitHub CLI (optional).
