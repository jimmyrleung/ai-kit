## [2026-05-15] — Explored second-brain/LLM-wiki KB; parked for think-time

**Summary:** Design-only session. User asked for an honest assessment on a skill that "maps a tasks document but for documentation tasks." Investigation showed the entire docs-loop pipeline (`map-tasks` + `document-workflow-loop` + `qa-loop-docs` + `tasks-loop --action document-workflow`) was already wired end-to-end — the real gap is upstream (a docs-tasks-*creator* skill). Conversation expanded to the broader second-brain / LLM-wiki KB design (Karpathy gist, visual-explainer for HTML view, multi-client vault isolation). User parked the initiative pending more think-time.

**Done:**

- Confirmed existing docs-loop pipeline covers everything except task-list creation. No new skills authored.
- Created `C:\ai-kit\ideas\` as a scratch folder for the parked initiative; gitignored via new `.gitignore` at repo root.
- Wrote two memory files (`karpathy-llm-wiki-gist`, `second-brain-kb-initiative`) + indexed in `MEMORY.md`.
- Logged two observations to `~/.claude/observations/2026-05-15-docs-kb-exploration.md` (pre-build investigation success; parked-initiative handoff).

**Decisions:**

- **Park the second-brain initiative; don't build the docs-tasks-creator yet.** Rejected: jumping straight to authoring the enumeration skill. Why: user wants more think-time on the broader KB design, and the recommended pilot path (handwrite one client's `docs-tasks.md`, run the existing loop, validate output, *then* design the creator) hasn't been run yet. Building upstream tooling before the downstream loop is validated is the wrong order.
- **If/when built, the docs-tasks-creator should be single-approach, not 3-way.** Rejected: cloning the granular/balanced/pragmatic structure from `integration-tasks` / `refactor-tasks`. Why: docs task size is effectively fixed (one workflow = one task), so the 3-way exploration would be cargo-culting. The real value lives in the *enumeration* phase (codebase audit for entry points) — closer to `refactor-audit` than to a tasks decomposer.
- **For the KB layout (when initiative resumes): markdown is canonical; HTML via visual-explainer is a *view* for select high-value docs.** Rejected: HTML-as-canonical. Why: breaks grep/RAG affordance and breaks incremental edit — the two things Karpathy's wiki pattern leans on hardest. HTML earns its keep for onboarding overviews, system maps, complex full-stack workflows — not meeting notes or simple workflow docs.
- **Split trees inside the KB:** machine-owned (`workflows/`, cc-loop overwrites freely) vs human-owned (`docs/meetings`, `docs/decisions`, `docs/runbooks`, never overwritten). Rejected: mixing both in single files. Why: code-derived docs are point-in-time snapshots that get re-derived; human-authored content is source-of-truth and must survive re-runs.

**Didn't work:**

- Initial framing of the new skill as a "tasks doc mapper for docs" — `map-tasks` is already action-agnostic, no docs-specific mapper needed. Cleared by reading `map-tasks/SKILL.md` and asking a clarifying question.
- "LLM persistent memory" framing — collapsed honestly into "well-structured markdown that the LLM can grep / RAG over." No vector store, no special MCP plumbing required.

**Next:** When user returns to this — read `second-brain-kb-initiative` memory first (do not restart the design conversation), then pilot: pick one client app, handwrite `docs-tasks.md`, run `/tasks-loop --tasks docs-tasks.md --action document-workflow`, see what cc-loop actually produces. Only then design the enumeration skill — informed by what the loop's output actually needs.

**Blockers:** none — user is taking think-time, not waiting on external input.

**Artifacts:**

- `C:\ai-kit\ideas\` (scratch folder, gitignored)
- `C:\ai-kit\.gitignore` (new — single entry: `ideas/`)
- `~/.claude/projects/C--ai-kit/memory/second-brain-kb-initiative.md`
- `~/.claude/projects/C--ai-kit/memory/karpathy-llm-wiki-gist.md`
- `~/.claude/observations/2026-05-15-docs-kb-exploration.md`
- Karpathy gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

---

## [2026-05-14] — Discussed SESSION_LOG centralization — deferred

**Summary:** Discussion-only. User asked whether `SESSION_LOG.md` should move to a centralized `~/.claude/session_logs/{repo}/` for cross-repo analysis. Concluded: keep current in-repo behavior; revisit when a future knowledge base lands.

**Done:** No code or skill changes.

**Decisions:**

- **Keep `SESSION_LOG.md` at the git root, committed with the work.** Rejected: moving it entirely to `~/.claude/session_logs/{repo}/`. Why: the commit-with-the-work handoff is half the point — a cross-machine teammate (or future-me on another box) sees the narrative in git history. Also rejected dual-write (repo + central mirror) for now — adds complexity ahead of need.
- **For cross-repo *workflow* analysis, use `~/.claude/observations/` (already centralized).** SESSION_LOG = project narrative (per-repo); observations = workflow meta-evidence (already pooled across all projects). Different corpora, different questions.

**Didn't work:** —

**Next:** When the user builds the planned knowledge base (combines session logs + meeting notes + other non-technical notes), revisit whether `/close` should dual-write or whether the KB ingests from repos. No action until that project starts.

**Blockers:** none

**Artifacts:** none — discussion only.

---

## [2026-05-14] — Broaden /close suggestion triggers in global CLAUDE.md

**Summary:** Discussed how to use `/close` during mid-workflow context resets (user resets at ~200K because Opus degrades past 256K), then widened the `/close` trigger rules in `~/.claude/CLAUDE.md` to fire on more than just "user says they're wrapping up."

**Done:**

- Edited `~/.claude/CLAUDE.md` `## Closing a session` to list four triggers: wrap-up language, pre-`/clear`/`/compact`, natural pause, stale `SESSION_LOG.md`. Added explicit `/compact` vs `/close` disambiguation.
- Committed `ca49856` and pushed to `claude-home` main.
- Wrote `user-context-management` memory + indexed it in `MEMORY.md`.
- Logged two observations to `~/.claude/observations/2026-05-14-close-trigger-broadening.md` (skill description doc-drift; rule-design principle).

