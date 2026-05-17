#!/usr/bin/env pwsh
<#
.SYNOPSIS
  ai-kit -> OpenAI Codex CLI adapter (Category-1, additive, Claude-untouched).

.DESCRIPTION
  Makes the single canonical ai-kit source consumable by Codex CLI, mirroring the
  existing ~/.claude junction model. Deterministic and idempotent.

  Verified against codex-cli 0.130.0 (2026-05-17). See ./README.md and
  ../../docs/codex-portability-assessment.md for the design + the recorded decision.

  What it does (NOTHING touches the canonical ai-kit tree; Claude is provably unaffected):

    1. Skills    : per-skill directory junction
                   $CODEX_HOME/skills/<name>  ->  <repo>/skills/<name>
                   (Codex enumerates <root>/<name>/SKILL.md; a single top-level
                    junction would nest one level too deep and not be discovered.)
                   openai.yaml is RECOMMENDED-not-required (verified) and is
                   deliberately NOT injected into the pristine canonical tree in v1.

    2. Agents    : the kit's 18 agents/*.md have no Codex analog (no ~/.codex/agents;
                   a skill IS the unit of agent invocation). Each is GENERATED as a
                   Codex skill at $CODEX_HOME/skills/<name>/ (Codex-only, never in
                   <repo>/) so every "@x-agent" the kit references is invokable as
                   "$x-agent". Generated with policy.allow_implicit_invocation:false
                   (workers, never user-triggered -> no per-session context bloat).

    3. AGENTS.md : prints the command to link adapters/codex/AGENTS.md to the Codex
                   global-instruction location. NOT done silently (home mutation +
                   global read-location is [verify on installed binary]).

    4. Validate  : runs Codex's own quick_validate.py over every exposed skill and
                   reports PASS/FAIL. Never auto-fixes (a canonical SKILL.md edit
                   would be Category-2 / out of recorded near-term scope).

.PARAMETER CodexHome
  Override the Codex home. Default: $env:CODEX_HOME, else ~/.codex.

.PARAMETER Prune
  Report kit-owned entries in the skills root whose source no longer exists.
  Reports only; add -Force to actually remove (guarded: never deletes .system,
  non-kit dirs, or junction targets).

.PARAMETER Force
  Permit recreating a stale/conflicting kit junction and (with -Prune) removing
  orphaned kit-owned entries. Without it, conflicts are reported, not changed.

.PARAMETER WhatIf
  Dry run: print every action, change nothing.

.EXAMPLE
  pwsh adapters/codex/sync.ps1 -WhatIf
.EXAMPLE
  pwsh adapters/codex/sync.ps1
