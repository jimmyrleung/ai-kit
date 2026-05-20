#!/usr/bin/env pwsh
<#
.SYNOPSIS
  ai-kit -> Cursor CLI adapter (Category-1, additive, Claude-untouched).

.DESCRIPTION
  Windows-native parity of sync.sh. Makes the single canonical ai-kit source
  consumable by the Cursor CLI (`cursor-agent`), mirroring the existing
  ~/.claude / ~/.codex junction model. Deterministic and idempotent.

  NOTE: the Cursor CLI on Windows hard-codes a PowerShell shell with documented
  cold-start hangs (no --shell override), so cursor-agent is commonly run under
  WSL — in that case run sync.sh from inside WSL instead (it targets the WSL
  ~/.cursor). This script is the Windows-native equivalent.

  Verified vs Cursor docs (cursor.com/docs), 2026-05-19. See ./README.md and
  ../../docs/cursor-portability-assessment.md for the design + decision record.

  What it does (NOTHING touches the canonical ai-kit tree; Claude unaffected):

    1. Skills (41) : per-skill directory JUNCTION
                     $CursorHome\skills\<name> -> <repo>\skills\<name>
                     (Cursor's native user-level skills root; self-contained,
                     does NOT depend on the ~/.claude compat root.)
    2. Orchestr.   : Cursor deprecated standalone slash-commands (folded into
                     Skills). The ~25 thin shims need nothing (skill already
                     junctioned). The 5 family ORCHESTRATORS + 3 per-task
                     EXECUTORS are GENERATED as Cursor skills with
                     `disable-model-invocation: true` (explicit-only /name,
                     never auto-triggers). Canonical commands/ untouched.
    3. Agents (17) : GENERATED as native Cursor subagents at
                     $CursorHome\agents\<name>.md (name+description+body;
                     model/tools/color dropped). Cursor has no explicit-only
                     flag for subagents (auto-delegation governed by the
                     description) — documented caveat, not a canonical edit.
    4. AGENTS.md   : prints where to place adapters/cursor/AGENTS.md.

.PARAMETER CursorHome
  Override the Cursor home. Default: $env:CURSOR_HOME, else ~/.cursor.
.PARAMETER Prune
  Report kit-owned entries whose source no longer exists. -Force to remove
  (guarded: never deletes a junction target or a non-kit entry).
.PARAMETER Force
  Permit recreating a stale kit junction and (with -Prune) removing orphans.
.PARAMETER WhatIf
  Dry run: print every action, change nothing.

.EXAMPLE
  pwsh adapters/cursor/sync.ps1 -WhatIf
.EXAMPLE
  pwsh adapters/cursor/sync.ps1
