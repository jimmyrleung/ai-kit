## [2026-05-15] — Normalize tasks-overview table across task-gen skills

**Summary:** User flagged that `/integration-balanced-tasks` and `/integration-create-tasks` produce a nice summary table (status, size, depends on) and asked to apply it to all task-generating skills. Audited 5 skills; 2 already conformed; updated 2; user opted to skip the 5th. Verified the downstream `map-tasks` parser is column-order agnostic before shipping.

**Done:**

- `skills/refactor-tasks/SKILL.md` — overview-table column spec: `Task | Complexity | Estimated Time | Status` → `Task | Title | Complexity | Est. Time | Depends On | Status`.
- `skills/tasks-creation/templates/tasks_template.md` — greenfield template: added `Depends On` column; renamed `Est.` → `Est. Time` for consistency with the reference shape.
- Verified `map-tasks/SKILL.md:24` reads the table with a wildcard middle (`| # | Title | … | Status |`), so the new column doesn't break the cc-loop runner.

**Decisions:**

- **Skip `docs-tasks-creator`.** Its tasks are uniform-size (one handler doc each) and inherently independent, so `Complexity='S'` and `Depends On='—'` rows would be filler. The existing `Trigger`/`Service` columns carry real domain signal; preserving them beats blind consistency. Rejected the "apply uniformly anyway" option.
- **Normalize column headers to `Complexity` / `Est. Time`** across the touched skills (matches the two reference skills exactly). Rejected leaving the legacy `Estimated Time` / `Est.` headers in place.
- **Didn't touch the worker agents (`integration-tasks-creator-agent`, `refactoring-tasks-creator-agent`) or wrapping commands.** They delegate to the skills ("follow the skill exactly"), so the skill body is the single source of truth — agents/commands inherit.

**Didn't work:** —

