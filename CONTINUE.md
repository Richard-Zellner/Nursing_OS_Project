# Continue here

One page for picking the Nursing OS portfolio back up. What's current: [plans/RESUME.md](plans/RESUME.md) (next steps)
and [plans/PROGRESS.md](plans/PROGRESS.md) (milestones). History: [plans/SESSION-LOG.md](plans/SESSION-LOG.md).

## Resume

Tell Claude Code or Codex: **"Resume the Nursing OS portfolio from plans/RESUME.md."**

The agent then:
1. resolves the project;
2. checks that the six repos are synced and the loop is healthy;
3. applies your answers from each repo's `memory/QUESTIONS.md`;
4. continues the agent work.

## Projects

All folders are on the Desktop (`C:\Users\14087\Desktop\`). GitHub account: `Richard-Zellner`.

| ID | Project | Folder | Visibility | Plan |
|---|---|---|---|---|
| Hub | Portfolio hub, plans | `Nursing_OS_Project` | public | [plans/](plans/README.md) |
| P0 | Nurse Handoff (Codex loop) | `Nursing_OS_Project/nurse-handoff` | public, v0.1.0 released | [P0](plans/projects/P0-nurse-handoff.md) |
| P1 | NurseBench | `nursebench` | private until release | [P1](plans/projects/P1-nursebench.md) |
| P2 | Charge Assign | `charge-assign` | private until release | [P2](plans/projects/P2-charge-assign.md) |
| P3 | Dysphagia Screen FHIR | `dysphagia-screen-fhir` | private until release | [P3](plans/projects/P3-dysphagia-screen-fhir.md) |
| P4 | Grounded Handoff | `grounded-handoff` | private until release | [P4](plans/projects/P4-grounded-handoff.md) |
| P5 | Stroke Abstraction Agent | `stroke-abstraction-agent` | private until release | [P5](plans/projects/P5-stroke-abstraction-agent.md) |

Every repo has the same files:

| File | Holds |
|---|---|
| `AGENTS.md` | rules for agents |
| `TASKS.md` | task state |
| `memory/HANDOFF.md` | last session and next step |
| `memory/QUESTIONS.md` | questions; answer in the Answer cell and set the status to `answered` |
| `memory/DECISIONS.md` | append-only decisions |
| `docs/clinical-spec*.md` | clinical content, with provenance on line 1 |

## Rules that always apply

- **Employer:** never named or used (G0).
- **Visibility:** new repos stay private until release (D-4). The hub is public, so keep personal details out of it.
- **Clinical content:** agents draft it under D-9. It stays marked `Owner RN review: pending` until you review it
  yourself, and public wording never says "RN-authored" for agent drafts.
- **Delegation:** since 2026-09-26/27, agents answer questions and give approvals as "delegated agent decisions".
  These stay yours:
  - RN attestation;
  - human measurement (labels, ratings, the blinded review, the blind abstraction);
  - your first-person writing;
  - releases and visibility.
- **Evidence:** results come only from real runs, with the model ID and date.
- **Hub edits:** commit and push promptly, between loop runs.

## Decisions

| Decided | Open |
|---|---|
| <ul><li>D-1 separate repos</li><li>G0</li><li>D-4 private until release</li><li>Morse dropped</li><li>D-8 parallel work</li><li>D-9 agent-drafted clinical content</li><li>Java HAPI instead of Docker</li><li>D-7 claude-cli extractor (delegated)</li><li>D-3 roster and cap recommended (delegated; your API keys are the go)</li></ul> | <ul><li>D-2 Nurse Handoff ends at v0.2</li><li>D-5 loop for new repos</li><li>D-6 exam dates</li></ul> |

Details: [memory/DECISIONS.md](memory/DECISIONS.md).

## Tools on this PC

- **On PATH:** Python 3.11, uv, Node 24, Git and the GitHub CLI (`gh`, logged in).
- **Portable JDK 21 and Maven**, not on PATH. For the Java repos, run
  `$env:JAVA_HOME='C:\Users\14087\.local\share\nursing-os-tools\jdk21\jdk-21.0.12.1+1'; $env:Path="$env:JAVA_HOME\bin;$env:Path"`.
- **HAPI FHIR** runs on the portable JDK (P3 on port 8080, P4 on 8082) and needs at least 6 GiB of free RAM. Docker
  Desktop is only a fallback.
- **Dysphagia form:** `npm run site` in `dysphagia-screen-fhir`, then open http://127.0.0.1:8123/site/.
