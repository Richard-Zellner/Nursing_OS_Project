# Nursing OS Project

Portfolio hub for the move from bedside nursing into nursing informatics and
clinical AI. Each subfolder is one self-contained project with its own README
and tests. All patient data in this repository is synthetic; nothing here is
intended for clinical use.

## Projects

| Project | Status | Summary |
|---|---|---|
| [`nurse-handoff/`](nurse-handoff/) | v0.1 in progress | Deterministic JSON-to-shift-handoff generator that preserves missing data as missing. Spec: [`docs/NURSE-HANDOFF-SPEC.md`](docs/NURSE-HANDOFF-SPEC.md). |

## How this repo is built

An unattended Codex loop (see `../loops/README.md`) runs one ticket from
`TASKS.md` per iteration (one cycle every 4 hours) under the contract in `AGENTS.md`. Progress and
handoff notes live in `memory/`. Humans review and commit between runs.

Verification:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tests/verify.ps1
```
