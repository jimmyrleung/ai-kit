---
name: close
description: "Distills the current session into a continuation log and optional durable records of decisions, learnings, dead ends, and open work. Use when wrapping up, stopping, preparing for a context reset, or pausing after work lands. Reconstructing a past tasks-doc run belongs to close-tasks."
---

<!-- intentionally-long: linear end-of-session ritual — 3 phases with 5 persistence sinks documented inline; each section is short and the procedure flows top-to-bottom, so a references/ split would add read latency for no navigation win. -->

# Close — end-of-session ritual

You are closing out a working session. Goal: leave breadcrumbs so the next session (possibly
days later, possibly after a context reset) doesn't rebuild context from vibes — AND, when a
recorder is configured, leave structured evidence of how the workflow performed. Resolve recorder,
store, schema, and execution identity from [the feedback contract](references/shared/feedback.md)
before persisting anything. Recording is optional; an undeclared private store is never assumed.

**This is a curated briefing, not a transcript.** Distill. Do not dump the conversation. Do not
carry forward your own stale intermediate reasoning — only conclusions, decisions, and what's next.

Three phases. Move through them in order; ask before the git step.

---

## Phase 1 — Retrospective (scan, then categorize)

**Step 0 — resolve this session boundary.** Prefer the host's opaque session ID. Otherwise generate
an opaque `execution_id` and retain it in this live session; include a host-supplied session start
time when available. Never use “top entry” or “same date” alone as identity.

Inspect the top `SESSION_LOG.md` entry only after resolving that identity:

- A completed receipt with the **same `execution_id`** belongs to this session. Harvest only work
  after that receipt. With no delta, report the prior counts, offer any remaining commit step, and
  stop. With a delta, extend the same entry and later append a superseding receipt.
- A `started` marker with the **same `execution_id`** is an interrupted current close. Resume it
  idempotently, checking stable record IDs before every append.
- A receipt/marker with a different or unprovable identity belongs to another boundary. Preserve it
  and prepend a new entry for this close. A new day always gets a newly dated entry, even if the
  prior entry is still on top.

Before the first persistence write, add a `started` marker with a unique `close_id` to the selected
entry. This marker is not a completion receipt:

```
<!-- close-state: v2 · close_id:<id> · execution_id:<id> · started_at:<ISO-8601> · state:started -->
```

Scan *this session's* context — only what's actually relevant; ignore noise — for:

- **Decisions made** — architectural / design / scoping choices, **with the `why`**. Filter each
  through the ADR gate: log it only if **(a)** it'd be hard/costly to reverse, **or (b)** it'd be
  surprising to a future reader without the context ("why is it done *this* way?"), **or (c)** it
  came from a genuine trade-off with a rejected alternative. If none of those hold, it's not worth
  recording — drop it.
- **Unreviewed decision records** — if a configured decision store or repository decision dir
  exists, scan it for lifecycle metadata whose review state is not `owned` or whose rationale or
  consequences remain assistant-drafted. Also recognize legacy `status: ai-drafted · UNREVIEWED`
  flags. For each, offer to review now: the human owns the **Rationale** (rewrites or confirms it),
  then set review state to `owned` only after every drafted field is confirmed or rewritten.
  **Staleness escalation:** a record still unreviewed after ~3 completed close receipts since
  `created_at` (or about a month by that timestamp) gets called out by name with its age, not
  re-listed neutrally:
  a capture→own pipeline where nothing ever gets owned is just a drafts folder. Offer the fork
  explicitly — own it now (2 minutes, the rationale is going stale), or consciously demote it
  (delete, or mark `status: parked` with a one-line why). Never let the backlog scroll by silently.
  If a legacy record has no valid creation date, report age `unknown`; do not infer it from file
  metadata. Never auto-own a draft. Conversely,
  if a load-bearing session decision deserves a standalone record it doesn't yet have, offer to capture
  it via the `record-decision` skill.
- **Learnings / surprises / inefficiencies** — gotchas discovered; "this cost me 20 min because X";
  a tool/pattern that worked unexpectedly well or badly.
