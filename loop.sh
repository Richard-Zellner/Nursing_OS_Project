#!/usr/bin/env bash
# loop.sh — run ONE Codex iteration for this project (Ralph loop body).
# Identical in all three projects; project-specific behaviour keys off $NAME.
# Called by ../loops/run-all.sh; also fine to run by hand.
#   bash loop.sh                one iteration
#   MAX_ITER=3 bash loop.sh     three back-to-back iterations (local testing)
#   DRY_RUN=1 bash loop.sh      print the command, run nothing
#   CODEX_TIMEOUT=5400          seconds before a run is killed (default 90 min)
#   EPHEMERAL=1                 add --ephemeral (no session rollout written to ~/.codex)
#   ALLOW_NO_BASELINE=1         run even if the repo has no commit (not recommended)
# Exit codes: 0 ok | 2 PROMPT.md missing | 3 locked | 4 sandbox prerequisite failed
#             5 no baseline commit | 6 codex flags changed | 7 agent left memory/BLOCKED.md
#             8 uncommitted edits to protected files | 124 timed out | else codex rc, then verify rc
set -u
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_WIN="$(cd "$PROJECT_DIR" && pwd -W)"
LOOPS_DIR="$(cd "$PROJECT_DIR/../loops" && pwd)"
NAME="$(basename "$PROJECT_DIR")"
MAX_ITER="${MAX_ITER:-1}"
MODEL="${MODEL:-gpt-5.6-luna}"
EFFORT="${EFFORT:-xhigh}"
CODEX_TIMEOUT="${CODEX_TIMEOUT:-5400}"
EXPECTED_CODEX="${EXPECTED_CODEX:-codex-cli 0.153.0}"
DRY_RUN="${DRY_RUN:-0}"
mkdir -p "$PROJECT_DIR/.loop" "$PROJECT_DIR/memory" "$LOOPS_DIR/diffs"
verify_rc=0

# Files the agent must never change. Human edits to these must be committed before a run.
PROTECTED=(AGENTS.md PROMPT.md loop.sh tests/verify.ps1)
case "$NAME" in
  Nursing_OS_Project) PROTECTED+=(docs/NURSE-HANDOFF-SPEC.md) ;;
  Megaphiliacs)       PROTECTED+=(docs/RUBRIC.md docs/SCRIPT-TEMPLATE.md) ;;
  Diaspora_of_Light)  PROTECTED+=(canon/00-CANON-LINE.md docs/STYLE.md characters/_TEMPLATE.md) ;;
esac

say() { echo "$NAME: $*"; }

# --- tooling checks ---------------------------------------------------------
if ! command -v codex >/dev/null 2>&1; then
  say "codex CLI not found on PATH (expected the npm global install)" >&2; exit 127
fi
if (( $(codex exec --help 2>/dev/null | grep -c -E -- '--output-last-message|--skip-git-repo-check|--sandbox|--profile') < 4 )); then
  say "codex exec flags changed ($(codex --version 2>/dev/null)); re-verify loop.sh before running" >&2; exit 6
fi
if [[ "$(codex --version 2>/dev/null)" != "$EXPECTED_CODEX" ]]; then
  say "warning: codex is '$(codex --version 2>/dev/null)'; this loop was validated with '$EXPECTED_CODEX'"
fi

# --- one iteration per project at a time (flock is not available in Git Bash) ---
LOCK="$PROJECT_DIR/.loop/lock"
if ! mkdir "$LOCK" 2>/dev/null; then
  say "another iteration holds $LOCK (rmdir it if stale)"; exit 3
fi
echo $$ > "$LOCK/pid"
trap 'rm -rf "$LOCK"' EXIT

# --- git helpers (the loop never commits; these only read or snapshot) ------
git_ok() { git -C "$PROJECT_DIR" rev-parse --verify HEAD >/dev/null 2>&1; }
protected_changes() { git -C "$PROJECT_DIR" diff --name-only HEAD -- "${PROTECTED[@]}" 2>/dev/null; }
# Snapshot the working tree (untracked included, .gitignore honoured) into a tree
# object through a throwaway index. Never touches the real index, refs, or history.
snap() {
  GIT_INDEX_FILE="$PROJECT_DIR/.loop/snap.index" git -C "$PROJECT_DIR" add -A . >/dev/null 2>&1
  GIT_INDEX_FILE="$PROJECT_DIR/.loop/snap.index" git -C "$PROJECT_DIR" write-tree 2>/dev/null
}

