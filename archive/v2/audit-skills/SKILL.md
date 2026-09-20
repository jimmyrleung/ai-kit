---
name: audit-skills
description: "Audits the canonical skill population for metadata, trigger coverage, size, redundancy, stale content, and broken references. Use to audit, lint, or check skill quality after authoring, before publishing, or when an audit is overdue. Stages findings for review; observation-driven friction review belongs to improve."
---

<!-- intentionally-long: 12 checks documented inline; splitting to references/ would hurt usability because each check is short, the procedure flows linearly, and progressive disclosure adds latency for no readability win at this size. -->

# Audit Skills — structural quality pass over the canonical skill population

You are running a structural audit of the repository's canonical skills, commands, and agents.
You do NOT edit any live file; you stage proposals under the active improvements store
exactly like the improve skill does. Same approval discipline: the user reviews and approves
one at a time.

Resolve `active-improvements-root`, recorder, and schema through
[the feedback contract](references/shared/feedback.md), relative to this skill folder. A compatible configured store supplies the staging/queue paths;
the preferred `~/.agents` profile is detected through `~/.agents/feedback-store.json`; a legacy
store remains usable when explicitly configured. Without one, run the read-only audit
and return the findings in chat with `persistence: disabled`; ask for a destination only if
persisting the packet is required. Never invent a private root or claim that an enabled but
unavailable recorder passed. Store bootstrap remains an explicitly authorized action.

This is the on-demand structural sibling of improve's evidence-driven fitness review.
Both use the maintained skill policy; this skill runs its 12 checks only when invoked.

## Inputs you read

- `<repo-root>/skills/**/SKILL.md` — all bodies + frontmatter.
- `<repo-root>/commands/*.md`, `<repo-root>/agents/*.md`, `<repo-root>/templates/**/*.md` —
  **retired 2026-08-06 (v2, archive/v1)**: all three dirs are deleted; enumerate as zero
  and skip when absent. Specs for their checks (8, 9, and the command/agent legs of 1/10)
  stay below, dormant, in case those entity types return.
- The most recent dated `REVIEW.md` in the active improvements store if present — for the
  observation-coverage column in the fitness table (not invocation telemetry). Optional input; skip if not present.
- `last-audit.txt` in the active improvements store — timestamp of last audit; missing = never run.

Resolution through provider deployment links is fine — same files.
Exclude bundled/system skills and Anthropic-shipped skills from any proposal.

## Outputs you write

- `<active-improvements-root>/{YYYY-MM-DD}/REVIEW.md` (one section per check; fitness table).
- `<active-improvements-root>/{YYYY-MM-DD}/proposals/NN-[audit]-<slug>.md` — one per
  **high-confidence finding (>90%)**, ready for one-at-a-time apply/skip/defer review.
  Tag filenames with `[audit]` so the improve skill and the human can tell audit-derived
  proposals from friction-derived ones.
- `<active-improvements-root>/backlog/NN-<slug>.md` — one per **lower-confidence finding
  (≤90%)**. **Persistent across audit runs** (NOT under the dated `{date}/` dir).
  Re-evaluated every run — confidence may rise with more data and promote to a proposal,
  or fall and close as won't-do.
- `<active-improvements-root>/last-audit.txt` — today's date + run-summary counts + the
  aggregate description budget (skill count · total description chars) for Check 2's
  growth comparison next run.
- Only on the user's explicit, per-item approval: the actual target files.

If `REVIEW.md` already exists for today (because the improve skill ran earlier), append a
`## Audit-derived findings — {YYYY-MM-DD HH:mm}` section to it instead of overwriting.

## Checks (12 total)

### Check 1 — Frontmatter validity
Run the final-tree commands in [the shared skill policy](references/shared/skill-policy.md).
Resolve bundled references relative to this skill folder.
The shipping checker owns strict YAML, standard fields, reviewed overlays, name bounds,
and inventory membership. Stage exact fixes from its errors; do not copy its schema or
require a private parser workaround. If archived entity types return, use their own
contracts rather than applying the skill profile to them.

### Check 2 — Description size and effective catalog
Use the shared policy's semantic guidance. Measure description characters and the
population by directory enumeration, including supported links. Record aggregate
size and change since the prior run separately from the host's observed catalog.
A growth or length flag prompts inspection and routing trials; it is not evidence of
wrong selection. Propose trimming procedure detail while preserving trigger boundaries.

