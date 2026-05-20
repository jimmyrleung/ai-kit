#!/usr/bin/env bash
# ai-kit -> Cursor CLI adapter (Category-1, additive, Claude-untouched).
#
# Makes the single canonical ai-kit source consumable by the Cursor CLI
# (`cursor-agent`), mirroring the existing ~/.claude / ~/.codex model.
# This is the OPERATIVE script: the Cursor CLI on Windows hard-codes a
# PowerShell shell with documented cold-start hangs, so cursor-agent is
# typically run under WSL — run THIS (sync.ps1 is Windows-native parity).
#
# Verified vs Cursor docs (cursor.com/docs), 2026-05-19. See ./README.md and
# ../../docs/cursor-portability-assessment.md for the design + decision record.
# Cursor ships near-daily; items tagged [verify on installed binary] in the
# README/assessment are version-sensitive — re-check after a Cursor update.
#
# What it does (NOTHING touches the canonical ai-kit tree; Claude unaffected):
#
#   1. Skills (41) : per-skill symlink  $CURSOR_HOME/skills/<name>
#                    -> <repo>/skills/<name>.  Cursor's NATIVE user-level
#                    skills root (self-contained — does NOT depend on the
#                    ~/.claude compat root). SKILL.md spec is identical;
#                    no body transform.
#   2. Orchestr.   : Cursor deprecated standalone slash-commands (folded
#                    into Skills; `/migrate-to-skills` converts them with
#                    disable-model-invocation:true). The ~25 thin per-phase
#                    shims need nothing (their skill is already symlinked).
#                    The 5 family ORCHESTRATORS + 3 per-task EXECUTORS carry
#                    real wiring no skill owns -> each is GENERATED as a
#                    Cursor skill with `disable-model-invocation: true`
#                    (explicit-only /name, never auto-triggers). Canonical
#                    commands/ is untouched (Claude keeps the /x UX).
#   3. Agents (17) : Cursor HAS a native subagent primitive. Each agents/*.md
#                    is GENERATED as $CURSOR_HOME/agents/<name>.md (Cursor
#                    native form: name+description+body; model/tools/color
#                    dropped -> model inherits). Cursor has no explicit-only
#                    flag for subagents (auto-delegation is governed by the
#                    description) — documented caveat, NOT a canonical edit.
#   4. AGENTS.md   : prints where to place adapters/cursor/AGENTS.md. Not
#                    done silently (global read-location is [verify]).
#
# Idempotent & safe: never clobbers a non-kit entry, never deletes a symlink
# target, --prune is report-only unless --force.
set -euo pipefail

DRY=0; PRUNE=0; FORCE=0
for a in "$@"; do case "$a" in
  --dry-run) DRY=1 ;; --prune) PRUNE=1 ;; --force) FORCE=1 ;;
  -h|--help) sed -n '2,40p' "$0"; exit 0 ;;
  *) echo "unknown arg: $a" >&2; exit 2 ;;
esac; done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"
AGENTS_SRC="$REPO_ROOT/agents"
CMD_SRC="$REPO_ROOT/commands"
CURSOR_HOME="${CURSOR_HOME:-$HOME/.cursor}"
SKILLS_ROOT="$CURSOR_HOME/skills"
AGENTS_ROOT="$CURSOR_HOME/agents"
GEN_MARKER=".ai-kit-generated"             # sentinel dir-file for generated skills
AGEN_MARKER="<!-- ai-kit-generated:"       # in-file sentinel for generated subagents

echo; echo "ai-kit -> Cursor adapter"
echo "  repo        : $REPO_ROOT"
echo "  cursor home : $CURSOR_HOME"
echo "  skills root : $SKILLS_ROOT"
echo "  agents root : $AGENTS_ROOT"
echo "  mode        : $([ $DRY -eq 1 ] && echo 'DRY RUN' || echo apply)"; echo
[ -d "$SKILLS_SRC" ] || { echo "canonical skills dir not found: $SKILLS_SRC" >&2; exit 1; }
if [ $DRY -ne 1 ]; then mkdir -p "$SKILLS_ROOT" "$AGENTS_ROOT"; fi

