# Portfolio review: round 3, September 25, 2026

[Plans index](README.md) · [Resume plan](RESUME.md) · [Progress](PROGRESS.md) · [Previous review](REVIEW-2026-09-25.md)

This records the third implementation round: Waves A and B of the
[previous resume plan](REVIEW-2026-09-25.md), run on 2026-09-25 by Claude
Code with six subagents, at most three at a time. The parent reviewed every
diff against the signed-off specs, reran each repo's verification, and then
committed and pushed. The previous review stays as the record of Sep 24–25
up to that point.

## Summary

- **Scope:** all six agent assignments in Waves A and B are complete. No
  owner answers arrived during the round, so none were applied.
- **Owner gates:** unchanged. No owner review, question or decision was
  recorded on the owner's behalf. New clinical text carries
  `Owner RN review: pending.`
- **Questions:** agents logged 28 new questions (86 open in total across P1–P5).
  All take the conservative reading and are listed below.
- **Paid runs:** none. No model API was called; Track 1 was exercised only
  with Inspect's mock model.

## What was built

| Wave | Repo | Tasks | Commit | Parent rerun |
|---|---|---|---|---|
| A1 | P1 NurseBench | P1-M1-6 Track 1 task and scorer; P1-M1-7 bootstrap and report | `a513968` | 629 pytest, validate, mock eval, mock Track 1 report (refused for `results/`) |
| A2 | P3 Dysphagia | P3-M3-3 CQL library, pinned ELM build; P3-M3-4 engine tests on all 15 fixtures | `b1228b1` | `npm run verify`: SUSHI, Node tests, Maven 55 JUnit tests |
| A3 | P2 Charge Assign | P2-M3-1 M1 and S1–S4; P2-M3-2 baselines; P2-M3-3 benchmark over 50 scenarios | `6b08d18` | Maven 107 tests (1 skipped: the on-demand benchmark) |
| B1 | P4 Grounded Handoff | P4-M3-2 fact sheet; P4-M4-2 value fidelity; P4-M4-5 omission check | `bfe05aa` | Maven 106 tests |
| B2 | P5 Stroke Agent | P5-M2-3a packets for C01–C20; P5-M4-1 shared measure engine | `29cccc1` | 536 pytest, verify-evidence, packet regeneration check, all 20 case evidence files consistent |
| B3 | P1 NurseBench | P1-M2-1 Track 4 spec draft (D-9); P1-M2-2 rules and sampler | `053d96f` | 756 pytest, validate, mock eval |

Hub commits: `21d1249` (Wave A dashboard) and the commit that adds this file.

### Notes per project

- **P1:**
  - The scorer applies spec §5.4–5.6. It uses a separate format-failure path and has a test for each of the five critical-error types.
  - Bootstrap intervals are deterministic from a recorded seed.
  - The report refuses to write mock runs into `results/` and never overwrites a results file.
  - The Track 4 spec paraphrases the public-domain NINDS scale and cites peer-reviewed sources only. It encodes 23 consistency rules and sets the major-error threshold at 4 points (Q-23).
  - Score vectors are written only to ignored `private/`.
- **P2:**
  - The soft scores use the spec's ×100 integer scaling.
  - Round-robin broke a hard rule in 9 of 50 scenarios, greedy in 3, and the solver in none.
  - The solver misses two §9 targets:
    - High-band continuity is 77.3%, against a target of 80%.
    - One scenario has an admission clash that could have been avoided.
  - Timefold Community 2.7.0 lacks `SolutionManager.analyze`, so explanations (P2-M4-2) will need the plain-Java replay.
- **P3:**
  - The literal reading of P3-Q019 lives in one CQL definition, so flipping it later is a one-line change.
  - `npm run verify` now also runs the Maven CQL build and needs JDK 21. RUNBOOK and RESUME were updated.
  - Translator 5.3.0 cannot reload ELM that contains functions. Keep the Library as CQL text for M4.
- **P4:**
  - HAPI's Bundle parser replaced resource ids with `urn:uuid:` entry URLs. The citation check would therefore have found no cited resources in overlay files.
  - The new `PatientBundle` reader parses each entry separately so resource ids are kept. The HAPI loader (P4-M1-2b) must keep ids the same way.
  - On the 37-patient cohort, layer 2 raised 0 false flags on 1,576 clean sentences and caught all 7,650 seeded mismatches.
- **P5:**
  - `gold.py` and the new engine share one core, `measures.py`. Engine and gold agree on all 60 truth vectors.
  - The generator refuses to produce more than 20 cases until the owner review (P5-M2-4) is done.
  - Sampler realism fixes changed the truth vectors for C06, C14, C15 and C31: those cases now use MCA stroke codes. Two new invariants cover midnight events and pre-arrival doses.

## Findings

1. **CI not observed.** The GitHub CLI is not installed, so the parent did
   not watch the Windows/Linux Actions runs for the six new repo commits.
   P3's CI now installs Java for the first time, and its Linux path has not
   run anywhere yet. Check the Actions tab, or install `gh`.
2. **New owner questions (28):**
   - P1 Q-16–Q-25:
     - scorer format and critical-error readings (Q-16, Q-17)
     - NIHSS coma, mute and ataxia readings (Q-18–Q-21)
     - cannot_score (Q-22)
     - the 4-point threshold (Q-23)
     - prompt design (Q-24)
     - sampler mix (Q-25)
   - P2 Q021–Q027: S1 rounding, S2/S3/S4 readings, orientee M1 grouping, fairness of the baselines, and metric definitions.
   - P3 Q021–Q022: a prior screen recorded as a date only, and response-selection readings.
   - P4 Q027–Q031: RxNorm matching until the offline table exists, section codes, unit rules, uncited explicit-none resources, and timing readings.
   - P5 Q020–Q023:
     - how `not_found` maps for AHASTR8 (Q020)
     - chart content outside the truth vector (Q021)
     - timing of evidence quotes (Q022)
     - C14's discharge medicines after a comfort-measures decision (Q023)
3. **New content awaiting owner review:**
   - P1: the Track 4 spec and rule list (P1-M2-1, P1-M2-2)
   - P3: the CQL library (tagged `authored-by-agent`)
   - P4: `docs/fact-sheet-and-verifiers.md`
   - P5:
     - the 20 chart packets (P5-M2-4; blank form in `data/review/P5-M2-4/`)
     - the engine paths (P5-M4-2)
     - `chart_text.py`
4. **P2 results are a first run, not a claim.** They are real and
   reproducible, but spec §9 targets, the fairness of the baselines (P2-Q026)
   and the limitations text (P2-M3-4) are the owner's to judge before any
   README results section.
5. **Registry hashes.** P5's agent edited `memory/PROJECT-BRIEF.md` (stale
   scope lines), so project-memory `health` will report that source as
   changed. Re-review it, rather than refreshing the hash blindly.
6. **Usage:** six Opus agents used about 2.8M tokens in this round, 300k–635k
   each. The weekly reset is Sep 27, 5am Pacific.

## State at the end of the round

- All six repos were clean and matched `origin/main` after their commits.
- The Nurse Handoff loop is `ready`; ticket 008 is the last one accepted.
- Test totals at the last parent reruns:
  - hub: 54
  - P1: 756
  - P2: 107
  - P3: 78 Node + 55 JUnit
  - P4: 106
  - P5: 536
- Every remaining agent task is either listed in the new
  [RESUME.md](RESUME.md) Wave C, or is blocked by an owner action, Docker, or
  a model and budget decision.