- **Dead ends — what did NOT work** — approaches tried and abandoned, so they're not re-attempted.
  (This section is high-value; don't skip it.)
- **Open tasks / next step** — what's unfinished and the *concrete* next action. Pull from the
  active task list if one exists.
- **References** — external URLs, tickets, dashboards, doc links mentioned this session.
- **Files touched** — run `git status --short` and `git diff --stat HEAD` (read-only; safe).

Then **categorize** each item into exactly one of:
- **(a) → auto-memory** — durable AND user-scoped or cross-repo: a confirmed user preference, a
  cross-project convention, a constraint/deadline, an external reference you'll want again from any
  repo. *Certain* stuff that doesn't belong to one codebase.
- **(b) → observations** — evidence of how a skill/workflow performed (friction, a missing capability,
  a workflow step that drifted). *Ambiguous* stuff that needs batch review later, not a snap memory write.
- **(c) → repo memory** — durable AND repo-scoped: a standard, policy, process, architectural pattern,
  where-to-find-X, how-to-do-Y, or a hard-won fact about *this* codebase that any agent (or teammate)
  should know next session. Gate it twice: **(1)** would it change what an agent *does* in a future
  session in this repo? **(2)** is it non-derivable from the code / git history / existing docs?
  Fail either → it's (b) or (e). One home per fact: repo-scoped never also goes to auto-memory.
  Note each (c) item's *shape* — fact/constraint vs re-runnable procedure — 2c routes them differently.
- **(d) → SESSION_LOG** — continuation state only: the concrete next step, blockers, dead ends,
  artifact links. State, not knowledge — if it would still be true in a month, it's (a) or (c).
- **(e) → just say it in chat** — one-off, not worth persisting anywhere.

**IMPORTANT**: If nothing falls into (a), (b) or (c), that's fine — say so and move on. Don't manufacture entries.

---

## Phase 2 — Persist

### 2a — User/cross-repo memory (the certain stuff)

For each (a) item, use the configured memory store and its declared profile. Apply the common
envelope and scope rules in the feedback contract, check for an existing record before creating
one, and update its index when the profile has one. The preferred `~/.agents` profile maps memory
through `~/.agents/feedback-store.json`; a legacy store remains usable when explicitly configured.
If no memory recorder is configured, report the candidate in the close summary and continue; do not
invent a path or silently enable storage.

Don't save what the repo, git history, or existing instructions already record, and don't duplicate
repo-scoped facts here; those are (c). If an existing memory record is in the wrong scope, offer a
reviewable migration rather than moving or deleting it automatically.

### 2b — Observations (the seam to the `improve` meta-skill)

When an observation recorder is configured, it owns this composed close execution. Nested skills'
candidates are inputs; do not write them again if their stable IDs/evidence are already present.
Write to the configured observation store. Under the preferred `~/.agents` profile, append to
`~/.agents/observations/{YYYY-MM-DD}-{short-slug}.md` (one file per session).

Use the feedback contract's common envelope and this compatible Markdown form per observation:

```
### Observation N: <short descriptive title>

- **schema_version:** 1
- **record_id:** <stable unique observation id>
- **recorded_at:** <ISO-8601 timestamp with offset>
- **record_kind:** observation
- **execution_id:** <this session's opaque id>
- **producer:** close
- **recorder:** close
- **project:** <repo name, e.g. studying / system_design_vault / <work repo>>
- **skill_or_workflow:** <e.g. analyze-work / implement-task / compile-kb / (none — ad-hoc)>
- **phase_area:** <which part, if applicable>
- **outcome:** success | mostly | partial | failed
- **evidence_kind:** lived
- **source_record_ids:** <derived source IDs, or none for lived session evidence>
- **evidence_identity:** <source record/content identity, or `session context` for lived evidence>
- **validation:** passed
- **friction_observed:** <free-text> — tag: <wrong_approach | buggy_code | misunderstood_request | scope_creep | read_skipped | rm_violation | line_budget_overrun | async_context_loss | sdk_version_drift | doc_drift | ...>
- **would_have_helped:** <what missing capability / step / rule would have prevented this>
- **improvement_suggestion:** <optional — a concrete proposed change; name the skill section if you can>
- **principle:** <the generalizable takeaway — why it matters beyond this one instance>
```

Number observations within the file (`### Observation 1`, `### Observation 2`, …). Keep stable
record IDs across copies. Keep it terse but specific enough to understand weeks later without this
conversation. Do **not** log one-off corrections that don't generalize — those are (e).

Use the public baseline tags in the feedback contract plus any explicit extension in the configured
store. This keeps fresh-user recording independent of a private taxonomy.

**Tag gate (read-only, before the close receipt).** Run
`node <close-skill-dir>/scripts/check-observation-tags.mjs <tag-contract> <new-observation-file>...`
on this close's observation files, where `<tag-contract>` is the configured store's tag document or
`references/shared/feedback.md` relative to this skill folder. The checker reads the canonical Tags section; every
observation must carry exactly one listed tag. Resolve errors from the evidence, then rerun;
do not create a receipt claiming completion while the check fails. This gate validates tag
shape only: assess friction from the narrative even when the final outcome was successful.
If this close produced zero observations, verify that the intended observation inventory is
empty and record `observations: 0`; do not create a placeholder observation or invoke the CLI
without an observation file. Other enabled recording checks still apply.

If recording is disabled, skip the write and tag check and report `observations: disabled`. If it is
enabled but the store or validation is unavailable, record that failure and do not issue a
completion receipt until the check passes or the owner explicitly disables that recording
requirement. Record any such configuration change; acceptance alone cannot turn failure into PASS.


### 2c — Repo memory (the repo-scoped durable layer)

For each (c) item, write it into the repo's rules directory and index it from the repo's root
agent-instructions file. Conventions:

- **Location:** `docs/rules/<topic>.md` at the git root, one topical file per concern
  (e.g. `testing.md`, `deploy.md`, `architecture.md`, `where-things-live.md`) — unless the repo
  already has an established rules/conventions directory; the existing convention wins.
- **Per-rule format** inside a topic file — statement first, then grounding:

  ```
  ## <short rule title>

  <the rule / fact / how-to — imperative, terse>

  **Why:** <the reason it exists — without this, rules get "cleaned up" by people who don't know better>
  *(added YYYY-MM-DD — <one-clause provenance: the session/incident/decision it came from>)*
  ```

- **Update-in-place discipline:** before writing, read the topic file (create if missing) and check
  whether an existing rule already covers it — refine that rule and refresh its date rather than
  appending a near-duplicate. Delete rules the session proved wrong; never leave both versions.
- **Index, don't inline:** the root `AGENTS.md` (or the repository's root instruction file if it
  uses another name; create `AGENTS.md` if neither exists) gets a pointer index — one line per
  topic file, never rule bodies:

  ```
  ## Repo memory
  <!-- rules-index:begin -->
  - [testing](docs/rules/testing.md) — <one-line hook: when to open this file>
  <!-- rules-index:end -->
  ```

  **Hard cap: ~12 index lines.** At the cap, merge topic files before adding new ones. The index is
  what loads every session; the bodies are read on demand — that asymmetry is the whole design.