issues=0
# YAML double-quoted scalar: escape backslash then double-quote.
yq(){ printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g'; }
# Body = everything after the second `---` fence, CR stripped.
body_of(){ awk 'BEGIN{n=0} /^---[[:space:]]*$/{n++; next} n>=2{print}' "$1" | tr -d '\r'; }
# fm_get FILE KEY -> value of a frontmatter key (within the first --- block;
# preserves colons in the value; CR stripped).
fm_get(){ awk -v key="$2" 'BEGIN{n=0}
  /^---[[:space:]]*$/{n++; if(n>=2) exit; next}
  n==1 && $0 ~ ("^"key":[[:space:]]") { sub("^"key":[[:space:]]*",""); gsub(/\r/,""); print; exit }' "$1"; }

# --- 1. Skills: per-skill symlink ----------------------------------------
for s in "$SKILLS_SRC"/*/; do
  name="$(basename "$s")"; link="$SKILLS_ROOT/$name"; tgt="${s%/}"
  if [ -e "$link" ] || [ -L "$link" ]; then
    if [ -L "$link" ]; then
      cur="$(readlink "$link")"
      if [ "$cur" = "$tgt" ]; then echo "  ok        skill  $name"; continue; fi
      if [ $FORCE -ne 1 ]; then echo "  conflict  skill  $name (-> $cur; use --force)"; issues=$((issues+1)); continue; fi
      [ $DRY -eq 1 ] || rm "$link"            # symlink only, never its target
    else
      echo "  skip      skill  $name (real dir, not kit-owned)"; continue
    fi
  fi
  if [ $DRY -eq 1 ]; then echo "  would-link skill $name"; else ln -s "$tgt" "$link"; echo "  linked    skill  $name"; fi
done

# --- 2. Orchestrators/executors -> generated explicit-only Cursor skills --
# Explicit allowlist (NEVER the ~25 thin shims — their skill is already
# symlinked). These 8 carry real orchestration prose no skill owns.
# disable-model-invocation:true => /name only, never auto-triggers.
ORCH_CMDS="full-bug-fix-workflow integration-feature-dev refactor-techdebt-dev full-incident-response greenfield-dev implement-task gf-implement-task implement-bug-fix"
for cn in $ORCH_CMDS; do
  cf="$CMD_SRC/$cn.md"
  [ -f "$cf" ] || { echo "  error     orch   $cn (commands/$cn.md not found)"; issues=$((issues+1)); continue; }
  desc="$(fm_get "$cf" description)"
  [ -n "$desc" ] || { echo "  error     orch   $cn (missing description)"; issues=$((issues+1)); continue; }
  dest="$SKILLS_ROOT/$cn"
  if [ -d "$dest" ] && [ ! -f "$dest/$GEN_MARKER" ] && [ ! -L "$dest" ]; then
    echo "  skip      orch   $cn (exists, not kit-generated)"; continue
  fi
  if [ $DRY -eq 1 ]; then echo "  would-gen orch   $cn"; continue; fi
  mkdir -p "$dest"
  { printf -- '---\nname: %s\ndescription: "%s"\ndisable-model-invocation: true\n---\n\n' "$cn" "$(yq "$desc")";
    body_of "$cf"; printf '\n'; } > "$dest/SKILL.md"
  echo "source: commands/$cn.md" > "$dest/$GEN_MARKER"
  echo "  generated orch   $cn (explicit-only /$cn)"
done

# --- 3. Agents -> generated native Cursor subagents ----------------------
if [ -d "$AGENTS_SRC" ]; then
  for a in "$AGENTS_SRC"/*.md; do
    [ -e "$a" ] || continue
    name="$(fm_get "$a" name | tr -d '"')"
    desc="$(fm_get "$a" description)"
    [ -n "$name" ] && [ -n "$desc" ] || { echo "  error     agent  $(basename "$a") (missing name/description)"; issues=$((issues+1)); continue; }
    dest="$AGENTS_ROOT/$name.md"
    if [ -f "$dest" ] && ! grep -q "ai-kit-generated:" "$dest" 2>/dev/null; then
      echo "  skip      agent  $name (exists, not kit-generated)"; continue
    fi
    if [ $DRY -eq 1 ]; then echo "  would-gen agent  $name"; continue; fi
    # name+description only (model/tools/color dropped -> Cursor model:inherit).
    { printf -- '---\nname: %s\ndescription: "%s"\n---\n' "$name" "$(yq "$desc")";
      printf '%s source: agents/%s — do not hand-edit -->\n\n' "$AGEN_MARKER" "$(basename "$a")";
      body_of "$a"; printf '\n'; } > "$dest"
    echo "  generated agent  $name"
  done
fi

# --- 4. AGENTS.md hint (never silent) ------------------------------------
echo; echo "AGENTS.md (Cursor instruction layer)"
echo "  Cursor reads project-root AGENTS.md + CLAUDE.md as rules; the global"
echo "  read-location is [verify on installed binary]. Place per project:"
echo "    ln -s $SCRIPT_DIR/AGENTS.md <your-project>/AGENTS.md   # or copy"
echo "  NOTE: kit Cursor-MECHANICS layer only. Your personal ~/.claude/CLAUDE.md"
echo "  conventions (confidence scoring, ask-before-assuming, scope discipline,"
echo "  read-before-edit, verification-before-completion, risky-command confirm)"
echo "  do NOT transfer — Cursor CLI never reads ~/.claude/CLAUDE.md globally."
echo "  Mirror them into a PRIVATE AGENTS.md yourself (keep it out of this public"
echo "  repo) — see adapters/cursor/README.md."

# --- Prune (report-only unless --force) ----------------------------------
if [ $PRUNE -eq 1 ]; then
  echo; echo "Prune (kit-owned orphans):"
  for d in "$SKILLS_ROOT"/*/; do
    [ -e "$d" ] || continue
    n="$(basename "$d")"
    kit=0
    if [ -L "${d%/}" ] && [ "$(readlink "${d%/}")" = "$SKILLS_SRC/$n" ]; then kit=1; fi
    [ -f "$d/$GEN_MARKER" ] && kit=1
    [ $kit -eq 1 ] || continue
    if [ -d "$SKILLS_SRC/$n" ] || [ -f "$CMD_SRC/$n.md" ]; then continue; fi
    if [ $FORCE -eq 1 ] && [ $DRY -ne 1 ]; then
      if [ -L "${d%/}" ]; then rm "${d%/}"; else rm -rf "$d"; fi; echo "  removed orphan skill: $n"
    else echo "  orphan skill (use --prune --force): $n"; fi
  done
  for f in "$AGENTS_ROOT"/*.md; do
    [ -e "$f" ] || continue
    grep -q "ai-kit-generated:" "$f" 2>/dev/null || continue
    n="$(basename "$f" .md)"
    [ -f "$AGENTS_SRC/$n.md" ] && continue
    # frontmatter `name:` may differ from filename — also keep if any agent's name matches
    keep=0
    for af in "$AGENTS_SRC"/*.md; do [ -e "$af" ] || continue
      [ "$(fm_get "$af" name | tr -d '"')" = "$n" ] && { keep=1; break; }; done
    [ $keep -eq 1 ] && continue
    if [ $FORCE -eq 1 ] && [ $DRY -ne 1 ]; then rm "$f"; echo "  removed orphan agent: $n"
    else echo "  orphan agent (use --prune --force): $n"; fi
  done
fi

echo
[ $issues -eq 0 ] && { echo "OK — restart cursor-agent to pick up new skills/subagents."; exit 0; } \
                   || { echo "$issues issue(s) reported (not auto-fixed — canonical edits are Category-2)."; exit 1; }
