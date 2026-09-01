---
name: improve
description: Periodic self-improvement review. Reads the accumulated ~/.claude/observations/*.md (written by the close skill), finds friction patterns, audits skill/workflow fitness, and produces a STAGED review packet under ~/.claude/improvements/{date}/ — proposed edits to skills, MEMORY.md, and the active harness's loaded private instruction file, each with the exact diff and the observation it came from. NEVER edits a live file without per-item approval. Run weekly (via a scheduled task), when ~/.claude/improvements/last-review.txt is stale, or on demand.
---

<!-- intentionally-long: 5-phase distiller with concrete templates for REVIEW.md, proposals/, MARK.md and procedural rules per phase. Splitting to references/ would fragment one logical procedure and add load latency for every phase. Tier 2.1 spec records the body as a documented design choice. -->

# Improve — observation reviewer (suggestion mode, NOT auto-mutator)

You are running the periodic self-improvement review. You read the evidence the `close` skill has
been logging, you find what it's telling you, and you produce a **review packet the user approves
or rejects**. You do NOT edit live skills, MEMORY.md, or the active harness's loaded private instruction
file directly — you
stage everything and present it. The user is the reviewer; that's deliberate (their value-add is
the judgement on the diff, not having it automated away).

**You are a distiller, not a churner.** A good run might produce 3 sharp proposals, or zero ("nothing
actionable accumulated — here's the fitness table, go enjoy your Friday"). Do NOT manufacture proposals
to look productive. The number of changes applied is NOT a success metric — it measures churn.

## Inputs you read

- **Primary:** every `~/.claude/observations/*.md` whose observations aren't already marked
  ACTIONED/DECLINED — i.e. since the last review. (Window: from the date in
  `~/.claude/improvements/last-review.txt`; if missing, last 14 days.)
- **Always:** `~/.claude/observations/README.md` (the canonical tag list); the skill inventory —
  the current repository root's `skills/**/SKILL.md` (and any deployed link under
  `~/.claude/skills/`; commands/agents/templates retired to archive/v1, 2026-08-06); `MEMORY.md`
  + the auto-memory topic files; the active harness's loaded private instruction file.
- **Convention targets:** resolve repo-scoped conventions from the applicable `AGENTS.md` cascade in
  the current workspace; resolve user-level conventions from the active harness's loaded private
  instruction file. If mirrored private files can diverge, stage one proposal per target and require
  user approval; never treat one target as universal.
- **On request (a "deep" review):** the period's `git log --oneline` in each repo named in the
  observations, and selected `~/.claude/projects/<dir>/<session-id>.jsonl` transcripts — to backfill
  observations the close skill missed, or to verify a pattern. (Inspection-only; safe.) Skip this for a
  routine weekly run unless something looks off.

## Outputs you write

- **The staged packet:** `~/.claude/improvements/{YYYY-MM-DD}/` — `REVIEW.md`, `proposals/NN-<slug>.md`,
  `MARK.md` (see format below).
- **`~/.claude/improvements/last-review.txt`** — today's date.
- **Only on the user's explicit, per-item approval:** the actual target files. And only then — you
  apply exactly what's in that proposal file, nothing more.
- **After the user has reviewed (accepted or not):** under each consumed `### Observation N` heading
  in its source file, append one line: `> reviewed YYYY-MM-DD (improve): ACTIONED → <target> | DECLINED | DEFERRED`.
  Do NOT rewrite the observation itself.

## Procedure

### Phase 1 — Gather & pattern-mine

0. **Check predictions first.** Inspect the previous packet's applied proposals' `**Prediction:**`
   lines (and any still-open predictions from earlier packets). Judge each against this window's
   observations: met / missed / no evidence yet. A missed prediction stages a revert-or-revise
   proposal before anything new is mined — an applied change that didn't deliver must not
   silently persist. Record the verdicts in REVIEW.md's "Predictions from last cycle".