for ((i = 1; i <= MAX_ITER; i++)); do
  if [[ -f "$PROJECT_DIR/STOP" ]]; then say "STOP present, paused"; exit 0; fi
  if [[ -f "$PROJECT_DIR/DONE" ]]; then say "DONE present, nothing to do (delete DONE to continue)"; exit 0; fi
  if [[ ! -f "$PROJECT_DIR/PROMPT.md" ]]; then say "PROMPT.md missing"; exit 2; fi

  if ! git_ok; then
    if [[ "${ALLOW_NO_BASELINE:-0}" == "1" || "$DRY_RUN" == "1" ]]; then
      say "warning: no baseline commit; per-run diffs and protected-file checks are disabled"
    else
      say "no baseline commit; commit the scaffold first (git add -A && git commit) or set ALLOW_NO_BASELINE=1"; exit 5
    fi
  elif [[ -n "$(protected_changes)" ]]; then
    say "uncommitted edits to protected files ($(protected_changes | tr '\n' ' ')); commit them before running"; exit 8
  fi

  # Nursing pre-flight on the host (which has network): build the venv if missing,
  # then prove the sandbox user can execute it. Fails fast without spending a run.
  if [[ "$NAME" == "Nursing_OS_Project" && "$DRY_RUN" != "1" ]]; then
    VENV_PY="$PROJECT_DIR/nurse-handoff/.venv/Scripts/python.exe"
    if [[ ! -x "$VENV_PY" ]]; then
      say "nurse-handoff/.venv missing; running loops/setup.ps1"
      powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "$(cd "$LOOPS_DIR" && pwd -W)/setup.ps1" >> "$PROJECT_DIR/.loop/setup.log" 2>&1
    fi
    if ! codex sandbox -P :workspace -C "$PROJECT_WIN" -- "nurse-handoff\\.venv\\Scripts\\python.exe" -c "import pytest" >/dev/null 2>&1; then
      say "sandbox cannot execute nurse-handoff/.venv python; run loops/setup.ps1 (it grants CodexSandboxUsers read access to the Python install)"; exit 4
    fi
  fi

  STAMP="$(date '+%Y%m%d-%H%M%S')"
  NOW="$(date '+%Y-%m-%d %H:%M')"
  LOG="$PROJECT_DIR/.loop/iteration-$STAMP.log"
  LAST="$PROJECT_DIR/.loop/last-message.md"
  LOGMD="$PROJECT_DIR/memory/LOG.md"
  LASTVERIFY="$PROJECT_DIR/.loop/last-verify.txt"
  prev_verify="$(head -n1 "$LASTVERIFY" 2>/dev/null || true)"
  prev_verify="${prev_verify:-none (first run)}"
  seed="$(shuf -n1 "$LOOPS_DIR/seeds-$NAME.txt" 2>/dev/null || true)"
  seed="${seed:-none}"
  lines_before=$(grep -c '^- ' "$LOGMD" 2>/dev/null || echo 0)

  # Prompt is fed on stdin ("-") so Windows argument quoting never touches it.
  # -p loop layers ~/.codex/loop.config.toml (notify off, MCP servers off) on the base config.
  CMD=(codex exec -C "$PROJECT_WIN" -p loop
       -m "$MODEL" -c "model_reasoning_effort=\"$EFFORT\""
       -c "approval_policy=\"never\"" -s workspace-write
       --disable browser_use --disable computer_use --disable image_generation
       --skip-git-repo-check --color never
       -o "$PROJECT_WIN/.loop/last-message.md" -)
  if [[ "${EPHEMERAL:-0}" == "1" ]]; then CMD+=(--ephemeral); fi

  if [[ "$DRY_RUN" == "1" ]]; then
    printf '%s: DRY_RUN\n  timeout -k 60 %s ' "$NAME" "$CODEX_TIMEOUT"; printf '%q ' "${CMD[@]}"
    printf '< {RUN/DATE/SEED/HOST-VERIFY header + PROMPT.md (%s bytes)}\n' "$(wc -c < "$PROJECT_DIR/PROMPT.md")"
    printf '  seed=%s | previous host verify=%s\n' "$seed" "$prev_verify"
    continue
  fi

  say "iteration $i start $STAMP"
  [[ -f "$LAST" ]] && cp -f "$LAST" "$PROJECT_DIR/.loop/prev-message.md"
  rm -f "$LAST"
  before="$(snap)"
  {
    printf 'RUN: %s\nDATE: %s\nSEED: %s\nHOST-VERIFY (previous run): %s\n\n' "$STAMP" "$NOW" "$seed" "$prev_verify"
    cat "$PROJECT_DIR/PROMPT.md"
  } | timeout -k 60 "$CODEX_TIMEOUT" "${CMD[@]}" > "$LOG" 2>&1
  rc=$?
  if (( rc == 124 )); then say "codex timed out after ${CODEX_TIMEOUT}s (log: $LOG)"; else say "codex exit $rc (log: $LOG)"; fi

  # What changed this run (a patch for review; still no commit).
  after="$(snap)"
  if [[ -n "$before" && -n "$after" ]]; then
    git -C "$PROJECT_DIR" diff-tree -r -p --stat "$before" "$after" > "$PROJECT_DIR/.loop/last-diff.patch" 2>/dev/null
    git -C "$PROJECT_DIR" diff-tree -r --stat "$before" "$after" > "$PROJECT_DIR/.loop/last-diff.txt" 2>/dev/null
    cp -f "$PROJECT_DIR/.loop/last-diff.patch" "$LOOPS_DIR/diffs/$NAME-$STAMP.patch"
    { echo '--- changed this run'; cat "$PROJECT_DIR/.loop/last-diff.txt"; } >> "$LOG"
  fi

  # The agent must not rewrite its own contract or its checks.
  if git_ok; then
    changed="$(protected_changes)"
    if [[ -n "$changed" ]]; then
      # shellcheck disable=SC2086
      git -C "$PROJECT_DIR" checkout -- $changed
      say "agent edited protected files, reverted: $(echo "$changed" | tr '\n' ' ')"
      printf -- '- %s | loop.sh reverted agent edits to protected files: %s | see .loop/iteration-%s.log and loops/diffs/%s-%s.patch\n' \
        "$NOW" "$(echo "$changed" | tr '\n' ' ')" "$STAMP" "$NAME" "$STAMP" >> "$PROJECT_DIR/memory/BLOCKED.md"
    fi
  fi

  # Verify on the host, independently of what the agent claimed.
  if [[ -f "$PROJECT_DIR/tests/verify.ps1" ]]; then
    powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "$PROJECT_WIN/tests/verify.ps1" >> "$LOG" 2>&1
    verify_rc=$?
    say "verify exit $verify_rc"
  fi
  verify_word=pass; (( verify_rc != 0 )) && verify_word=fail
  printf '%s | %s | codex=%s | run=%s\n' "$verify_word" "$NOW" "$rc" "$STAMP" > "$LASTVERIFY"

  # DONE is only valid when the host verification agrees.
  if [[ -f "$PROJECT_DIR/DONE" && $verify_rc -ne 0 ]]; then
    rm -f "$PROJECT_DIR/DONE"; say "agent wrote DONE but host verify failed; DONE removed"
  fi

  # Guarantee a LOG.md line in the documented shape if the agent did not add one.
  lines_after=$(grep -c '^- ' "$LOGMD" 2>/dev/null || echo 0)
  if (( lines_after <= lines_before )); then
    if [[ -s "$LOGMD" && -n "$(tail -c1 "$LOGMD")" ]]; then echo >> "$LOGMD"; fi
    printf -- '- %s | (loop fallback: agent wrote no log line) | .loop/iteration-%s.log | verify: %s\n' "$NOW" "$STAMP" "$verify_word" >> "$LOGMD"
  fi

  # Keep only the 30 most recent iteration logs.
  ls -1t "$PROJECT_DIR"/.loop/iteration-*.log 2>/dev/null | tail -n +31 | xargs -r rm -f

  if (( rc != 0 )); then exit "$rc"; fi
  if [[ -f "$PROJECT_DIR/memory/BLOCKED.md" ]]; then say "memory/BLOCKED.md present; human action needed"; exit 7; fi
done
exit "$verify_rc"
