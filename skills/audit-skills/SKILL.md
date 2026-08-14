---
name: audit-skills
description: On-demand structural audit of the local Claude skill/command/agent population — frontmatter validity, description size + aggregate description budget, trigger-keyword coverage, body length, cross-skill redundancy, dead references, frontmatter-vs-directory mismatch, naming consistency, volatile-content rot. Stages proposals under ~/.claude/improvements/{date}/ with one per finding; never auto-edits. Run after authoring a new skill, before a publish-quality run, or accept the staleness prompt at session start. Invoke as /audit-skills. Complements /improve's friction-driven Phase 2 inline audit.
---

<!-- intentionally-long: 12 checks documented inline; splitting to references/ would hurt usability because each check is short, the procedure flows linearly, and progressive disclosure adds latency for no readability win at this size. -->

# Audit Skills — structural quality pass over the local skill population

You are running a structural audit of the user's custom skills, commands, and agents.
You do NOT edit any live file; you stage proposals under `~/.claude/improvements/{date}/`
exactly like `/improve` does. Same approval discipline: the user reviews and approves
one at a time.

This is the deep, on-demand sibling of `/improve`'s Phase 2 inline thin audit
(vague-description + >150-line flags). It runs wider (12 checks) and only when invoked.

## Inputs you read

- `C:\ai-kit\skills\**\SKILL.md` — all bodies + frontmatter.
- `C:\ai-kit\commands\*.md`, `C:\ai-kit\agents\*.md`, `C:\ai-kit\templates\**\*.md` —
  **retired 2026-08-06 (v2, archive/v1)**: all three dirs are deleted; enumerate as zero
  and skip when absent. Specs for their checks (8, 9, and the command/agent legs of 1/10)
  stay below, dormant, in case those entity types return.
- The most recent `~/.claude/improvements/{date}/REVIEW.md` if present — for the
  invocation-count column in the fitness table. Optional input; skip if not present.
- `~/.claude/improvements/last-audit.txt` — timestamp of last audit; missing = never run.

Resolution via the `~/.claude/{skills,commands,agents}/` junctions is fine — same files.
Exclude bundled/system skills and Anthropic-shipped skills from any proposal.

## Outputs you write

- `~/.claude/improvements/{YYYY-MM-DD}/REVIEW.md` (one section per check; fitness table).
- `~/.claude/improvements/{YYYY-MM-DD}/proposals/NN-[audit]-<slug>.md` — one per
  **high-confidence finding (>90%)**, ready for one-at-a-time apply/skip/defer review.
  Tag filenames with `[audit]` so `/improve` and the human can tell audit-derived
  proposals from friction-derived ones.
- `~/.claude/improvements/backlog/NN-<slug>.md` — one per **lower-confidence finding
  (≤90%)**. **Persistent across audit runs** (NOT under the dated `{date}/` dir).
  Re-evaluated every run — confidence may rise with more data and promote to a proposal,
  or fall and close as won't-do.
- `~/.claude/improvements/last-audit.txt` — today's date + run-summary counts + the
  aggregate description budget (skill count · total description chars) for Check 2's
  growth comparison next run.
- Only on the user's explicit, per-item approval: the actual target files.

If `REVIEW.md` already exists for today (because `/improve` ran earlier), append a
`## Audit-derived findings — {YYYY-MM-DD HH:mm}` section to it instead of overwriting.

## Checks (12 total)