**Decisions:**

- **Content-based triggers, not token-threshold** for `/close` suggestions. Rejected: "suggest /close if context > 150K tokens" — I don't have a reliable token counter exposed, so a threshold rule would fire inconsistently. Chose intent signals I can actually observe (user message content, file state).
- **`/compact` ≠ `/close`** explicitly called out in CLAUDE.md so future-me doesn't conflate "context is large" (→ compact) with "session is ending" (→ close).

**Didn't work:**

- Token-threshold trigger (proposed, rejected). Don't re-propose unless the harness starts exposing a live token counter to the model.

**Next:** Consider mirroring the broadened triggers into the `close` skill's own `description:` frontmatter line — currently says only "end of a working session," which is narrower than the CLAUDE.md rule (see observation 1 in `2026-05-14-close-trigger-broadening.md`). `/improve` will likely surface this.

**Blockers:** none

**Artifacts:**

- Commit `ca49856` (claude-home) — `docs: broaden /close suggestion triggers in CLAUDE.md`
- `~/.claude/CLAUDE.md` — `## Closing a session` section
- `~/.claude/observations/2026-05-14-close-trigger-broadening.md`
- `~/.claude/projects/C--ai-kit/memory/user-context-management.md`

---

## [2026-05-13] — Add INVENTORY quick-reference docs (Claude-Code-aware placement)

**Summary:** Added quick-reference inventories for every component kind in the kit (agents, commands, skills, docs, templates). Routed through a discovery-vs-rendering trade-off and landed on a single `/INVENTORY/` folder at repo root.

**Done:**

- Created 11 markdown files under `INVENTORY/` — `README.md` (index) + `agents.md`, `commands.md`, `skills.md`, `docs.md`, `templates.md`, plus per-subfolder `templates-bugfix.md` / `templates-feature-addition.md` / `templates-greenfield-dev.md` / `templates-incident-response.md` / `templates-refactoring-tech-debt.md`.
- Each inventory groups by workflow family (greenfield / feature-integration / bugfix / refactor / incident-response / QA / meta) and includes the registered `name` and model pin for agents.
- Commit `58a18e6` pushed to `origin/main`.

**Decisions:**

- **Centralize inventories in `/INVENTORY/` instead of in each folder** — because `agents/`, `commands/`, `skills/` are auto-scanned by Claude Code via the `~/.claude/` junction, and any `.md` inside those folders gets auto-registered as a command/agent. Rejected alternatives: per-folder `INVENTORY.md` (registered `/INVENTORY` as a slash command — confirmed empirically), per-folder `_INVENTORY.md` (also registered — underscore is not filtered), per-folder extensionless `INVENTORY` (worked for Claude Code, but GitHub won't render markdown without the `.md` extension).
- **Single flat folder over nested mirror** — `templates-bugfix.md` rather than `INVENTORY/templates/bugfix.md`. Trade-off: lose the structural mirror of the source folders; gain a flat folder where every file renders on GitHub from the README.

**Didn't work:**

- `_INVENTORY.md` rename — still registered as `/_INVENTORY` on the next session-reminder. Underscore prefix is NOT a Claude Code filter convention; only the `.md` extension is.

**Next:** Optional — add a short note to `README.md` or a new `CONTRIBUTING.md` explaining the folder semantics ("files in `agents/`, `commands/`, `skills/` auto-register via the junction; place helper docs under `/INVENTORY/` or `/docs/`"). Would prevent the same rediscovery for future contributors / future-me.

**Blockers:** none

**Artifacts:**

- Commit `58a18e6` — `docs: add INVENTORY quick-reference for agents, commands, skills, templates`
- `INVENTORY/README.md` — landing page (auto-renders on folder entry on github.com)
