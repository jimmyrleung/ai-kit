---
name: close
description: "End-of-session ritual. Retrospect on the session (decisions + why, learnings, dead ends, open tasks, references, files touched), persist the durable parts to the right layer — repo-scoped rules/standards/how-tos to the repo's docs/rules/ (indexed from AGENTS.md) or, offer-gated, a repo-local skill pair (.claude/skills/ + .agents/skills/), user/cross-repo facts to auto-memory, skill/workflow-performance evidence to ~/.claude/observations/ — prepend a slim continuation-only SESSION_LOG.md entry at the git root, and propose a commit. Run at the end of a working session, when the user says they're wrapping up, before a context reset, or at a natural pause after a task or PR lands. NOT a context dump: it distills, it doesn't transcribe."
---

<!-- intentionally-long: linear end-of-session ritual — 3 phases with 5 persistence sinks documented inline; each section is short and the procedure flows top-to-bottom, so a references/ split would add read latency for no navigation win. -->

# Close — end-of-session ritual

You are closing out a working session. Goal: leave breadcrumbs so the next session (possibly
days later, possibly after a context reset) doesn't rebuild context from vibes — AND leave
structured evidence of how the workflow performed, so the periodic improvement review has data.

**This is a curated briefing, not a transcript.** Distill. Do not dump the conversation. Do not
carry forward your own stale intermediate reasoning — only conclusions, decisions, and what's next.

Three phases. Move through them in order; ask before the git step.

---

## Phase 1 — Retrospective (scan, then categorize)

**Step 0 — already-closed guard.** Before scanning, read the top entry of the git root's
`SESSION_LOG.md` (if one exists):

- **It carries a `<!-- close-receipt: ... -->` line** → a close already completed. Say so
  ("already closed at <time> — memory:N · rules:N · skills:N · obs:N") and harvest **only the delta**: work
  that happened after the receipt timestamp. If there is no new work, offer the remaining commit
  step (if the tree is dirty) and stop. Do NOT prepend a second SESSION_LOG entry — extend the
  existing one and refresh its receipt line.
- **Top entry is from today but has no receipt** → a prior close was interrupted mid-run. Resume
  idempotently: before appending to today's observations file, check what it already contains;
  2a/2c are update-in-place by design, so re-running them is safe.
- **Neither** → normal close; proceed.

Scan *this session's* context — only what's actually relevant; ignore noise — for:

- **Decisions made** — architectural / design / scoping choices, **with the `why`**. Filter each
  through the ADR gate: log it only if **(a)** it'd be hard/costly to reverse, **or (b)** it'd be
  surprising to a future reader without the context ("why is it done *this* way?"), **or (c)** it
  came from a genuine trade-off with a rejected alternative. If none of those hold, it's not worth
  recording — drop it.
- **Unreviewed decision records** — if a decision dir exists (`docs/decisions/`, `adr/`, or
  `~/.claude/ownership/{topic}/`), scan it for records flagged `status: ai-drafted · UNREVIEWED`
  (captured this session or earlier via the `record-decision` skill). For each, offer to review now: the human
  owns the **Rationale** (rewrites or confirms it), then flip
  the flag to `status: owned`. **Staleness escalation:** a record still UNREVIEWED after ~3 closes
  (or ~a month — judge from its date) gets called out by name with its age, not re-listed neutrally:
  a capture→own pipeline where nothing ever gets owned is just a drafts folder. Offer the fork
  explicitly — own it now (2 minutes, the rationale is going stale), or consciously demote it
  (delete, or mark `status: parked` with a one-line why). Never let the backlog scroll by silently.
  Never auto-own them — an unreviewed AI draft is not an ADR. Conversely,
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

### 2a — Auto-memory (the certain stuff)

For each (a) item, follow the existing auto-memory conventions exactly (you already know them):
write/update a file under `~/.claude/projects/<project>/memory/` with the right `type:`
(`user` / `feedback` / `project` / `reference`), `**Why:**` + `**How to apply:**` lines for
feedback/project, `[[links]]` to related memories, and add/refresh a one-line pointer in `MEMORY.md`.
Check for an existing file that already covers it before creating a new one. Don't save what the
repo / git history / the existing instruction layer already records — and don't save repo-scoped facts here; those
are (c) and go to the repo's own rules layer (2c). If an *existing* auto-memory turns out to be
repo-scoped, offer to migrate it: write it into that repo's `docs/rules/` and slim or delete the
auto-memory copy.

### 2b — Observations (the seam to the `improve` meta-skill)

For each (b) item, append to `~/.claude/observations/{YYYY-MM-DD}-{short-slug}.md`
(create the file if it's the first observation this session; `{short-slug}` = 2–3 kebab words
describing the session, e.g. `close-skill-spec`). Use this format per observation:

