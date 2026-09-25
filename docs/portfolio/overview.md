# Nursing Informatics Portfolio: Project Plans

Sep 24, 2026 · @Richard Zellner

Eight projects become five repos: NurseBench bundles projects 1, 2, 4 and 5 as eval tracks, and 11, 7, 6 and 13 each get their own repo. NurseBench v0.1 ships by end of October (résumé-eligible), the full benchmark by January, then the optimizer, the FHIR pair and the stroke agent — roughly 325 hours, finishing around June 2027 at \~10 h/week.

## Build order

NurseBench goes first because it's the next step on your blueprint, and Track 1 alone makes it résumé-eligible. November stays light for NCA-GENL, and nothing gets built Dec 1–8 before CAHIMS.

| # | Repo | Projects | Target window | Rough hours | Why this slot |
| --- | --- | --- | --- | --- | --- |
| 1 | `nursebench` | 1, 4, 2, 5 (as tracks) | Oct 2026 – Jan 2027 | \~110 | Blueprint's next step; deterministic tracks (1, 4) before model-graded ones (2, 5) |
| 2 | `charge-assign` | 11 | Feb 2027 | \~45 | Pure Java; a fast win after exam season |
| 3 | `dysphagia-screen-fhir` | 7 | Mar 2027 | \~40 | FHIR on-ramp: Questionnaire + CQL before a full SMART app |
| 4 | `grounded-handoff` | 6 | Apr – May 2027 | \~60 | Blueprint's FHIR+AI project; reuses #7's local HAPI server |
| 5 | `stroke-abstraction-agent` | 13 | May – Jun 2027 | \~70 | Capstone; reuses NurseBench's seeded-case generator and NIHSS work |

Hours are rough, assuming AI-assisted coding at \~10 h/week. Running #11 alongside NurseBench would pull the finish date into spring.

Changes from the original list, based on the licensing and measure research:

- **Braden dropped from Track 4.** It needs a paid license. Morse is free but needs the author's permission, so it waits for v1.1. *(Update 2026-09-24: the owner dropped Morse; no fall-risk scale is planned.)*
- **Dysphagia screening and door-to-needle are Get With The Guidelines (GWTG) measures, not Joint Commission ones.** The Joint Commission retired its dysphagia measure (STK-7), so project 13 now pulls from both sources.
- **Inspect replaces promptfoo as the eval harness.** OpenAI acquired promptfoo in March 2026, which is awkward for a benchmark that also grades OpenAI models.

## Ground rules for every repo

Use synthetic or public data only, and write every clinical spec yourself — that authorship is the hiring signal.

- **No employer material.** That means no employer policies, order sets, Epic screenshots, build details or cases, even "de-identified" ones. The employer is never named or used, and portfolio work happens outside shift hours.
- **AI-assisted coding is fine.** The clinical spec, gold answers, rubrics and constraint weights must be yours, and you should be able to defend every scorer and constraint in an interview.
- **Résumé rule:** a repo goes on the résumé only once v0.1 is public. Metrics come only from actual runs.

| Source | Use in a public repo | Status |
| --- | --- | --- |
| NIH Stroke Scale (NINDS) | Items and scoring OK with NINDS citation; don't copy AHA/NIHSS certification-course material | Treated as public domain everywhere; no explicit NINDS statement found |
| Braden Scale | Don't embed item text | License fee required — verified |
| Morse Fall Scale | Not used (dropped by the owner on 2026-09-24) | Free, permission required — verified |
| TOR-BSST swallow screen | Don't use | Proprietary, paid training — verified |
| Schmitt-Thompson triage protocols | Don't reproduce | Proprietary — verified |
| NHS Safer Nursing Care Tool | Don't replicate its bands | Licensed — verified |
| MedlinePlus health-topic summaries (EN + ES) | Reuse freely; attribution requested | Public domain — verified |
| Raschke 1993 / Menon 2001 heparin nomograms | Encode the numbers with citation; write your own prose | Dosing facts, not expression — low risk (my read, not legal advice) |
| Yale swallow protocol, BJH-SDS, GUSS | Paraphrase the logic and cite; don't copy forms | No open license found |
| I-PASS | Cite Starmer, NEJM 2014; skip I-PASS Institute materials | Trademark status unconfirmed |
| MIMIC-IV demo | Attribution + share-alike on derived databases | Open Database License (ODbL) — verified |
| Full MIMIC (credentialed) | Never send to third-party LLM APIs | PhysioNet policy — verified |

Every repo ships with:

- A README (problem → why a nurse built it → demo GIF → results → limitations)
- `docs/clinical-spec.md`, written by you
- Tests plus GitHub Actions CI
- Licenses: Apache-2.0 for code, CC BY 4.0 for authored data
- A DISCLAIMER: educational, not a medical device, not clinical advice
- A CHANGELOG with tagged releases
- A 600–900-word write-up for LinkedIn

## What each repo proves

Each repo targets a different hiring signal, and together they cover the role families on your job scan.

| Repo | Hiring signal | Role types it maps to (examples from roles you've tracked) |
| --- | --- | --- |
| NurseBench | Clinical AI evaluation: RN-authored gold data, rubrics, critical-error taxonomies | AI clinical safety / validation / testing (Hippocratic AI AI Clinical Solutions Specialist, OutcomesAI Clinical Testing Manager, SmarterDx Clinical AI Data Specialist) |
| Optimizer (11) | Java + operations research on a real charge-nurse problem | Inpatient-flow implementation (LeanTaaS iQueue roles) |
| Dysphagia CDS (7) | FHIR Questionnaire, CQL, clinical decision support logic, terminology | Clinical informatics analyst / informaticist (hospital IT, Aledade, Verantos) |
| Handoff (6) | SMART on FHIR + grounded, verifiable LLM output | Clinical AI implementation / product (Abridge, Knowtex ambient-AI rollouts) |
| Stroke agent (13) | Agentic abstraction with evidence spans + human review | Quality / registry AI (Layer Health, SmarterDx quality roles) |
