---
name: audit-skills
description: On-demand structural audit of the local Claude skill/command/agent population — frontmatter validity, description size, trigger-keyword coverage, body length, cross-skill redundancy, dead references, frontmatter-vs-directory mismatch, naming consistency. Stages proposals under ~/.claude/improvements/{date}/ with one per finding; never auto-edits. Run after authoring a new skill, before a publish-quality run, or accept the staleness prompt at session start. Invoke as /audit-skills. Complements /improve's friction-driven Phase 2 inline audit.
---

<!-- intentionally-long: 10 checks documented inline; splitting to references/ would hurt usability because each check is short, the procedure flows linearly, and progressive disclosure adds latency for no readability win at this size. -->

# Audit Skills — structural quality pass over the local skill population

You are running a structural audit of the user's custom skills, commands, and agents.
You do NOT edit any live file; you stage proposals under `~/.claude/improvements/{date}/`
exactly like `/improve` does. Same approval discipline: the user reviews and approves
one at a time.

This is the deep, on-demand sibling of `/improve`'s Phase 2 inline thin audit
(vague-description + >150-line flags). It runs wider (10 checks) and only when invoked.

## Inputs you read

- `C:\ai-kit\skills\**\SKILL.md` — all bodies + frontmatter.
- `C:\ai-kit\commands\*.md` — frontmatter only (verify name + description).
- `C:\ai-kit\agents\*.md` — frontmatter only.
- `C:\ai-kit\templates\**\*.md` — existence + cross-skill template references.
- The most recent `~/.claude/improvements/{date}/REVIEW.md` if present — for the
  invocation-count column in the fitness table. Optional input; skip if not present.
- `~/.claude/improvements/last-audit.txt` — timestamp of last audit; missing = never run.

Resolution via the `~/.claude/{skills,commands,agents}/` junctions is fine — same files.
Exclude bundled/system skills and Anthropic-shipped skills from any proposal.

## Outputs you write

- `~/.claude/improvements/{YYYY-MM-DD}/REVIEW.md` (one section per check; fitness table).
- `~/.claude/improvements/{YYYY-MM-DD}/proposals/NN-[audit]-<slug>.md` — one per finding.
  Use the same directory as `/improve`. Tag filenames with `[audit]` so `/improve` and
  the human can tell audit-derived proposals from friction-derived ones.
- `~/.claude/improvements/last-audit.txt` — today's date.
- Only on the user's explicit, per-item approval: the actual target files.

If `REVIEW.md` already exists for today (because `/improve` ran earlier), append a
`## Audit-derived findings — {YYYY-MM-DD HH:mm}` section to it instead of overwriting.

## Checks (10 total)

### Check 1 — Frontmatter validity
For each SKILL.md / command / agent file:
- `---` fences front and back; YAML parses.
- `name:` matches the directory (skills) or filename stem (commands/agents).
- `description:` present and non-empty.
- No unknown fields beyond `name`, `description`, `allowed-tools` (skills),
  `argument-hint` / `arguments` (commands), `model` (agents).
- Skills live as `skills/<name>/SKILL.md` (not loose `.md`); commands are flat in
  `commands/`; agents are flat in `agents/`.

→ Each failure: one proposal with the exact diff to fix.

### Check 2 — Description size
- Soft-flag: > 600 chars. Surface in fitness table, suggest tightening.
- Hard-flag: > 1,536 chars. Proposal includes a concrete rewrite.

Show current description, proposed shorter one, char-count delta.

### Check 3 — Description trigger-keyword coverage
List plausible synonyms a user might invoke this skill with that are NOT in the
description. Bias toward common verbs: `verify` / `check` / `validate` / `audit` /
`review` / `final` / `before publish` / `lint` — pick the ones matching this skill's
domain. Skills missing ≥2 likely synonyms → one proposal showing the description with
synonyms folded inline (preserve the char budget — don't tack on a new sentence).

### Check 4 — Body length
- Soft-flag: > 150 lines. Note in fitness table; ask "intentional or candidate for split?".
- Hard-flag: > 250 lines. Propose splitting reference content into `references/`
  per Anthropic's progressive-disclosure pattern.

Honor an `<!-- intentionally-long: <reason> -->` HTML comment at the top of a SKILL.md
body — if present, downgrade the soft-flag to a noted-and-accepted line in the table.

### Check 5 — Cross-skill redundancy (description-based)
Pairwise compare descriptions. For any two with ≥5 shared trigger phrases in the
first 50 words, surface the overlap: "Skills X and Y overlap on triggers A, B, C —
consider differentiating descriptions, or merging if bodies overlap too." Do NOT
propose a merge diff; surface and let the user decide.

### Check 6 — Cross-skill redundancy (body-based, lightweight)
For each pair in the same family (heuristic: same first segment before `-`), compare
top-level section headers (`##` lines). ≥60% header match → soft finding. Same
disposition as Check 5: surface, don't propose a merge.

### Check 7 — Dead references in skill bodies
Scan each SKILL.md body for:
- Paths containing `agent-workflows/` (stale post-3.1).
- Paths containing `agent-docs/` (stale post-3.1).
- Paths containing the per-family `{bugfix,feature-addition,greenfield-dev,
  incident-response,refactoring-tech-debt}/` segments (stale post-3.1 flatten).
- File references that don't resolve (templates that no longer exist; cross-skill
  references to skills that have been deleted or renamed).
