# Delivery plans

[Project home](../README.md) · [Research plans](../docs/portfolio/README.md)

How the six Nursing OS projects get finished: order, milestones, who does what, and where things stand. The research
plans in [docs/portfolio/](../docs/portfolio/README.md) say what each project is and why.

## Read in this order

1. [CONTINUE.md](../CONTINUE.md): the one-page card.
2. [RESUME.md](RESUME.md): current state, how to start a session, verification and rules.
3. [PROGRESS.md](PROGRESS.md): dashboard, milestone checkboxes and owner gates.
4. The plan for your project in [projects/](#files).

For background, read [MASTER-PLAN.md](MASTER-PLAN.md) (finish line, dependencies, shared rules) and
[RUNBOOK.md](RUNBOOK.md) (how to run a session, start a repo and release). History is in
[SESSION-LOG.md](SESSION-LOG.md) and the three `REVIEW-2026-09-25*.md` records.

## Files

| File | Holds |
|---|---|
| [RESUME.md](RESUME.md) | current state and how to continue (replaced, not appended) |
| [PROGRESS.md](PROGRESS.md) | milestone state across all projects |
| [SESSION-LOG.md](SESSION-LOG.md) | one row per work session |
| [MASTER-PLAN.md](MASTER-PLAN.md) | the global plan |
| [RUNBOOK.md](RUNBOOK.md) | how the work is done and recorded |
| [projects/P0-nurse-handoff.md](projects/P0-nurse-handoff.md) | Nurse Handoff v0.1 and v0.2 (loop-driven, in this hub) |
| [projects/P1-nursebench.md](projects/P1-nursebench.md) | the four-track nursing AI benchmark |
| [projects/P2-charge-assign.md](projects/P2-charge-assign.md) | the Timefold assignment optimizer |
| [projects/P3-dysphagia-screen-fhir.md](projects/P3-dysphagia-screen-fhir.md) | the FHIR Questionnaire and CQL screen |
| [projects/P4-grounded-handoff.md](projects/P4-grounded-handoff.md) | the SMART on FHIR cited handoff |
| [projects/P5-stroke-abstraction-agent.md](projects/P5-stroke-abstraction-agent.md) | stroke measure abstraction |
| [templates/](templates/) | repo scaffold, clinical-spec skeleton, release checklist |
| `REVIEW-2026-09-25*.md` | records of the first rounds (history) |

## Where state lives

| State | Authority |
|---|---|
| P0 tickets | the hub [TASKS.md](../TASKS.md), kept by the loop |
| P1–P5 tasks | each repo's own `TASKS.md` |
| Milestones and gates across projects | [PROGRESS.md](PROGRESS.md) |
| Task definitions and acceptance criteria | `projects/*.md` |
| Owner decisions | [memory/DECISIONS.md](../memory/DECISIONS.md) and [memory/ACTIVE-DECISIONS.md](../memory/ACTIVE-DECISIONS.md) |

These plans set the order of work. They don't approve new scope for the loop, and they don't override the Nurse
Handoff specs or the hub [AGENTS.md](../AGENTS.md).
