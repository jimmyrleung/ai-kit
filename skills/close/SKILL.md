---
name: close
description: "Distills the current session into a continuation log and optional durable records of decisions, learnings, dead ends, and open work. Use when wrapping up, stopping, preparing for a context reset, or pausing after work lands."
---

# Close — end-of-session ritual

## Goal

Close out a working session:

- Leave breadcrumbs so the next session (possibly days later, possibly after a context reset) doesn't rebuild context from vibes
- Optionally record structured evidence of how any workflows performed
- Optionally extract valuable decisions, lessons learned, rules, skills idea, and key information.

**This is a curated briefing, not a transcript.** Distill. Do not dump the conversation. Do not carry forward your own stale intermediate reasoning — only conclusions, decisions, what's next, etc..

## Phase 1 — Retrospective (scan, then categorize)

**Execute the steps below sequentially.**

1. Scan _this session's_ context to find:

- **Decisions made**: architectural / design / scoping choices, **with the `why`**
- **Learnings / surprises / inefficiencies**: gotchas discovered; "this cost me 20 min because X"; a tool/pattern that worked unexpectedly well or badly.
- **Dead ends — what did NOT work**: approaches tried and abandoned, so they're not re-attempted.
- **Open tasks / next step**: what's unfinished and the _concrete_ next action. Pull from the active task list if one exists.
- **References**: external URLs, tickets, dashboards, doc links mentioned this session.
- **Files touched**: run `git status --short` and `git diff --stat HEAD` (read-only; safe).

3. Build one list per type of finding, then categorize each one into:

- **(a) → long-term memory**: durable facts that would benefit any agents if they already existed in the `AGENTS.md` or were part of one of the repo rules. Examples are:
  - a confirmed user preference
  - a project's convention
  - architectural patterns
  - standards
  - policies
  - processes
  - a constraint/deadline
  - an external reference you'll want again from any repo, etc.
  - a hard-won fact about _this_ codebase that any agent (or teammate) should know next session
  - anything that would improve an agent experience in a future session in this repo?

- **(b) → local skills candidates**: situational things that could be extracted to local skills, like: "where-to-find-X" or "how-to-do-Y"
- **(c) → decisions**: important decisions made that are candidates to be ingested into a knowledge base, llm wiki, etc.
- **(d) → observations**: evidence of how a skill/workflow performed (friction, a missing capability, a workflow step that drifted). _Ambiguous_ stuff that needs batch review later, not a snap memory write. These are intended to be used as evidence for the `improve` skill
- **(d) → LOGS**: continuation state only: the concrete next step, blockers, dead ends, artifact links. State, not knowledge — if it would still be true in a month, it's (a).
- **(e) → session call-out to just say it in chat**: one-off, not worth persisting anywhere.

**IMPORTANT**: If nothing falls into (a), (b) or (c), that's fine — say so and move on. Don't manufacture entries.

5. Display the retrospective to the user: list of findings organized by category to be reviewed. Once reviewed/approved, proceed to [Phase 2 — Persist].

## Phase 2 — Persist

### 2a — User/cross-repo memory (the certain stuff)

Guidance for persisting:

- `observations` goes into the private `~/.agents/observations/` repo
- the rest goes into the local repo: `./sessions/yyyyMMddhhmmss_[slug]/` folder, where `slug` is a meaningful name for the session.
  - write `LOGS.md` → follow [Session logs guidance] below
  - write `./sessions/yyyyMMddhhmmss_[slug]/long_term_memory.md` for `long-term memory` you think should be added to either `AGENTS.md` or `rules/`
  - write a draft for each `local skills candidates` into `./sessions/yyyyMMddhhmmss_[slug]/skills/`
  - write `decisions` on `./sessions/yyyyMMddhhmmss_[slug]/decisions/`

> Important: the user is responsible for reviewing and deciding if something goes into `AGENTS.md` `rules/` or `skills` - you should just write the drafts within the sessions folder

You can proceed to [Phase 3] once everything is persisted.

#### Session logs

Use the following structure for the session logs:

```
## [YYYY-MM-DD] — <title>

**Summary:** 1 sentence — what this session was and where it landed.
**Next:** <the concrete next action — "start here">
**Blockers:** <unresolved things needing a decision / external input — or "none">
**Didn't work:** <abandoned approaches, so they're not re-attempted — or "—">
**Artifacts:** <links to the main doc(s) / PR / key commits — the things a fresh session opens first>
```

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
     `observations/`, `improvements/`, and their manifest or READMEs.
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
