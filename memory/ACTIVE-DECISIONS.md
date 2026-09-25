# Active decisions (owner-maintained summary)

- This is a clinical-informatics portfolio hub. The first product is the deterministic Nurse Handoff package under nurse-handoff/.
- Synthetic data only. Missing data remains unknown; null or absent never becomes assumed room air or an empty list.
- Python standard library plus pytest only. Use nurse-handoff/.venv/Scripts/python.exe. No installation during a worker run.
- v0.1 and v0.2 are finite approved milestones. The human owns releases and any v0.3 scope. DONE must pass independent milestone checks.
- Ticket 001 permits pytest exit 5 and requires CLI usage/exit 2. Later completed tickets require their files and tests. Patient CLI checks begin at ticket 013.

- The shared controller in ../loops owns scheduling, per-project state, retry limits, rotation, and acceptance.
- Runs use gpt-5.6-luna with xhigh reasoning. Each run gets a fresh session and one assigned WORK-ID.
- Shell work and independent generated-code verification run in the workspace sandbox. No network tools, publishing, commits, tags, or pushes are allowed to the worker.
- The controller archives before/candidate snapshots. A rejected attempt is rolled back; successful artifact progress advances state. For Git-enabled runs, owner edits must be reviewed, committed and pushed before the next unit.
- Rules, verifier scripts, this active summary, human checkpoints, release checkboxes, and existing owner decisions are protected by before/after comparisons. Questions and decision logs are append-only.
- Return structured JSON with status, work_id, summary, artifact_paths, and verify. No log-only run counts as progress.
- After three failures or two successful exits with no artifact progress, the controller blocks until an explicit reset after repair.
- Read this active summary, recent decision history, and search older relevant decisions. Search growing indexes/glossaries for the selected unit instead of reading the entire archive each time.

Full historical rationale is preserved in DECISIONS.md. The owner refreshes this summary during review.

- 2026-09-24 Owner authorized automatic controller commits/pushes after independent acceptance to https://github.com/Richard-Zellner/Nursing_OS_Project (public). Workers remain unable to commit or handle credentials; release and creative review gates still apply.
- 2026-09-24 Owner decision D-1: the five portfolio projects are separate GitHub repositories; this hub is the index, delivery plan (plans/) and home of nurse-handoff/.
- 2026-09-24 Owner decisions G0 and D-4: portfolio work happens off shift and never names or uses the employer; new portfolio repos stay private until their release.
