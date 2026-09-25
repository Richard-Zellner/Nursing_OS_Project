# Nursing OS Project

Portfolio hub for the move from bedside nursing into nursing informatics and
clinical AI. Each subfolder is one self-contained project with its own README
and tests. All patient data in this repository is synthetic; nothing here is
intended for clinical use.

## Start here

- [Portfolio plans](docs/portfolio/README.md) — overview, five planned repos,
  and research sources.
- [Delivery plan](plans/README.md) — master plan, per-project milestones,
  progress tracker, and runbook for finishing all six projects.
- [Nurse Handoff](nurse-handoff/README.md) — the existing Python project.
- [Documentation](docs/README.md) — implementation specs and portfolio plans.
- [Task ledger](TASKS.md) and [latest handoff](memory/HANDOFF.md) — implementation
  progress and the next unit of work.

## Projects

| Project | Status | Summary |
|---|---|---|
| [`nurse-handoff/`](nurse-handoff/) | v0.1 in progress | Deterministic JSON-to-shift-handoff generator that preserves missing data as missing. Spec: [`docs/NURSE-HANDOFF-SPEC.md`](docs/NURSE-HANDOFF-SPEC.md). |

The broader portfolio plans live in [`docs/portfolio/`](docs/portfolio/README.md).
The planned `grounded-handoff` FHIR/AI app is separate from the existing
deterministic `nurse-handoff` package.

## Folder guide

| Location | Contents |
|---|---|
| `docs/` | Nurse Handoff specifications and a documentation index |
| `docs/portfolio/` | Portfolio overview, individual project plans, and research sources |
| `plans/` | Delivery plan: master plan, project milestone plans, progress, runbook, templates |
| `nurse-handoff/` | Python package, synthetic-data directory, package tests, and local virtual environment |
| `tests/` | Repository verification script |
| `memory/` | Handoff, decisions, iteration log, and owner questions |
| `.loop/` | Local controller output; ignored by Git |

`AGENTS.md`, `PROMPT.md`, `TASKS.md`, and `loop.sh` stay at the root for the
development controller. Git metadata and configuration also stay in place.

## How this repo is built

An unattended Codex loop (see `../loops/README.md`) runs one ticket from
`TASKS.md` per iteration (one cycle every 4 hours) under the contract in `AGENTS.md`. Progress and
handoff notes live in `memory/`. After independent verification, the controller commits and pushes accepted work.
See [GitHub setup](memory/GIT-SETUP-2026-09-24.md) for synchronization and owner-edit rules.

Verification:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tests/verify.ps1
```
