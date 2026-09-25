# Template: new portfolio repo scaffold

[Runbook §4](../RUNBOOK.md#4-starting-a-new-repo)

Use this for P1–P5. Language-specific folders (`src/`, `tracks/`, Maven
layout) come from each project plan. The files below are common to all five.

```text
<repo>/
  README.md             problem → why a nurse built it → demo GIF → results → limitations
  DISCLAIMER.md         educational; not a medical device; not clinical advice
  LICENSE               Apache-2.0 (code)
  DATA_LICENSE          CC BY 4.0 (owner-authored data)
  CHANGELOG.md          Keep a Changelog format; SemVer; one entry per tag
  AGENTS.md             agent contract (below)
  CLAUDE.md             one line: "Read AGENTS.md."
  TASKS.md              task ledger copied from plans/projects/Pn-*.md, same IDs
  docs/
    clinical-spec.md    OWNER-authored (templates/clinical-spec.md)
  memory/
    HANDOFF.md          rewritten each session (max 40 lines)
    DECISIONS.md        append-only, one line of why each
    QUESTIONS.md        append-only table for the owner
  tests/
  results/              real run outputs only, each with model ID and date
  .github/workflows/ci.yml
  .gitignore            .env, *.key, venv/target/node_modules, private/, caches
```

## DISCLAIMER.md

```markdown
# Disclaimer

This is an educational portfolio project. It is not a medical device, has not
been clinically validated, and is not clinical advice. All patient data is
synthetic or from public sources. It contains no employer material. Cited
instruments and guidelines belong to their authors; this project is not
affiliated with them.
```

## AGENTS.md

```markdown
# <repo>: agent contract

Part of the Nursing OS portfolio. The plan is in
Nursing_OS_Project/plans/projects/<Pn-file>.md, and progress is in
Nursing_OS_Project/plans/PROGRESS.md.

## Read first
memory/HANDOFF.md → TASKS.md → docs/clinical-spec.md → memory/DECISIONS.md (recent).

## Authorship boundary
The owner writes all clinical content: specs, protocol values, gold answers,
labels, rubrics, weights and thresholds. You implement it exactly. Never
write or draft clinical content. If a needed clinical fact is missing, add
a row to memory/QUESTIONS.md and stop that task.

## Hard rules
- Synthetic or public data only. No employer material. No real patients.
- Never send credentialed datasets to third-party APIs.
- Secrets only in environment variables or a git-ignored .env. Never print or commit them.
- Results come only from real runs; record model ID, version and date. Never estimate a metric.
- Do not tag, release, publish, or change repo visibility. Commit only when the owner asks.
- Paid model runs need a 20-item smoke run and the owner's go-ahead.

## Verification
<exact command, e.g. `uv run pytest -q` or `mvn verify`>

## Before you finish
Tick finished tasks in TASKS.md, rewrite memory/HANDOFF.md, and append
decisions and questions. Tell the owner if a milestone completed so they
can update PROGRESS.md.
```

## TASKS.md

```markdown
# <repo>: task ledger

Task definitions: Nursing_OS_Project/plans/projects/<Pn-file>.md.
Tick only when acceptance is verified in the same session.
OWNER tasks are ticked by the owner.

## M0 <name>
- [ ] P1-M0-1 (OWNER) <deliverable>. Acceptance: <...>
- [ ] P1-M0-2 (AGENT) <deliverable>. Acceptance: <...>
```

## CI (`.github/workflows/ci.yml`)

At minimum, on push and pull request:
- install pinned dependencies
- run the full test suite
- validate every data file against its schema
- never call paid APIs; use mock or offline models, and service containers for HAPI

## README outline

1. One-line summary and the disclaimer link
2. The problem, in bedside terms
3. Why a nurse built it (two or three sentences)
4. Demo GIF or sample output
5. How it works (diagram)
6. Results (tables from `results/`, with model IDs and dates)
7. Limitations
8. Run it yourself
9. Sources and licenses
10. Changelog link
