# Project-local verification for Nursing OS Project / nurse-handoff.
# Exit 0 = pass, 1 = fail. The controller invokes its trusted copy inside
# the workspace sandbox after every iteration.
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$failures = 0
function Check([string]$name, [bool]$ok, [string]$detail) {
    $label = if ($ok) { 'PASS' } else { 'FAIL' }
    Write-Host ("{0,-5} {1,-34} {2}" -f $label, $name, $detail)
    if (-not $ok) { $script:failures++ }
}
function Invoke-Python([string[]]$Arguments) {
    # Windows PowerShell turns redirected native stderr into ErrorRecords.
    # Expected usage/errors must be judged by exit status instead of terminating
    # this verifier before Check can evaluate the contract.
    $savedPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = 'Continue'
        $lines = @(& $script:py @Arguments 2>&1)
        $code = $LASTEXITCODE
    } finally { $ErrorActionPreference = $savedPreference }
    return [pscustomobject]@{ Code = $code; Lines = $lines; Text = ($lines | Out-String) }
}

# 1. Required loop documents.
foreach ($f in 'AGENTS.md', 'PROMPT.md', 'TASKS.md', 'README.md', 'memory/HANDOFF.md', 'memory/DECISIONS.md', 'memory/LOG.md', 'memory/QUESTIONS.md',
                'docs/NURSE-HANDOFF-SPEC.md', 'docs/PATIENT-SCHEMA.md', 'docs/OUTPUT-FORMAT.md') {
    Check "required:$f" (Test-Path (Join-Path $root $f) -PathType Leaf) ''
}

# 2. Memory discipline: HANDOFF stays short, LOG lines keep their shape, QUESTIONS is a table.
$handoff = @(Get-Content -Encoding UTF8 (Join-Path $root 'memory/HANDOFF.md') -ErrorAction SilentlyContinue)
Check 'handoff-lines' ($handoff.Count -le 40) "$($handoff.Count) lines (max 40)"
$logLines = @(Get-Content -Encoding UTF8 (Join-Path $root 'memory/LOG.md') -ErrorAction SilentlyContinue | Where-Object { $_ -match '^- ' })
$lastLog = if ($logLines.Count -gt 0) { $logLines[-1] } else { '' }
Check 'log-format' ($lastLog -match '^- \d{4}-\d{2}-\d{2} \d{2}:\d{2} \| .+ \| verify: (pass|fail|not-run)\s*$') $lastLog
$questions = Get-Content -Encoding UTF8 (Join-Path $root 'memory/QUESTIONS.md') -Raw -ErrorAction SilentlyContinue
Check 'questions-table' ($questions -match '(?m)^\| Id \| Date \| Question \| Status \| Answer \|') ''
$badQ = [regex]::Matches([string]$questions, '(?m)^\|\s*Q-\d{3,}\s*\|(?:[^|]*\|){2}\s*(?!open|answered)[a-z]+\s*\|')
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

# Claimed progress must be backed by files and a complete milestone.
$tasks = Get-Content -Encoding UTF8 (Join-Path $root 'TASKS.md') -Raw
$ticketMatches = [regex]::Matches($tasks, '(?m)^- \[[xX]\] \*\*(\d{3,})')
$completed = @($ticketMatches | ForEach-Object { [int]$_.Groups[1].Value })
$requiredByTicket = @{
    1 = @('README.md','requirements.txt','nurse_handoff/__init__.py','nurse_handoff/__main__.py','tests/__init__.py','conftest.py')
    2 = @('nurse_handoff/schema.py')
    3 = @('data/simple_patient.json','data/chf_patient.json','data/incomplete_patient.json','data/complex_patient.json')
    4 = @('nurse_handoff/loader.py','tests/test_loader.py')
    5 = @('nurse_handoff/validator.py','tests/test_validator.py')
    6 = @('nurse_handoff/generator.py')
    10 = @('nurse_handoff/rules.py','tests/test_rules.py')
    14 = @('tests/test_no_real_data.py')
    15 = @('README.md')
}
foreach ($ticket in $requiredByTicket.Keys) {
    if ($completed -contains $ticket) {
        foreach ($file in $requiredByTicket[$ticket]) {
            Check "ticket-$ticket/$file" (Test-Path (Join-Path $root "nurse-handoff/$file") -PathType Leaf) 'required by completed ticket'
        }
    }
}
if ($completed.Count -gt 0) {
    Check 'claimed-package' (Test-Path (Join-Path $root 'nurse-handoff/nurse_handoff/__init__.py')) ''
}
if (Test-Path (Join-Path $root 'DONE')) {
    $released = $tasks -match '(?mi)^- \[[xX]\] v0\.1 released'
    $requiredTickets = if ($released) { @(101..110 | Where-Object { $_ -ne 107 }) } else { @(1..15) }
    $missingTickets = @($requiredTickets | Where-Object { $completed -notcontains $_ })
    Check 'done-tickets' ($missingTickets.Count -eq 0) "missing completed tickets: $($missingTickets -join ',')"
    $version = if ($released) { 'v0.2' } else { 'v0.1' }
    $block = [regex]::Match($tasks, '(?ms)^### Definition of Done[^\n]*' + [regex]::Escape($version) + '[^\n]*\n(.*?)(?=^#{2,3} |\z)')
    $doneItems = if ($block.Success) { [regex]::Matches($block.Groups[1].Value, '(?m)^- \[[xX]\]') } else { @() }
    Check 'done-checklist' ($block.Success -and $doneItems.Count -ge 10 -and $block.Groups[1].Value -notmatch '(?m)^- \[ \]') 'complete current-version Definition of Done required'
}

