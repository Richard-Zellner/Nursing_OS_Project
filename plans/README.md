# Portfolio delivery plans

[Project home](../README.md) · [Research plans](../docs/portfolio/README.md)

This folder holds the plan for finishing all six Nursing OS projects: the
existing Nurse Handoff package and the five portfolio repos. The research
plans in [`docs/portfolio/`](../docs/portfolio/README.md) cover what each
project is and why. This folder covers the order, the milestones, who does
each task, and where things stand.

## Reading order

**Resuming work?** The one-page card is [CONTINUE.md](../CONTINUE.md). Then read [RESUME.md](RESUME.md), the continue-from-here
plan, and the latest review, [REVIEW-2026-09-25.md](REVIEW-2026-09-25.md).

1. [MASTER-PLAN.md](MASTER-PLAN.md): finish line, calendar, dependencies,
   source precedence, open owner decisions, shared rules
2. [PROGRESS.md](PROGRESS.md): dashboard, milestone checkboxes, owner gates, session log
3. [RUNBOOK.md](RUNBOOK.md): how to run a work session, start a repo, release and record progress
4. The plan for the project you are working on

## Files

```text
plans/
  README.md                      this index
  MASTER-PLAN.md                 global plan
  PROGRESS.md                    progress: milestone state across all projects
  RUNBOOK.md                     instructions for completing the work
  RESUME.md                      continue-from-here plan: owner queue, agent waves, blockers
  REVIEW-2026-09-25.md           record of Sep 24–25 work, decisions, verification, findings
  projects/
    P0-nurse-handoff.md          finish v0.1 and v0.2 (loop-driven, in this hub)
    P1-nursebench.md             4-track nursing AI benchmark (Oct 2026 – Jan 2027)
    P2-charge-assign.md          Timefold assignment optimizer (Feb 2027)
    P3-dysphagia-screen-fhir.md  FHIR Questionnaire + CQL CDS (Mar 2027)
    P4-grounded-handoff.md       SMART on FHIR cited handoff (Apr – May 2027)
    P5-stroke-abstraction-agent.md  stroke measure abstraction (May – Jun 2027)
  templates/
    repo-scaffold.md             standard files, AGENTS.md, TASKS.md, CI, README outline
    clinical-spec.md             owner-authored spec skeleton
    release-checklist.md         v0.1 and v1.0 release gate
```

## Where state lives

| State | Authority |
|---|---|
| P0 ticket state | hub [`TASKS.md`](../TASKS.md), maintained by the loop |
| P1–P5 task state | each repo's own `TASKS.md` |
| Milestones, gates and decisions across projects | [PROGRESS.md](PROGRESS.md) |
| Task definitions and acceptance criteria | `projects/*.md` |
| Owner decisions | [`memory/DECISIONS.md`](../memory/DECISIONS.md) and [`memory/ACTIVE-DECISIONS.md`](../memory/ACTIVE-DECISIONS.md) |

These plans are sequencing aids. They do not approve new scope for the
unattended loop, and they do not override the Nurse Handoff specs or the
hub [`AGENTS.md`](../AGENTS.md).