#>
[CmdletBinding()]
param(
  [string]$CodexHome,
  [switch]$Prune,
  [switch]$Force,
  [switch]$WhatIf
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# --- Resolve roots --------------------------------------------------------
$RepoRoot   = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$SkillsSrc  = Join-Path $RepoRoot 'skills'
$AgentsSrc  = Join-Path $RepoRoot 'agents'
if (-not $CodexHome -or $CodexHome -eq '') {
  $CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
}
$SkillsRoot = Join-Path $CodexHome 'skills'
$GenMarker  = '.ai-kit-generated'   # sentinel: identifies a kit-GENERATED agent-skill
$Validator  = Join-Path $CodexHome 'skills\.system\skill-creator\scripts\quick_validate.py'

Write-Host ""
Write-Host "ai-kit -> Codex adapter" -ForegroundColor Cyan
Write-Host ("  repo        : {0}" -f $RepoRoot)
Write-Host ("  codex home  : {0}" -f $CodexHome)
Write-Host ("  skills root : {0}" -f $SkillsRoot)
Write-Host ("  mode        : {0}" -f $(if ($WhatIf) {'DRY RUN (-WhatIf)'} else {'apply'}))
Write-Host ""

if (-not (Test-Path $SkillsSrc)) { throw "canonical skills dir not found: $SkillsSrc" }
if (-not (Test-Path $SkillsRoot)) {
  if ($WhatIf) { Write-Host "would create skills root: $SkillsRoot" }
  else { New-Item -ItemType Directory -Path $SkillsRoot -Force | Out-Null }
}

$results = [System.Collections.Generic.List[object]]::new()
function Add-Result($name, $kind, $status, $note) {
  $results.Add([pscustomobject]@{ Name=$name; Kind=$kind; Status=$status; Note=$note })
}

# Is $path a reparse point (junction/symlink)?
function Test-Reparse($path) {
  if (-not (Test-Path $path)) { return $false }
  return ((Get-Item $path -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0
}
function Get-ReparseTarget($path) {
  try { return (Get-Item $path -Force).Target } catch { return $null }
}

# --- 1. Skills: per-skill directory junctions -----------------------------
$skillDirs = Get-ChildItem $SkillsSrc -Directory | Sort-Object Name
foreach ($s in $skillDirs) {
  $name = $s.Name
  $link = Join-Path $SkillsRoot $name
  $tgt  = $s.FullName

  if (Test-Path $link) {
    if (Test-Reparse $link) {
      $cur = Get-ReparseTarget $link
      if ($cur -and ((Resolve-Path $cur -ErrorAction SilentlyContinue).Path -eq $tgt)) {
        Add-Result $name 'skill' 'ok' 'junction current'
        continue
      }
      if (-not $Force) {
        Add-Result $name 'skill' 'conflict' "junction -> '$cur' (stale); rerun with -Force"
        continue
      }
      if ($WhatIf) { Add-Result $name 'skill' 'would-relink' "stale -> $tgt"; continue }
      [System.IO.Directory]::Delete($link, $false)   # removes reparse point only, never target
    }
    else {
      Add-Result $name 'skill' 'skip' 'real dir exists (not kit-owned) — left untouched'
      continue
    }
  }
  if ($WhatIf) { Add-Result $name 'skill' 'would-link' "$link -> $tgt"; continue }
  New-Item -ItemType Junction -Path $link -Target $tgt | Out-Null
  Add-Result $name 'skill' 'linked' 'junction created'
}

# --- 2. Agents -> generated Codex skills ----------------------------------
function Read-Frontmatter($mdPath) {
  $raw = Get-Content -Raw -LiteralPath $mdPath
  $m = [regex]::Match($raw, '(?s)^---\r?\n(.*?)\r?\n---\r?\n?(.*)$')
  if (-not $m.Success) { return $null }
  $fmText = $m.Groups[1].Value
  $body   = $m.Groups[2].Value
  $fm = @{}
  foreach ($line in ($fmText -split "\r?\n")) {
    $kv = [regex]::Match($line, '^([A-Za-z0-9_-]+):\s*(.*)$')
    if ($kv.Success) { $fm[$kv.Groups[1].Value] = $kv.Groups[2].Value.Trim().Trim('"') }
  }
  return [pscustomobject]@{ Fm=$fm; Body=$body.Trim() }
}
function To-Title($n) { ((($n -replace '-', ' ') -split ' ') | ForEach-Object {
  if ($_){ $_.Substring(0,1).ToUpper() + $_.Substring(1) } }) -join ' ' }

if (Test-Path $AgentsSrc) {
  foreach ($a in (Get-ChildItem $AgentsSrc -Filter '*.md' | Sort-Object Name)) {
    $parsed = Read-Frontmatter $a.FullName
    if (-not $parsed -or -not $parsed.Fm.ContainsKey('name') -or -not $parsed.Fm.ContainsKey('description')) {
      Add-Result $a.BaseName 'agent' 'error' 'missing name/description frontmatter'
      continue
    }
    $name = $parsed.Fm['name']
    $desc = $parsed.Fm['description']
    $dest = Join-Path $SkillsRoot $name

    if ((Test-Path $dest) -and -not (Test-Path (Join-Path $dest $GenMarker))) {
      Add-Result $name 'agent' 'skip' 'name exists and is not kit-generated — left untouched'
      continue
    }
    if ($WhatIf) { Add-Result $name 'agent' 'would-gen' "Codex skill <- agents/$($a.Name)"; continue }

    New-Item -ItemType Directory -Path (Join-Path $dest 'agents') -Force | Out-Null
    # SKILL.md: name+description only (drop model/tools/color); body verbatim.
    $skillMd = "---`nname: $name`ndescription: $desc`n---`n`n" + $parsed.Body + "`n"
    Set-Content -LiteralPath (Join-Path $dest 'SKILL.md') -Value $skillMd -NoNewline -Encoding utf8
    # openai.yaml: the functionally-required bit is policy.allow_implicit_invocation:false
    $oy = @(
      "# Generated by ai-kit/adapters/codex/sync.ps1 from agents/$($a.Name) — do not hand-edit."
      "interface:"
      "  display_name: `"$(To-Title $name)`""
      "  default_prompt: `"Use `$$name as a worker sub-agent; it follows its bound skill.`""
      "policy:"
      "  allow_implicit_invocation: false"
    ) -join "`n"
    Set-Content -LiteralPath (Join-Path $dest 'agents\openai.yaml') -Value ($oy + "`n") -NoNewline -Encoding utf8
    Set-Content -LiteralPath (Join-Path $dest $GenMarker) -Value "source: agents/$($a.Name)`n" -NoNewline -Encoding utf8
    Add-Result $name 'agent' 'generated' 'Codex skill (implicit-invocation off)'
  }
}

# --- 3. AGENTS.md: print link command (never silent) ----------------------
$agentsMdSrc = Join-Path $PSScriptRoot 'AGENTS.md'
Write-Host ""
Write-Host "AGENTS.md (Codex global instruction layer)" -ForegroundColor Cyan
if (Test-Path $agentsMdSrc) {
  Write-Host "  Codex's global AGENTS.md read-location is [verify on installed binary]."
  Write-Host "  Project-scope is standard: copy/junction into the repo you run Codex from:"
  Write-Host ("    cmd /c mklink /J `"<your-project>\AGENTS.md`" `"{0}`"   # or copy" -f $agentsMdSrc) -ForegroundColor Yellow
  Write-Host "  Global analog (parallels ~/.claude/CLAUDE.md), if your build supports it:"
  Write-Host ("    {0}  ->  {1}\AGENTS.md" -f $agentsMdSrc, $CodexHome) -ForegroundColor Yellow
} else {
  Write-Host "  (adapters/codex/AGENTS.md missing — run from a complete checkout)" -ForegroundColor Red
}

# --- 4. Validation (Codex's own validator; advisory, NEVER gates) ---------
# Self-test first: the validator must cleanly pass a known-good .system skill.
# A missing/broken host python or missing PyYAML must degrade to "skipped"
# (exit 0) — it must NOT mark skills FAIL. Junction+generation is the
# deliverable; validation is an optional report best run from Codex's own env.
Write-Host ""
$valOk = $false
if (Test-Path $Validator) {
  $py = (Get-Command python -ErrorAction SilentlyContinue)
  if (-not $py) { $py = (Get-Command python3 -ErrorAction SilentlyContinue) }
  $selfSkill = Join-Path $SkillsRoot '.system\skill-creator'
  if ($py -and (Test-Path $selfSkill)) {
    try {
      $st = & $py.Source $Validator $selfSkill 2>&1
      if ($LASTEXITCODE -eq 0 -and ("$st" -match 'valid')) { $valOk = $true }
      else { Write-Host ("  validation skipped — validator self-test failed (host python issue): {0}" -f ("$st".Trim())) -ForegroundColor Yellow }
    } catch { Write-Host ("  validation skipped — validator self-test errored: {0}" -f $_) -ForegroundColor Yellow }
  } else { Write-Host "  validation skipped — python/.system unavailable" -ForegroundColor Yellow }
} else {
  Write-Host ("  validation skipped — quick_validate.py not found ({0})" -f $Validator) -ForegroundColor Yellow
}
if ($valOk) {
  foreach ($r in @($results | Where-Object { $_.Status -in @('linked','ok','generated') })) {
    $sp = Join-Path $SkillsRoot $r.Name
    try {
      $out = & $py.Source $Validator $sp 2>&1
      if ($LASTEXITCODE -ne 0) { $r.Note = ("VALIDATE FAIL: {0}" -f ("$out".Trim())) }
    } catch { $r.Note = "VALIDATE ERROR: $_" }
  }
  Write-Host "  validator self-test OK — per-skill results in summary" -ForegroundColor Green
} else {
  Write-Host "  (host-python problem only — junctions/generation are unaffected; run validation from Codex if wanted)" -ForegroundColor DarkGray
}

# --- Prune (report-only unless -Force) ------------------------------------
if ($Prune) {
  Write-Host ""
  Write-Host "Prune (kit-owned orphans)" -ForegroundColor Cyan
  foreach ($d in (Get-ChildItem $SkillsRoot -Directory -Force | Where-Object { $_.Name -ne '.system' })) {
    $kitSkill = (Test-Reparse $d.FullName) -and ((Get-ReparseTarget $d.FullName) -like (Join-Path $SkillsSrc '*'))
    $kitAgent = Test-Path (Join-Path $d.FullName $GenMarker)
    if (-not ($kitSkill -or $kitAgent)) { continue }
    $srcName = $d.Name
    $stillThere = (Test-Path (Join-Path $SkillsSrc $srcName)) -or (Test-Path (Join-Path $AgentsSrc "$srcName.md"))
    if ($stillThere) { continue }
    if ($Force -and -not $WhatIf) {
      if ($kitSkill) { [System.IO.Directory]::Delete($d.FullName, $false) }   # reparse point only
      else { Remove-Item -LiteralPath $d.FullName -Recurse -Force }            # kit-generated dir we own
      Write-Host ("  removed orphan: {0}" -f $srcName) -ForegroundColor Yellow
    } else {
      Write-Host ("  orphan (use -Prune -Force to remove): {0}" -f $srcName)
    }
  }
}

# --- Summary --------------------------------------------------------------
Write-Host ""
Write-Host "Summary" -ForegroundColor Cyan
$results | Sort-Object Kind, Name | Format-Table -AutoSize Kind, Name, Status, Note
$bad = @($results | Where-Object { $_.Status -in @('error','conflict') -or $_.Note -like 'VALIDATE*' })
Write-Host ("skills+agents exposed: {0}   issues: {1}" -f $results.Count, $bad.Count)
if ($bad.Count -gt 0) {
  Write-Host "Issues are reported, not auto-fixed (a canonical SKILL.md change is Category-2)." -ForegroundColor Yellow
  exit 1
}
Write-Host "Restart Codex to pick up new/changed skills." -ForegroundColor Green
exit 0
