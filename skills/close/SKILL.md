---
name: close
description: End-of-session ritual. Retrospect on the session (decisions + why, learnings, dead ends, open tasks, references, files touched), persist the durable parts to auto-memory and the skill/workflow-performance evidence to ~/.claude/observations/, prepend a SESSION_LOG.md entry at the git root, and propose a commit. Run at the end of a working session — invoke as /close or when the user says they're wrapping up. NOT a context dump: it distills, it doesn't transcribe.
---

# Close — end-of-session ritual

You are closing out a working session. Goal: leave breadcrumbs so the next session (possibly
days later, possibly after a `/compact` reset) doesn't rebuild context from vibes — AND leave
structured evidence of how the workflow performed, so the periodic improvement review has data.

**This is a curated briefing, not a transcript.** Distill. Do not dump the conversation. Do not
carry forward your own stale intermediate reasoning — only conclusions, decisions, and what's next.

Three phases. Move through them in order; ask before the git step.

---

## Phase 1 — Retrospective (scan, then categorize)

Scan *this session's* context — only what's actually relevant; ignore noise — for:

- **Decisions made** — architectural / design / scoping choices, **with the `why`**. Filter each
  through the ADR gate: log it only if **(a)** it'd be hard/costly to reverse, **or (b)** it'd be
  surprising to a future reader without the context ("why is it done *this* way?"), **or (c)** it
  came from a genuine trade-off with a rejected alternative. If none of those hold, it's not worth
  recording — drop it.
- **Learnings / surprises / inefficiencies** — gotchas discovered; "this cost me 20 min because X";
  a tool/pattern that worked unexpectedly well or badly.