- **Procedural how-tos — rule vs repo-local skill:** when a (c) item is a multi-step, clearly
  re-runnable procedure (not a fact/constraint), offer a choice — never auto-mint, ≤2 offers per close:
  1. **Mint a repo-local skill now** — close time is when the procedure's details are freshest
     in context. Author via the `write-skills` skill's **portable profile** (Codex-safe
     frontmatter, tool-neutral body, dual-write to `.claude/skills/<name>/` +
     `.agents/skills/<name>/` as one never-drift unit — see that skill for the exact constraints).
  2. **Capture as a rule** (the default when unsure, or the procedure may be one-off): write the
     rule entry and tag it `<!-- skill-candidate -->`.
  Either way, log a paired (b) observation. Ladder: tagged rule → repo-local skill (offer-gated,
  minted here) → global ai-kit skill (the `improve` skill mints on recurrence in a 2nd repo — a minted
  repo-local skill IS that evidence).
- **Decision-shaped items:** a real *decision* (trade-off, rejected alternative) routes to the
  `record-decision` skill / the ADR dir; the rules file carries only the resulting rule + ADR link.
- **Public-repo hygiene:** in a public repo, rule bodies are world-readable — `~/` not user paths,
  no client codenames, no internal URLs.

### 2d — SESSION_LOG.md (the continuation handoff)

Find the git root (`git rev-parse --show-toplevel`); fall back to `~/SESSION_LOG.md` if not in a
repo. Use the entry selected by Phase 1's execution-boundary check: extend or resume that entry
when its identity matches, otherwise **prepend** a new entry (newest-first). Never create another
entry merely because this persistence phase runs. This entry is deliberately thin — its only
job is letting a fresh session resume; `git log` covers what got done, and durable knowledge has
already gone to 2a/2c:

```
## [YYYY-MM-DD] — <title>

**Summary:** 1 sentence — what this session was and where it landed.
**Next:** <the concrete next action — "start here">
**Blockers:** <unresolved things needing a decision / external input — or "none">
**Didn't work:** <abandoned approaches, so they're not re-attempted — or "—">
**Artifacts:** <links to the main doc(s) / PR / key commits — the things a fresh session opens first>
```

