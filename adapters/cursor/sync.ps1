#!/usr/bin/env pwsh
<#
.SYNOPSIS
  Compatibility entry point for the common ai-kit sync engine.

.DESCRIPTION
  Translates the legacy PowerShell surface into the shared Python CLI. The
  common engine owns canonical enumeration, link classification, mutation,
  ownership, recovery, and rollback.
#>
[CmdletBinding()]
param(
  [switch]$WhatIf,
  [switch]$Check,
  [switch]$Uninstall,
  [switch]$Force,
  [switch]$Prune,
  [string[]]$Preserve,
  [string]$UserHome,
  [string]$CursorHome
)

$ErrorActionPreference = 'Stop'

if ($PSBoundParameters.ContainsKey('CursorHome') -or $null -ne $env:CURSOR_HOME) {
  [Console]::Error.WriteLine('CursorHome/CURSOR_HOME is no longer accepted; use -UserHome or --home for an isolated user base.')
  exit 2
}

$python = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python -ErrorAction SilentlyContinue }
if (-not $python) {
  Write-Error 'Python 3 is required to run scripts/sync-skills.py.'
  exit 1
}

$scriptPath = (Resolve-Path (Join-Path $PSScriptRoot '..\..\scripts\sync-skills.py')).Path
$commonArgs = [System.Collections.Generic.List[string]]::new()
if ($WhatIf) { $commonArgs.Add('--dry-run') }
if ($Check) { $commonArgs.Add('--check') }
if ($Uninstall) { $commonArgs.Add('--uninstall') }
if ($Force) { $commonArgs.Add('--force') }
if ($Prune) { $commonArgs.Add('--prune') }
foreach ($entry in $Preserve) {
  $commonArgs.Add('--preserve')
  $commonArgs.Add($entry)
}
if ($PSBoundParameters.ContainsKey('UserHome')) {
  if ([string]::IsNullOrWhiteSpace($UserHome)) {
    [Console]::Error.WriteLine('-UserHome requires a non-empty path.')
    exit 2
  }
  $commonArgs.Add('--home')
  $commonArgs.Add($UserHome)
}

& $python.Source $scriptPath @commonArgs
exit $LASTEXITCODE
