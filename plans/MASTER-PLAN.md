# Nursing OS portfolio: master plan

[Plans index](README.md) · [Progress](PROGRESS.md) · [Runbook](RUNBOOK.md)

Created 2026-09-24. This plan covers six projects: the existing Nurse Handoff
package and the five repos in the [portfolio overview](../docs/portfolio/overview.md).
It turns those designs into a sequence of milestones, each with a finish line,
and marks which work belongs to the owner and which an agent may do. The
research plans in `docs/portfolio/` remain the design authority. This plan
does not change their scope.

## Finish line

The portfolio is finished when all of the following are true:

1. Each of the six projects has a public tagged release that meets the
   [shared release standard](templates/release-checklist.md). For Nurse
   Handoff that is v0.2.0; for the other five it is v1.0.0.
2. The hub [README](../README.md) links every repo with its status and
   headline result.
3. Every results table and résumé line comes from real runs, with the model
   version and run date recorded.
4. Each repo has a published write-up of 600–900 words.

At about 10 hours a week, the target is **end of June 2027** (about 330 hours).

## Projects

| ID | Project | Location | Finish | Hours | Window | Plan |
|---|---|---|---|---|---|---|
| P0 | Nurse Handoff | this hub, `nurse-handoff/` | v0.2.0 | ~6 owner hours; the loop does the rest | Sep 24 – Oct 9, 2026 | [P0](projects/P0-nurse-handoff.md) |
| P1 | NurseBench | new repo `nursebench` | v1.0.0 (4 tracks) | ~110 | Oct 2026 – Jan 2027 | [P1](projects/P1-nursebench.md) |
| P2 | Charge Assign | new repo `charge-assign` | v1.0.0 | ~45 | Feb 2027 | [P2](projects/P2-charge-assign.md) |
| P3 | Dysphagia Screen FHIR | new repo `dysphagia-screen-fhir` | v1.0.0 | ~40 | Mar 2027 | [P3](projects/P3-dysphagia-screen-fhir.md) |
| P4 | Grounded Handoff | new repo `grounded-handoff` | v1.0.0 | ~60 | Apr – mid-May 2027 | [P4](projects/P4-grounded-handoff.md) |
| P5 | Stroke Abstraction Agent | new repo `stroke-abstraction-agent` | v1.0.0 | ~70 | mid-May – Jun 2027 | [P5](projects/P5-stroke-abstraction-agent.md) |

## Calendar

```text
2026  Sep 24 ─ Oct 9    P0 v0.1 + v0.2 run in the loop; owner reviews and tags releases
      Oct 1  ─ Oct 11   P1 M0 scaffolding (private repo)
      Oct 12 ─ Oct 31   P1 M1 Track 1 → NurseBench v0.1 (the résumé gate)
      Nov               P1 M2 Track 4 NIHSS, kept light for the NCA-GENL exam
      Dec 1  ─ Dec 8    no build work (CAHIMS exam Dec 8)
      Dec 9  ─ Dec 31   P1 M3 Track 2 escalation red-team
2027  Jan               P1 M4 Track 5 → NurseBench v1.0
      Feb               P2 Charge Assign (Java/Maven scaffold started Sep 24)
      Mar               P3 Dysphagia FHIR CDS (install Docker Desktop in February)
      Apr ─ mid-May     P4 Grounded Handoff (reuses P3's HAPI server)
      mid-May ─ Jun     P5 Stroke Abstraction Agent (reuses P1's seeded generator)
      end of Jun        portfolio close-out: hub README, write-ups, résumé
```

Exam dates come from the September 24 overview. The owner confirms the actual
bookings (decision D-6).

On September 24 the owner requested parallel agent work on all projects with
parent review. Independent scaffolding and mechanical validators advanced
early; the clinical dependencies and release targets above remain unchanged.
See [current progress](PROGRESS.md) for completed work.

## Dependencies

```text
P0 missing-data rules ─────────► P4 required-content checklist (absent ≠ normal)
P1 seeded-truth generator ─────► P5 chart generator
P1 T4 NIHSS rule work ─────────► P5 stroke clinical context
P1 grader-vs-RN kappa method ──► P4 judge validation, P5 human agreement
P3 HAPI server in Docker ──────► P4 M1 server setup
P3 AHASTR8 dysphagia logic ────► P5 AHASTR8 measure
```

Code moves between repos by copying it with a note of where it came from.
No repo depends on another at runtime, so each one builds and reviews on its
own.

## Source precedence

1. Explicit owner instructions, then `memory/ACTIVE-DECISIONS.md`.
2. Nurse Handoff specs (`docs/NURSE-HANDOFF-SPEC.md`, `docs/PATIENT-SCHEMA.md`,
   `docs/OUTPUT-FORMAT.md`) and `TASKS.md` for P0.
3. The research plans in `docs/portfolio/` (Sep 24, 2026) for P1–P5.
4. This `plans/` folder, which covers sequencing, task breakdown and progress.
   It never approves scope.
5. The owner's earlier career blueprint (Sep 2, 2026). Where it differs from
   item 3, item 3 is newer and wins.

### Conflicts found while planning

