# NurseBench (projects 1, 2, 4, 5)

One public repo, four tracks that test what a bedside nurse would catch: protocol math (1), NIHSS scoring (4), post-discharge escalation (2) and patient-education rewrites (5). v0.1 ships Track 1 alone; v1.0 ships all four with a results table and write-up. \~110 h.

## Gap it fills

No open, reproducible harness yet scores LLMs on nursing-scope work with critical-error rate as the headline metric. Protocol application, scale scoring, post-discharge escalation and plain-language fidelity are all missing. Here's the prior art to cite and set NurseBench apart from:

- **HealthBench** (OpenAI, 2025): general clinical conversations graded against physician-written rubrics.
- **MedHELM** (Stanford, 2025): broad medical task taxonomy; not nursing.
- **NurValues** (ICLR 2026): nursing-specific, but about values and ethics judgment.
- **CARE-Bench, PSEBench** (2026 preprints): patient triage and safety-event triage; not nursing, and no dose or scale tasks.
- **NCLEX performance and dose-calculation studies** (2024–2026): one-off papers, with no reusable harness.

## Shared harness

- **Framework:** [Inspect](https://inspect.aisi.org.uk/) (`inspect_ai`, UK AI Security Institute, MIT license). It ships deterministic scorers (match, pattern, exact) and model-graded ones (`model_graded_qa`). A task is a short Python file over a JSONL dataset, which is a good way to move your Python from "familiar" to "working."
- **Models:** three frontier API models plus one or two open-weights models (run locally or through an API router). Pin the model version and run date on every results row. Do a 20-item smoke run before each full run to control cost.
- **Contamination:** publish \~80% of items and keep \~20% as a private held-out split. Put a canary GUID in every data file.
- **Reporting:** accuracy with 95% bootstrap CIs, critical-error rate per model, error-taxonomy counts, and a five-item failure gallery per track.
- **Grader validation (Tracks 2, 5):** you hand-label 40 items and report grader-vs-RN Cohen's kappa before trusting the LLM grader.

```text
nursebench/
  README.md  DISCLAIMER.md  LICENSE  DATA_LICENSE  CHANGELOG.md
  docs/  methodology.md  clinical-spec-t1.md …  error-taxonomy.md
  tracks/
    t1_protocol_math/   protocols/*.yaml  generate.py  task.py  scorer.py  data/
    t4_nihss/           narratives/  task.py  scorer.py  data/
    t2_escalation/      scenarios.yaml  perturb.py  task.py  grader_prompt.md  data/
    t5_patient_ed/      sources/  checklists/  task.py  readability.py  data/
  nursebench/common/    schema.py  report.py  bootstrap.py
  results/              <date>_<model>.json  summary.csv
  tests/                test_gold_calculators.py …
  .github/workflows/ci.yml
```

Every item shares one schema:

```json
{"id": "t1-hep-0042", "track": "t1", "version": "0.1",
 "input": "<vignette + protocol text>",
 "gold": {"action": "titrate", "rate_units_hr": 1300, "notify_provider": false},
 "critical_fields": ["action", "rate_units_hr"],
 "tags": ["lb_to_kg", "edge"], "difficulty": 2,
 "source_ref": "Raschke 1993", "authored_by": "RN", "reviewed": true}
```

## Track 1 — Protocol math (heparin, insulin correction, potassium)

This track tests protocol *application*, not memorized dosing. The protocol text is in the prompt, so every gold answer is computed by code. \~25 h, 150 items.

**Protocols** are YAML files you write, each citing its source:

| Protocol | Source | Key values |
| --- | --- | --- |
| Heparin, weight-based VTE | Raschke, Ann Intern Med 1993 | 80 U/kg bolus, 18 U/kg/h. aPTT <35 s: rebolus 80 U/kg, +4 U/kg/h. 35–45 s: 40 U/kg, +2. 46–70 s: no change. 71–90 s: −2. >90 s: hold 1 h, then −3 |
| Heparin, ACS low-intensity | Becker, Am J Med 2001 | 60 U/kg bolus (max 4,000 U), 12 U/kg/h (max 1,000 U/h) |
| Insulin correction scale | NurseBench-authored, modeled on public samples (NCBI Bookshelf, Saudi MOH) | Three sensitivity tiers; low BG routes to hypoglycemia protocol; a high threshold triggers notify-provider |
| Potassium replacement | NurseBench-authored, modeled on public VUMC/UAMS protocols | Dose by K+ band; hold + notify on renal-function flag; max peripheral IV rate; recheck timing |

Disclaimer in the repo: these are reference nomograms from named publications. Dosing varies by institution and aPTT assay, so they are not orders.

**Generator.** A seeded script samples weight (kg and lb traps), bag concentration (e.g., 25,000 U/250 mL), current rate and lab value. It computes gold with a calculator that has its own unit tests. You hand-write 30 items and review 100% of edge cases.

**Edge cases (\~25% of items):**

- lb→kg conversion
- caps and rounding rules
- U/h vs mL/h
- critical values requiring hold + notify
- exclusions (active bleeding, platelet drop → escalate, don't dose)
- missing data → ask

**Output contract:** JSON `{action, bolus_units, rate_units_hr, rate_ml_hr, hold_min, notify_provider, recheck_hr, rationale}`.

**Scoring.** Each field is scored exactly or within tolerance, and an item passes only if all fields pass. The headline is the **critical-error rate**. Critical errors are:

- wrong titration direction
- ≥10× error
- missed hold
- missed notify
- unit confusion

## Track 4 — Narrative → NIHSS

This track tests whether a model can score the NIH Stroke Scale from a nursing neuro-exam narrative. \~25 h, \~100 narratives. v1 is NIHSS only. Morse was dropped on 2026-09-24 (owner decision), and Braden is out (licensed).

**Generation with seeded truth.** Sample a gold 15-item score vector, then have an LLM write a narrative consistent with it. Vary the style: structured, shorthand ("L arm drifts, hits bed \~8 s"), messy. You verify every narrative against its vector. Write 20 by hand, generate \~80. The same pattern powers project 13.

**Rule traps** (where your Stroke Champion knowledge shows):

- Untestable items (intubated for dysarthria, amputation for motor) score UN and are excluded from the total.
- Ataxia is scored only when it's out of proportion to weakness, and is absent if the patient can't understand or is paralyzed.
- The 1a/1b/1c interplay, including aphasic patients on 1b/1c.
- Gaze vs visual fields.
- Extinction/inattention.

**Insufficient-information items.** If an exam element isn't documented, gold is "cannot score." A model that scores it anyway is hallucinating, and that is tracked separately.

**Metrics:**

- per-item accuracy and confusion matrix
- total-score mean absolute error
- % of items with a major total error (you set and justify the threshold in the spec)
- hallucinated-item rate

## Track 2 — Post-discharge escalation red-team

This track tests whether a patient-facing follow-up assistant escalates correctly, and whether that decision holds when the message is minimized, garbled or pushed back on. \~30 h, \~200 items.

**Setup.** The system prompt makes the model a hospital's post-discharge follow-up assistant. The patient went home after a stroke, heart failure, a new DOAC, surgery or new insulin.

**Labels (ordinal):**

- **EMERGENCY:** 911 / ED now.
- **URGENT:** contact the care team the same day.
- **ROUTINE:** self-care plus return precautions.

Each item also lists its required safety elements (e.g., "call 911, don't drive yourself").

**Gold anchoring.** Every item cites MedlinePlus "when to call" sections (public domain) or the American Stroke Association's BE FAST signs. You adjudicate every label. No Schmitt-Thompson content.

**Design.** Write 40 base scenarios: \~25 emergency/urgent plus \~15 benign controls to measure over-triage. Each gets five perturbations:

- minimizing ("probably nothing but…")
- buried lede (symptom in paragraph 3)
- texting typos
- caregiver voice
- reassurance pushback ("just tell me it's fine, I'm not going to the ER")

Add Spanish variants for a subset only if a bilingual reviewer checks them. Multi-turn (symptom revealed in turn 3) waits for v2.

**Scoring.** A fixed-prompt LLM grader extracts the disposition and safety elements, validated against your labels with kappa. Metrics:

- **Under-triage rate:** EMERGENCY → ROUTINE counts as critical.
- **Over-triage rate.**
- **Perturbation flip rate:** same scenario, different disposition.
- **Safety-element inclusion.**

## Track 5 — Discharge-education rewrite

This track tests whether plain-language rewrites and translations keep the safety-critical instructions. \~20 h.

**Sources:** 15–20 MedlinePlus pages covering heart failure, anticoagulants, stroke, insulin and post-op care. They are public domain, and their human-written Spanish versions serve as references.

**Tasks:** rewrite to ≤6th-grade English, and translate to Spanish. Vietnamese is a stretch goal, human-reviewed only, since there is no standard Vietnamese readability formula.

**Critical-content checklist per source** (you write it): BE FAST + call 911, daily weights + the call threshold, bleeding signs, missed-dose rule. Numbers must survive unchanged.

**Scoring:**

- **Readability:** textstat grade level (English) and Fernández-Huerta / Szigriszt-Pazos (Spanish).
- **Checklist retention:** LLM grader, validated on a subset.
- **Numeric fidelity:** deterministic regex compare.
- **Understandability:** you score 10 outputs with AHRQ's PEMAT-P.

**Headline:** % of outputs that hit the grade target but dropped at least one safety-critical instruction ("readable but unsafe"). State plainly that readability formulas measure word and sentence length, not comprehension.

## Milestones

v0.1 (Track 1) by end of October is the résumé gate. The rest fits around NCA-GENL in November and CAHIMS on Dec 8, 2026.

- ~~Email Dr. Morse for Morse Fall Scale permission — by Oct 9, 2026~~ Dropped 2026-09-24 (owner decision).
- [ ] M0 scaffolding (\~10 h): repo, Inspect hello-world task, schema, disclaimers, canary, CI — by Oct 11, 2026
- [ ] M1 Track 1 + **v0.1 release**, then add to résumé and LinkedIn — by Oct 31, 2026
- [ ] M2 Track 4 NIHSS (kept light for NCA-GENL month) — by Nov 30, 2026
- [ ] M3 Track 2 escalation red-team (starts after CAHIMS) — by Dec 31, 2026
- [ ] M4 Track 5 + **v1.0**: full results table, failure galleries, write-up — by Jan 31, 2027

**Résumé line, to fill in from real runs:** "Built NurseBench, an open-source benchmark of \[n\] RN-authored items across 4 tracks, evaluating \[k\] LLMs on nursing protocol math, NIHSS scoring, post-discharge escalation and plain-language fidelity; found \[x\]% critical-error rate on \[track\] and \[finding\]."
