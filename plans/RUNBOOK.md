# Runbook: how to complete the portfolio

[Plans index](README.md) · [Master plan](MASTER-PLAN.md) · [Progress](PROGRESS.md)

These instructions apply to the owner and to any agent session (Claude Code,
Codex) working on a portfolio project. The unattended loop follows the hub
[`AGENTS.md`](../AGENTS.md) instead, and nothing here overrides it.

## 1. Roles and the authorship boundary

Every task in a project plan carries one of three tags:

| Tag | Who | Covers |
|---|---|---|
| **OWNER** | the owner; agents draft the clinical items under D-9 | Clinical specs, protocol values, gold answers, labels, rubrics, acuity and constraint weights, thresholds (agent-drafted since D-9); final RN sign-off on all clinical content; reviewer recruitment, decisions, releases, public posts and credentials (owner only) |
| **AGENT** | an agent | Scaffolding, code, calculators and scorers that implement the spec, generators, tests, CI, UI, reports, format fixes |
| **PAIR** | the agent drafts structure, the owner writes and approves the substance | README, DISCLAIMER, CHANGELOG, methodology structure |

**Clinical drafting (D-9, owner decision 2026-09-24).** The owner delegated
clinical input to agents ("use your discretion for the clinical input to the
best of your ability"). Agents may draft specs, protocol values, gold
answers, labels, rubrics, weights and thresholds, under these rules:

- Every agent-drafted clinical file starts with a provenance line:
  `Provenance: agent-drafted YYYY-MM-DD under owner delegation (D-9). Owner RN review: pending.`
- Every value cites a public source, or is marked project-authored with a
  one-line rationale. Anything not checked against its source is marked
  `VERIFY:` with exactly what to check.
- Data items record `authored_by: agent` (or the repo's equivalent) and
  `reviewed: false` until the owner reviews them. Never label agent work as
  RN-authored.
- Downstream work may build on drafts, so milestones can finish on drafted
  content. The owner's RN sign-off is required before any **release**:
  the owner changes the provenance line to `Owner RN review: YYYY-MM-DD`.
- Public claims (README, write-ups, résumé) say "RN-reviewed" for
  agent-drafted content, and "RN-authored" only for content the owner wrote.
- Licensing rules still apply: no licensed instrument text, no employer
  material, and no copying of forms. Paraphrase and cite.

When a clinical fact cannot be established from a public source, draft the
most defensible choice, mark it `VERIFY:`, and add a row to the repo's
`memory/QUESTIONS.md`.

**Human measurements are outside D-9.** Some tasks exist to measure a human
judgment against a model. If an agent produced them, the result would compare
one model with another. These stay with the owner, an RN, or other named
human reviewers:

- grader and judge validation labels used for kappa (P1-M3-6, P1-M4-4, P4-M4-4)
- PEMAT-P scoring (P1-M4-4) and usefulness/safety ratings (P4-M5-3)
- the blinded charge-nurse review (P2-M5-3)
- the blind abstraction for human agreement (P5-M6-1)

Agents may prepare packets, forms and answer keys for these tasks, but never
the judgments themselves.

## 2. Prerequisites

Checked on RGB on 2026-09-24. Re-check before relying on this list.

| Tool | Needed by | Status | Install |
|---|---|---|---|
| Python 3.11, uv | P1, P5 | present | — |
| Node 24 | P3 (SUSHI), P4 frontend | present | — |
| Git | all | present | — |
| JDK 21, Maven | P2; P3 cql-to-elm; P4 backend; Synthea | portable Temurin 21.0.12.1+1 and Maven 3.9.16 verified in P2/P4 | RGB: `%USERPROFILE%/.local/share/nursing-os-tools/`; set process JAVA_HOME to its JDK; repo wrappers pin Maven |
| Docker Desktop with WSL2 | P3, P4 (HAPI) | missing | docker.com installer; set a memory cap in `%UserProfile%\.wslconfig` |
| SUSHI | P3 | project-local 3.20.1 verified | From dysphagia-screen-fhir: `npm ci --ignore-scripts`, then `npm run verify`; no global install needed |
| GitHub CLI | optional | missing | `winget install GitHub.cli` |

Other things the owner sets up: LLM API keys as user environment variables,
a loinc.org account, SNOMED browser access, and a GitHub account (already
exists). RAM is 32 GB and Qwen runs manually, so check free memory and stop
Qwen before Docker-heavy work.

## 3. Work-session protocol

Use this for every session, owner or agent.

**Start**
1. Resolve the project:
   `node C:/Users/14087/.agent-memory/project-system/project-memory.cjs boot "<task>" --owner --json`
   (owner sessions only; other sessions omit `--owner`).
2. Read [RESUME.md](RESUME.md) (the current continue-from-here plan), then
   [PROGRESS.md](PROGRESS.md), then the project's plan in `projects/`,
   then the repo's `memory/HANDOFF.md` and `TASKS.md`, then the research plan
   in `docs/portfolio/` for design detail.
3. Pick the **first unfinished task in the current milestone** whose inputs
   exist. If it is an OWNER task and you are an agent, do not do it. Report
   what the owner must do, and take the next AGENT task only if it does not
   depend on that owner task.

**Work**
4. Do one task, or a small group of tasks from the same milestone, completely,
   with tests.
5. Run the repo's verification command, and report the real result.

**Close**
6. Tick the task in the repo's `TASKS.md`, rewrite the repo's
   `memory/HANDOFF.md` (what was done, what comes next, open questions), and
   append durable choices to `memory/DECISIONS.md`.
7. If a milestone or gate finished, tick it in [PROGRESS.md](PROGRESS.md) and
   update the dashboard row. Always add a session-log row.
8. Commit only when the owner asks, or when the owner has authorized commits
   for that repo. Never tag, release or publish. Those are owner actions.

A quick way to start an agent session is to tell it:
"Continue the Nursing OS portfolio, project P1 NurseBench." The resolver
routes to this hub, and this runbook routes to the plan.

## 4. Starting a new repo

Do this at each project's first milestone. It is an owner-led step: an
agent can run it once the owner says to.

1. **Owner:** create the GitHub repo as **private** (D-4; public only at release).
   D-1 is decided: separate repos. Create the GitHub repo
   `Richard-Zellner/<repo>` with no template files.
2. Clone it to `C:\Users\14087\Desktop\<repo>`.
3. **Agent:** scaffold from [templates/repo-scaffold.md](templates/repo-scaffold.md),
   including the repo `AGENTS.md`, `TASKS.md`, `memory/` files and CI.
4. **Agent:** copy the plan's milestone tasks into the repo `TASKS.md`, using
   the same task IDs (for example `P1-M0-3`). The plan defines the tasks, and
   the repo ledger tracks their state.
5. Configure a repository-local Git identity (the hub uses the GitHub
   noreply address). Make the first commit and push.
6. Register the repo so later sessions resolve it. Follow the "Start a new
   project" steps in `C:/Users/14087/AGENTS.md`: a source brief, then a
   registry entry with purpose, aliases, path and a pointer back to this hub
   (`nursing-os`).
7. Add a row to the hub [README](../README.md) projects table (status "in
   development", or omit it while the repo is private).

## 5. Milestone and release flow

```text
clinical spec (OWNER) → build (AGENT) → verify (tests + CI) → owner review → tick → next milestone
                                                                      └→ at v0.1 / v1.0: release checklist (OWNER)
```

- Spec before code. An AGENT task that depends on an unfinished spec waits.
- Generated clinical content (items, narratives, charts, perturbations) is
  not final until the owner reviews it as its plan task says. Record the
  review with `reviewed: true` or in `memory/DECISIONS.md`.
- Paid model runs: a 20-item smoke run first, a cost projection against the
  D-3 cap, then the full run. Pin the model ID and date in every result file.
- Releases follow [templates/release-checklist.md](templates/release-checklist.md)
  and are always owner actions.

## 6. Updating progress

| What changed | Where to record it |
|---|---|
| A task finished | repo `TASKS.md` and repo `memory/HANDOFF.md` |
| A milestone or gate finished | [PROGRESS.md](PROGRESS.md): tick it and update the dashboard row |
| Any session | a PROGRESS.md session-log row, and owner hours in the Hours table |
| An owner decision | hub `memory/DECISIONS.md` (append), a tick in PROGRESS.md, and a refresh of `memory/ACTIVE-DECISIONS.md` by the owner |
| A scope or schedule change | edit the project plan, note why in `memory/DECISIONS.md`, and add a PROGRESS.md log row |
| A P0 loop ticket | nothing extra; the loop updates `TASKS.md` and `memory/LOG.md` |

A continuity receipt can also be added with the project-memory `handoff`
command (see `C:/Users/14087/.agent-memory/project-system/README.md`).

## 7. The hub, the loop and Git

The hub is loop-driven and auto-pushed, which puts constraints on edits here:

- The controller refuses to start while the working tree has uncommitted
  changes. After **any** edit in this hub, including files under `plans/`,
  commit and push before the next loop unit
  ([memory/GIT-SETUP-2026-09-24.md](../memory/GIT-SETUP-2026-09-24.md)).
- Do not edit the hub's protected files: `AGENTS.md`, `PROMPT.md`, `loop.sh`,
  `tests/verify.ps1`, `.gitignore`, `.gitattributes`, the three
  `docs/*` specs, the rules text of `TASKS.md`, and
  `memory/ACTIVE-DECISIONS.md` (owner only).
- Controller commands, from `C:\Users\14087\Desktop\loops`:
  `powershell -NoProfile -File controller.ps1 status` and
  `controller.ps1 git-sync --project Nursing_OS_Project`.
- The hub is **public**. Anything written in `plans/` becomes public when it
  is pushed. Keep personal career details out of it, and never name the employer.
- New repos are **not** enrolled in the loop (D-5). Enrolling one would need
  owner-authorized controller changes in `loops/policy.py` plus a loop
  contract for that repo.

## 8. When something goes wrong

| Situation | Response |
|---|---|
| A spec contradicts a research plan | The spec written later by the owner wins; note it in `DECISIONS.md` |
| A task is too big for one session | Split it in the repo `TASKS.md` with sub-IDs (`P1-M1-4a`), and keep the plan task as the parent |
| A tool will not install or run | Record the exact error in the repo `HANDOFF.md`, mark the dashboard `blocked`, and move to an independent task |
| Behind schedule | Use the project's scope-cut ladder, or ask the owner. Never skip owner reviews or invent results. |
| A kappa below threshold | Revise the grader prompt once; if it is still low, report human-scored results for that metric |
| The loop blocks on P0 | Follow P0's risk table, then reset through the controller after repair |

## 9. Weekly rhythm (about 10 h)

- Mid-week session (~2–3 h): AGENT tasks and verification.
- Weekend session (~4–5 h): OWNER spec and label work, reviews.
- End of week (~15 min): update PROGRESS.md and check next week's gates
  against the [calendar](MASTER-PLAN.md#calendar).
- November: P1 M2 only (exam month). Dec 1–8: no build work.