#>
[CmdletBinding()]
param(
  [string]$CursorHome,
  [switch]$Prune,
  [switch]$Force,
  [switch]$WhatIf
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot  = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$SkillsSrc = Join-Path $RepoRoot 'skills'
$AgentsSrc = Join-Path $RepoRoot 'agents'
$CmdSrc    = Join-Path $RepoRoot 'commands'
if (-not $CursorHome -or $CursorHome -eq '') {
  $CursorHome = if ($env:CURSOR_HOME) { $env:CURSOR_HOME } else { Join-Path $HOME '.cursor' }
}
$SkillsRoot = Join-Path $CursorHome 'skills'
$AgentsRoot = Join-Path $CursorHome 'agents'
$GenMarker  = '.ai-kit-generated'           # sentinel dir-file for generated skills

Write-Host ""
Write-Host "ai-kit -> Cursor adapter" -ForegroundColor Cyan
Write-Host ("  repo        : {0}" -f $RepoRoot)
Write-Host ("  cursor home : {0}" -f $CursorHome)
Write-Host ("  skills root : {0}" -f $SkillsRoot)
Write-Host ("  agents root : {0}" -f $AgentsRoot)
Write-Host ("  mode        : {0}" -f $(if ($WhatIf) {'DRY RUN (-WhatIf)'} else {'apply'}))
Write-Host ""

if (-not (Test-Path $SkillsSrc)) { throw "canonical skills dir not found: $SkillsSrc" }
foreach ($r in @($SkillsRoot, $AgentsRoot)) {
  if (-not (Test-Path $r)) {
    if ($WhatIf) { Write-Host "would create: $r" } else { New-Item -ItemType Directory -Path $r -Force | Out-Null }
  }
}

$results = [System.Collections.Generic.List[object]]::new()
function Add-Result($name, $kind, $status, $note) {
  $results.Add([pscustomobject]@{ Name=$name; Kind=$kind; Status=$status; Note=$note })
}
function Test-Reparse($path) {
  if (-not (Test-Path $path)) { return $false }
  return ((Get-Item $path -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0
}
function Get-ReparseTarget($path) { try { return (Get-Item $path -Force).Target } catch { return $null } }
function Read-Frontmatter($mdPath) {
  $raw = Get-Content -Raw -LiteralPath $mdPath
  $m = [regex]::Match($raw, '(?s)^---\r?\n(.*?)\r?\n---\r?\n?(.*)$')
  if (-not $m.Success) { return $null }
  $fm = @{}
  foreach ($line in ($m.Groups[1].Value -split "\r?\n")) {
    $kv = [regex]::Match($line, '^([A-Za-z0-9_-]+):\s*(.*)$')
    if ($kv.Success) { $fm[$kv.Groups[1].Value] = $kv.Groups[2].Value.Trim().Trim('"') }
  }
  return [pscustomobject]@{ Fm=$fm; Body=$m.Groups[2].Value.Trim() }
}
# YAML double-quoted scalar escaping.
function Esc-Yaml($s) { return ($s -replace '\\','\\' -replace '"','\"') }

# --- 1. Skills: per-skill directory junctions -----------------------------
foreach ($s in (Get-ChildItem $SkillsSrc -Directory | Sort-Object Name)) {
  $name = $s.Name; $link = Join-Path $SkillsRoot $name; $tgt = $s.FullName
  if (Test-Path $link) {
    if (Test-Reparse $link) {
      $cur = Get-ReparseTarget $link
      if ($cur -and ((Resolve-Path $cur -ErrorAction SilentlyContinue).Path -eq $tgt)) {
        Add-Result $name 'skill' 'ok' 'junction current'; continue
      }
      if (-not $Force) { Add-Result $name 'skill' 'conflict' "junction -> '$cur' (stale); -Force"; continue }
      if ($WhatIf) { Add-Result $name 'skill' 'would-relink' "stale -> $tgt"; continue }
      [System.IO.Directory]::Delete($link, $false)   # reparse point only, never target
    } else {
      Add-Result $name 'skill' 'skip' 'real dir exists (not kit-owned) — left untouched'; continue
    }
  }
  if ($WhatIf) { Add-Result $name 'skill' 'would-link' "$link -> $tgt"; continue }
  New-Item -ItemType Junction -Path $link -Target $tgt | Out-Null
  Add-Result $name 'skill' 'linked' 'junction created'
}

# --- 2. Orchestrators/executors -> generated explicit-only Cursor skills ---
$OrchCmds = @(
  'full-bug-fix-workflow','integration-feature-dev','refactor-techdebt-dev',
  'full-incident-response','greenfield-dev',
  'implement-task','gf-implement-task','implement-bug-fix'
)
foreach ($cn in $OrchCmds) {
  $cf = Join-Path $CmdSrc "$cn.md"
  if (-not (Test-Path $cf)) { Add-Result $cn 'orch' 'error' "commands/$cn.md not found"; continue }
  $parsed = Read-Frontmatter $cf
  if (-not $parsed -or -not $parsed.Fm.ContainsKey('description')) {
    Add-Result $cn 'orch' 'error' 'missing description frontmatter'; continue
  }
  $dest = Join-Path $SkillsRoot $cn
  if ((Test-Path $dest) -and -not (Test-Path (Join-Path $dest $GenMarker)) -and -not (Test-Reparse $dest)) {
    Add-Result $cn 'orch' 'skip' 'name exists and is not kit-generated — left untouched'; continue
  }
  if ($WhatIf) { Add-Result $cn 'orch' 'would-gen' "Cursor skill <- commands/$cn.md"; continue }
  New-Item -ItemType Directory -Path $dest -Force | Out-Null
  $fm = "---`nname: $cn`ndescription: `"$(Esc-Yaml $parsed.Fm['description'])`"`ndisable-model-invocation: true`n---`n`n"
  Set-Content -LiteralPath (Join-Path $dest 'SKILL.md') -Value ($fm + $parsed.Body + "`n") -NoNewline -Encoding utf8
  Set-Content -LiteralPath (Join-Path $dest $GenMarker) -Value "source: commands/$cn.md`n" -NoNewline -Encoding utf8
  Add-Result $cn 'orch' 'generated' "explicit-only /$cn"
}

# --- 3. Agents -> generated native Cursor subagents -----------------------
if (Test-Path $AgentsSrc) {
  foreach ($a in (Get-ChildItem $AgentsSrc -Filter '*.md' | Sort-Object Name)) {
    $parsed = Read-Frontmatter $a.FullName
    if (-not $parsed -or -not $parsed.Fm.ContainsKey('name') -or -not $parsed.Fm.ContainsKey('description')) {
      Add-Result $a.BaseName 'agent' 'error' 'missing name/description frontmatter'; continue
    }
    $name = $parsed.Fm['name']; $dest = Join-Path $AgentsRoot "$name.md"
    if ((Test-Path $dest) -and -not (Select-String -LiteralPath $dest -Pattern 'ai-kit-generated:' -Quiet)) {
      Add-Result $name 'agent' 'skip' 'name exists and is not kit-generated — left untouched'; continue
    }
    if ($WhatIf) { Add-Result $name 'agent' 'would-gen' "Cursor subagent <- agents/$($a.Name)"; continue }
    # name+description only (model/tools/color dropped -> Cursor model:inherit).
    $out = "---`nname: $name`ndescription: `"$(Esc-Yaml $parsed.Fm['description'])`"`n---`n" +
           "<!-- ai-kit-generated: source: agents/$($a.Name) — do not hand-edit -->`n`n" +
           $parsed.Body + "`n"
    Set-Content -LiteralPath $dest -Value $out -NoNewline -Encoding utf8
    Add-Result $name 'agent' 'generated' 'native Cursor subagent'
  }
}

# --- 4. AGENTS.md hint ----------------------------------------------------
$agentsMdSrc = Join-Path $PSScriptRoot 'AGENTS.md'
Write-Host ""
Write-Host "AGENTS.md (Cursor instruction layer)" -ForegroundColor Cyan
if (Test-Path $agentsMdSrc) {
  Write-Host "  Cursor reads project-root AGENTS.md + CLAUDE.md as rules; global"
  Write-Host "  read-location is [verify on installed binary]. Place per project:"
  Write-Host ("    cmd /c mklink `"<your-project>\AGENTS.md`" `"{0}`"   # or copy" -f $agentsMdSrc) -ForegroundColor Yellow
  Write-Host "  NOTE: kit Cursor-MECHANICS layer only. Your personal ~/.claude/CLAUDE.md" -ForegroundColor Yellow
  Write-Host "  conventions (confidence scoring, ask-before-assuming, scope discipline," -ForegroundColor Yellow
  Write-Host "  read-before-edit, verification-before-completion, risky-command confirm)" -ForegroundColor Yellow
  Write-Host "  do NOT transfer. Mirror them into a PRIVATE AGENTS.md yourself (keep it" -ForegroundColor Yellow
  Write-Host "  out of this public repo) — see adapters/cursor/README.md." -ForegroundColor Yellow
} else {
  Write-Host "  (adapters/cursor/AGENTS.md missing — run from a complete checkout)" -ForegroundColor Red
}

# --- Prune (report-only unless -Force) ------------------------------------
if ($Prune) {
  Write-Host ""
  Write-Host "Prune (kit-owned orphans)" -ForegroundColor Cyan
  $AgentNames = @{}
  if (Test-Path $AgentsSrc) {
    foreach ($af in (Get-ChildItem $AgentsSrc -Filter '*.md')) {
      $ap = Read-Frontmatter $af.FullName
      if ($ap -and $ap.Fm.ContainsKey('name')) { $AgentNames[$ap.Fm['name']] = $true }
    }
  }
  foreach ($d in (Get-ChildItem $SkillsRoot -Directory -Force -ErrorAction SilentlyContinue)) {
    $kitSkill = (Test-Reparse $d.FullName) -and ((Get-ReparseTarget $d.FullName) -like (Join-Path $SkillsSrc '*'))
    $kitGen   = Test-Path (Join-Path $d.FullName $GenMarker)
    if (-not ($kitSkill -or $kitGen)) { continue }
    if ((Test-Path (Join-Path $SkillsSrc $d.Name)) -or (Test-Path (Join-Path $CmdSrc "$($d.Name).md"))) { continue }
    if ($Force -and -not $WhatIf) {
      if ($kitSkill) { [System.IO.Directory]::Delete($d.FullName, $false) } else { Remove-Item -LiteralPath $d.FullName -Recurse -Force }
      Write-Host ("  removed orphan skill: {0}" -f $d.Name) -ForegroundColor Yellow
    } else { Write-Host ("  orphan skill (use -Prune -Force): {0}" -f $d.Name) }
  }
  foreach ($f in (Get-ChildItem $AgentsRoot -Filter '*.md' -Force -ErrorAction SilentlyContinue)) {
    if (-not (Select-String -LiteralPath $f.FullName -Pattern 'ai-kit-generated:' -Quiet)) { continue }
    if ($AgentNames.ContainsKey($f.BaseName)) { continue }
    if ($Force -and -not $WhatIf) { Remove-Item -LiteralPath $f.FullName -Force; Write-Host ("  removed orphan agent: {0}" -f $f.BaseName) -ForegroundColor Yellow }
    else { Write-Host ("  orphan agent (use -Prune -Force): {0}" -f $f.BaseName) }
  }
}

# --- Summary --------------------------------------------------------------
Write-Host ""
Write-Host "Summary" -ForegroundColor Cyan
$results | Sort-Object Kind, Name | Format-Table -AutoSize Kind, Name, Status, Note
$bad = @($results | Where-Object { $_.Status -in @('error','conflict') })
Write-Host ("skills+orchestrators+agents exposed: {0}   issues: {1}" -f $results.Count, $bad.Count)
if ($bad.Count -gt 0) {
  Write-Host "Issues are reported, not auto-fixed (a canonical edit is Category-2)." -ForegroundColor Yellow
  exit 1
}
Write-Host "Restart cursor-agent to pick up new skills/subagents." -ForegroundColor Green
exit 0