### Check 1 — Frontmatter validity
For each SKILL.md / command / agent file:
- `---` fences front and back; the frontmatter block parses under a **STRICT YAML parser (js-yaml)** — not just the Claude-lenient/regex check. Specifically flag an **unquoted `description:` (or any plain scalar) containing `: ` (colon-space)** or other YAML-special constructs (leading `[`/`{`/`&`/`*`/`|`/`>`, an unescaped `#` mid-scalar) that strict parsers (**Codex**, claude.ai, the open-standard, the API) reject while Claude Code tolerates. Validate with **Node + js-yaml** (the local PyYAML segfaults on this machine — see memory `skill-frontmatter-strict-yaml`; don't reach for it). Each failure → a proposal that quotes the value.
- `name:` matches the directory (skills) or filename stem (commands/agents). **Commands
  (`commands/*.md`) carry no `name:` field by kit convention — the filename is the name.**
  Absence of `name:` on a command is an expected non-finding; flag only a `name:` that is
  *present but mismatched* with the file stem. (Skills and agents still require `name:`
  matching the dir/stem.)
- `description:` present and non-empty.
- No unknown fields beyond `name`, `description`, `allowed-tools`, `argument-hint`,
  `arguments`, `disable-model-invocation` (skills — the last three per
  code.claude.com/docs/en/skills, verified 2026-07-19; `arguments` is the documented
  named positional-argument mapping, also the cc-looper worker-skill spawn contract),
  `argument-hint` / `arguments` (commands), `model` / `tools` / `color` (agents).
- Skills live as `skills/<name>/SKILL.md` (not loose `.md`); commands are flat in
  `commands/`; agents are flat in `agents/`.

→ Each failure: one proposal with the exact diff to fix.

### Check 2 — Description size (tiered by role — house decision 2026-08-05; canonical spec, write-skills points here)
- ≤ 600: target for new single-job skills (write-skills enforces at authoring) — nothing to flag.
- 600–800: accepted band for evolved skills and mode-detecting heads — fitness-table note only, never a proposal.
- 800–1,024: multi-sibling consolidation heads only (a skill that absorbed several retired
  entry points legitimately carries their trigger surfaces). Flag ONLY if the excess is
  process detail discoverable in the body — then propose a trim of exactly that; trigger
  keywords are the head doing its job, never trim those. A non-consolidation skill in this
  band gets a trim proposal.
- > 1,024: hard fail — **exceeds the portable/open-standard cap** (Codex / claude.ai / API
  reject). Always a proposal with a concrete rewrite. (Claude Code's own 1,536 cap is
  academic once 1,024 is enforced.)
- **Aggregate budget:** every description is always in startup context, so the population's
  total matters, not just each file's. Sum description chars across all skills; report
  skill count + total in REVIEW.md and store both in `last-audit.txt`. Soft-flag when the
  total grew > 20% since the last audit — wrong-skill selection rises as the population
  and its descriptions grow (Databricks / PostHog field data).

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
body. It downgrades the soft-flag unconditionally. It also covers the HARD flag —
house decision 2026-08-13 (backlog 23) — but only when the reason names why a
`references/` split specifically fails (read-latency, linear procedure, load-once
contract), not just "it's long"; a marked >250 body becomes a noted-and-accepted
line in the table, tracking its line count run-over-run. A >250 body with NO marker
(or a marker whose reason doesn't address length) still gets a split proposal.

Canonical line metric: `(Get-Content <file>).Count` — `Measure-Object -Line` undercounts
(~40% observed) and produced a false-clean cap check.

### Check 5 — Cross-skill redundancy (description-based)
Pairwise compare descriptions. For any two with ≥5 shared trigger phrases in the
first 50 words, surface the overlap: "Skills X and Y overlap on triggers A, B, C —
consider differentiating descriptions, or merging if bodies overlap too." Do NOT
propose a merge diff; surface and let the user decide.

### Check 6 — Cross-skill redundancy (body-based, lightweight)
For each pair in the same family (heuristic: same first segment before `-`), compare
top-level section headers (`##` lines). ≥60% header match → soft finding. Same
disposition as Check 5: surface, don't propose a merge.

### Check 7 — Dead references in skill, command, and agent bodies
Scan each SKILL.md, command, and agent body for:
- Paths containing `agent-workflows/` (stale post-3.1).
- Paths containing `agent-docs/` (stale post-3.1).
- Paths containing the per-family `{bugfix,feature-addition,greenfield-dev,
  incident-response,refactoring-tech-debt}/` segments (stale post-3.1 flatten).
- File references that don't resolve (templates that no longer exist; cross-skill
  references to skills that have been deleted or renamed).
- `~/.claude/` paths that don't resolve through the junctions.

Each finding: one proposal per file with exact line numbers and the suggested
replacement path.

Expected non-findings (do not flag): the cc-looper worker skills' `templates/*.md`
references resolve against cc-looper's source tree at runtime (its slice-09 techspec
§3.12), not the skill dir — verify existence under
`~/projects/cc-looper/templates/` before flagging. audit-skills' own Check 7 text
mentions the dead-path classes verbatim — self-matches are not findings. Skill-local
`templates/<name>.md` references resolve against the skill's own dir (its
`skills/<name>/templates/`), not the kit root — Test-Path there before flagging.
Path-like strings inside fenced example blocks that illustrate a convention the skill
creates at runtime in *target* repos (e.g. close 2c's `docs/rules/testing.md` index
example) are illustrative, not references — check the enclosing fence and whether the
path is meant to exist in this kit before flagging.

Derive the retired-name sweep list MECHANICALLY from the `archive/` directory listings
(archived skill/command/agent names), never from recall — a hand-enumerated regex omitted
one name and its dead refs survived the audit. When a CONVENTION (not an entity) is
retired, add its descriptive phrases to the sweep list — live-names-only sweeps missed
retired doctrine taught as current in 3 separate runs.

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
- No `name:` field collides across skills/commands/agents. (Command-wraps-skill pairing was
  the pre-refactor convention — retired 2026-08-05, no command wrappers; a same-name command
  today is a finding to surface, not an intended pairing.)
- No skill name ends in `-skill`; no command name starts with `/` in the name field.

