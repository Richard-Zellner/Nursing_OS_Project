# P5: Stroke Abstraction Agent (capstone)

[Master plan](../MASTER-PLAN.md) · [Progress](../PROGRESS.md) · [Runbook](../RUNBOOK.md)

| | |
|---|---|
| Repo | `stroke-abstraction-agent`, a new repo at `C:\Users\14087\Desktop\stroke-abstraction-agent` |
| Design authority | [docs/portfolio/stroke-abstraction-agent.md](../../docs/portfolio/stroke-abstraction-agent.md) |
| Stack | Python, with orchestration chosen at M3 (D-7); JSON-schema structured outputs; one local open-weights model; a small review-queue web page |
| Measures (v1) | STK-2, STK-5, STK-6, STK-10 (Joint Commission) plus AHASTR8 (GWTG dysphagia) |
| v0.1 | after M4: an end-to-end pipeline on 60 cases with element accuracy reported |
| Finish line | v1.0.0: review queue, router curve, human-agreement kappa, cost per chart, write-up |
| Window | mid-May to Jun 2027, ~70 h |

## Before starting

- P1 finished (seeded generator and kappa tooling to reuse); P3 finished
  (AHASTR8 logic).
- M1 task: check whether a newer Joint Commission Specs Manual than v2026A1
  or newer GWTG definitions exist, and use the current ones.
- Owner: decide D-7 (orchestration) at the start of M3.
- Local model: check whether the RGB Qwen server is running and has enough
  memory, or pick another open-weights route.

## M1: measure digest (~12 h)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P5-M1-1 | OWNER | `docs/measure-digest.md`: paraphrased data-element table and algorithm flow (denominator → exclusions → numerator) for each measure, from the Specs Manual and GWTG definitions | Every element cites its manual section |
| P5-M1-2 | OWNER | Hospital-day rules and edge cases (arrival near midnight, thrombolytic timing) | In the digest |

## M2: synthetic charts with seeded truth (~15 h)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P5-M2-1 | OWNER | Truth-vector field definitions and the distractor catalog (home vs discharge meds, held-then-given aspirin, negation, midnight ambiguity, copy-forward text, contradictions, wrong-role documentation) | In `docs/clinical-spec.md` |
| P5-M2-2 | AGENT | Truth-vector sampler (adapted from P1, with a note of its origin) | Seeded and tested |
| P5-M2-3 | AGENT | Chart-packet generator: ED note, H&P, 2–3 nursing notes, MAR table, discharge med rec, discharge summary | Packet plus truth vector per case |
| P5-M2-4 | OWNER | Hand-validate the first 20 cases before the other 40 are generated | 20/20 reviewed; fixes fed back into the generator |
| P5-M2-5 | AGENT | Generate the remaining 40; the owner spot-checks | 60 cases total |

## M3: segmenter, extractors, evidence verifier (~15 h)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P5-M3-1 | OWNER | D-7 orchestration choice | Recorded |
| P5-M3-2 | AGENT | Segmenter: documents, timestamps, hospital-day index | Unit tests, including the midnight cases |
| P5-M3-3 | AGENT | Extractors, one per element group, returning `{element, value, evidence:[{doc_id, quote, char_start, char_end}], confidence}` | Schema-valid output |
| P5-M3-4 | AGENT | Evidence verifier: the quote appears at its offsets and dates are consistent | Tests with corrupted spans |

## M4: measure engine, then v0.1 (~10 h)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P5-M4-1 | AGENT | Deterministic measure engine following the digest | One unit test per algorithm path |
| P5-M4-2 | OWNER | Review the engine paths against the digest | Signed off |
| P5-M4-3 | AGENT | End-to-end run on all 60 cases; element accuracy/F1 and measure agreement | Real results committed |
| P5-M4-4 | OWNER | Release v0.1.0 | Release checklist |

## M5: review queue and router (~8 h)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P5-M5-1 | AGENT | Router with confidence and conflict thresholds | Configurable; tested |
| P5-M5-2 | AGENT | Review page showing the element, proposed value and highlighted evidence, with accept/override; every decision logged | Works locally |

## M6: evaluation and v1.0 (~10 h)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P5-M6-1 | OWNER | Blind abstraction of 20 cases (plus a colleague if one is available) | Labels committed |
| P5-M6-2 | AGENT | Metrics: evidence validity, automation-vs-accuracy curve across thresholds, cost and latency per chart, human–human and human–pipeline kappa | Results from real runs |
| P5-M6-3 | AGENT | Open-weights model run for comparison | In the results table |
| P5-M6-4 | PAIR | README (the LLM-extracts, code-computes split as the headline design point), prior art, limitations, CHANGELOG | Owner approves |
| P5-M6-5 | OWNER | Release v1.0.0, write-up, résumé line | Release checklist |

v2 (outside this plan): STK-1, STK-3, and GWTG door-to-needle (AHASTR13/49).

## Risks

| Risk | Response |
|---|---|
| Generated charts are too clean | Distractor catalog; owner validation of the first 20 |
| Cost per chart | Measure it early on 5 cases; cache extractor outputs |
| Local model too slow or large for RGB | Run the open-weights comparison on a subset; state it |
