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
