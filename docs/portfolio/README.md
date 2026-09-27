# Portfolio research plans

[Project home](../../README.md) · [Documentation](../README.md) · [Delivery plans](../../plans/README.md)

These are the original research plans of 2026-09-24: what each project is, why it matters, and how it was meant to be
built. They are kept as written. All five repos now exist (private until release), and some choices changed during the
build: for example, HAPI FHIR runs on Java instead of Docker. For the current state, read
[plans/RESUME.md](../../plans/RESUME.md); for milestones, read [plans/projects/](../../plans/README.md).

Start with the [overview](overview.md): build order, timeline and shared requirements.

| Order | Repo | Plan | Original project numbers | Delivery plan |
|---|---|---|---|---|
| 1 | `nursebench` | [Nursing AI evaluation tracks](nursebench.md) | 1, 2, 4, 5 | [P1](../../plans/projects/P1-nursebench.md) |
| 2 | `charge-assign` | [Acuity-based assignment optimizer](charge-assign.md) | 11 | [P2](../../plans/projects/P2-charge-assign.md) |
| 3 | `dysphagia-screen-fhir` | [Dysphagia screening CDS](dysphagia-screen-fhir.md) | 7 | [P3](../../plans/projects/P3-dysphagia-screen-fhir.md) |
| 4 | `grounded-handoff` | [SMART on FHIR handoff app](grounded-handoff.md) | 6 | [P4](../../plans/projects/P4-grounded-handoff.md) |
| 5 | `stroke-abstraction-agent` | [Stroke measure abstraction](stroke-abstraction-agent.md) | 13 | [P5](../../plans/projects/P5-stroke-abstraction-agent.md) |

[Research sources](sources.md) holds the original bibliography and its verification notes. The agent reference log is
separate: [memory/SOURCES.md](../../memory/SOURCES.md).

The Nurse Handoff package in this hub has its own [spec](../NURSE-HANDOFF-SPEC.md) and [task ledger](../../TASKS.md).
Grounded Handoff is a separate FHIR and AI project; it does not replace that package.
