# PowerShell wrapper to make `tos cd <ENV>` change the current PS location.
#
# How to use:
# 1) Adjust $TosCliPath if needed to point to main.py
# 2) Dot-source this file in your profile or session:
#      . "$PSScriptRoot\tos.ps1"
# 3) Then use:
#      tos cd AK_HOME

param()

# Try to resolve main.py relative to this script; fallback to 'main.py' in PATH/cwd
$TosCliPath = Join-Path $PSScriptRoot '..\..\main.py'
try {
  $TosCliPath = (Resolve-Path -Path $TosCliPath -ErrorAction Stop).Path
} catch {
  $TosCliPath = 'main.py'
}

function tos {
  param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $Args
  )

  if ($Args.Length -ge 1 -and $Args[0] -eq 'cd') {
    if ($Args.Length -lt 2) {
      Write-Error 'Usage: tos cd <ENV_NAME>'
      return
    }
    $envName = $Args[1]
    $path = & python $TosCliPath path $envName 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $path) {
      Write-Error "Environment '$envName' not found or path resolution failed."
      return
    }
    Set-Location -Path $path
    return
  }

& python $TosCliPath @Args
}


# --- Improved resolver and wrapper below ---
function Resolve-TosPath([string] $EnvName) {
  $ext = Get-Command tos -CommandType Application -ErrorAction SilentlyContinue
  if ($ext) {
    try {
      $p = & $ext.Source path $EnvName 2>$null
      if ($LASTEXITCODE -eq 0 -and $p) { return $p }
    } catch {}
  }

  try {
    $p = & python -m main path $EnvName 2>$null
    if ($LASTEXITCODE -eq 0 -and $p) { return $p }
  } catch {}

  try {
    $LocalMain = Join-Path $PSScriptRoot '..\..\main.py'
    $LocalMain = (Resolve-Path -Path $LocalMain -ErrorAction Stop).Path
    $p = & python $LocalMain path $EnvName 2>$null
    if ($LASTEXITCODE -eq 0 -and $p) { return $p }
  } catch {}

  return $null
}

Remove-Item Function:tos -ErrorAction SilentlyContinue | Out-Null
Remove-Item Function:t -ErrorAction SilentlyContinue | Out-Null
function tos {
  param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $Args
  )

  if ($Args.Length -ge 1 -and $Args[0] -eq 'cd') {
    if ($Args.Length -lt 2) {
      Write-Error 'Usage: tos cd <ENV_NAME>'
      return
    }
    $envName = $Args[1]
    $path = Resolve-TosPath -EnvName $envName
    if (-not $path) {
      Write-Error "Environment '$envName' not found or path resolution failed."
      return
    }
    Set-Location -Path $path
    return
  }

  $ext = Get-Command tos -CommandType Application -ErrorAction SilentlyContinue
  if ($ext) {
    & $ext.Source @Args
  } else {
    & python -m main @Args
  }
}

function t {
  param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $Args
  )

  if ($Args.Length -ge 1 -and $Args[0] -eq 'cd') {
    if ($Args.Length -lt 2) {
      Write-Error 'Usage: t cd <ENV_NAME>'
      return
    }
    $envName = $Args[1]
    $path = Resolve-TosPath -EnvName $envName
    if (-not $path) {
      Write-Error "Environment '$envName' not found or path resolution failed."
      return
    }
    Set-Location -Path $path
    return
  }

  $ext = Get-Command t -CommandType Application -ErrorAction SilentlyContinue
  if ($ext) {
    & $ext.Source @Args
  } else {
    & python -m main @Args
  }
}
