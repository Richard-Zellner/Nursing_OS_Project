# Iteration log (append one line per run)

Format: `- YYYY-MM-DD HH:MM | Ticket NNN <title> | files touched | verify: pass|fail|not-run`
Use the DATE line the loop runner puts at the top of the prompt. End the file with a newline.

- 2026-09-04 20:30 | bootstrap (human) | AGENTS.md PROMPT.md TASKS.md docs/* tests/verify.ps1 memory/* loop.sh | verify: pass
- 2026-09-05 18:30 | review fixes (human) | loop.sh PROMPT.md AGENTS.md TASKS.md tests/verify.ps1 memory/* | verify: pass
