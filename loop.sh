#!/usr/bin/env bash
# Compatibility entry point; the persistent controller owns locking and policy.
set -eu
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOOPS_DIR="$(cd "$PROJECT_DIR/../loops" && pwd)"
ARGS=(run --project "$(basename "$PROJECT_DIR")" --once)
[[ "${DRY_RUN:-0}" == "1" ]] && ARGS+=(--dry-run)
exec powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "$(cd "$LOOPS_DIR" && pwd -W)/controller.ps1" "${ARGS[@]}"
