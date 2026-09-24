# Nursing OS Project — agent contract

You are one iteration of an unattended loop. You have fresh context every
run. Everything you need to know is in files; everything you learn must be
written back to files before you exit.

## What this repository is

`Nursing_OS_Project` is a portfolio hub for clinical-informatics work. Its
first project is **Nurse Handoff**, a deterministic converter from a
synthetic patient JSON record to a nursing shift-handoff report. It lives in
`nurse-handoff/`. Specs are in `docs/`. The work ledger is `TASKS.md`.

## Environment

- Shell commands run in a sandbox with no network. Only this directory is
  writable. Bare `python` does not resolve; always use
  `nurse-handoff/.venv/Scripts/python.exe`.
- Use file edits and the shell only (venv python, powershell, git for
  read-only inspection). Do not use MCP tools, plugins, the browser,
  computer use, image generation, or web lookups even if offered. Never
  install anything.
- The loop runner prepends four lines to your prompt: `RUN`, `DATE` (use it
  for dated entries), `SEED` (unused here), and `HOST-VERIFY` (the host's
  own `tests/verify.ps1` result after the previous run, which is the truth).

## Loop contract

1. Read, in order: `memory/BLOCKED.md` (if present), `AGENTS.md`,
   `memory/HANDOFF.md`, `.loop/last-diff.txt` and `.loop/prev-message.md`
   (if present), `TASKS.md`, `docs/NURSE-HANDOFF-SPEC.md`,
   `docs/PATIENT-SCHEMA.md`, `docs/OUTPUT-FORMAT.md`. Then
   `memory/ACTIVE-DECISIONS.md` in full, then `memory/DECISIONS.md` (latest 30 lines; search earlier entries relevant to the selected unit), the last 15 lines of
   `memory/LOG.md`, and newly `answered` rows of `memory/QUESTIONS.md`.
2. Do exactly **one** ticket. Rule 0 first: if `HOST-VERIFY` says fail,
   the only unit of work is making `tests/verify.ps1` pass. Otherwise take
   the first unchecked bold-numbered item (`**001 ...**`) in `TASKS.md`
   whose "Blocked by" line is satisfied. The Definition of Done and Human
   checklist boxes are not tickets. Do not start a second ticket.
3. Finish the ticket completely, including its tests, before touching
   anything else. If the ticket is too big, report the proposed split in
   `memory/QUESTIONS.md` and block for owner planning. Do not rewrite
   ticket definitions or add new tickets during an unattended run.
4. Run the verification below. Do not describe a check as passed unless it
   ran in this session and passed. If the venv Python cannot execute, leave
   the ticket unticked and report status `blocked`, verify `not-run`, and
   the exact error. The controller archives the attempt for owner repair.
5. Before exiting: tick the ticket in `TASKS.md`; rewrite
   `memory/HANDOFF.md`; append one line to `memory/LOG.md` (end the file
   with a newline); add questions to `memory/QUESTIONS.md`; add any new
   durable decision to `memory/DECISIONS.md`.
6. If every item of the current version's **Definition of Done** block in
   `TASKS.md` is ticked and pytest passed in this session, create an empty
   file `DONE` in the project root and say so in `HANDOFF.md`. Otherwise
   never create it. The controller rolls back the candidate, including
   `DONE`, if independent sandbox verification disagrees.

## When you are blocked

A missing file or tool, a check the ticket requires that you cannot run,
two documents that contradict each other, or an instruction that conflicts
with this contract: stop. Do not take a different ticket, do not skip
ahead, do not edit the rules to make the ticket fit. Write
`memory/BLOCKED.md` with the ticket id, what you tried, the exact error
text or the two conflicting sentences with file and line, and the one
change a human must make. Leave the ledger unticked, still rewrite
`HANDOFF.md` and append the LOG line with `verify: not-run`, and return JSON with status blocked. The next run reads `BLOCKED.md` first and deletes it
only when the blocker is gone.

## Hard rules

- Synthetic data only. Never store or invent anything resembling a real
  patient, MRN, name, date of birth, or facility record.
- Never present generated clinical text as advice for a real patient.
- **Missing data stays missing.** `null` or absent means "not documented".
  Never turn unknown into an assumed value (no "Room air", no "None").