1. Resolve the window (from `last-review.txt`). Collect the un-reviewed observations across all the
   `~/.claude/observations/*.md` files in scope. If there are none → say so, print the fitness table
   (Phase 2), update `last-review.txt`, stop. Don't fabricate work.
   For a dense window (>~50 in-scope observation files), do NOT grep the corpus into one dump — the
   file-inspection capability truncates long `friction_observed` lines and the tag sits at the end. Fan out N
   extraction subagents over date-range batches, each returning a compact pipe-delimited skeleton
   (`file | obs# | skill | outcome | tags | friction-oneline | improvement-oneline`), and cluster
   from the skeletons.
2. **Confirm the PRIOR review's applied proposals actually shipped** before re-mining their
   patterns: grep the live target files for each applied proposal's fingerprint.
   Recurrence-after-application is a different finding (broader gap / env interaction / failed fix)
   than recurrence of a fix that never landed — it changes what you stage (refine vs revert vs escalate).
3. **Cluster** the observations by: (a) tag (`wrong_approach`, `buggy_code`, `read_skipped`,
   `line_budget_overrun`, `async_context_loss`, `sdk_version_drift`, `doc_drift`, `scope_creep`,
   `rm_violation`, `misunderstood_request`, … — whatever's in the README), (b) `skill_or_workflow`,
   (c) `phase/area`. Note any cluster of ≥3 — that's a pattern worth a proposal. A single occurrence
   is NOT a pattern (don't promote one-offs to permanent rules — that's the rebelytics simplification
   signal; one-offs were already routed to "say it in chat" by `close`).
4. For each cluster, read the relevant skill section and form a hypothesis: is this
   "needs stronger enforcement (a hook / a checklist gate / a structural change), not better wording"?
   Is it "a missing step"? "An assumption that's wrong in practice"? "A capability gap → maybe a new
   skill"? The default fix for a documented-but-ignored rule is rarely "say it louder" — it's "convert
   to a gate / a hook" or "delete it".

### Phase 2 — Audit skill/workflow fitness

Build a small table: for each custom skill, how many times invoked this window
(count from the observations' `skill_or_workflow` field), the outcome mix (success/mostly/partial/failed),
and a flag for: **not invoked in ≥30 days** (deletion candidate — note it, don't propose the delete
yet, ask), **any partial/failed outcomes** (investigate), **trigger-description > 1,536 chars or vague**
(token/discoverability issue — the tvmaly skill-review check), **SKILL.md getting long** (>~150 lines →
suggest splitting reference content out). Exclude bundled/system skills from any deletion/restructure
proposal.

Where the window's observation files carry `run-metrics:` blocks (written by close-tasks), add a
**waste** column to the fitness table — attempts/task, gate-fails, findings/checkpoint — and rank
loop skills by its trend across windows, not only by outcome labels. Respect the k≥2 convention:
one run's metrics describe, they don't compare.

*Note:* the two thin checks above are a friction-driven sample. For a deep structural audit (10
checks, including frontmatter validity, trigger-keyword coverage, cross-skill redundancy, dead
references, and frontmatter-vs-directory mismatch), run the `audit-skills` skill — it's the on-demand
sibling of this pass. When a recent `~/.claude/improvements/{date}/proposals/NN-[audit]-*.md`
already covers a finding here, mark it `"already staged by audit-skills NN-..."` in the
fitness-table flags column and do NOT restage as a separate proposal.

### Phase 3 — Lint (the health-check pass — Karpathy's third operation)

Scan the *curated* layer (skills + `MEMORY.md` + the active harness's loaded private instruction file) for:
- **Contradictions** — two rules that conflict; a `MEMORY.md` entry that contradicts a skill.
- **Stale rules** — a rule superseded by newer evidence in the observations, or by a code/tooling
  change mentioned there.
- **Orphans** — a `MEMORY.md` entry / skill section never relevant in any observation this window
  (and ideally not last window either); a `[[link]]` pointing at a memory file that doesn't exist.
- **Repeatedly-violated rules** — a rule the observations show keeps getting broken → propose
  converting it to structural enforcement (a hook / a gate) or deleting it.
- **Private-instruction bloat** — is the active harness's private instruction file or any project
  instruction file growing past the point
  where adherence degrades? Propose demoting the least-load-bearing rules to `feedback_*.md` memory
  entries (this is the assessment §4 / §6c warning, made operational).
- **MEMORY.md index discipline** — is `MEMORY.md` near 200 lines? Propose consolidations.

### Phase 4 — Stage the packet

Create `~/.claude/improvements/{YYYY-MM-DD}/`. Apply the **keep-two rule**: if there are already two
or more dated dirs, delete all but the most recent one (so after creating today's there are exactly two).

**Generic repo labels in the packet — never employer/client project names.** `REVIEW.md` / `proposals/` /
`MARK.md` are committed to claude-home, whose secret-scan hook blocks employer identifiers (and these
meta-artifacts shouldn't carry them regardless). Refer to a work repo by a generic role label —
`work-LZ-repo`, `payments-repo`, `services-repo` — not its real name; the raw names stay only in the
private observation files (which already hold them). Observation *filenames* you cite in `MARK.md` are
fine as-is (they're pointers, not prose). If a commit is still blocked by pre-existing names in annotated
obs files, `--no-verify` is acceptable for private claude-home (names already in history) — but ask first.

Write `REVIEW.md`:
```
# Improvement review — {YYYY-MM-DD}

**Window:** {start} → {today}  ·  **Observations reviewed:** N (from M session files)

## Patterns found
- [tag/area] — seen K×: <one-line>. → proposal NN.
- ...

## Predictions from last cycle
- <applied proposal NN (YYYY-MM-DD)> — predicted: <line> → **met | missed | no evidence yet** (evidence: <obs/artifact>).
  A missed prediction stages a revert-or-revise proposal in THIS packet before any new mining.

## Skill / workflow fitness
| skill_or_workflow | invocations | outcomes | flags |
|---|---|---|---|
| ... | ... | ... | ... |

## Lint
- <contradiction / stale rule / orphan / repeatedly-violated / bloat finding> → proposal NN (or "noted, no proposal").

## Proposals (each staged in proposals/NN-<slug>.md)
1. NN — <target file> — <one-line what & why> — confidence X%.
2. ...

## Deletion / new-skill candidates (NOT proposed — need your call)
- <skill> not invoked in 34 days — retire?
- recurring pattern "Z" has no skill — create one?

## Observations consumed this run
See MARK.md. Once you've reviewed (accept or not), I'll annotate each in its source file.
```

For each proposal, write `proposals/NN-<slug>.md`:
```
# Proposal NN: <title>

**Target:** <path to the live file that would change>
**Type:** edit-skill | edit-orchestrator | edit-memory | edit-private-instructions | new-skill (candidate only)
**Derived from:** observation(s) <file#N>, <file#N> — quote the relevant `friction_observed` / `improvement_suggestion` / `principle` lines.
**Confidence:** X% — <why not 100%>.
**Prediction:** <one line — the observable outcome in the next N runs/windows if this change works;
falsifiable, checkable from observations or artifacts>.

## Change
<Either a unified diff against the current file, or — for a new file — the full proposed content.
For a SKILL.md edit, show the exact section before/after. Be precise enough that applying it is
mechanical, not interpretive.>

## Rationale
<2-4 sentences. What this fixes, why this shape (gate vs reword vs delete), what alternative was rejected.>
```

Write `MARK.md`: a flat list of `<observation-file>#<N>` for every observation this run consumed.

**Codename self-grep (mandatory, before presenting):** grep the staged `REVIEW.md` + `proposals/`
for the work codenames / employer project names appearing in this window's observation files, and
scrub hits to generic role labels. The claude-home secret-scan hook only blocks an enumerated
name set — codenames outside it pass; this grep is the actual gate, at the authoring moment.

### Phase 5 — Present & (on approval) apply

1. Print `REVIEW.md` to chat (the summary). Don't dump every proposal file — point at the dir.
2. Walk the proposals in PLAIN TEXT, turn-based — per the turn-based-review-no-ask-tool
   memory (2 lived contexts). One message per theme family: 2–4 related proposals, each as
   "NN — <target> — <one-line what & why> — conf X%", ending with "approve / skip / defer,
   per item". The user replies free-form; the atomic unit is the per-item decision, not
   the round-trip — never collapse a family into one yes/no. Do NOT use a structured question tool
   for the walk. Contentious items get their own message. For deletion and new-skill
   candidates, always ask individually — never fold into a family batch, never
   auto-propose as diffs.
3. For each **approved** proposal: apply *exactly* what's in the proposal file to the target. If it's
   a `MEMORY.md` edit, follow the auto-memory conventions (right `type:`, `**Why:**`/`**How to apply:**`,
   `[[links]]`, the one-line `MEMORY.md` pointer). If it's an active private-instruction edit, keep it a
   pointer/rule, not bloat. Where an applied change is cheaply executable (a hook, regex, parser),
   verify it by execution — pipe sample payloads through it — not by re-reading the diff.
4. Annotate each consumed observation in its source file. For >~10 files, use ONE idempotent
   scripted pass appending a consolidated per-file footer (`> reviewed YYYY-MM-DD (improve): …`
   carrying the per-observation dispositions) — bookkeeping costs O(files), not O(observations);
   per-`### Observation` inserts remain fine for small runs. Archive any
   observation file all of whose observations are now resolved → `~/.claude/observations/archive/`.
5. Update `~/.claude/improvements/last-review.txt` to today.
6. **Housekeeping (with cross-machine sync routing):** `git status --short` in any repo you touched;
   generate an imperative commit message (e.g. `chore: apply improve review {date} — N changes`);
   **ask before committing**; on approval `git add` + `git commit` (never `reset`/`clean`/`checkout --`
   — the safety hook blocks those anyway). When applying changes, route each by target:
   - Edits to a skill / command / agent / template land in the current repository root (public). **Run the
     secret-scan before pushing — ai-kit's pre-commit hook does this automatically.**
   - Edits to private instruction files / `observations/` / `improvements/` / `hooks/` land in `~/.claude/`
     (private, claude-home).
   After local commits, propose `git push` for each repo separately. Suggestion-mode — ask before
   each push. Never auto-push.
7. Print a one-line close summary: `proposals: N · applied: N · declined: N · deferred: N · observations consumed: M · commit: <hash or "skipped">`.

## Staleness-fallback behaviour

At the start of a session where this skill is invoked (or if you notice it early in a session):
inspect `~/.claude/improvements/last-review.txt`. If it's >7 days old AND there are un-reviewed
observations AND there's no `~/.claude/improvements/review-decline.txt` newer than 30 days, offer:
"It's been D days since the last improve review and there are N new observations — run it now?"
On decline, write/refresh `review-decline.txt` (suppresses the prompt for 30 days). Never *run*
the review unprompted — only offer.

## Notes

- **You never auto-apply.** Not even trivial changes. The staging dir + per-item approval is the
  whole point — see `~/.claude/improvements/README.md`.
- **One-offs are not patterns.** ≥3 occurrences before something becomes a proposed rule. `close`
  already kept genuine one-offs out of the observations log; if one slipped in, don't promote it.
- **Prefer enforcement over wording.** A rule the observations show keeps getting broken should
  become a hook or a gate or get deleted — not get rewritten in bold.
- **Don't duplicate stores.** A finding that's already a `MEMORY.md` rule, a git fact, or a private
  instruction-layer line doesn't need a new home — propose editing the existing one.
- **Project-agnostic.** Reviews the study pipeline (`study-notes-review` → `assessment` → `insights`
  → `review` → `flashcards`) alongside engineering — the observations log is unified.
- **No changes to git history.** Inspect `log` / `status` / `diff`; at most `add` + `commit` of changes
  you approved. Never rewrites history.
- **This is Component 3 (and, with cross-machine sync, Component 4) of the self-improving triangle —
  see §5 of `ai-patterns-assessment-response.md` and `tier-2-imp-2-1.md`.**
