# Handoff

Status: scaffold complete and reviewed, no product code yet. Next run takes
Ticket 001.

## What the last run did

Human bootstrap (2026-09-04) wrote the loop scaffold. Human review fixes
(2026-09-05): the loop runner now builds and probes `nurse-handoff/.venv`
itself, feeds a RUN/DATE/SEED/HOST-VERIFY header, snapshots a per-run
diff, reverts edits to protected files, and records the host verify result
in `.loop/last-verify.txt`. The sandbox can execute the venv python (probe
passed); bare `python` does not resolve there.

## What the next run should do

Ticket 001 (Skeleton) in `TASKS.md`. Use
`nurse-handoff/.venv/Scripts/python.exe` for every python or pytest
command. The venv already exists with pytest installed.

## Open questions for the human

- Q-001 (memory/QUESTIONS.md): when to create the GitHub repository.
