# PyProtect PowerShell Wrapper
param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pyprotectPath = Join-Path $scriptDir "pyprotect.py"

# Try to find Python
$pythonCmd = $null

# Try py launcher first
if (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
}
# Then try python
elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
}
# Then try python3
elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
}
else {
    Write-Error "ERROR: Python not found. Please ensure Python is installed and in PATH."
    exit 1
}

# Run pyprotect.py with arguments
& $pythonCmd $pyprotectPath $Arguments