**Next:** none — change is self-contained. (The next time someone runs `/create-tasks` or `/refactor-techdebt-dev`'s tasks phase, the new shape will be produced.)

**Blockers:** none.

**Artifacts:**

- `C:\ai-kit\skills\refactor-tasks\SKILL.md` (modified)
- `C:\ai-kit\skills\tasks-creation\templates\tasks_template.md` (modified)

---

## [2026-05-15] — Workflow-doc staleness signals (schema v1) + cc-looper integration check

**Summary:** Added staleness-detection metadata to `document-workflow` (the interactive command) and `document-workflow-loop` (the cc-looper headless skill). Then confirmed the changes don't break cc-looper's runner — discovered ai-kit's loop-related skills/commands are symlinks to cc-looper's `claude-config/`, so edits already propagated. Two real concerns surfaced during the impact check; both fixed.

**Done:**

- Added `Created`, `Last Updated`, `Generated From` (short commit SHA), `Schema: v1` rows to the Summary table of produced workflow docs (in both the command and the loop skill).
- Added `## Source Files` (machine-readable `Role | Path` table — the input to automated staleness detection) and `## Change Log` (`Date | Change | Reason` with an initial-creation row) sections at the end of produced docs.
- Added populate instructions: command's Guidelines + loop skill's Workflow 2 (new step 4 = single Bash call `git rev-parse --short HEAD`, with a fallback clause for denied/failed cases → set `unknown` + `[TODO: verify SHA]` rather than pausing the task).
- Updated `qa-loop-docs` Gate 0 hint list to include the new sections + the four doc-meta Summary rows, with an explicit acceptance rule (`unknown` Generated From with the marker is NOT a Gate 3 finding; literal placeholders left as `YYYY-MM-DD` or `<short-sha>` ARE findings).
- Discovered via `Get-Item -Force` that `C:\ai-kit\skills\{document-workflow-loop, qa-loop-docs, qa-loop, implement-task-loop, map-tasks, review-checkpoint}` and `C:\ai-kit\commands\tasks-loop.md` are all Windows SymbolicLinks to cc-looper's canonical copies — wrote [[cc-looper-symlink-topology]] memory.
- Updated [[second-brain-kb-initiative]] memory to reflect schema v1 + flag staleness detector as the next remaining gap.

**Decisions:**

- **Change Log columns: `Date | Change | Reason`** (chose recommended 3-col over 2-col minimal / 4-col with editor). Rejected the 4-col `Editor` field because no human-vs-skill distinction is needed yet; rejected 2-col because the `Reason` nudge gives future edits context without much cost.
- **`Generated From` advances on every update**, doesn't stay frozen like `Created`. Why: the SHA represents "the state of the codebase this doc was last verified against," not "first generation" — the Change Log is the audit trail.
- **Schema v1 explicit version row**, not implicit. Why: cheap insurance for future template migrations — a 1-line grep finds every doc on an old schema.
- **`git rev-parse` denial → route-around with `unknown`, not pause.** Why: target repos (client codebases being documented) often won't have `Bash(git:*)` in their `.claude/settings.json`, and per the headless preamble a Bash denial would otherwise pause the task. The SHA is a nice-to-have, not load-bearing — the doc is still useful without it.
- **Source Files table as a separate section** (not woven into Sequence of Calls). Why: machine-readable; future detector skill's `git log <generated-from>..HEAD -- <paths>` invocation needs a clean list.
- **Edited via the cc-looper-target paths' ai-kit symlink aliases** once discovered — same physical file, but Read-tracking pinned to whichever path was first opened.

**Didn't work:**

- First Edit attempt on `~/projects/cc-looper/claude-config/skills/qa-loop-docs\SKILL.md` failed with `File has not been read yet` because I'd Read the ai-kit symlink path first. Recovered by re-issuing against the path I'd Read.

**Next:**

- **Build the staleness detector skill** (offered + parked this session). Sketch: read every `workflows/**/*.md`, extract `Last Updated` + `Generated From` + `## Source Files`, run `git log <generated-from>..HEAD -- <paths>` per doc, output a triage list (stale / probably-fresh / unknown). Pairs with `audit-skills` as a structural-quality check for the raw/ layer of the second-brain init.
- Real-world validation of the schema-v1 metadata on a docs run (the `docs-tasks-creator` validation list from the prior session still applies — staleness signals just rode along).

**Blockers:** none.

**Artifacts:**

- `C:\ai-kit\commands\document-workflow.md` — modified (Summary rows + Source Files + Change Log sections + Guidelines populate rule + git-denial fallback)
- `~/projects/cc-looper/claude-config/skills/document-workflow-loop\SKILL.md` (via `C:\ai-kit\skills\document-workflow-loop` symlink) — modified (same additions + Workflow 2 step 4 git-SHA capture with fallback)
- `~/projects/cc-looper/claude-config/skills/qa-loop-docs\SKILL.md` — modified (Gate 0 hint list updated with new sections + Summary doc-meta rows + `unknown` acceptance rule)
- `~/.claude/projects/C--ai-kit/memory/cc-looper-symlink-topology.md` (new — reference memory)
- `~/.claude/projects/C--ai-kit/memory/second-brain-kb-initiative.md` (updated — schema v1 milestone + detector as next gap)
- `~/.claude/observations/2026-05-15-workflow-doc-staleness-signals.md` (new — 3 observations: symlink Read-tracking gotcha, triaged-brainstorm pattern win, runner-allowlist fact-check win)

---

## [2026-05-15] — Built docs-tasks-creator skill (decoupled, multi-stack, monorepo-aware)

**Summary:** Built v1 of the `docs-tasks-creator` skill — the concrete bucket-1 gap from this morning's KB workflow iteration. Scans a codebase, detects HTTP/message/job handlers via pluggable detectors, emits a consumer-agnostic tasks doc (one task per handler) + a synthesized `project-overview.md`. Also deprioritized the `active-context.md` proposal (priorities-doc line 14) — user flagged it as a habit-sustainability risk.

**Done:**

- Read existing `document-workflow-loop`, `map-tasks`, and `document-workflow` skills to ground the design — confirmed how the output-path mechanism works (the consuming tool writes to `<repo>/workflows/...` where `<repo>` is its primary repo).
- Authored `C:\ai-kit\skills\docs-tasks-creator\SKILL.md` (~280 lines):
  - **10 v1 detectors**: Next.js (App Router / Pages API / Server Actions), Express, Fastify, NestJS, ASP.NET Core (attribute + minimal API), GRPC .NET, .NET BackgroundService.
  - **Monorepo handling**: workspace detection (pnpm-workspace.yaml / package.json workspaces / nx.json / lerna.json / rush.json / turbo.json / multi-`.csproj`-from-.sln / heuristic fallback); interactive selection (AskUserQuestion for 2–4 workspaces, plain text for 5+); per-workspace artifacts under `$output_dir/<workspace-slug>/`.
  - **Consumer-agnostic emitted tasks doc** — no cc-loop coupling; each task has `Status:`, `Reference:`, `Files affected:`, `Trigger:`, `Acceptance criteria:`.
  - **Inline project-overview.md generation** in Phase 4 (not a separate cc-loop task).
- Updated [[second-brain-kb-initiative]] memory to reflect docs-tasks-creator v1 built.
- Wrote new feedback memory: [[prefer-decoupled-designs]].

**Decisions:**

- **Consumer-agnostic emitted tasks doc.** Rejected cc-loop-coupled v1 (initial draft included a `## How to run` block with `bun cc-loop ...`, a `**Repos**:` header, and `document-workflow-loop` references). Why: user explicitly said "if someone wants to generate doc tasks but do all of them manually that's fine" — the artifact should serve manual workflows too.
- **Pluggable multi-stack detectors from v1.** Rejected my proposal of "pick one stack first, generalize later." Why: user works across React+TS, Node, .NET — locking to one stack would leave most of their surface unscanned.
- **One tasks doc per workspace in monorepos.** Rejected one giant combined doc. Why: per-workspace isolation matches how docs are consumed (one workspace = one engagement boundary); a 30-workspace doc would be unworkable.
- **One handler per task** (not per-class clustering). Why: matches "one doc per handler" output shape and the priorities-doc framing.
- **Inline setup work, no `Task 0`.** Scaffolding + project-overview.md done by docs-tasks-creator itself in Phase 4, not emitted as a cc-loop task. Why: cc-loop's `document-workflow` action is for tracing workflows, not synthesizing overviews — a Task 0 would have no compatible runner.
- **Deprioritized `active-context.md`** (line 14 of priorities doc). Why: user self-flagged habit-sustainability risk ("I'd stop doing it in a week or two"). Parked.

**Didn't work:**

- Initial Cline-style `active-context.md` proposal — rejected by user on habit-sustainability grounds. The hot/stable section split + decay rules + 300-line cap design was probably fine; the weekly-debrief dependency was the unworkable part.
- Initial single-stack v1 framing — user redirected to multi-stack.
- Initial cc-loop coupling in the emitted tasks doc — user flagged for removal.
- Initial monorepo-blind v1 — missed entirely until user surfaced it.

**Next:**

- Real-world validation on `docs-tasks-creator` against an actual client codebase. Specifically validate: (a) the multi-`--repo` cc-loop invocation works (only inferred from map-tasks' `$repos` plural reference; not verified against `bun cc-loop` CLI); (b) Server Actions detector false-positive rate; (c) service-name derivation on real monorepo layouts; (d) heuristic-fallback workspace detection on `client/`+`server/`-style non-monorepo splits.
- Remaining bucket-1 items: `raw/{client}/{project}/` folder skeleton + weekly debrief cadence.

**Blockers:** none.

**Artifacts:**

- `C:\ai-kit\skills\docs-tasks-creator\SKILL.md` (new, ~280 lines)
- `~/.claude/projects/C--ai-kit/memory/second-brain-kb-initiative.md` (updated — docs-tasks-creator v1 built)
- `~/.claude/projects/C--ai-kit/memory/prefer-decoupled-designs.md` (new — feedback memory)
- `~/.claude/observations/2026-05-15-docs-tasks-creator-build.md` (new — 3 observations on initial-draft missteps)

---

## [2026-05-15] — KB workflow iteration 2: research + prioritized roadmap

**Summary:** Un-parked the second-brain/LLM-wiki KB initiative for iteration 2. Ran three parallel research streams (SOTA / staleness tooling / skeptical), iterated through key design questions with the user, produced two artifacts: iteration 2 section appended to the main idea doc + a new prioritized roadmap doc.

**Done:**

- Three parallel research-agent streams (general-purpose with WebSearch): SOTA for LLM-consumable codebase KBs, doc staleness tooling, critical / failure-history pass.
- Surfaced key findings: Karpathy LLM Wiki pattern is mainstream (~5k stars, ~1:1 to user's `raw/+kb/` design); HackerNoon 6-Rails case study at $10–20/mo; DORA 2024 (AI doc adoption +7.5% quality but −1.5% throughput and −7.2% stability); Karpathy v1 documented month-1 failures + v2 fork by rohitg00; Hansen/Nohria/Tierney HBR 1999 (personalization > codification for customized-engagement consulting).
- Appended **Iteration 2** section to `C:\ai-kit\ideas\knowledge-and-docs-wf.md` (research approach, findings, 4 decisions, kill criteria, strategic reframe, v2-vs-v1, out-of-scope, open items, references).
- Created `C:\ai-kit\ideas\knowledge-and-docs-wf-priorities.md` — 4-bucket prioritized roadmap (do now / do soon / good-to-have / don't do) + sequencing logic + kill-criteria reminder.

**Decisions:**

- **`kb/` is a build artifact, not source of truth.** Rejected SSOT framing. Why: defuses both the staleness rot problem (regenerate, don't maintain) and the Hansen-codification anti-pattern. Contradictions resolve to primary source.
- **Kill criteria ordered c > b > a** (maintenance cost > trust events > re-query rate). Rejected equal weighting. Why: the KB's primary consumer is the user, not the LLM — LLM query rate is a use-pattern indicator, not a fitness test. A KB the LLM ignores but the human uses is still doing its job.
- **Strategic reframe: personal knowledge augmentation, not team codification.** Rejected "this is a docs project for the LLM." Why: weakens DORA / Hansen concerns which are about *teams* producing doc volume for *other readers*.
- **Sequence: build `raw/` + `active-context.md` + `docs-tasks-creator` FIRST; `kb/` consolidation is an experiment LATER.** Rejected "build kb/ first as foundation." Why: minimum viable version delivers value with zero buy-in to the risky bet. If `kb/` never works, the rest still earns its keep.
- **If/when `kb/` is built, adopt Karpathy v2 affordances from day 1.** Rejected v1 unmodified. Why: v1 has documented month-1 failure modes (identity collisions, level collapse, link cascade); v2 (rohitg00 fork) adds confidence scoring, supersession, provenance to address these.
- **HTML output is for the user, not clients.** Relaxes freshness contract since user is the only consumer who knows which pages are stale.

**Didn't work:**

- Visual-explainer integration for HTML output (already rejected iteration 1, re-confirmed: wrong shape — re-generates everything when only incremental updates are needed).
- "kb/ as source of truth" framing — rejected explicitly in iteration 2.
- My initial framing of kill criteria as equally-weighted — user's reordering (c > b > a) was sharper and required reshaping the operational design.

**Next:** Build the `docs-tasks-creator` skill — most concrete bucket-1 item; independent of the `kb/` bet. Scans codebase, emits one document-workflow task per endpoint/job + setup task, feeds cc-loop. Single-approach (not 3-way) per prior memory. See `C:\ai-kit\ideas\knowledge-and-docs-wf-priorities.md` for full sequencing.

**Blockers:** none — iteration 2 captured; #5 (personalization fallback) explicitly parked for further thought with a starting question.

**Artifacts:**

- `C:\ai-kit\ideas\knowledge-and-docs-wf.md` (iteration 2 appended)
- `C:\ai-kit\ideas\knowledge-and-docs-wf-priorities.md` (new)
- `~/.claude/projects/C--ai-kit/memory/second-brain-kb-initiative.md` (updated — un-parked, iteration 2 decisions)
- `~/.claude/projects/C--ai-kit/memory/karpathy-llm-wiki-gist.md` (updated — v2 fork + failure modes)
- `~/.claude/observations/2026-05-15-kb-iteration-2.md` (new — primary-consumer reframe observation)
- Karpathy v2 fork: https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2
- HackerNoon case study: https://hackernoon.com/how-i-built-a-self-maintaining-knowledge-base-for-6-projects-using-claude-code-and-karpathys-llm-wiki

---

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
