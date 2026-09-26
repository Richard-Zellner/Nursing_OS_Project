# Portfolio review: round 4, September 25, 2026

[Plans index](README.md) · [Resume plan](RESUME.md) · [Progress](PROGRESS.md) · [Round 3](REVIEW-2026-09-25-round3.md) · [First review](REVIEW-2026-09-25.md)

This records the fourth implementation round, run on the evening of
2026-09-25 (Pacific) by Claude Code. The owner asked to "continue working on
all projects with claude opus 5.5 xhigh and run subagents to run in parallel"
while OpenAI Codex had an outage. Scope was Waves C and D of the round-3
resume plan, plus Nurse Handoff tickets 009–015, which the loop could not run.

The method was the same as rounds 1–3:
- at most three subagents at a time;
- the parent reviewed every diff against the specs;
- the parent reran each repo's verification, then committed and pushed.

## Summary

- **Scope:** every Wave C and D item is done, and the P0 v0.1 build is complete.
- **Owner decisions:** one new decision, quoted in hub DECISIONS: "yes, add the
  Java HAPI route to Wave C". HAPI now runs on the portable JDK in P3 and P4,
  and Docker Desktop is a fallback only.
- **Owner answers:** none arrived, so none were applied. No owner review,
  question or release was recorded on the owner's behalf.
- **New questions:** 34 were logged: 33 in the five repos and hub Q-002.
  Open questions now total 119 across P1–P5, plus 1 in the hub.
- **Paid model calls:** none.

## What was built

| Item | Repo | Tasks | Commit | Parent rerun |
|---|---|---|---|---|
| P0 | Hub | Nurse Handoff tickets 009–015 (direct session, loop paused with `STOP`) | `e8dee59` | `tests/verify.ps1` PASS, 238 pytest |
| P0 repair | Hub | Validator: non-negative age, string list items (the controller's trusted check rejected `DONE`) | `e2ecbe4` | 242 pytest, verify PASS, trusted acceptance PASS on a copy |
| C1 | P3 | P3-M4-1..3: HAPI v8.10.0-3 on the portable JDK, PlanDefinition, ActivityDefinitions, `$apply` runner | `81bc905` | `npm run verify`; `hapi.ps1 test`: 86 JUnit, all 15 fixtures |
| C2 | P1 | P1-M2-6 Track 4 task, scorer, report measures | `382b104` | 948 pytest; Track 1 mock report unchanged |
| C3 | P2 | P2-M4-1 floor map, M4-2 reasons, M5-1 replanning | `5c93e63` | Maven 125 tests (1 skipped) |
| C4 | P5 | P5-M5-1 router, M5-2 review page and decision log | `b739469` | 752 pytest, verify-evidence, both regeneration checks |
| D0 | P4 | P4-M1-1b/2b/4b: cohort loaded into HAPI with ids kept; US Core 6.1.0 validation | `8f32925` | Maven 126 with and without the server |
| D1 | P4 | P4-M3-4 citation view; P4-M5-4a DocumentReference and Provenance export | `ccd1b9e` | Maven 150 (8 skipped); the new HAPI view test not run (finding 3) |
| D2 | P1 | P1-M3-1 Track 2 spec draft, M3-2 draft scenarios (kept private), M3-3 templated perturbations | `fb9abe4` | 1112 pytest locally; 1094 + 18 skipped without `private/` |
| D3 | P1 | P1-M4-2 tool part: readability, numeric fidelity, snapshot guard | `b9d4601` | 1480 pytest |

Hub commits:
- `be92d30`: Java HAPI decision
- `3df643d`: MedlinePlus licensing correction
- the commit that adds this file

## Findings

1. **P0 v0.1 is waiting for the owner, with a known next check.**
   - The controller's own acceptance check caught two validator gaps that our tests missed. `e2ecbe4` fixed them.
   - Counters were reset with the documented `controller.ps1 reset`.
   - On its next scheduled run the controller verifies again. For a repair unit it runs baseline verification before any model call, so no Codex call is needed.
   - If it honours `DONE`, G1 is the owner's: tag `v0.1.0`, tick "v0.1 released", delete `DONE`.
   - Q-002 now covers only empty optional strings.
2. **MedlinePlus licensing (NurseBench Q-29, Q-30).**
   - Only health-topic summaries are public domain. The "when to call" sections are A.D.A.M. encyclopedia content, which is copyrighted.
   - Checked on the MedlinePlus content-usage page. The agent also reports that A.D.A.M. page footers forbid AI testing.
   - Track 2 uses only the summaries, and the hub planning docs were corrected.
   - The agent had fetched about 60 encyclopedia pages before it read the footer. It deleted them, and none of that text is in the repo.
   - The signed-off Track 1 spec cites one A.D.A.M. value (the potassium range; Q-30).
3. **One HAPI test not yet run.** P4's `HandoffViewHapiTest` needs the server.
   - Free RAM stayed below the 6 GiB guard (5.5–5.9 GiB), with the ChatGPT desktop app holding about 6 GiB.
   - Nothing was stopped and the guard was not lowered.
   - To run it: `hapi.ps1 start`, then `mvnw verify -Dgroundedhandoff.hapi.required=true`, then `hapi.ps1 stop`.
4. **Held-out safety.**
   - The 40 Track 2 scenarios exist only in Git-ignored `nursebench/private/t2_escalation/`, until Q-37 decides on a held-out split. **Back that folder up.**
   - The Track 1 full set is also in `private/`, but it can be regenerated from its seed.
5. **Licences to decide before release.**
   - NurseBench now depends on `textstat`, which pulls in GPL-3.0 `cmudict` (Q-43).
   - The P4 export tags the demo document as AI-involved (P4-Q037).
6. **CI not observed.** The GitHub CLI is not installed. New CI-relevant changes:
   - P3's HAPI tests skip in CI;
   - P1's CI now skips 18 private-data tests;
   - P4's server tests skip.

   Check the Actions tab.
7. **Local disk use.**
   - HAPI WAR: 378 MB, shared.
   - P4 H2 database `.hapi/h2-8082/`: 1.7 GB, git-ignored; `hapi.ps1 reset` removes it.
   - HL7 validator and package cache: about 1.1 GB under `nursing-os-tools/`.
8. **Usage.**
   - This round's nine agent runs used about 3.8M tokens.
   - Rounds 3 and 4 together used about 6.6M.
   - The weekly reset is Sep 27, 5am Pacific.

## State at the end of the round

- **Repos:** all six repos are clean and match `origin/main`. The Nurse Handoff loop is unpaused, with counters reset.
- **Test totals at the last parent reruns:**

  | Repo | Tests |
  |---|---|
  | Hub | 242 |
  | P1 | 1480 locally (1462 + 18 skipped without `private/`) |
  | P2 | 125 (1 skipped) |
  | P3 | 85 Node + 55 JUnit without a server (86 JUnit with HAPI) |
  | P4 | 150 (8 skipped without a server) |
  | P5 | 752 |

- **Milestones completed this round:**
  - P0 M1 (v0.1 build)
  - P3 M4 (`$apply` on local HAPI)
  - P4 M1 (HAPI, Synthea, overlay)
  - P5 M5 (router and review page)
- **What limits progress now:** almost all remaining work waits on the owner:
  - reviews and question answers;
  - D-3 models and budget;
  - D-7;
  - the P5 packet review;
  - release gates.

  The unblocked agent work left is listed as Wave E in [RESUME.md](RESUME.md).
