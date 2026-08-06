#!/usr/bin/env bash
# ai-kit -> Cursor CLI adapter (v2 — Category-1, additive, Claude-untouched).
#
# Makes the single canonical ai-kit source consumable by the Cursor CLI
# (`cursor-agent`), mirroring the existing ~/.claude / ~/.codex model.
# This is the OPERATIVE script: the Cursor CLI on Windows hard-codes a
# PowerShell shell with documented cold-start hangs, so cursor-agent is
# typically run under WSL — run THIS from inside WSL (sync.ps1 is
# Windows-native parity). It targets the invoking shell's ~/.cursor.
#
# Rewritten 2026-08-06 for the v2 kit (skill-centric refactor). Base mechanics
# verified vs Cursor docs (cursor.com/docs) 2026-05-19 + live probe; Cursor
# ships near-daily — re-check [verify] items in README.md after an update.
#
# What it does (NOTHING touches the canonical ai-kit tree; Claude unaffected):
#
#   1. Skills    : per-skill symlink  $CURSOR_HOME/skills/<name>
#                  -> <repo>/skills/<name>, for EVERY canonical skill.
#                  Cursor's native user-level skills root; SKILL.md spec is
#                  identical — no body transform. This is the ONLY live
#                  mechanism in v2.
#   2. Orchestr. : NONE in v2 — every command was archived (skills are
#                  invoked directly as /name). ORCH_CMDS is empty; the
#                  generation path below is retained dormant — repopulate
#                  only if a command with a body no skill owns ever returns.
#   3. Agents    : NONE in v2 — the kit-refactor (2026-08) archived all named
#                  agents (generic subagents ride inside skill prose). The
#                  generation path is retained dormant; agents/ absent means
#                  it no-ops. This also moots the #160426 CLI parity gap for
#                  the kit (nothing is installed at ~/.cursor/agents anymore).
#   4. AGENTS.md : prints guidance for activating adapters/cursor/AGENTS.md
#                  (the kit's Cursor-MECHANICS layer). NOT done silently: a
#                  deployed AGENTS.md is the user's PRIVATE conventions layer —
#                  the kit block is pasted at its include point (kit-mechanics
#                  markers), never plain-copied over.
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
AGENTS_SRC="$REPO_ROOT/agents"             # absent in v2 — path retained dormant
CMD_SRC="$REPO_ROOT/commands"              # absent in v2 — path retained dormant
CURSOR_HOME="${CURSOR_HOME:-$HOME/.cursor}"
SKILLS_ROOT="$CURSOR_HOME/skills"
AGENTS_ROOT="$CURSOR_HOME/agents"
GEN_MARKER=".ai-kit-generated"             # sentinel dir-file for generated skills

echo; echo "ai-kit -> Cursor adapter (v2)"
echo "  repo        : $REPO_ROOT"
echo "  cursor home : $CURSOR_HOME"
echo "  skills root : $SKILLS_ROOT"
echo "  mode        : $([ $DRY -eq 1 ] && echo 'DRY RUN' || echo apply)"; echo
[ -d "$SKILLS_SRC" ] || { echo "canonical skills dir not found: $SKILLS_SRC" >&2; exit 1; }
[ $DRY -eq 1 ] || mkdir -p "$SKILLS_ROOT"

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

# --- 1. Skills: per-skill symlink (the only live v2 mechanism) ------------
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

# --- 2. Orchestrators/executors: NONE in v2 (dormant) ---------------------
# v1 generated 8 command-bodied skills here. All commands are archived; the
# allowlist is empty by design. Repopulate only if a command with a body no
# junctioned skill owns ever returns.
ORCH_CMDS=""
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

# --- 3. Agents: NONE in v2 (dormant — agents/ absent means no-op) ---------
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
    mkdir -p "$AGENTS_ROOT"
    # name+description only (model/tools/color dropped -> Cursor model:inherit).
    { printf -- '---\nname: %s\ndescription: "%s"\n---\n' "$name" "$(yq "$desc")";
      printf -- '<!-- ai-kit-generated: source: agents/%s — do not hand-edit -->\n\n' "$(basename "$a")";
      body_of "$a"; printf '\n'; } > "$dest"
    echo "  generated agent  $name"
  done
fi

# --- 4. AGENTS.md hint (never silent) ------------------------------------
echo; echo "AGENTS.md (Cursor instruction layer)"
echo "  Cursor reads project-root AGENTS.md + CLAUDE.md as rules; a global"
echo "  read-location is [verify on installed binary]. DO NOT plain-copy the"
echo "  kit file over a deployed AGENTS.md: that file is the user's PRIVATE"
echo "  conventions layer. After editing the kit file, refresh ONLY the block"
echo "  between its kit-mechanics markers at the include point:"
echo "    source : $SCRIPT_DIR/AGENTS.md"
echo "    target : your private AGENTS.md  (between <!-- kit-mechanics:begin/end -->)"
echo "  Project-scope also works: copy/link the kit file into the project root."
echo "  NOTE: your personal ~/.claude/CLAUDE.md conventions do NOT transfer —"
echo "  mirror them into a PRIVATE AGENTS.md yourself (keep it out of this"
echo "  public repo) — see adapters/cursor/README.md."

# --- Prune (report-only unless --force) ----------------------------------
# Iterates plain entries (not `*/`) so DANGLING symlinks — e.g. junctions to
# skills that moved to archive/v1 — are seen and pruned too.
if [ $PRUNE -eq 1 ]; then
  echo; echo "Prune (kit-owned orphans):"
  for p in "$SKILLS_ROOT"/*; do
    [ -e "$p" ] || [ -L "$p" ] || continue
    n="$(basename "$p")"
    kit=0
    if [ -L "$p" ]; then
      case "$(readlink "$p")" in "$SKILLS_SRC"/*) kit=1 ;; esac
    elif [ -d "$p" ] && [ -f "$p/$GEN_MARKER" ]; then kit=1; fi
    [ $kit -eq 1 ] || continue
    if [ -d "$SKILLS_SRC/$n" ] || [ -f "$CMD_SRC/$n.md" ]; then continue; fi
    if [ $FORCE -eq 1 ] && [ $DRY -ne 1 ]; then
      if [ -L "$p" ]; then rm "$p"; else rm -rf "$p"; fi; echo "  removed orphan skill: $n"
    else echo "  orphan skill (use --prune --force): $n"; fi
  done
  if [ -d "$AGENTS_ROOT" ]; then
    for f in "$AGENTS_ROOT"/*.md; do
      [ -e "$f" ] || continue
      grep -q "ai-kit-generated:" "$f" 2>/dev/null || continue
      n="$(basename "$f" .md)"
      [ -f "$AGENTS_SRC/$n.md" ] && continue
      # frontmatter `name:` may differ from filename — also keep if any agent's name matches
      keep=0
      if [ -d "$AGENTS_SRC" ]; then
        for af in "$AGENTS_SRC"/*.md; do [ -e "$af" ] || continue
          [ "$(fm_get "$af" name | tr -d '"')" = "$n" ] && { keep=1; break; }; done
      fi
      [ $keep -eq 1 ] && continue
      if [ $FORCE -eq 1 ] && [ $DRY -ne 1 ]; then rm "$f"; echo "  removed orphan agent: $n"
      else echo "  orphan agent (use --prune --force): $n"; fi
    done
  fi
fi

echo
[ $issues -eq 0 ] && { echo "OK — restart cursor-agent to pick up new skills."; exit 0; } \
                   || { echo "$issues issue(s) reported (not auto-fixed — canonical edits are Category-2)."; exit 1; }
