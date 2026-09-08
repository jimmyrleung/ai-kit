---
name: improve
description: "Reviews recorded agent/workflow friction and unresolved improvement proposals to find supported patterns and stage changes for owner review. Use for a periodic self-improvement review, recurring workflow problems, or a stale review watermark. Structural skill-population lint belongs to audit-skills."
---

<!-- intentionally-long: 5-phase distiller with concrete templates for REVIEW.md, proposals/, MARK.md and procedural rules per phase. Splitting to references/ would fragment one logical procedure and add load latency for every phase. Tier 2.1 spec records the body as a documented design choice. -->

# Improve — observation reviewer (suggestion mode, NOT auto-mutator)

You are running the periodic self-improvement review. You read the evidence the `close` skill has
been logging, you find what it's telling you, and you produce a **review packet the user approves
or rejects**. You do NOT edit live skills, MEMORY.md, or the active harness's loaded private instruction
file directly — you
stage everything and present it. The user is the reviewer; that's deliberate (their value-add is
the judgement on the diff, not having it automated away).

Resolve recorder, store, schema, discovery watermark, and unresolved queue from
[the feedback contract](references/shared/feedback.md). The established `~/.claude` layout is a
supported profile when configured, not a prerequisite. If no compatible store is configured, report
that review input is unavailable and stop without inventing or migrating data.