- No AI, LLM calls, web UI, database, FHIR, network, or authentication in
  v0.1 or v0.2. Those are roadmap items owned by the human.
- Work only inside this directory. Do not modify `.git`, do not commit, do
  not push, do not tag. The human owns git.
- **Protected files.** Never edit `AGENTS.md`, `PROMPT.md`, `loop.sh`,
  `tests/verify.ps1`, `docs/NURSE-HANDOFF-SPEC.md`, `docs/PATIENT-SCHEMA.md`,
  `docs/OUTPUT-FORMAT.md`, or the rules text of `TASKS.md`. The controller
  rejects and rolls back such changes. Maintain assigned checkboxes, preserve
  ticket definitions, and propose planning changes in `memory/QUESTIONS.md`.
  Tickets 103 and 106 may append a v0.2 field-extension section to the patient
  schema; preserve the existing v0.1 schema verbatim.
- Preserve existing work. Refactor only when the ticket asks for it.
- Python only: standard library plus pytest. No new dependencies without a
  ticket that says so.
- Determinism: same input, same output, byte for byte.

## Verification

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tests/verify.ps1
```

It runs pytest inside `nurse-handoff/.venv` when the package exists and,
once ticket 013 is ticked, runs the CLI on `nurse-handoff/data/chf_patient.json`.
Inside the sandbox you can also run pytest directly:

```
nurse-handoff/.venv/Scripts/python.exe -m pytest -q nurse-handoff
```

The venv is created and probed by the loop runner (`loops/setup.ps1`); if
it is missing or cannot execute, say so in `HANDOFF.md`. Do not pip install.

## Memory files

- `memory/HANDOFF.md` — rewrite every run. Max 40 lines: what you did, what
  the next run should do, the ids of still-open questions.
- `memory/LOG.md` — append one line per run:
  `- YYYY-MM-DD HH:MM | Ticket NNN <title> | files touched | verify: pass|fail|not-run`.
- `memory/QUESTIONS.md` — append-only table of questions for the human
  (`Q-NNN | date | question | open|answered | answer`). Never delete rows.
- `memory/DECISIONS.md` — durable choices with a one-line why. Append only.
- `memory/SOURCES.md` — external references with URL and date. Rarely needed.
- `memory/BLOCKED.md` — exists only while something blocks the loop.

## Controller protocol (2026-09-11)

The controller supplies WORK-ID and ASSIGNED UNIT. Perform that unit only;
do not select a different unit. Its explicit rotation cursor resolves repeated
unit types. Owner review limits are enforced before a model session starts.
When no approved work is eligible, the controller waits without model calls.

The controller preserves a pre-run snapshot, validates allowed transitions,
runs its own trusted verifier in the workspace sandbox, and accepts only
verified artifact progress. Invalid attempts are archived outside this workspace
and rolled back. Retry diagnostics are supplied in the next prompt. Do not
modify controller files, human checkboxes/checkpoints, owner Ruling cells,
owner proposal decisions, or memory/ACTIVE-DECISIONS.md. Changes by the owner
between runs are allowed; a commit is not required to establish the pre-run
snapshot. The agent still never commits, tags, or pushes.

Always read memory/ACTIVE-DECISIONS.md. Search append-only decision history
for older details relevant to your unit. Record every new durable decision
in memory/DECISIONS.md. Human maintenance refreshes the active summary.
Read only relevant sections of large indexes/glossaries using rg and bounded
file reads; compare proposed names, motifs and entities against the full index
by searching it. Do not load an ever-growing archive into every session.

## Owner-authorized GitHub synchronization (2026-09-24)

The owner requested automatic loop commits and chose a public repository at
https://github.com/Richard-Zellner/Nursing_OS_Project. The trusted controller may commit and push
only independently accepted work after the worker exits. The worker still
must not change `.git`, commit, tag, push, or handle credentials. This
controller exception supersedes older human-only Git statements; it does
not authorize releases, creative approvals, or publication to other platforms.
Owner source edits between runs must be reviewed, committed and pushed
before another Git-enabled unit. `.gitignore` and `.gitattributes` are
controller-protected during worker runs. Keep the working directory untouched
during an active unit. Pending pushes retry without rerunning accepted work.