- **Dead ends — what did NOT work** — approaches tried and abandoned, so they're not re-attempted.
  (This section is high-value; don't skip it.)
- **Open tasks / next step** — what's unfinished and the *concrete* next action. Pull from the
  TodoWrite list if one is active.
- **References** — external URLs, tickets, dashboards, doc links mentioned this session.
- **Files touched** — run `git status --short` and `git diff --stat HEAD` (read-only; safe).

Then **categorize** each item into exactly one of:
- **(a) → auto-memory** — generally-applicable and durable: a confirmed user preference, a clear new
  convention, a project constraint/deadline, an external reference you'll want again. *Certain* stuff.
- **(b) → observations** — evidence of how a skill/workflow performed (friction, a missing capability,
  a workflow step that drifted). *Ambiguous* stuff that needs batch review later, not a snap memory write.
- **(c) → SESSION_LOG** — this-session narrative: what got done, the load-bearing decisions+why, the
  dead ends, the next step, blockers, artifact links.
- **(d) → just say it in chat** — one-off, not worth persisting anywhere.

**IMPORTANT**: If nothing falls into (a) or (b), that's fine — say so and move on. Don't manufacture entries.

---

## Phase 2 — Persist

### 2a — Auto-memory (the certain stuff)

For each (a) item, follow the existing auto-memory conventions exactly (you already know them):
write/update a file under `~/.claude/projects/<project>/memory/` with the right `type:`
(`user` / `feedback` / `project` / `reference`), `**Why:**` + `**How to apply:**` lines for
feedback/project, `[[links]]` to related memories, and add/refresh a one-line pointer in `MEMORY.md`.
Check for an existing file that already covers it before creating a new one. Don't save what the
repo / git history / `CLAUDE.md` already records.

### 2b — Observations (the seam to the `/improve` meta-skill)

For each (b) item, append to `~/.claude/observations/{YYYY-MM-DD}-{short-slug}.md`
(create the file if it's the first observation this session; `{short-slug}` = 2–3 kebab words
describing the session, e.g. `close-skill-spec`). Use this format per observation:

```
### Observation N: <short descriptive title>

- **project:** <repo name, e.g. studying / system_design_vault / <work repo>>
- **skill_or_workflow:** <e.g. integration-feature-dev / pragmatic-techspec / full-bug-fix-workflow / (none — ad-hoc)>
- **phase/area:** <which part, if applicable>
- **outcome:** success | mostly | partial | failed
- **friction_observed:** <free-text> — tag: <wrong_approach | buggy_code | misunderstood_request | scope_creep | read_skipped | rm_violation | line_budget_overrun | async_context_loss | sdk_version_drift | doc_drift | ...>
- **would_have_helped:** <what missing capability / step / rule would have prevented this>
- **improvement_suggestion:** <optional — a concrete proposed change; name the skill section if you can>
- **principle:** <the generalizable takeaway — why it matters beyond this one instance>
```

Number observations within the file (`### Observation 1`, `### Observation 2`, …). One file per
session means no collisions. Keep it terse but specific enough to understand weeks later without
this conversation. Do **not** log one-off corrections that don't generalize — those are (d).

Tags should align with the `/insights` taxonomy so the pile stays comparable to that retrospective.
See `~/.claude/observations/README.md` for the running tag list and the observations-vs-memory rationale.

### 2c — SESSION_LOG.md (the human-readable handoff)

Find the git root (`git rev-parse --show-toplevel`); fall back to `~/SESSION_LOG.md` if not in a
repo. **Prepend** a new entry at the top (newest-first):

```
## [YYYY-MM-DD] — <title>

**Summary:** 1–2 sentences — what this session was and where it landed.
**Done:** <bullet list of what got completed>
**Decisions:** <only the load-bearing ones> X because Y (rejected Z).
**Didn't work:** <abandoned approaches — or "—">
**Next:** <the concrete next action — "start here">
**Blockers:** <unresolved things needing a decision / external input — or "none">
**Artifacts:** <links to the main doc(s) / PR / key commits>
```

If `SESSION_LOG.md` is getting long (~30+ entries / ~1500+ lines), move the *oldest* half to
`SESSION_LOG_ARCHIVE.md` at the same location (a big file degrades agent processing — same reason
the handoff pattern archives completed items).

---

## Phase 3 — Housekeeping & close

1. **Show the diff** — `git status --short` and `git diff --stat HEAD` (already run in Phase 1; re-show
   if it's scrolled away). Generate an English imperative commit message (Conventional-Commits style,
   e.g. `feat: add /close skill`, `docs: session log + memory update`).
2. **Ask before committing.** Present the message; on approval run `git add <files>` + `git commit`
   (never `reset` / `clean` / `checkout --` / force-push — those are blocked by the safety hook anyway).
   If the user declines, leave the working tree as-is.
3. **Cross-machine sync routing.** If either of these git working trees exists, propose a commit +
   push per repo, routed by content kind:
   - `~/.claude/.git/` (claude-home, private) — for edits to: `CLAUDE.md`, `observations/`,
     `improvements/`, `hooks/`, `statusline-command.sh`, `settings.example.json`.
   - `C:\ai-kit\.git\` (ai-kit, public) — for edits to: `skills/`, `commands/`, `agents/`,
     `templates/`, `docs/`. **Run the secret-scan before pushing ai-kit (its pre-commit hook does this
     automatically; --no-verify is the bypass and should be used sparingly).**
   One commit per repo when each has content. **Ask before each commit and before each push.** Never
   auto-push. If either repo has unmerged paths from a prior pull, resolve them first.
4. **Print the close summary** — a one-liner with the counters: `memory: N updated · observations: N
   written · SESSION_LOG: updated · commit: <hash or "skipped">`.
4. **Print a session-rename suggestion** — `[YYYY-MM-DD] <short title>` — for copy-pasting as the
   session name.

---

## Notes

- **Observations ≠ memory** — see `~/.claude/observations/README.md`. Memory = distilled durable rules
  (few, terse, indexed); observations = raw dated per-session evidence (many, full context, tagged).
  `close` triages: certain → memory now; ambiguous skill-performance evidence → observations for the
  periodic `/improve` review (it reads `~/.claude/observations/*.md`).
  They're a pipeline, not a duplicate.
- **This skill is read-only on git history.** It reads (`status`, `diff`, `log`, `rev-parse`) and at
  most `add` + `commit`. It never rewrites history.
- **Project-agnostic.** Works for the study pipeline too — at the end of a study session, log "topic X
  notes done, flashcards generated, next: topic Y" and observe the study commands' friction.
- **Don't manufacture entries.** A short session that genuinely produced no durable learnings should
  produce a thin SESSION_LOG entry, zero memory writes, zero observations — and that's correct.