# 5. Package checks, only once the package exists.
$pkg = Join-Path $root 'nurse-handoff'
$py = Join-Path $pkg '.venv\Scripts\python.exe'
$tasks = Get-Content -Encoding UTF8 (Join-Path $root 'TASKS.md') -Raw
$cliReady = $tasks -match '- \[[xX]\] \*\*013'
if (Test-Path (Join-Path $pkg 'nurse_handoff\__init__.py')) {
    if (-not (Test-Path $py)) {
        Check 'venv' $false 'nurse-handoff/.venv missing; run loops/setup.ps1'
    } else {
        Push-Location $pkg
        try {
            if ($completed -contains 1) {
                $usage = Invoke-Python -Arguments @('-m', 'nurse_handoff')
                Check 'cli-usage' ($usage.Code -eq 2 -and $usage.Text -match '(?i)usage') 'no path must print usage and exit 2'
            }
            $testDir = Join-Path $pkg 'tests'
            $hasTests = (Test-Path $testDir) -and ((Get-ChildItem $testDir -Filter 'test_*.py' -ErrorAction SilentlyContinue).Count -gt 0)
            if ($hasTests) {
                $pytestOut = Invoke-Python -Arguments @('-m', 'pytest', '-q')
                Check 'pytest' ($pytestOut.Code -eq 0) (($pytestOut.Lines | Select-Object -Last 1) -join '')
            } else {
                if ($completed -contains 1 -and @($completed | Where-Object { $_ -ge 2 }).Count -eq 0) {
                    $emptyTests = Invoke-Python -Arguments @('-m', 'pytest', '-q')
                    Check 'pytest-skeleton' ($emptyTests.Code -in @(0,5)) 'ticket 001 allows no tests collected'
                } else {
                    Check 'pytest' $false 'tests are required once ticket 002 is complete'
                }
            }
            $sample = Join-Path $pkg 'data\chf_patient.json'
            if ((Test-Path $sample) -and $cliReady) {
                $cli = Invoke-Python -Arguments @('-m', 'nurse_handoff', $sample)
                $cliText = $cli.Text
                Check 'cli-runs' ($cli.Code -eq 0) "exit $($cli.Code)"
                Check 'cli-header' ($cliText -match 'NURSING HANDOFF') ''
                Check 'cli-no-room-air' ($cliText -notmatch 'Room air') 'must never invent room air'
            } elseif (Test-Path $sample) {
                Check 'cli' $true 'cli checks skipped until ticket 013 is ticked'
            } else {
                Check 'cli' (-not $cliReady) 'sample required once ticket 013 is complete'
            }
        } finally { Pop-Location }
    }
} else {
    Check 'package' ($completed.Count -eq 0 -and -not (Test-Path (Join-Path $root 'DONE'))) 'nurse-handoff package not created yet (skipped)'
}

Write-Host ''
if ($failures -gt 0) { Write-Host "VERIFY: FAIL ($failures)"; exit 1 }
Write-Host 'VERIFY: PASS'
exit 0
