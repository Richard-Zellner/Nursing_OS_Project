# Nursing OS Project

A nurse's portfolio for the move from bedside nursing into nursing informatics and clinical AI. This public hub holds
the plans and the first project, Nurse Handoff. The other five projects live in their own repositories, private until
each is released.

All patient data is synthetic. Nothing here is for clinical use ([DISCLAIMER.md](DISCLAIMER.md)).

## Projects

| Project | What it is | Status |
|---|---|---|
| [Nurse Handoff](nurse-handoff/README.md) | Deterministic JSON-to-shift-handoff generator that keeps missing data visible | v0.1.0 released; v0.2 in progress |
| NurseBench | Benchmark of nursing tasks for AI models: protocol math, NIHSS, escalation, patient education | private until release |
| Charge Assign | Acuity-based nurse assignment optimizer (Java, Timefold) | private until release |
| Dysphagia Screen FHIR | Bedside swallow screen as a FHIR Questionnaire with CQL decision support | private until release |
| Grounded Handoff | SMART on FHIR app that drafts a handoff and cites the FHIR resource behind each sentence | private until release |
| Stroke Abstraction Agent | LLM extraction of stroke quality-measure data with evidence quotes and human review | private until release |

## Start here

- [CONTINUE.md](CONTINUE.md): the one-page card for picking the work back up.
- [plans/](plans/README.md): current state, milestones and how the work runs.
- [docs/portfolio/](docs/portfolio/README.md): the original research plan for each project.
- [docs/](docs/README.md): the Nurse Handoff specs.

## How this repo is built

A Codex loop (`../loops/`, outside this repo) takes one ticket from [TASKS.md](TASKS.md) every 4 hours under the rules
in [AGENTS.md](AGENTS.md). A controller verifies each ticket independently, then commits and pushes it. Progress and
handoff notes are in [memory/](memory/HANDOFF.md). `AGENTS.md`, `PROMPT.md`, `TASKS.md` and `loop.sh` stay at the root
for the controller.

Verify:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tests/verify.ps1
```

## Folders

| Folder | Holds |
|---|---|
| `nurse-handoff/` | the Python package, synthetic data and tests |
| `docs/` | Nurse Handoff specs; `docs/portfolio/` holds the research plans |
| `plans/` | resume plan, progress, session log, runbook and project plans |
| `memory/` | handoff, decisions, questions and the loop's log |
| `tests/` | the repository check |

## License

Code is Apache-2.0 ([LICENSE](LICENSE)).
