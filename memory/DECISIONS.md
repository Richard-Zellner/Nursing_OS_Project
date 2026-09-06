# Decisions (append only, one line of why each)

- 2026-09-04 Hub layout: `Nursing_OS_Project` is a portfolio hub; each project is a subfolder. First project: `nurse-handoff/`. Why: room for later projects (NurseBench, eval harnesses) without re-rooting.
- 2026-09-04 Runner: OpenAI Codex CLI, `gpt-5.6-luna`, `xhigh`, workspace-write sandbox, no approvals. Previous Pi harness retired. Why: single runner, native AGENTS.md support.
- 2026-09-04 Cadence: one ticket per iteration, one cycle every 4 h (fixed cadence, 6 cycles/day) via `../loops/run-all.sh`. Why: fresh context per ticket, small verified steps.
- 2026-09-04 Git: the loop never commits, tags, or pushes; the human does between cycles. Why: human review gate.
- 2026-09-04 Stack: Python standard library + pytest only, venv at `nurse-handoff/.venv` created by `loops/setup.ps1`. Why: sandbox has no network; keep dependencies at zero.
- 2026-09-04 v0.1 has no AI, web, database, or FHIR. After the human releases v0.1, the loop proceeds into the v0.2 rule tickets on its own but never into v0.3+. Why: owner instruction.
- 2026-09-04 Missing data stays missing: `null`/absent renders `Not documented`; explicit `[]` renders `None`; `oxygen:false` is a fact, `oxygen` absent is unknown. Why: core safety principle of the spec.
- 2026-09-04 Visibility: private development first; synthetic patients `SYNTH-###` only, no name/DOB/MRN/facility keys ever.
- 2026-09-05 Sandbox python: the Codex sandbox runs as `CodexSandboxOffline`; `loops/setup.ps1` grants that group read/execute on the Python install and probes the venv inside the sandbox. Bare `python` still does not resolve there; every command uses `nurse-handoff/.venv/Scripts/python.exe`. Why: verified 2026-09-05 that the per-user Python was unreadable to the sandbox.
- 2026-09-05 Host truth: `loop.sh` runs `tests/verify.ps1` on the host after every run, records it in `.loop/last-verify.txt`, feeds it back as `HOST-VERIFY`, and deletes `DONE` if the host disagrees. Why: the agent cannot be the only judge of its own checks.
- 2026-09-05 Protected files: AGENTS.md, PROMPT.md, loop.sh, tests/verify.ps1, docs/NURSE-HANDOFF-SPEC.md, and the rules text of TASKS.md are reverted by the loop runner if the agent edits them. Why: the loop must not rewrite its own contract or checks.
- 2026-09-05 Blocked protocol: a blocked run writes `memory/BLOCKED.md` and stops instead of improvising; three consecutive failed runs auto-pause the project with a STOP file. Why: unattended loops must fail loudly, not creatively.