### Check 11 — Output-doc filename contract
For each workflow family (orchestrator + its standalone per-phase commands), the output-doc filenames
must agree with `C:\ai-kit\docs\output-filename-contract.md`. Flag: (a) a `{token}_<suffix>.md`
reference whose token disagrees with the family's canonical token (e.g. `{feature}_techspec.md` or
`{prefix}_techspec.md` where the contract says `{feature_name}`); (b) an orchestrator-stated output
filename with no matching standalone command output (or vice-versa); (c) a family/phase not yet listed
in the contract table. Read filenames from command/skill bodies (grep `_techspec.md` / `_integration.md`
/ `_tasks.md` / `_investigation.md` / `_impact_analysis.md` / `_regression_test_plan.md` / `_audit.md`
/ `_plan.md` and the bare incident names). Surface mismatches; propose the token normalization, don't
silently rewrite.

One proposal per finding.

### Check 12 — Volatile-content rot
Scan skill bodies for content that drifts with time and rots the skill (the lint
counterpart of write-skills rules 4 and 8):
- **Baked-in runtime specifics:** hardcoded counts, version numbers, "as of …" dates,
  line-number references into *other* files. Exempt: dated provenance notes recording
  *when a fact was verified* (e.g. "verified 2026-07-19") — those are audit trail, not
  content that silently drifts.
- **Duplicated reference content** that has a canonical source elsewhere (a docs page,
  a repo file) → propose replacing the copy with a pointer to the single source of truth.
- **Patch-accretion smell:** ≥3 stacked exception/edge-case clauses appended to one
  section across successive fixes → surface as a regenerate-don't-patch candidate
  (propose regenerating the body from the skill's one-job spec, not another patch).

audit-skills' own Check 12 text names these patterns verbatim — self-matches are not
findings (same discipline as Check 7). Judgement-heavy check: expect most findings to
land in backlog (≤90%) rather than proposals; that's a valid outcome.

## Procedure

### Phase 1 — Enumerate
Glob the input directories that exist (skills always; commands/agents/templates only if
restored — see Inputs). Build a structured inventory:
`{ skills: [...], commands: [...], agents: [...], templates: [...] }` (empty arrays are valid).

Also read `~/.claude/improvements/pending-trigger-tests.txt` if present: any listed skill
gets a trigger-simulation check this run and is removed from the queue on pass.

### Phase 2 — Run all 12 checks
Walk each check across the relevant subset. Collect findings as (check, file) pairs;
group by file for the report. Don't fabricate findings to look productive — zero
findings on a check is a valid result.

A detector added since the last run implies a ONE-TIME population back-sweep on its first
run — even in a FOCUSED run (a new angle-bracket detector found a long-standing hit two
FULL audits had missed).

### Phase 3 — Stage the packet
Apply the keep-two rule (same as `/improve`): if there are already two or more dated
dirs under `~/.claude/improvements/`, delete all but the most recent one (so after
creating today's there are exactly two). The user is the only deleter — surface the
candidate dirs and ask before removing. The `backlog/` dir is NOT a dated dir and is
NEVER pruned by the keep-two rule.

**Disposition rule (confidence gate):** for each finding, score confidence per the
project's "Score Confidence" guidance (CLAUDE.md). If **> 90%** (strictly greater —
91% and up), stage as a `proposals/NN-[audit]-<slug>.md` file. If **≤ 90%**, write to
`backlog/NN-<slug>.md` instead — same finding, but flagged for re-evaluation on the
next audit run. Keep numbering stable across the two directories (a finding that
started as proposal 04 stays numbered 04 if it moves to backlog) so audit-run history
is traceable.

**Walk the existing backlog before staging new items.** For each `backlog/NN-*.md`,
re-score with current data:
- Confidence rose to > 90% → move to today's `proposals/` (same number), update the
  re-evaluation date.
- Confidence still ≤ 90% but applicable → bump the `last-re-evaluated:` date and the
  current-confidence line; leave in backlog.
- No longer applicable (the target was rewritten, the rule changed, the user closed
  it) → move to `backlog/closed/` with a one-line close reason. Don't delete.

**Backlog file format** (lighter than the proposal format — no mechanical diff yet,
because by definition the finding isn't ready to mechanically apply):

```
# Backlog NN: <title>

**Target:** <path>
**Type:** edit-skill | edit-orchestrator | edit-memory | edit-CLAUDE.md | design-question
**Derived from:** <which Check, which audit run>
**Original confidence:** X% — <why not >90% on first sighting>
**Last re-evaluated:** YYYY-MM-DD
**Current confidence:** X%

## Finding
<terse — what was observed>

## Suggested change (sketch)
<what to do; exact line ranges NOT required yet>

## What would raise confidence
- <signal A — what new data, observation, or user feedback would push this >90%>

## What would lower confidence (or close as won't-do)
- <signal A — what evidence would close this>
```

Create or append-to today's REVIEW.md:

```
# Improvement review — {YYYY-MM-DD}  (or "## Audit-derived findings — {timestamp}" if appending)

**Population audited:** N skills (+ commands/agents/templates only if restored)
**Description budget:** N skills · T total description chars (Δ vs last audit)
**Findings:** P (across 12 checks)  ·  **Proposals staged:** P

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
