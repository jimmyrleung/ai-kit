# Kit refactor — current state vs. archive comparison (2026-08-05)

Comparison done. Everything below is derived from `ls` of `C:/ai-kit/skills|commands|agents|templates` vs `C:/ai-kit/archive/*` plus greps run this session. Headline: the archive-only delta is **25 skills, ~24 commands, all 17 agents** — but most of it is already absorbed by the consolidation work. The genuine "bring back or kill" list is short: **triage, roadmap-creation, create-qa-scenarios, bug-regression-test, migrate-notion**, plus the two families already on your backlog (incident, ownership). I also found one live breakage worth knowing about: the loop skills still hard-reference the archived `code-reviewer-agent`.

## 1. Absorbed — nothing to bring back (successor exists and covers it)

| Archived | Live successor |
|---|---|
| prd-creation, integration-analysis, refactor-audit (+ create-prd, integration-analyze-feature, audit-refactor-techdebt cmds) | `analyze` (modes) |
| techspec-creation, integration-techspec, pragmatic-techspec, refactor-plan, impact-analysis (+ create-techspec, integration-create/pragmatic-techspec, analyze-impact cmds) | `techspec` (work-type detection + impact lens) |
| tasks-creation, balanced-tasks-creation, integration-tasks, refactor-tasks (+ create-tasks, integration-balanced/create-tasks cmds) | `tasks-breakdown` |
| implement-task, gf-implement-task, implement-bug-fix cmds | `implement-task` skill (fix lens) |
| investigate-bug cmd | `bug-investigation` skill |
| review-techspec, review-investigation cmds | `review-artifact` |
| implementation-quality-assurance, qa-gates cmds | `qa-gates` skill |
| document-workflow, update-workflow-docs, document-terraform, lay-of-the-land, audit-skills, review-implementation cmds | same-named skills |
| greenfield-dev, integration-feature-dev, refactor-techdebt-dev, full-bug-fix-workflow cmds | deliberately dropped — "no command wrappers" direction |
| all 17 agents (integration-*, diagnosis-*, audit-*, hotfix-planner, post-mortem, code-reviewer-agent, …) | deliberately dropped — "no named agents" direction (but see §4) |

Templates: live `templates/` and `archive/templates/` are byte-identical (`diff -rq` clean) — the archive copy is redundant, nothing to restore.

## 2. Already on your backlog — no new decision needed, just sequencing