**You are a distiller, not a churner.** A good run might produce 3 sharp proposals, or zero ("nothing
actionable accumulated — here's the fitness table, go enjoy your Friday"). Do NOT manufacture proposals
to look productive. The number of changes applied is NOT a success metric — it measures churn.

## Inputs you read

- **New discovery:** configured observation records after the discovery watermark (or the store's
  bounded bootstrap window when none exists). The watermark records scanning only, never resolution.
- **Always:** every `open`/`deferred` improvement item and every open/no-evidence prediction in the
  configured queue, regardless of source date; the public feedback contract and store profile; the
  current repository's canonical skill inventory; configured memory records; and applicable
  repository/user instructions.
- **Authoring/audit policy:** read [the maintained skill policy](references/shared/skill-policy.md).
  Use its shipping checker for executable schema rules and its guidance for catalog/body review;
  do not copy field limits, check counts, or local parser history into this skill.
- **Convention targets:** resolve repo-scoped conventions from the applicable `AGENTS.md` cascade in
  the current workspace; resolve user-level conventions from the active harness's loaded private
  instruction file. If mirrored private files can diverge, stage one proposal per target and require
  user approval; never treat one target as universal.
- **On request (a "deep" review):** the period's `git log --oneline` in each repo named in the
  observations, and selected configured host transcripts — to backfill observations the close skill
  missed, or to verify a pattern. (Inspection-only; safe.) Skip this for a routine weekly run unless
  something looks off.

## Outputs you write

- **The staged packet:** the configured improvement store's dated packet — `REVIEW.md`,
  `proposals/NN-<slug>.md`, `MARK.md` (see format below).
- **The discovery watermark and unresolved queue:** append/update their separate records only after
  the packet and source dispositions are durable.
- **Only on the user's explicit, per-item approval:** the actual target files. And only then — you
  apply exactly what's in that proposal file, nothing more.
- **After the user has reviewed (accepted or not):** append a disposition event to the queue and,
  when supported, a compatible source annotation. Do not rewrite the observation itself. A deferred
  item stays open and reachable.

## Procedure

### Phase 1 — Gather & pattern-mine

0. **Check predictions first.** Resolve every open prediction from the queue to its packet; do not
   limit this to the latest dated directory. Judge each against newly discovered observations and
   other named evidence: met / missed / no evidence yet. A missed prediction stages a revert-or-revise
   proposal before anything new is mined — an applied change that didn't deliver must not
   silently persist. Record the verdicts in REVIEW.md's "Predictions from last cycle".
1. Resolve new discovery from the watermark and collect all unreviewed observations in scope.
   Separately load every open/deferred queue item, including sources older than the watermark. If
   there are no new observations, continue with open items, predictions, and the fitness table; if
   all are empty, emit a no-op packet/result and advance only the discovery watermark. Don't
   fabricate work.
   For a dense window (>~50 in-scope observation files), do NOT grep the corpus into one dump — the
   file-inspection capability truncates long `friction_observed` lines and the tag sits at the end. Fan out N
   extraction subagents over date-range batches, each returning a compact pipe-delimited skeleton
   (`file | obs# | skill | outcome | tags | friction-oneline | improvement-oneline`), and cluster
   from the skeletons.
2. **Confirm applied proposals actually shipped** before re-mining their patterns: inspect the live
   target for every queue item whose application or prediction is still open.
   Recurrence-after-application is a different finding (broader gap / env interaction / failed fix)
   than recurrence of a fix that never landed — it changes what you stage (refine vs revert vs escalate).
3. **Cluster** the observations by: (a) tag (`wrong_approach`, `buggy_code`, `read_skipped`,
   `line_budget_overrun`, `async_context_loss`, `sdk_version_drift`, `doc_drift`, `scope_creep`,
   `rm_violation`, `misunderstood_request`, … — whatever's in the README), (b) `skill_or_workflow`,
   (c) `phase/area`. Note any cluster of ≥3 — that's a pattern worth a proposal. A single occurrence
   is NOT a pattern (don't promote one-offs to permanent rules — that's the rebelytics simplification
   signal; one-offs were already routed to "say it in chat" by `close`).
   Deduplicate replicas by `record_id`; for legacy records use the feedback contract's content-hash
   fallback. Preserve distinct observations from one execution as observations, never invocations.
4. For each cluster, read the relevant skill section and form a hypothesis: is this
   "needs stronger enforcement (a hook / a checklist gate / a structural change), not better wording"?
   Is it "a missing step"? "An assumption that's wrong in practice"? "A capability gap → maybe a new
   skill"? The default fix for a documented-but-ignored rule is rarely "say it louder" — it's "convert
   to a gate / a hook" or "delete it".

### Phase 2 — Audit skill/workflow fitness

Build a small table for each custom skill with **observation count**, observed outcome mix,
**measured invocation count**, invocation-source coverage, and flags. Observation rows are selected
feedback, not usage telemetry. Populate invocation count only from a configured, instrumented
invocation source after deduplicating by `invocation_id`; otherwise write `unavailable`. Never infer
non-use, deletion candidacy, or a failure rate from missing/selective observations. Backup/synced
replicas count once by stable record ID.

Investigate partial/failed observations and other signals named by the maintained skill policy.
Apply that policy's distinction between catalog routing, body quality, and final-tree structural
validation. Treat size/overlap signals as investigation leads, not automatic restructure findings.
Exclude bundled/system skills from deletion/restructure proposals.

Where the window's observation files carry `run-metrics:` blocks (written by close-tasks), add a
**waste** column to the fitness table — attempts/task, gate-fails, findings/checkpoint — and rank
loop skills by its trend across windows, not only by outcome labels. Respect the k≥2 convention:
one run's metrics describe, they don't compare.

For a deep structural audit, run the `audit-skills` skill — it is the on-demand sibling of this
pass and uses the maintained policy/checker contract. When a recent configured improvement packet
already covers a finding here, mark it `"already staged by audit-skills NN-..."` in the
fitness-table flags column and do NOT restage as a separate proposal.

### Phase 3 — Lint (the health-check pass — Karpathy's third operation)

Scan the *curated* layer (skills + `MEMORY.md` + the active harness's loaded private instruction file) for:
- **Contradictions** — two rules that conflict; a `MEMORY.md` entry that contradicts a skill.
- **Stale rules** — a rule superseded by newer evidence in the observations, or by a code/tooling
  change mentioned there.
- **Orphans** — broken memory links, unreachable supporting resources, or inventory members absent
  from the maintained catalog. Missing observations do not establish that a rule/skill is unused.
- **Repeatedly-violated rules** — a rule the observations show keeps getting broken → propose
  converting it to structural enforcement (a hook / a gate) or deleting it.
- **Private-instruction bloat** — is the active harness's private instruction file or any project
  instruction file growing past the point
  where adherence degrades? Propose demoting the least-load-bearing rules to `feedback_*.md` memory
  entries (this is the assessment §4 / §6c warning, made operational).
- **Memory index discipline** — apply the configured store profile and maintained policy; treat size
  as a prompt to inspect usefulness, not sufficient evidence for consolidation.

### Phase 4 — Stage the packet

Create the dated packet in the configured improvement store. Assign stable proposal IDs and update
the unresolved queue by append-only disposition events. Before assigning a proposal, match its
source observation IDs plus target/finding identity against open/deferred items so a repeated review
does not duplicate it.

Retention is state-aware: every open/deferred item and open/no-evidence prediction must retain a
working packet/evidence locator. Resolved packets may remain in place or be moved to a configured
archive with locators updated. Never discard a packet merely to enforce a dated-window count.

**Generic repo labels in the packet — never employer/client project names.** These meta-artifacts
must remain safe for their configured store. Under the established claude-home profile, a secret-scan
hook also checks them. Refer to a work repo by a generic role label —
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
| skill_or_workflow | observations | observed outcomes | measured invocations | invocation coverage | flags |
|---|---:|---|---:|---|---|
| ... | ... | ... | ... |

## Lint
- <contradiction / stale rule / orphan / repeatedly-violated / bloat finding> → proposal NN (or "noted, no proposal").

## Proposals (each staged in proposals/NN-<slug>.md)
1. NN — <target file> — <one-line what & why> — confidence X%.
2. ...

## Deletion / new-skill candidates (NOT proposed — need your call)
- <skill> has no measured invocations in a fully instrumented coverage window — retire?
- recurring pattern "Z" has no skill — create one?

## Observations consumed this run
See MARK.md. Open/deferred items remain in the unresolved queue after this watermark advances.
```

For each proposal, write `proposals/NN-<slug>.md`:
```
# Proposal NN: <title>

**Target:** <path to the live file that would change>
**Type:** edit-skill | edit-orchestrator | edit-memory | edit-private-instructions | new-skill (candidate only)
**Derived from:** observation record IDs + store locators — quote the relevant `friction_observed` / `improvement_suggestion` / `principle` lines.
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

Write `MARK.md`: a flat list of stable observation IDs plus their store locators for every
observation consumed. For legacy records, include the computed legacy ID and original `<file>#<N>`.

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
3. For each **approved** proposal: apply *exactly* what's in the proposal file to the target. For a
   memory edit, preserve the configured store's native format and attach/update the feedback
   envelope in its compatible representation. If it's an active private-instruction edit, keep it a
   pointer/rule, not bloat. Where an applied change is cheaply executable (a hook, regex, parser),
   verify it by execution — pipe sample payloads through it — not by re-reading the diff.
4. Append one disposition event per reviewed item to the unresolved queue. `DEFERRED` remains open;
   `ACTIONED`/`DECLINED` resolve the proposal but an applied proposal's prediction remains open
   until judged. When the configured profile supports source annotations, add an idempotent footer
   that references stable observation/item IDs. Archive a source file only when all of its items and
   predictions are resolved and the queue locator is updated; preserve historical bytes.
5. Advance the discovery watermark after packet, queue, and source dispositions persist. The
   watermark never substitutes for the unresolved queue.
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
7. Print a one-line close summary: `proposals: N · applied: N · declined: N · deferred/open: N · observations consumed: M · invocation coverage: <measured|unavailable> · commit: <hash or "skipped">`.

## Staleness-fallback behaviour

At the start of a session where this skill is invoked (or if you notice it early in a session):
inspect the configured discovery watermark. If it's >7 days old AND there are unreviewed
observations or open queue items AND the configured decline receipt is not newer than 30 days, offer:
"It's been D days since the last improve review and there are N new observations — run it now?"
On decline, write/refresh the profile's decline receipt (suppresses the prompt for 30 days). Never *run*
the review unprompted — only offer.

## Notes

- **You never auto-apply.** Not even trivial changes. The staged packet + per-item approval is the
  whole point; follow the configured store profile.
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