```
### Observation N: <short descriptive title>

- **project:** <repo name, e.g. studying / system_design_vault / <work repo>>
- **skill_or_workflow:** <e.g. analyze-work / implement-task / compile-kb / (none — ad-hoc)>
- **phase/area:** <which part, if applicable>
- **outcome:** success | mostly | partial | failed
- **friction_observed:** <free-text> — tag: <wrong_approach | buggy_code | misunderstood_request | scope_creep | read_skipped | rm_violation | line_budget_overrun | async_context_loss | sdk_version_drift | doc_drift | ...>
- **would_have_helped:** <what missing capability / step / rule would have prevented this>
- **improvement_suggestion:** <optional — a concrete proposed change; name the skill section if you can>
- **principle:** <the generalizable takeaway — why it matters beyond this one instance>
```

Number observations within the file (`### Observation 1`, `### Observation 2`, …). One file per
session means no collisions. Keep it terse but specific enough to understand weeks later without
this conversation. Do **not** log one-off corrections that don't generalize — those are (e).

Tags should align with the `insights` taxonomy so the pile stays comparable to that retrospective.
See `~/.claude/observations/README.md` for the running tag list and the observations-vs-memory rationale.

**Tag gate (read-only, before the close receipt).** Run
`node <close-skill-dir>/scripts/check-observation-tags.mjs <observations-README> <new-observation-file>...`
on this close's observation files. The checker reads the canonical Tags section; every
observation must carry exactly one listed tag. Resolve errors from the evidence, then rerun;
do not create a receipt claiming completion while the check fails. This gate validates tag
shape only: assess friction from the narrative even when the final outcome was successful.


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
repo. **Prepend** a new entry at the top (newest-first). This entry is deliberately thin — its only
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

Append one machine-readable line as the last line of the SESSION_LOG entry you just prepended:

```
<!-- close-receipt: YYYY-MM-DD HH:mm · memory:N · rules:N · skills:N · obs:N -->
```

Written here — after all persistence, *before* the Phase 3 commit — so it rides inside the commit.
This line is what Phase 1's step-0 guard reads: receipt present = that close completed. It carries
no commit hash on purpose (all counters are known pre-commit; the commit itself is visible in
`git log`). Mirrors the `close-tasks` harvest-marker pattern.

---

## Phase 3 — Housekeeping & close

1. **Show the diff** — `git status --short` and `git diff --stat HEAD` (already run in Phase 1; re-show
   if it's scrolled away). Generate an English imperative commit message (Conventional-Commits style,
   e.g. `feat: add close skill`, `docs: session log + memory update`).
2. **Ask before committing.** Present the message; on approval run `git add <files>` + `git commit`
   (never `reset` / `clean` / `checkout --` / force-push — those are blocked by the safety hook anyway).
   If the user declines, leave the working tree as-is.
3. **Cross-machine sync routing.** If either of these git working trees exists, propose a commit +
   push per repo, routed by content kind:
   - `~/.claude/.git/` (claude-home, private) — for edits to: private instruction files, `observations/`,
     `improvements/`, `hooks/`, `statusline-command.sh`, `settings.example.json`.
   - the ai-kit repository root's `.git/` (public, resolved from the current workspace) — for edits to: `skills/`, `commands/`, `agents/`,
     `templates/`, `docs/`. **Run the secret-scan before pushing ai-kit (its pre-commit hook does this
     automatically; --no-verify is the bypass and should be used sparingly).**
   One commit per repo when each has content. **Ask before each commit and before each push.** Never
   auto-push. If either repo has unmerged paths from a prior pull, resolve them first.
4. **Print the close summary** — a one-liner: `memory: N · repo rules: N · repo skills: N ·
   observations: N · SESSION_LOG: updated · commit: <hash or "skipped">`.
   (Human-facing echo of the 2e receipt — the durable copy lives in SESSION_LOG.)
5. **Print a session-rename suggestion** — `[YYYY-MM-DD] <short title>` — for copy-pasting as the
   session name.

---

## Notes

- **Observations ≠ memory** — see `~/.claude/observations/README.md`. Memory = distilled durable
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
  artifact-aggregation (completion notes / `_qa.md` / `.cc-loop/state.json` / `git log`, idempotent
  via a harvest marker). Don't stack both on the same window — pick one per run.
- **This skill is read-only on git history** — reads (`status`, `diff`, `log`, `rev-parse`), at most `add` + `commit`; never rewrites history.
- **Project-agnostic.** Works for the study pipeline too — at the end of a study session, log "topic X
  notes done, flashcards generated, next: topic Y" and observe the study commands' friction.
- **Don't manufacture entries.** A short session with no durable learnings should produce a thin
  SESSION_LOG entry and zero memory/rules/skills/observations — that's correct.