- **Incident family** — ✅ RESOLVED 2026-08-06 (step 8), on the suggested shape: `post-mortem` rebuilt as the only new live skill (no named agents, loose inputs accepting legacy incident-dir or kit-shaped artifacts); diagnosis folded into `bug-investigation` as an **incident lens** (log/trace/metric evidence + timeline correlation, 5-Whys depth, P1 streamlined ≥70% gate); hotfix folded into `techspec` fix mode as a **hotfix variant** (executable playbook, rollback triggers, escalation flags, tech-debt hand-off list for the post-mortem). All archived bodies read before folding (closing the §Confidence caveat for this family). Commands stay archived per no-command-wrappers; `start-incident`/`incident-status` scaffolding dropped (the loose input contracts replace them; `templates/incident-response/incident-report.md` still referenced as the report shape). Backlog 28 closed — qa-gates' streamlined mode kept, now with live callers. Trigger test 4/4.
- **Ownership family** — ✅ RESOLVED 2026-08-06 (step 9, partial restore): `onboard-me` + `record-decision` restored from archive (git mv) and simplified to stand alone — all `adr-first`/`challenge-me` awareness stripped (record-decision owns its store/numbering directly; UNREVIEWED review path is the human, in-session or via /close's sweep, with an own-it-now path added). `adr-first`, `challenge-me`, `predict-first`, `debug-first` stay archived — user call on real-usage grounds (friction rituals unused under deadline pressure; may return if genuinely missed). Callers fixed: `close` sweep keeps /record-decision and drops the /adr-first hop; `walkthrough-implementation` routes only to `onboard-me`/`walkthrough`. Zero dead-reference echoes in live surfaces (grep -R); Codex synced (33 exposed, 0 issues). Backlog 27 closed.

## 3. Genuine decision items — no successor, not on any list

All five dispositioned 2026-08-06 (step 10):

| Item | Decision |
|---|---|
| **triage** (skill) | ✅ RESTORED (git mv) and adapted to the skill-centric kit: routes to chain entry skills (`analyze` / `bug-investigation` / `lay-of-the-land`) instead of the retired workflow orchestrators; Phase-0 mid-flight detection now reads the kit's artifact conventions (`_analysis` / `_techspec` / `_tasks` / `_investigation` + `## Review` stamps) and recommends the next chain step; short-circuit table rebuilt from live skills; loop-primitive routing table kept (loop-recipes.md's "exactly two places" contract healed). The global CLAUDE.md "offer /triage" instruction is no longer dangling |
| **roadmap-creation** (+ create-roadmap cmd) | ✅ Stays archived until a roadmap need is actually felt — user call. Restore-individually-on-felt-need, same posture as the ownership family's archived four |
| **create-qa-scenarios** (cmd) | ✅ Absorbed into `techspec`: new post-write **QA-scenario pass** (Process 7) — once the spec is written it's re-read as a QA engineer and the Test plan (§6) gains priority + automatable columns, with every committed behavior mapped to ≥1 scenario (happy/error/edge/integration) and the old command's proportionality guard carried over. The final doc = the spec + how to test it. Command stays archived per no-command-wrappers |
| **bug-regression-test** (cmd, pairs with regression-test-plan skill) | ✅ Already absorbed — verified 2026-08-06: `implement-task` fix lens requires tests covering the bug scenario + the techspec impact section's edge cases; `qa-gates` verifies. Killed with the incident family (step 8) |
| **migrate-notion** (skill) | ✅ Stays archived — one-off migration tool, dead |

## 4. Live breakage found during the sweep (not a bring-back question, but surfaced by it)

`qa-loop`, and per their descriptions `qa-loop-docs` and `review-checkpoint`, still fan out `@code-reviewer-agent` via the Task tool (`qa-loop/SKILL.md:57-75,194`) — and the live `agents/` dir (both repo and `~/.claude/agents/`) is empty. Under the claude-code provider those Task calls target a subagent that no longer exists. `review-implementation:53` mentions it only as a style reference, which is harmless. This fits naturally into your already-planned cc-looper loop-skill bite: retarget the loop skills to generic reviewer subagents, the same move `review-implementation` already made. (Side note: these three skill dirs are the cc-looper junctions — the Grep tool silently skipped them; bash grep caught it, consistent with your symlink-topology memory.)

## Recommendation

Bring nothing back wholesale. The only items I'd act on: (1) ~~decide triage~~ — restored + adapted (step 10, 2026-08-06), (2) fold the code-reviewer-agent fix into the cc-looper bite — **still open, the only remaining item from this doc**, (3) ~~kill roadmap/qa-scenarios/migrate-notion explicitly~~ — dispositioned (step 10, 2026-08-06: roadmap + migrate-notion stay archived, qa-scenarios absorbed into techspec), (4) ~~sequence incident + ownership as the already-named bites~~ — incident done (step 8, 2026-08-06); ownership done (step 9, 2026-08-06, partial restore).

Confidence: 93% — the enumeration and absorption mapping are grounded in this session's listings and greps. The 7%: I dispositioned archived items from their filenames and your session history without reading each archived body, so an archived skill could contain a capability its successor genuinely lacks (most plausible for `regression-test-plan` and the incident family); and I didn't verify whether `qa-loop-docs`/`review-checkpoint` bodies (vs just descriptions) carry the agent reference, since those junctions need direct reads.