- `~/.claude/` paths that don't resolve through the junctions.

Each finding: one proposal per file with exact line numbers and the suggested
replacement path.

### Check 8 — Frontmatter-vs-directory mismatch
- A `SKILL.md` whose frontmatter looks like a command (has `argument-hint`, no long
  description) → propose "might belong at `C:\ai-kit\commands\`".
- A command file whose frontmatter looks like a skill (long description with trigger
  phrases, no `argument-hint`) → propose the inverse.
- An agent file whose frontmatter looks like a command/skill → propose moving.

Anti-pattern context: `discovery-agent.md` was misfiled at `~/.claude/commands/`
pre-3.1. This check is what would have caught that class of mistake.

### Check 9 — Coverage: commands without skill bodies
For each `C:\ai-kit\commands\<X>.md`, check whether it has a corresponding skill OR
whether it is itself the implementation (thin self-contained command — fine for
one-shots). Soft-flag any thin command where the body length suggests it should be a
skill (> 50 lines of non-frontmatter content in a command file).

### Check 10 — Naming consistency
- All skills/commands/agents use kebab-case (no underscores, no camelCase).
- No `name:` field collides across skills/commands/agents.
- No skill name ends in `-skill`; no command name starts with `/` in the name field.

One proposal per finding.

## Procedure

### Phase 1 — Enumerate
Glob the four input directories. Build a structured inventory:
`{ skills: [...], commands: [...], agents: [...], templates: [...] }`.

### Phase 2 — Run all 10 checks
Walk each check across the relevant subset. Collect findings as (check, file) pairs;
group by file for the report. Don't fabricate findings to look productive — zero
findings on a check is a valid result.

### Phase 3 — Stage the packet
Apply the keep-two rule (same as `/improve`): if there are already two or more dated
dirs under `~/.claude/improvements/`, delete all but the most recent one (so after
creating today's there are exactly two). The user is the only deleter — surface the
candidate dirs and ask before removing.

Create or append-to today's REVIEW.md:

```
# Improvement review — {YYYY-MM-DD}  (or "## Audit-derived findings — {timestamp}" if appending)

**Population audited:** N skills + M commands + K agents + L templates
**Findings:** P (across 10 checks)  ·  **Proposals staged:** P

## Findings by check
| Check | Findings | Skills affected |
|---|---|---|
| 1. Frontmatter validity | 0 | — |
| 2. Description size | … | … |
| … | | |

## Skill fitness table
| skill | body lines | desc chars | last invoked | flags |
|---|---|---|---|---|
| … | | | | |

## Proposals
1. NN-[audit]-<slug> — <target> — <one-line what & why>.
2. …

## Cross-cutting observations
- <patterns, not per-file>
```

Write one `proposals/NN-[audit]-<slug>.md` per finding using `/improve`'s proposal
template (Target / Type / Derived from / Confidence / Change / Rationale).

Write `last-audit.txt` with today's date.

### Phase 4 — Present & (on approval) apply
Same procedure as `/improve` Phase 5:
1. Print REVIEW.md (the summary) to chat. Point at the dir, don't dump proposals.
2. Walk proposals one at a time. Ask before each: "Apply / skip / defer?"
3. For each approved proposal: apply *exactly* what's in it.
4. Route commits by target per Tier 3.1: skill/command/agent/template edits → `ai-kit`;
   `CLAUDE.md` / `observations/` / `improvements/` / `hooks/` → `claude-home`.
   Run the secret-scan before pushing (the ai-kit pre-commit hook does this).
5. Ask before committing; ask before pushing. Never auto-push.
6. Print a one-line close summary: `findings: P · applied: A · declined: D · deferred: F · commit: <hash or "skipped">`.

## Staleness behaviour
At session start: if `last-audit.txt` is missing OR > 90 days old AND the skill count
has changed by > 3 since the timestamp inside `last-audit.txt`, offer once:
"It's been D days since the last skill audit (N new/changed skills) — run /audit-skills now?"
Same offer-don't-run discipline as `/improve`. Never run unprompted.

## Composition with /improve

- `/improve` keeps its inline Phase 2 thin audit (vague-description + >150-line flags).
  It still runs every week as part of friction review and is fine for the small
  population subset that has invocations.
- `/audit-skills` runs on-demand and on a 90-day floor.
- When both surface the same finding: `/improve` checks for an `[audit]`-tagged
  proposal on the same target in the current staging dir; if present, it marks its
  own finding "already staged by audit-skills NN-…" and does not restage.

## What this skill does NOT do
- **Effectiveness scoring** (which skills work well) — `/improve`'s fitness table owns this.
- **CLAUDE.md / MEMORY.md / orchestrator lint** — `/improve` Phase 3 owns this.
- **New-skill synthesis** (capability gaps) — `/improve` owns this via observation patterns.
- **Auto-fix** — every finding is a proposal the user approves one at a time.
- **Effectiveness benchmarking** — out of scope. See the agent-tuning research note.

This is a structural-quality lint, not a churn engine. A run that produces a clean
report and zero proposals is a good run.
