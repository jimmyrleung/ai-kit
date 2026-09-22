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

1. Scan _this session's_ context.

2. Build a session summary, containing:

- **Decisions made**: architectural / design / scoping choices, **with the `why`**
- **Learnings / surprises / inefficiencies**: gotchas discovered; "this cost me 20 min because X"; a tool/pattern that worked unexpectedly well or badly.
- **Dead ends — what did NOT work**: approaches tried and abandoned, so they're not re-attempted.
- **Open tasks / next step**: what's unfinished and the _concrete_ next action. Pull from the active task list if one exists.
- **References**: external URLs, tickets, dashboards, doc links mentioned this session.
- **Files touched**: run `git status --short` and `git diff --stat HEAD` (read-only; safe).

3. Document session findings, categorizing each one into:

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
- **(d) → logs**: continuation state only: the concrete next step, blockers, dead ends, artifact links. State, not knowledge — if it would still be true in a month, it's `long-term memory` and not `logs`
- **(e) → session call-out to just say it in chat**: one-off, not worth persisting anywhere.

**IMPORTANT**: If nothing falls into (a), (b) or (c), that's fine — say so and move on. Don't manufacture entries.

4. Display the retrospective to the user: session summary + session findings. Once reviewed/approved, proceed to [Phase 2 — Persist].

## Phase 2 — Persist

### Private repo

In the private repo, you should persist:

- `observations`, under `~/.agents/observations/`

### Local repo

In the local repo, you should create a new `./sessions/yyyyMMddhhmmss_[slug]/` folder, where `slug` is a meaningful name for the session, and persist within:

- `SUMMARY.md` → the session summary
- `LOGS.md` → continuation logs following [Session logs guidance] below
- `long_term_memory.md` → `long-term memory` what should be added to either `AGENTS.md` or `rules/`
- `skills/[skill_draft].md` → one `skill draft` md document for each `local skills candidates`
- `decisions/[decision].md` → one `decision` md document for the most important decisions, ADR style

> Important: the user is responsible for reviewing and deciding if something goes into `AGENTS.md` `rules/` or `skills` - you should just write the drafts within the sessions folder

You can proceed to [Phase 3] once everything is persisted.

#### Session logs

Use the following structure for the session logs in `LOGS.md`:

```
## [YYYY-MM-DD] — <title>

**Summary:** 1 sentence — what this session was and where it landed.
**Next:** <the concrete next action — "start here">
**Blockers:** <unresolved things needing a decision / external input — or "none">
**Didn't work:** <abandoned approaches, so they're not re-attempted — or "—">
**Artifacts:** <links to the main doc(s) / PR / key commits — the things a fresh session opens first>
```

> The idea is for the user to be able to just point to a specific `LOGS.md` and being able to continue a given session

## Phase 3 — Housekeeping & close

Private repo: suggest commit and push

Local repo: no commit or push, the user should handle it