| # | Conflict | This plan follows | Status |
|---|---|---|---|
| C1 | `DECISIONS.md` 2026-09-04 says each project is a hub subfolder. The Sep 24 overview says five separate repos, each with its own license, CI and releases. | Separate repos. The hub `AGENTS.md` also forbids AI, FHIR, network access and non-stdlib dependencies, all of which P1–P5 need. Decided 2026-09-24 (D-1) |
| C2 | The blueprint defines NurseBench v0.1 as 50 post-discharge triage cases. The overview defines v0.1 as Track 1 protocol math. | Overview. Triage becomes Track 2. | Resolved by recency |
| C3 | The blueprint puts CAHIMS around Oct 31. The overview says Dec 8. | Dec 8 | **D-6** |
| C4 | The blueprint says MIT license. The overview says Apache-2.0 for code and CC BY 4.0 for data. | Overview | Resolved by recency |
| C5 | The Nurse Handoff roadmap lists v0.3 web, v0.4 FHIR, v0.5 LLM and v0.6 AI-output evaluation, which overlaps P4. | P0 ends at v0.2. P4 covers v0.4–v0.6 as a separate repo. | **D-2** |

## Open owner decisions

| ID | Decision | Recommendation | Needed by |
|---|---|---|---|
| D-1 | Separate repos (overview) or hub subfolders (Sep 4 decision) | **Decided 2026-09-24 by the owner: separate repos**, with the hub kept as the index | Done |
| D-2 | Treat Nurse Handoff as finished at v0.2, with its roadmap v0.3+ covered by P4 | Yes | At the P0 v0.2 release |
| D-3 | NurseBench model roster and API budget cap | 3 frontier API models plus 1 open-weights model; cap set by the owner (the blueprint estimated about $50) | Before the P1 M1 runs (~Oct 25) |
| D-4 | Repo visibility during development | **Decided 2026-09-24 by the owner: private until ready**, then public at release (the résumé rule only needs v0.1 public) | Done |
| D-5 | Enroll new repos in the unattended loop | No. Use interactive agent sessions. Enrolling a repo needs owner-authorized controller work. | Any time |
| D-6 | Confirm the CAHIMS and NCA-GENL exam dates | Keep the overview's dates | Now |
| D-7 | P5 orchestration: Claude Agent SDK, `claude -p` scripts, or Java (LangChain4j / Spring AI) | Decide at the P5 M3 start | May 2027 |
| D-8 | Build later projects alongside NurseBench instead of in sequence | **Decided 2026-09-24 by the owner: yes, parallel work on all projects.** Release targets are unchanged. | Done |
| D-9 | Who drafts clinical content | **Decided 2026-09-24 by the owner: agents draft it**; the owner signs off as RN before each release | Done |

Record each answer in `memory/DECISIONS.md`, refresh `memory/ACTIVE-DECISIONS.md`,
and tick the decision in [PROGRESS.md](PROGRESS.md).

## Rules for every repo

These come from the overview's ground rules.

- **Employer:** portfolio work happens outside shift hours. The employer is
  never named, referenced or used in any repo, write-up or post (owner
  confirmed 2026-09-24).
- **Data:** synthetic or public only. No employer material: no policies,
  order sets, EHR screenshots, build details or cases, even de-identified
  ones. Never send credentialed data such as full MIMIC to a third-party LLM.
- **Licensed instruments:** follow the licensing table in the overview.
  Braden, Morse, TOR-BSST, Schmitt-Thompson and the NHS SNCT are excluded.
  Morse was dropped by the owner on 2026-09-24, so no permission is sought.
- **Authorship (D-9):** agents draft clinical content (specs, protocol
  values, gold answers, labels, rubrics, weights, thresholds) under the
  owner's delegation. Every draft records its provenance, and the owner
  signs off as RN before any release. Public claims say "RN-reviewed" for
  agent-drafted content. See [RUNBOOK §1](RUNBOOK.md#1-roles-and-the-authorship-boundary).
- **Evidence:** metrics come only from real runs. Record the model ID,
  version and run date with every result, and never estimate a number.
- **Standard files:** README, DISCLAIMER, Apache-2.0 LICENSE, CC BY 4.0
  DATA_LICENSE, CHANGELOG with SemVer tags, `docs/clinical-spec.md`, tests,
  GitHub Actions CI and a write-up. See [repo scaffold](templates/repo-scaffold.md).
- **Secrets:** API keys stay in the user environment or a git-ignored `.env`.
  Every release includes a secrets scan.

## Risks

| Risk | Early sign | Response |
|---|---|---|
| Schedule slips during exam months | P1 M1 not code-complete by Oct 24 | Use the P1 scope-cut ladder. v0.1 ships smaller rather than late. |
| LLM grader disagrees with RN labels | kappa below the owner's threshold | Revise the grader prompt once, then report human-scored results for that metric and state the limitation |
| API cost overrun | The 20-item smoke run projects over the cap | Fewer models or items; use the local open-weights model for iteration |
| Tooling gaps on RGB | Docker and optional gh are missing; portable Java/Maven and project-local SUSHI were verified Sep 24 | Install remaining tools when their integration task is ready ([RUNBOOK §2](RUNBOOK.md#2-prerequisites)) |
| RAM contention (32 GB; Qwen runs manually) | HAPI or Docker fails while Qwen is loaded | Stop Qwen during Docker work and check free memory first |
| Source or standard changes (Specs Manual, US Core, Timefold 2.x) | Newer version at milestone start | Each plan's first milestone includes a "verify current version" task |
| Employer named or implied in a public file | A release-time search finds the name or an abbreviation | Remove it before the repo goes public. Outside work is permitted off shift (owner, 2026-09-24). |