### Check 3 — Description trigger-keyword coverage
List plausible synonyms a user might invoke this skill with that are NOT in the
description. Bias toward common verbs: `verify` / `check` / `validate` / `audit` /
`review` / `final` / `before publish` / `lint` — pick the ones matching this skill's
domain. Skills missing ≥2 likely synonyms → one proposal showing the description with
synonyms folded inline (preserve the char budget — don't tack on a new sentence).

### Check 4 — Body size and reference boundaries
Measure full-file logical lines (including blanks), whitespace words, and conditional
reference sizes with a cross-platform file API. Use the shared policy: length is an
inspection lead, not an automatic split. Honor documented reasons for keeping a
linear procedure inline, then test whether the proposed organization preserves outcomes.

### Check 5 — Cross-skill redundancy (description-based)
Pairwise compare descriptions. For any two with ≥5 shared trigger phrases in the
first 50 words, inspect whether actual routing boundaries conflict before surfacing: "Skills X and Y overlap on triggers A, B, C —
consider differentiating descriptions, or merging if bodies overlap too." Do NOT
propose a merge diff; surface and let the user decide.

### Check 6 — Cross-skill redundancy (body-based, lightweight)
For each pair in the same family (heuristic: same first segment before `-`), compare
top-level section headers (`##` lines). ≥60% header match → inspection lead; confirm duplicated obligations before a finding. Same
disposition as Check 5: surface, don't propose a merge.

### Check 7 — Dead references in skill, command, and agent bodies
Scan each SKILL.md, command, and agent body for:
- Paths containing `agent-workflows/` (stale post-3.1).
- Paths containing `agent-docs/` (stale post-3.1).
- Paths containing the per-family `{bugfix,feature-addition,greenfield-dev,
  incident-response,refactoring-tech-debt}/` segments (stale post-3.1 flatten).
- File references that don't resolve (templates that no longer exist; cross-skill
  references to skills that have been deleted or renamed).
- provider deployment paths that don't resolve through their managed links.

Each finding: one proposal per file with exact line numbers and the suggested
replacement path.

Expected non-findings (do not flag): the cc-looper worker skills' `templates/*.md`
references resolve against cc-looper's source tree at runtime (its slice-09 techspec
§3.12), not the skill dir — verify existence under
`~/projects/cc-looper/templates/` before flagging. audit-skills' own Check 7 text
mentions the dead-path classes verbatim — self-matches are not findings. Skill-local
`templates/<name>.md` references resolve against the skill's own dir (its
`skills/<name>/templates/`), not the kit root — inspect that directory before flagging.
Path-like strings inside fenced example blocks that illustrate a convention the skill
creates at runtime in *target* repos (e.g. close 2c's `docs/rules/testing.md` index
example) are illustrative, not references — check the enclosing fence and whether the
path is meant to exist in this kit before flagging.

Derive the retired-name sweep list MECHANICALLY from the `archive/` directory listings
(archived skill/command/agent names), never from recall — a hand-enumerated regex omitted
one name and its dead refs survived the audit. When a CONVENTION (not an entity) is
retired, add its descriptive phrases to the sweep list — live-names-only sweeps missed
retired doctrine taught as current in 3 separate runs.

### Check 8 — Entity placement
Check the entity's declared purpose and current schema before proposing a move.
Reviewed skill overlays such as `argument-hint` are valid metadata, not evidence that
an entity belongs in the retired command tree. A move needs a real contract mismatch.

### Check 9 — Coverage: commands without skill bodies
For each `<repo-root>/commands/<X>.md`, check whether it has a corresponding skill OR
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
For each live skill that emits a workflow phase document, verify its output filename
against the skill-centric rows in [the bundled filename contract](references/shared/output-filename-contract.md).
Compare both producers and consumers: flag (a) placeholder tokens or suffixes that
conflict with the matching live row; (b) a consumer's expected phase filename that
conflicts with its producer; and (c) a new workflow phase output with no contract row.
Derive the filename sweep from the current contract rather than a fixed suffix list.
Archived rows are compatibility references for historical artifacts, not current
producer requirements. Input-only legacy filenames and examples are not output drift.
Surface mismatches and propose the exact normalization; do not silently rewrite.

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
Enumerate the input directories that exist (skills always; commands/agents/templates only if
restored — see Inputs). Build a structured inventory:
`{ skills: [...], commands: [...], agents: [...], templates: [...] }` (empty arrays are valid).

