# Nursing informatics portfolio plans

[Project home](../../README.md) · [Documentation](../README.md)

Start with the [portfolio overview](overview.md) for the proposed build order,
timeline, and shared requirements. These planning documents were added on
September 24, 2026; organizing them does not change their content or advance
the implementation ledger.

## Project plans

The order below follows the overview. The repo names identify planned projects;
their code repositories have not been created by this organization pass.

| Order | Planned repo | Plan | Original project numbers |
|---|---|---|---|
| 1 | `nursebench` | [Nursing AI evaluation tracks](nursebench.md) | 1, 2, 4, 5 |
| 2 | `charge-assign` | [Acuity-based assignment optimizer](charge-assign.md) | 11 |
| 3 | `dysphagia-screen-fhir` | [Dysphagia screening CDS](dysphagia-screen-fhir.md) | 7 |
| 4 | `grounded-handoff` | [SMART on FHIR handoff app](grounded-handoff.md) | 6 |
| 5 | `stroke-abstraction-agent` | [Stroke measure abstraction](stroke-abstraction-agent.md) | 13 |

Execution plans (milestones, owner and agent tasks, progress) are in
[`plans/`](../../plans/README.md).

[Research sources](sources.md) contains the original bibliography and its
verification notes. It is separate from the agent reference log at
[`memory/SOURCES.md`](../../memory/SOURCES.md).

## Existing implementation

The deterministic Python [Nurse Handoff package](../../nurse-handoff/README.md)
has its own [specification](../NURSE-HANDOFF-SPEC.md) and
[task ledger](../../TASKS.md). The `grounded-handoff` plan describes a separate
FHIR/AI project; it does not replace that package or its approved milestones.
