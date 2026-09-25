# P3: Dysphagia Screen as FHIR CDS

[Master plan](../MASTER-PLAN.md) · [Progress](../PROGRESS.md) · [Runbook](../RUNBOOK.md)

| | |
|---|---|
| Repo | `dysphagia-screen-fhir`, a new repo at `C:\Users\14087\Desktop\dysphagia-screen-fhir` |
| Design authority | [docs/portfolio/dysphagia-screen-fhir.md](../../docs/portfolio/dysphagia-screen-fhir.md) |
| Stack | FHIR R4; FSH compiled with SUSHI (Node); CQL with cql-to-elm (Java/Maven); HAPI FHIR JPA server in Docker with Clinical Reasoning `$apply`; LHC-Forms |
| v0.1 | after M4: `$apply` on local HAPI returns the right CarePlan for every fixture |
| Finish line | v1.0.0: CI running HAPI in Docker against all fixtures, README, demo GIF, write-up |
| Window | Mar 2027, ~40 h |

## Before starting

- Owner: install Docker Desktop with WSL2 by the end of February; it was not
  installed on 2026-09-24. Check free RAM, and stop the manually run Qwen
  server while HAPI runs.
- Owner: JDK and Maven (installed for P2). SUSHI: `npm install -g fsh-sushi`
  (Node 24 is present).
- Owner: free loinc.org account; SNOMED CT browser access.
- M1 task: confirm the CQL version the pinned HAPI image's engine supports
  (1.5.x is widely deployed; 2.0.0 is trial-use).

## M1: clinical spec (~8 h)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P3-M1-1 | OWNER | `docs/clinical-spec.md`: the Yale Swallow Protocol paraphrased as primary and BJH-SDS as comparison (no form copied verbatim); final decision table (Incomplete / Unable / Fail / Pass) | Every path has a cited rationale |
| P3-M1-2 | OWNER | Pull the exact dysphagia-screening wording and class/level of evidence from the 2026 AHA/ASA guideline (DOI 10.1161/STR.0000000000000513). This was blocked during research. | Quoted with citation, or the gap stated |
| P3-M1-3 | OWNER | GWTG AHASTR8 anchor; note that TJC retired STK-7 | In spec |
| P3-M1-4 | OWNER | Terminology: confirm SNOMED 450819000 and 40739000; search LOINC for a bedside-swallow panel, and if none exists, justify a local CodeSystem citing AJSLP 2025 | Terminology table in spec |
| P3-M1-5 | PAIR | DISCLAIMER: "educational re-implementation of published screening logic; not a certified clinical tool; not affiliated with the original authors" | Present |

## M2: Questionnaire (~8 h)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P3-M2-1 | AGENT | Repo scaffold; SUSHI project (`sushi-config.yaml`) | `sushi .` builds with no errors |
| P3-M2-2 | AGENT | SDC Questionnaire in FSH, with pre-screen items gating water-trial items through `enableWhen`, following the owner's spec | Validates, and the gating matches the decision table |
| P3-M2-3 | AGENT | Static LHC-Forms page rendering the Questionnaire | Opens locally; gating works by hand |
| P3-M2-4 | OWNER | Check that item wording is a paraphrase, not a copy | Approved |

## M3: CQL logic and fixtures (~10 h)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P3-M3-1 | OWNER | Fixture table: 12–15 cases, each with its expected result (a clean pass, each failure sign alone, each exclusion alone, incomplete, contradictory, rescreen after a fail, a pass with no diet order) | Table in `docs/fixtures.md` |
| P3-M3-2 | AGENT | QuestionnaireResponse JSON for each fixture | Validates against the Questionnaire |
| P3-M3-3 | AGENT | CQL Library defining Screen Complete, Unable To Screen, Failed and Passed; ELM compiled in the Maven build | Compiles without errors |
| P3-M3-4 | AGENT | Tests evaluating the CQL against every fixture | All match the owner's table |

## M4: PlanDefinition and `$apply`, then v0.1 (~8 h)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P3-M4-1 | AGENT | `docker-compose.yml` for HAPI JPA with a pinned image and Clinical Reasoning enabled; load script | Server up and resources loaded. P4 reuses this file. |
| P3-M4-2 | AGENT | PlanDefinition (ECA rule) and ActivityDefinitions: NutritionOrder NPO, ServiceRequest SLP consult, CommunicationRequest to notify | Load without errors |
| P3-M4-3 | AGENT | Fixture runner: `$apply` per fixture, with the CarePlan/RequestGroup actions compared to the expected table (JUnit, or bash + curl + jq) | All fixtures pass |
| P3-M4-4 | OWNER | Release v0.1.0 | Release checklist |

## M5: CI and v1.0 (~6 h)

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P3-M5-1 | AGENT | GitHub Actions: SUSHI build, ELM compile, HAPI service container, all fixtures | Green |
| P3-M5-2 | PAIR | README, including the stroke-workflow note (screen before any PO, meds included; GWTG timing; link to P5), demo GIF, CHANGELOG | Owner approves |
| P3-M5-3 | OWNER | Release v1.0.0, write-up, résumé line with the real fixture count | Release checklist |

## Hand-offs

- To P4: the HAPI `docker-compose.yml`, load scripts, and terminology-lookup notes.
- To P5: the AHASTR8 logic and the timing rule (screen before first PO).

## Risks

| Risk | Response |
|---|---|
| `$apply` behavior differs across HAPI versions | Pin the image tag; record it in the README |
| Docker on Windows Home uses too much memory | Stop Qwen and cap WSL memory in `.wslconfig` |
| No LOINC panel exists | Local CodeSystem with a documented rationale, which is itself a finding |
