# Project-local verification for Nursing OS Project / nurse-handoff.
# Exit 0 = pass, 1 = fail. No external harness. Runs on the host after every
# loop iteration and inside the sandbox when the agent calls it.
[CmdletBinding()]
param()
$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
$failures = 0
function Check([string]$name, [bool]$ok, [string]$detail) {
    $label = if ($ok) { 'PASS' } else { 'FAIL' }
    Write-Host ("{0,-5} {1,-34} {2}" -f $label, $name, $detail)
    if (-not $ok) { $script:failures++ }
}

# 1. Required loop documents.
foreach ($f in 'AGENTS.md', 'PROMPT.md', 'TASKS.md', 'README.md', 'memory/HANDOFF.md', 'memory/DECISIONS.md', 'memory/LOG.md', 'memory/QUESTIONS.md',
                'docs/NURSE-HANDOFF-SPEC.md', 'docs/PATIENT-SCHEMA.md', 'docs/OUTPUT-FORMAT.md') {
    Check "required:$f" (Test-Path (Join-Path $root $f) -PathType Leaf) ''
}

# 2. Memory discipline: HANDOFF stays short, LOG lines keep their shape, QUESTIONS is a table.
$handoff = @(Get-Content (Join-Path $root 'memory/HANDOFF.md') -ErrorAction SilentlyContinue)
Check 'handoff-lines' ($handoff.Count -le 40) "$($handoff.Count) lines (max 40)"
$logLines = @(Get-Content (Join-Path $root 'memory/LOG.md') -ErrorAction SilentlyContinue | Where-Object { $_ -match '^- ' })
$lastLog = if ($logLines.Count -gt 0) { $logLines[-1] } else { '' }
Check 'log-format' ($lastLog -match '^- \d{4}-\d{2}-\d{2} \d{2}:\d{2} \| .+ \| verify: (pass|fail|not-run)\s*$') $lastLog
$questions = Get-Content (Join-Path $root 'memory/QUESTIONS.md') -Raw -ErrorAction SilentlyContinue
Check 'questions-table' ($questions -match '(?m)^\| Id \| Date \| Question \| Status \| Answer \|') ''
$badQ = [regex]::Matches([string]$questions, '(?m)^\|\s*Q-\d{3}\s*\|(?:[^|]*\|){2}\s*(?!open|answered)[a-z]+\s*\|')
Check 'questions-status' ($badQ.Count -eq 0) ($(if ($badQ.Count) { 'statuses must be open|answered' } else { '' }))

# 3. No real-patient-looking keys anywhere in data files.
$dataDir = Join-Path $root 'nurse-handoff\data'
if (Test-Path $dataDir) {
    $bad = Get-ChildItem $dataDir -Filter *.json | Where-Object {
        (Get-Content $_.FullName -Raw) -match '"(name|first_name|last_name|dob|date_of_birth|mrn|ssn|facility)"'
    }
    Check 'synthetic-data-keys' ($bad.Count -eq 0) ($(if ($bad) { ($bad.Name -join ', ') } else { 'no forbidden keys' }))
}

# 4. Secret-like files.
$secrets = Get-ChildItem $root -Recurse -Force -File -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '[\\/](\.git|\.venv|\.loop)[\\/]' -and $_.Name -match '^(\.env(\..*)?|.*\.(key|pem|pfx|p12))$' }
Check 'secret-scan' ($secrets.Count -eq 0) ($(if ($secrets) { ($secrets.Name -join ', ') } else { 'none' }))

# 5. Package checks, only once the package exists.
$pkg = Join-Path $root 'nurse-handoff'
$py = Join-Path $pkg '.venv\Scripts\python.exe'
$tasks = Get-Content (Join-Path $root 'TASKS.md') -Raw
$cliReady = $tasks -match '- \[x\] \*\*013'
if (Test-Path (Join-Path $pkg 'nurse_handoff\__init__.py')) {
    if (-not (Test-Path $py)) {
        Check 'venv' $false 'nurse-handoff/.venv missing; run loops/setup.ps1'
    } else {
        Push-Location $pkg
        try {
            $testDir = Join-Path $pkg 'tests'
            $hasTests = (Test-Path $testDir) -and ((Get-ChildItem $testDir -Filter 'test_*.py' -ErrorAction SilentlyContinue).Count -gt 0)
            if ($hasTests) {
                & $py -m pytest -q 2>&1 | Tee-Object -Variable pytestOut | Out-Null
                Check 'pytest' ($LASTEXITCODE -eq 0) (($pytestOut | Select-Object -Last 1) -join '')
            } else {
                Check 'pytest' $true 'no tests yet (skipped)'
            }
            $sample = Join-Path $pkg 'data\chf_patient.json'
            if ((Test-Path $sample) -and $cliReady) {
                $cli = & $py -m nurse_handoff $sample 2>&1
                $cliText = ($cli | Out-String)
                Check 'cli-runs' ($LASTEXITCODE -eq 0) "exit $LASTEXITCODE"
                Check 'cli-header' ($cliText -match 'NURSING HANDOFF') ''
                Check 'cli-no-room-air' ($cliText -notmatch 'Room air') 'must never invent room air'
            } elseif (Test-Path $sample) {
                Check 'cli' $true 'cli checks skipped until ticket 013 is ticked'
            } else {
                Check 'cli' $true 'data/chf_patient.json not present yet (skipped)'
            }
        } finally { Pop-Location }
    }
} else {
    Check 'package' $true 'nurse-handoff package not created yet (skipped)'
}

Write-Host ''
if ($failures -gt 0) { Write-Host "VERIFY: FAIL ($failures)"; exit 1 }
Write-Host 'VERIFY: PASS'
exit 0
