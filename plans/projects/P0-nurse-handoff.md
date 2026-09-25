# P0: Nurse Handoff (finish v0.1 and v0.2)

[Master plan](../MASTER-PLAN.md) · [Progress](../PROGRESS.md) · [Runbook](../RUNBOOK.md)

| | |
|---|---|
| Location | this hub, `nurse-handoff/` |
| Design authority | [spec](../../docs/NURSE-HANDOFF-SPEC.md), [patient schema](../../docs/PATIENT-SCHEMA.md), [output format](../../docs/OUTPUT-FORMAT.md) |
| Task ledger | [`TASKS.md`](../../TASKS.md), the only place ticket state lives |
| Execution | unattended loop, one ticket per run, up to 6 runs a day (`../loops`) |
| Finish line | v0.2.0 tagged and pushed; hub README shows "v0.2 released" |
| Owner effort | about 6 h: two release reviews plus a portfolio polish pass |

## Current state (2026-09-24)

Tickets 001–003 are done and pushed (`916b48b`). The next ticket is 004 Loader.
The loop is enabled, but today's six runs are spent, so work resumes after
the local-day reset.

## Milestones

### P0-M1: v0.1 build (loop)

Tickets 004–015 in `TASKS.md`. There are 12 tickets. At 6 runs a day and
with no failures, that is about 2 days.

The owner only needs to act when:
- `memory/BLOCKED.md` appears, or a `memory/QUESTIONS.md` row is `open`
- the controller reports a Git error: run
  `..\loops\controller.ps1 git-sync --project Nursing_OS_Project`
- the owner edits any file, including files in `plans/`. Commit and push the
  edit before the next unit. The controller refuses to start on a dirty tree.

Done when all ten v0.1 Definition of Done boxes are ticked and the `DONE`
file exists after controller verification.

### P0-G1: v0.1 release gate (owner)

1. Run the verifier and read the real output for all four patients:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File tests/verify.ps1
   cd nurse-handoff
   foreach ($p in 'simple','chf','incomplete','complex') { .\.venv\Scripts\python.exe -m nurse_handoff "data\${p}_patient.json" }
   ```
2. Check against spec §5: missing data renders `Not documented`, no
   `Room air` is invented, and warnings match spec §8.
3. Tick the human-checklist boxes that are already true ("Create the GitHub
   repository…", Q-001 answered). Tick "v0.1 released" and delete `DONE`.
4. `git tag v0.1.0`, then commit and push the checklist edit and the tag
   before the next loop unit.
5. Update [PROGRESS.md](../PROGRESS.md).

### P0-M2: v0.2 clinical rules (loop)

Tickets 101–110: version bump, rules 5–9, the ticket-107 placeholder
deletion, patients E and F, the rule registry, and the v0.2 Definition of
Done. That is about 2 more loop days. Tickets 103 and 106 may append a v0.2
section to `PATIENT-SCHEMA.md`, and the controller enforces that.

### P0-G2: v0.2 release gate (owner)

Same steps as G1, plus a check of `python -m nurse_handoff --rules`. Tag
`v0.2.0`. Record decision **D-2**, which proposes that the spec roadmap
v0.3–v0.6 moves to P4 Grounded Handoff. If the owner instead wants a v0.3 web
UI here, add owner-approved tickets to `TASKS.md` and extend this plan.

### P0-M3: portfolio polish (pair, after G2)

Bring the hub up to the shared standard without disturbing the loop. Do
this between loop runs, or after the loop is disabled for this project.

| Task | Type | Deliverable | Acceptance |
|---|---|---|---|
| P0-M3-1 | AGENT | `LICENSE` (Apache-2.0), `DISCLAIMER.md`, `CHANGELOG.md` with v0.1.0 and v0.2.0 entries | Files present; CHANGELOG matches the tags |
| P0-M3-2 | AGENT | `.github/workflows/ci.yml` running pytest on Python 3.11 | CI green on `main` |
| P0-M3-3 | AGENT | Sample-output block or terminal GIF in `nurse-handoff/README.md` | Output copied from a real CLI run |
| P0-M3-4 | OWNER | 600–900-word write-up: why "missing stays missing" matters at the bedside | Posted, and linked from the hub README |
| P0-M3-5 | OWNER | Decide whether the loop keeps running here after v0.2 (projects.json `enabled`) | Decision recorded |

## Hand-offs

- The rule that `null` or absent means not documented, never normal, carries
  into P4's required-content checklist and omission flags.
- The spec's research question (can AI handoffs be checked against the
  source record?) is the core of P4.

## Risks

| Risk | Response |
|---|---|
| Loop blocks on a ticket that is too large | Read `BLOCKED.md`/`QUESTIONS.md`, split the ticket as the owner, commit and push, then reset through the controller |
| Owner edits left uncommitted stall the loop | Commit and push after every edit session, including edits under `plans/` |
| Model-usage limits | The loop waits and resumes; nothing needs to happen |