If `SESSION_LOG.md` is getting long (~30+ entries / ~1500+ lines), move the *oldest* half to
`SESSION_LOG_ARCHIVE.md` at the same location (a big file degrades agent processing — same reason
the handoff pattern archives completed items).

### 2e — Close receipt (the idempotency marker)

After all enabled records validate and persist, append one machine-readable receipt as the last
line of the selected SESSION_LOG entry:

```
<!-- close-receipt: v2 · close_id:<id> · execution_id:<id> · completed_at:<ISO-8601> · supersedes:<id-or-none> · memory:N · rules:N · skills:N · observations:N|disabled -->
```

Keep the earlier receipt when extending the same session; the new receipt names it in `supersedes`.
Remove or mark complete only the matching `started` marker. The receipt carries no commit hash: its
boundary is the execution identity, and git history remains supporting context. Never write this
receipt while an enabled observation/tag gate is failed or unavailable.

---

## Phase 3 — Housekeeping & close

1. **Show the diff** — `git status --short` and `git diff --stat HEAD` (already run in Phase 1; re-show
   if it's scrolled away). Generate an English imperative commit message (Conventional-Commits style,
   e.g. `feat: add close skill`, `docs: session log + memory update`).
2. **Ask before committing.** Present the message; on approval run `git add <files>` + `git commit`
   (never `reset` / `clean` / `checkout --` / force-push — those are blocked by the safety hook anyway).
   If the user declines, leave the working tree as-is.
3. **Cross-machine sync routing.** For each git working tree touched, propose a commit +
   push per repo, routed by content kind:
   - `~/.agents/.git/` (provider-neutral maintenance home, private) — for feedback-store edits to
     `observations/`, `improvements/`, `memory/`, `ownership/`, `learning/`, and their manifest or READMEs.
   - the active provider's private configuration repository, when one exists — for that provider's
     instruction files, hooks, statusline, or settings. Do not route those provider-specific files
     into `~/.agents` merely because the feedback store lives there.
   - the ai-kit repository root's `.git/` (public, resolved from the current workspace) — for edits to: `skills/`, `commands/`, `agents/`,
     `templates/`, `docs/`. **Run the secret-scan before pushing ai-kit (its pre-commit hook does this
     automatically; --no-verify is the bypass and should be used sparingly).**
   One commit per touched repo. **Ask before each commit and before each push.** Never
   auto-push. If either repo has unmerged paths from a prior pull, resolve them first.
4. **Print the close summary** — a one-liner: `memory: N · repo rules: N · repo skills: N ·
   observations: N · SESSION_LOG: updated · commit: <hash or "skipped">`.
   (Human-facing echo of the 2e receipt — the durable copy lives in SESSION_LOG.)
5. **Print a session-rename suggestion** — `[YYYY-MM-DD] <short title>` — for copy-pasting as the
   session name.

---

## Notes

- **Observations ≠ memory** — see the public feedback contract and any configured store profile. Memory = distilled durable
  rules (few, terse, indexed); observations = raw dated per-session evidence (many, tagged). `close`
  triages: certain → memory now; ambiguous performance evidence → observations for the periodic
  `improve` review. A pipeline, not a duplicate.
- **Routing in one line:** *scope* picks the layer — user/cross-repo → auto-memory (a); repo-scoped
  knowledge → repo rules, or a repo-local skill pair for re-runnable procedures (c); session state →
  SESSION_LOG (d); performance evidence → observations (b). One home per fact.
- **Repo memory staleness:** rules rot as code changes. The per-rule date + provenance line lets a
  future audit find stale entries; when a session touches an area whose rule no longer holds, fixing
  the rule file is part of that session's (c) work — same discipline as spec-and-doc updates.
- **The `close` skill vs the `close-tasks` skill.** `close` distills *this session's* live context.
  For a tasks-doc run that spanned multiple sessions or ran headless under a loop runner, use
  **`close-tasks`** —
  artifact-aggregation (completion notes / `_qa.md` / verified runner state / `git log`, idempotent
  via a content-bound harvest receipt). Don't stack both on the same execution window; the shared
  recorder/evidence IDs are the final duplicate guard.
- **This skill is read-only on git history** — reads (`status`, `diff`, `log`, `rev-parse`), at most `add` + `commit`; never rewrites history.
- **Project-agnostic.** Works for the study pipeline too — at the end of a study session, log "topic X
  notes done, flashcards generated, next: topic Y" and observe the study commands' friction.
- **Don't manufacture entries.** A short session with no durable learnings should produce a thin
  SESSION_LOG entry and zero memory/rules/skills/observations — that's correct.
