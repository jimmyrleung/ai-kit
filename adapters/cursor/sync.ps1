#!/usr/bin/env pwsh
<#
.SYNOPSIS
  ai-kit -> Cursor CLI adapter (v2 — Category-1, additive, Claude-untouched).

.DESCRIPTION
  Windows-native parity of sync.sh. Makes the single canonical ai-kit source
  consumable by the Cursor CLI (`cursor-agent`), mirroring the existing
  ~/.claude / ~/.codex junction model. Deterministic and idempotent.

  NOTE: the Cursor CLI on Windows hard-codes a PowerShell shell with documented
  cold-start hangs (no --shell override), so cursor-agent is commonly run under
  WSL — in that case run sync.sh from inside WSL instead (it targets the WSL
  ~/.cursor). This script is the Windows-native equivalent.

  Rewritten 2026-08-06 for the v2 kit (skill-centric refactor). Base mechanics
  verified vs Cursor docs (cursor.com/docs) 2026-05-19 + live probe; Cursor
  ships near-daily — re-check [verify] items in README.md after an update.

  What it does (NOTHING touches the canonical ai-kit tree; Claude unaffected):

    1. Skills    : per-skill directory JUNCTION
                   $CursorHome\skills\<name> -> <repo>\skills\<name>,
                   for EVERY canonical skill. Cursor's native user-level
                   skills root; SKILL.md spec identical — no body transform.
                   This is the ONLY live mechanism in v2.
    2. Orchestr. : NONE in v2 — every command was archived (skills are
                   invoked directly as /name). $OrchCmds is empty; the
                   generation path is retained dormant.
    3. Agents    : NONE in v2 — the kit-refactor (2026-08) archived all named
                   agents (generic subagents ride inside skill prose). The
                   generation path is retained dormant; agents/ absent means
                   it no-ops. This also moots the #160426 CLI parity gap for
                   the kit (nothing is installed at ~/.cursor/agents anymore).
    4. AGENTS.md : prints guidance for activating adapters/cursor/AGENTS.md
                   (the kit's Cursor-MECHANICS layer). NOT done silently: a
                   deployed AGENTS.md is the user's PRIVATE conventions layer —
                   the kit block is pasted at its include point (kit-mechanics
                   markers), never plain-copied over.

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
$AgentsSrc = Join-Path $RepoRoot 'agents'    # absent in v2 — path retained dormant
$CmdSrc    = Join-Path $RepoRoot 'commands'  # absent in v2 — path retained dormant
if (-not $CursorHome -or $CursorHome -eq '') {
  $CursorHome = if ($env:CURSOR_HOME) { $env:CURSOR_HOME } else { Join-Path $HOME '.cursor' }
}
$SkillsRoot = Join-Path $CursorHome 'skills'
$AgentsRoot = Join-Path $CursorHome 'agents'
$GenMarker  = '.ai-kit-generated'           # sentinel dir-file for generated skills

Write-Host ""
Write-Host "ai-kit -> Cursor adapter (v2)" -ForegroundColor Cyan
Write-Host ("  repo        : {0}" -f $RepoRoot)
Write-Host ("  cursor home : {0}" -f $CursorHome)
Write-Host ("  skills root : {0}" -f $SkillsRoot)
Write-Host ("  mode        : {0}" -f $(if ($WhatIf) {'DRY RUN (-WhatIf)'} else {'apply'}))
Write-Host ""

if (-not (Test-Path $SkillsSrc)) { throw "canonical skills dir not found: $SkillsSrc" }
if (-not (Test-Path $SkillsRoot)) {
  if ($WhatIf) { Write-Host "would create: $SkillsRoot" } else { New-Item -ItemType Directory -Path $SkillsRoot -Force | Out-Null }
}

$results = [System.Collections.Generic.List[object]]::new()
function Add-Result($name, $kind, $status, $note) {
  $results.Add([pscustomobject]@{ Name=$name; Kind=$kind; Status=$status; Note=$note })
}
# Get-Item -Force succeeds on a reparse point even when its TARGET is gone —
# unlike Test-Path, which resolves through it and false-negatives on dangling
# junctions. Use these for existence/reparse checks on link paths.
function Test-Entry($path) {
  try { $null = Get-Item -LiteralPath $path -Force -ErrorAction Stop; return $true } catch { return $false }
}
function Test-Reparse($path) {
  try { $item = Get-Item -LiteralPath $path -Force -ErrorAction Stop } catch { return $false }
  return ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0
}
function Get-ReparseTarget($path) { try { return (Get-Item -LiteralPath $path -Force).Target } catch { return $null } }
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

# --- 1. Skills: per-skill directory junctions (the only live v2 mechanism) -
foreach ($s in (Get-ChildItem $SkillsSrc -Directory | Sort-Object Name)) {
  $name = $s.Name; $link = Join-Path $SkillsRoot $name; $tgt = $s.FullName
  if (Test-Entry $link) {
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

# --- 2. Orchestrators/executors: NONE in v2 (dormant) ----------------------
# v1 generated 8 command-bodied skills here. All commands are archived; the
# allowlist is empty by design. Repopulate only if a command with a body no
# junctioned skill owns ever returns.
$OrchCmds = @()
foreach ($cn in $OrchCmds) {
  $cf = Join-Path $CmdSrc "$cn.md"
  if (-not (Test-Path $cf)) { Add-Result $cn 'orch' 'error' "commands/$cn.md not found"; continue }
  $parsed = Read-Frontmatter $cf
  if (-not $parsed -or -not $parsed.Fm.ContainsKey('description')) {
    Add-Result $cn 'orch' 'error' 'missing description frontmatter'; continue
  }
  $dest = Join-Path $SkillsRoot $cn
  if ((Test-Entry $dest) -and -not (Test-Path (Join-Path $dest $GenMarker)) -and -not (Test-Reparse $dest)) {
    Add-Result $cn 'orch' 'skip' 'name exists and is not kit-generated — left untouched'; continue
  }
  if ($WhatIf) { Add-Result $cn 'orch' 'would-gen' "Cursor skill <- commands/$cn.md"; continue }
  New-Item -ItemType Directory -Path $dest -Force | Out-Null
  $fm = "---`nname: $cn`ndescription: `"$(Esc-Yaml $parsed.Fm['description'])`"`ndisable-model-invocation: true`n---`n`n"
  Set-Content -LiteralPath (Join-Path $dest 'SKILL.md') -Value ($fm + $parsed.Body + "`n") -NoNewline -Encoding utf8
  Set-Content -LiteralPath (Join-Path $dest $GenMarker) -Value "source: commands/$cn.md`n" -NoNewline -Encoding utf8
  Add-Result $cn 'orch' 'generated' "explicit-only /$cn"
}

# --- 3. Agents: NONE in v2 (dormant — agents/ absent means no-op) ----------
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
    if (-not (Test-Path $AgentsRoot)) { New-Item -ItemType Directory -Path $AgentsRoot -Force | Out-Null }
    # name+description only (model/tools/color dropped -> Cursor model:inherit).
    $out = "---`nname: $name`ndescription: `"$(Esc-Yaml $parsed.Fm['description'])`"`n---`n" +
           "<!-- ai-kit-generated: source: agents/$($a.Name) — do not hand-edit -->`n`n" +
           $parsed.Body + "`n"
    Set-Content -LiteralPath $dest -Value $out -NoNewline -Encoding utf8
    Add-Result $name 'agent' 'generated' 'native Cursor subagent'
  }
}

# --- 4. AGENTS.md hint (never silent) --------------------------------------
$agentsMdSrc = Join-Path $PSScriptRoot 'AGENTS.md'
Write-Host ""
Write-Host "AGENTS.md (Cursor instruction layer)" -ForegroundColor Cyan
if (Test-Path $agentsMdSrc) {
  Write-Host "  Cursor reads project-root AGENTS.md + CLAUDE.md as rules; a global"
  Write-Host "  read-location is [verify on installed binary]. DO NOT plain-copy the"
  Write-Host "  kit file over a deployed AGENTS.md: that file is the user's PRIVATE"
  Write-Host "  conventions layer. After editing the kit file, refresh ONLY the block"
  Write-Host "  between its kit-mechanics markers at the include point:"
  Write-Host ("    source : {0}" -f $agentsMdSrc) -ForegroundColor Yellow
  Write-Host "    target : your private AGENTS.md  (between <!-- kit-mechanics:begin/end -->)" -ForegroundColor Yellow
  Write-Host "  Project-scope also works: copy/link the kit file into the project root."
  Write-Host "  NOTE: your personal ~/.claude/CLAUDE.md conventions do NOT transfer —" -ForegroundColor Yellow
  Write-Host "  mirror them into a PRIVATE AGENTS.md yourself (keep it out of this" -ForegroundColor Yellow
  Write-Host "  public repo) — see adapters/cursor/README.md." -ForegroundColor Yellow
} else {
  Write-Host "  (adapters/cursor/AGENTS.md missing — run from a complete checkout)" -ForegroundColor Red
}

# --- Prune (report-only unless -Force) --------------------------------------
# Enumerated with -Force so junctions whose targets are gone (e.g. skills that
# moved to archive/v1) are seen and pruned too.
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

# --- Summary ----------------------------------------------------------------
Write-Host ""
Write-Host "Summary" -ForegroundColor Cyan
$results | Sort-Object Kind, Name | Format-Table -AutoSize Kind, Name, Status, Note
$bad = @($results | Where-Object { $_.Status -in @('error','conflict') })
Write-Host ("skills exposed: {0}   issues: {1}" -f $results.Count, $bad.Count)
if ($bad.Count -gt 0) {
  Write-Host "Issues are reported, not auto-fixed (a canonical edit is Category-2)." -ForegroundColor Yellow
  exit 1
}
Write-Host "Restart cursor-agent to pick up new skills." -ForegroundColor Green
exit 0