Also read `pending-trigger-tests.txt` in the active improvements store if present: any listed skill
gets a trigger-simulation check this run and is removed from the queue on pass.

### Phase 2 — Run all 12 checks
Walk each check across the relevant subset. Collect findings as (check, file) pairs;
group by file for the report. Don't fabricate findings to look productive — zero
findings on a check is a valid result.

A detector added since the last run implies a ONE-TIME population back-sweep on its first
run — even in a FOCUSED run (a new angle-bracket detector found a long-standing hit two
FULL audits had missed).

### Phase 3 — Stage the packet
Apply the retention rules in [the feedback contract](references/shared/feedback.md).
Before moving any dated packet, reconcile it against the unresolved queue. Keep every
packet containing an open/deferred item or an open/no-evidence prediction reachable at
its recorded locator. Resolved packets may remain in place or move to a configured
archive only after queue locators are updated; never discard a packet merely to enforce
a dated-directory count. The persistent backlog is never date-pruned. Any destructive
cleanup remains an explicit owner action.

**Disposition rule (confidence gate):** for each finding, score confidence per the
project's loaded "Score Confidence" guidance. If **> 90%** (strictly greater —
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
**Type:** edit-skill | edit-orchestrator | edit-memory | edit-private-instructions | design-question
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
| skill | body lines | desc chars | last observed outcome / coverage | flags |
|---|---|---|---|---|
| … | | | | |

## Proposals
1. NN-[audit]-<slug> — <target> — <one-line what & why>.
2. …

## Cross-cutting observations
- <patterns, not per-file>
```

Write one `proposals/NN-[audit]-<slug>.md` per finding using the improve skill's proposal
template (Target / Type / Derived from / Confidence / Change / Rationale).

Write `last-audit.txt` with today's date.

### Phase 4 — Present & (on approval) apply
Same procedure as the improve skill's Phase 5:
1. Print REVIEW.md (the summary) to chat. Point at the dir, don't dump proposals.
2. Walk proposals one at a time. Ask before each: "Apply / skip / defer?"
3. For each approved proposal: apply *exactly* what's in it.
4. Route commits by target per Tier 3.1: skill/command/agent/template edits → `ai-kit`;
   private instructions / `observations/` / `improvements/` / `hooks/` → the active maintenance home.
   Run the secret-scan before pushing (the ai-kit pre-commit hook does this).
5. Ask before committing; ask before pushing. Never auto-push.
6. Print a one-line close summary: `findings: P · applied: A · declined: D · deferred: F · commit: <hash or "skipped">`.

## Staleness behaviour
At session start: if `last-audit.txt` is missing OR > 90 days old AND the skill count
has changed by > 3 since the timestamp inside `last-audit.txt`, offer once:
"It's been D days since the last skill audit (N new/changed skills) — run audit-skills now?"
Same offer-don't-run discipline as the improve skill. Never run unprompted.

## Composition with the improve skill

- The improve skill's Phase 2 fitness review uses the maintained skill policy.
  It runs as part of a requested friction review and is suitable for the small
  population subset with relevant observations; unobserved usage remains unknown.
- This skill runs on-demand and on a 90-day floor.
- When both surface the same finding: the improve skill checks for an `[audit]`-tagged
  proposal on the same target in the unresolved queue and all reachable packet locators; if present, it marks its
  own finding "already staged by audit-skills NN-…" and does not restage.

## What this skill does NOT do
- **Task-outcome benchmarking** — the shared evaluation protocol owns this; selective observations in improve do not establish success rates.
- **Private instruction / memory / orchestrator lint** — the improve skill's Phase 3 owns this.
- **New-skill synthesis** (capability gaps) — the improve skill owns this via observation patterns.
- **Auto-fix** — every finding is a proposal the user approves one at a time.
- **Effectiveness benchmarking** — out of scope. See the agent-tuning research note.

This is a structural-quality lint, not a churn engine. A run that produces a clean
report and zero proposals is a good run.
