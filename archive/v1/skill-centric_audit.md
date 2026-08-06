# Skill-centric refactor — audit

> Phase 1 (audit) of the skill-centric refactor of ai-kit. Reference map only — the design lands in `skill-centric_plan.md` (next phase: `/refactor-plan` — well, the skill; the command still works too, which is rather the point of this document).
>
> Produced 2026-07-29 on branch `kit-refactor` by the `refactor-audit` skill (3 `@audit-agent` workers: skill input-coupling / commands + fork drift / downstream surfaces), consolidated with four user scope decisions recorded below.

## Executive summary

The original three-axis request — (1) commands become copyable templates, (2) skills decoupled from named artifacts to information contracts, (3) headless forks retired for mode parameters — collided with three structural facts: `~/.claude/commands` is a **junction directly at `commands/`** (the repo dir *is* the deployment), six of the "fork" skills are **symlinks into `~/projects/cc-looper`** whose runner binds their names in TypeScript, and `templates/` **already exists** as a different documented concept. Four scope decisions (below) resolved these conservatively: nothing moves, cc-looper is deferred, and the refactor becomes: input-contract fallbacks on ~15 skills, ~5 skill extractions from logic-carrying commands, a new non-scanned `recipes/` dir, and 5 fork-fix back-ports.

- **Complexity:** Medium
- **Risk Level:** Medium
- **Estimated Scope:** Medium

**Confidence score: 92%**
- Why 92%: all 49 `skills/` entries opened/grepped this session; all 39 command frontmatters + 15 bodies read end-to-end; junction/symlink topology, both codex sync scripts, and cc-looper's dispatch layer verified by direct command output; scope ambiguities resolved by explicit user decisions (§ Decisions).
- 8% uncertainty: 24 command bodies not read end-to-end (a shim-vs-logic misclassification in that tail is possible — affects the extraction list's edges, not its core); cc-looper consumer-side constraints (plan.json assertions, Recommendation-regex) read only at the dispatch layer, relevant to the back-port phase.

## Decisions (user, 2026-07-29 — these bound the scope)

| # | Question | Decision |
|---|---|---|
| D1 | cc-looper in scope? | **No — defer fork retirement.** ai-kit-only; back-port the 5 fork-only fixes into ai-kit originals so nothing is lost. |
| D2 | Depth of input decoupling | **Canonical name + prose fallback.** Keep `docs/output-filename-contract.md` + audit-skills Check 11; extend with the input-side fallback rule. No pure-information-contract rewrite. |
| D3 | `commands/` disposition | **Thin in place, don't move.** Junction, adapters, cc-looper installer, triage routes all keep working. Copyable templates land in a NEW non-scanned dir (`recipes/`, name = gray area). |
| D4 | Hard gates | **Soften artifact gates, keep review gates.** Missing-named-file → fallback + confidence flag; missing `## Review` section stays a stop. |

## 1. Skill input-coupling map

49 entries in `skills/`: 41 real dirs + 8 symlinks (6 → `~/projects/cc-looper/claude-config/skills/`, 2 → `~/.agents/skills/` — vendored `find-skills`, `teach`). **Tooling caveat:** Glob/Grep/ripgrep do not traverse the symlinked dirs — any scripted sweep must use `Get-ChildItem` or Bash `grep -r` (per `docs/rules/skill-authoring.md`).

Gate legend: **GATE** = stops when the named artifact is absent · **FALLBACK** = proceeds + flags · **SILENT** = names artifact, no missing-case · **—** = no upstream artifact.

### Already at target state (the exemplars)

| Skill | Evidence |
|---|---|
| `integration-techspec` | :42 — the named reference pattern: proceed on lighter input, flag gaps in confidence section |
| `pragmatic-techspec` | :28-33 — `## Input contract` opens "Expect **one or both** of" |
| `lay-of-the-land` | :28-29 — degraded input is a first-class path ("Or a brief description (fallback path)") |
| `walkthrough` | :22-23 — accepts "a doc section, review output, or pasted list"; creates its own artifact if none |
| `document-terraform` | :41 — `$spec_file` optional; "If absent, discover everything from the code" |
| `review-artifact` | :14-23 — doc identity is a parameter pair (`artifact_path` + `artifact_label`), 8 named inputs incl. `mode: full\|abbreviated`; :25 "If a required input wasn't supplied, ask the caller". The convergence model for both axis 2 and the mode-parameter pattern. |
| `regression-test-plan` | :24 — names three artifacts, states the reconstruction path for the missing one |

### Needs the fallback pattern (axis-2 worklist, D2+D4 applied)

| Skill | Coupling (file:line) | Today | Change class |
|---|---|---|---|
| `balanced-tasks-creation` | techspec :41, integration :43 | GATE on techspec | soften artifact gate |
| `integration-tasks` | techspec :39, integration :40 | GATE on techspec | soften artifact gate |
| `refactor-tasks` | plan :39, audit :40 | GATE on plan | soften artifact gate |
| `refactor-plan` | audit + `## Review` section :41 | GATE | soften the *file* gate; **review-section gate stays** (D4) |
| `hotfix-plan` | diagnosis + `## Review` section :47 | GATE | same split as refactor-plan |
| `incident-diagnosis` | report + required sections :41 | GATE (asks to fill sections) | soften: accept equivalent prose carrying the same info |
| `impact-analysis` | `{bug_id}.md` + `_investigation.md` "required" :33 | SILENT | add explicit fallback |
| `post-mortem` | report/diagnosis/plan "required" :36-38 | SILENT | add explicit fallback |
| `qa-gates` | Gate 0 glob :47, Gate 4 names four siblings :188-189 | SILENT ("whichever exist") | make the whichever-exist behavior an explicit input contract |
| `techspec-creation` | hard relative `./PRD.md` :23 | SILENT | parameterize the path; fallback to prose spec |
| `tasks-creation` | PRD Done-when checkboxes :59 | SILENT | explicit fallback |
| `bug-investigation` / `integration-analysis` / `refactor-audit` / `prd-creation` / `challenge-me` | SOFT already | FALLBACK | normalize wording to the exemplar pattern |

### Structurally coupled — out of reach of prose input (do NOT touch under axis 2)

- **In-place editors** (need a real doc to write into, regardless of how they learned about it): `qa-gates:32` (`## QA` append), `verify-task:25` (`## Verify` inside a task section), `review-implementation:24`, `review-artifact:16`, `close-tasks:162` (harvest marker into the tasks doc).
- **Status-line / anchor protocol** (cc-looper-owned semantics, out of scope per D1): `implement-task-loop:67,73`, `document-workflow-loop:266-284`, `map-tasks:26,81` (physical `Status:` line requirement; line-range anchors).
- **Cross-skill protocol markers**: `qa-gates:35` `(verified at:)` vs `review-implementation:25` `(reviewed at:)` stamps; `qa-loop:107-111` reads `Baseline:` written by `implement-task-loop:39-42`; `review-checkpoint:37` / `qa-loop:172` pin `**Recommendation:**`/`**Summary:**` for the runner's regex.
- **Detection-by-filename**: `triage:23-25` globs six artifact patterns; renames fail *silently* there. D2 (keep canonical names) protects this.

### Worst offenders (recorded for the plan's ordering, not all in scope)

1. `qa-loop-docs:39` — reads **another skill's SKILL.md by absolute path** (both `~/.claude/skills/…` and repo spellings). cc-looper-owned; out of scope per D1, but the pattern is the anti-example.
2. `qa-gates` + fork `qa-loop` — filename coupling + in-place edit + cross-skill stamp protocol meet here.
3. `close-tasks` — five artifact classes by name (:51,:57,:67) + writes back into the tasks doc (:162) + keys on other skills' block headings (:83-89).
4. `refactor-plan` / `hotfix-plan` — hardest gates; D4 splits them (file soft, review hard).
5. `integration-tasks` / `balanced-tasks-creation` — hard techspec gates; `balanced-tasks-creation:41` already grew three named escape hatches (a gate becoming a fallback organically).

## 2. Commands inventory

39 files: 38 tracked + `tasks-loop.md` (**symlink** → `~/projects/cc-looper/claude-config/commands/tasks-loop.md`; cc-looper's `src/cli/install.ts:107` also writes into `~/.claude/commands` from outside — two reasons D3 keeps the dir in place).

**Thin shims (15)** — already skill-centric; unchanged: `analyze-impact`, `bug-regression-test`, `create-post-mortem`, `diagnose`, `document-terraform`, `integration-analyze-feature`, `integration-create-tasks`, `integration-create-techspec`, `investigate-bug`, `lay-of-the-land`, `plan-hotfix`, `audit-skills`, `qa-gates`, `implementation-quality-assurance` (alias), `review-implementation`.

**Zero-skill commands (5)** — the extraction worklist; their logic exists nowhere else:

| Command | Size | Logic that needs a skill home |
|---|---|---|
| `document-workflow.md` | 373 lines | 9-step tracing (:44-165), ~190-line output template (:173-360), 95% confidence rule. **Highest value**: the template is duplicated verbatim in cc-looper's `document-workflow-loop:102-261` and already diverging (boundary-rows drift). `update-workflow-docs:58` names this command "the canonical contract". |
| `update-workflow-docs.md` | 82 | staleness triage Current/Stale/Unverifiable (:46-52), Edit-over-Write rule |
| `incident-status.md` | 254 | phase-state machine, file-existence scan, progress rendering |
| `start-incident.md` | 49 | dir naming, template copy from `templates/incident-response/` |
| `create-qa-scenarios.md` | 31 | scope branch, scenario categories (gray area: may be too small to mint) |
| **Partially logic-carrying (9)** | | `create-prd` (slice resolution + 5 quality gates), `gf-implement-task`/`implement-task`/`implement-bug-fix` (review hooks; `verify-task` covers only step 7), `integration-balanced-tasks:33-59` + `integration-pragmatic-techspec:30-48` (embedded reviewer checklists), `create-roadmap`/`create-techspec`/`create-tasks` (slice-resolution prose) |

**Orchestrators (5)**: 4 chain *skills* (`full-bug-fix-workflow`, `full-incident-response` — the only one with real skip routing via severity, `refactor-techdebt-dev`, `integration-feature-dev` — size-routed). **`greenfield-dev.md:39-57` chains slash commands**, the only one — harmless under D3 (commands keep working) but the outlier if the kit ever revisits D3.

**Argument conventions (recipes must preserve both):** `$ARGUMENTS` positional blob (20 files; three flavors — pass-through, parsed, prefix-glob) and the non-standard `arguments:` named-param frontmatter + `$name` in-body (11 files, same convention as the cc-looper fork skills).

**`templates/` collision (D3 context):** kit-level `templates/` = 8 user-input scaffolds in 5 family subdirs, indexed by 6 `INVENTORY/` files (`INVENTORY/templates.md:13` states the two-tier rule); skill-level `skills/*/templates/` = 5 output shells. The recipes dir must be a third, clearly-named thing.

## 3. Fork-pair drift (D1: deferred — recorded for the back-port list and the future cc-looper project)

| Pair | Drift | Notes |
|---|---|---|
| `implement-task-loop` vs `commands/implement-task.md` | **MAJOR, bidirectional** | Fork lacks any `verify-task` call (original's :45-56); fork frozen 2026-07-05, original changed 2026-07-23 (batched review) |
| `document-workflow-loop` vs `commands/document-workflow.md` | **MAJOR** | 190-line template duplicated + shape-diverged; fork fixed git-root anchoring the command still lacks |
| `qa-loop` vs `qa-gates` | **MAJOR, bidirectional** | qa-loop:209 claims "gate semantics are identical" — now false (BLOCKED outcome, compiled≠executed, committed-state exist only in qa-gates) |
| `qa-loop-docs` vs `qa-gates` | **MAJOR by design** | genuine re-specification for docs; has a post-freeze fix (provenance, 2026-06-26) with no qa-gates counterpart |
| `review-checkpoint` vs `review-implementation` | **MINOR** | cleanest pair; relationship documented in both directions |

**Back-port worklist (fork-only fixes to bring into ai-kit originals — the D1 consolation):**
1. `Baseline:` recording before first edit (`implement-task-loop:39-42`) → `implement-task` family checklist.
2. Denied-command ⇒ `Status: Blocked`, never `Done` (`implement-task-loop:61`) → `implement-task` family (`qa-gates` already has the analogous BLOCKED; the commands never surface it).
3. Git-root output anchoring (`document-workflow-loop:91-93`) → `document-workflow` (:169-171 is still ambiguous; cited downstream failure: doc "reported missing by qa-loop-docs Gate 1").
4. Never-worse-than-baseline (`qa-loop:107-112`) → `qa-gates`.
5. Produced-doc provenance + uniqueness (`qa-loop-docs`, commit `511226b`) → the ai-kit docs-QA path (no counterpart exists).

Risk note for #1/#2/#4: `qa-gates` and the implement commands changed 2026-07-23 (`50e7419`, batched review) — back-ports must be reconciled against that topology, not the forks' frozen assumptions.

## 4. Dependencies & preserved contracts

**Deployment:** `~/.claude/{commands,skills,agents}` are directory junctions → the repo dirs. The repo *is* the live install; every edit is live-on-save. No build step, no staging.

**Codex adapter** (`adapters/codex/sync.ps1` + `sync.sh`; cursor twins exist but `~/.cursor` is not deployed): `$CmdSrc` hardcoded to `commands/` (:86); the "generated command-skills" rule is a **static 10-name allowlist** (:214-221), not the dynamic detection the header comment (:32-40) describes; prune treats a missing `commands/<name>.md` as orphan → `Remove-Item -Recurse -Force` (:332-336). Deployed: 77 entries in `~/.codex/skills` (49 junctions + 28 generated copies). **Preserved contract under D3** — but minting a real `document-workflow` (or `update-workflow-docs`) skill makes its *generated* Codex twin redundant: the next sync must transition it deliberately (dry-run before `-Prune -Force`, per standing rule).

**cc-looper (external, D1):** runner binds `implement-task-loop` / `document-workflow-loop` / `run-task-loop` (`src/loop/skill-dispatch.ts:4-6`), `map-tasks` (`src/phases/plan.ts:430`), `review-checkpoint`, `close-tasks-loop`; installer writes into `~/.claude/commands` (`src/cli/install.ts:107`). Three cc-looper skills are not mirrored into ai-kit at all (`run-task-loop`, `qa-loop-generic`, `close-tasks-loop`) — the mirror set is partial.

**Anti-drift machinery (survives per D2):** `docs/output-filename-contract.md` (12-row table, zero drift as of 2026-07-19) + `audit-skills` Check 11 (:146-154). Two uncovered families it should gain rows for at plan time: loop/QA filenames (`<base>_qa.md`, `_checkpoint-<id>_review.md`, `plan.json` — parked as "canonical in cc-looper") and greenfield (`specs/00-roadmap.md`, `slices/slice-NN/…`).

**Cross-reference census:** 376 slash-refs across 76 files; 80 `commands/` path refs across 23 files. Heaviest: `INVENTORY/commands.md` (35), `triage` (29 routes; output contract is "user types the command"), `incident-status.md` (29). All remain valid under D3. `SESSION_LOG*.md` (47 combined) are historical record — never rewrite.

**Name-collision note:** `qa-gates` and `audit-skills` exist as both a command and a skill (benign twin pattern); `implement-task` and `tasks-loop` are command-only.

## 5. Scope definition

**In scope**
1. Input-contract fallbacks on the ~15 skills in §1's worklist, following the exemplar pattern; artifact gates soften, review gates stay (D4).
2. Extend `docs/output-filename-contract.md` with the input-fallback rule (+ the two missing family rows); extend Check 11 accordingly.
3. Extract skills from the 5 zero-skill commands (minting decision per file at plan time) and push residual logic out of the 9 partially-logic-carrying commands; commands become thin shims.
4. New `recipes/` dir (final name at plan time) for copyable chain templates + an INVENTORY entry.
5. Back-port the 5 fork-only fixes (§3) into ai-kit originals.
6. Codex/cursor adapter follow-through for any minted/changed skills (`sync.ps1` dry-run first; standing rule).

**Out of scope**
- cc-looper repo, the 6 symlinked loop skills, `commands/tasks-loop.md`, fork retirement / mode-parameter unification (deferred project).
- Vendored `find-skills`, `teach` (per `audit-skills:29`).
- Moving/renaming `commands/` or `templates/`; junction changes; codex allowlist mechanics beyond the follow-through above.
- `triage` rewrite; `greenfield-dev`'s command-chaining; SESSION_LOG history; review-gate semantics.

**Gray areas — need a decision at plan time**
- `recipes/` naming + whether recipes are generated from the thinned commands or authored fresh.
- Which of the 5 zero-skill commands actually deserve skills (`create-qa-scenarios` at 31 lines may not; `incident-status` is a state renderer — skill or command-native?).
- Context-cost budget: ~5 new skill descriptions land in every session's context; description discipline per `write-skills`.
- Whether the two argument conventions (`$ARGUMENTS` vs `arguments:`+`$name`) get normalized in the thinned commands or left as-is.
- Disposition of the generated-Codex twins once real skills exist (retire via prune vs keep until cc-looper project).

## 6. Risk classification

**Breaking-change risk (High if mishandled)**
- `document-workflow` extraction: the command body is a named canonical contract (`update-workflow-docs:58`) with a live duplicate in cc-looper. Mitigation: extraction must be format-preserving (byte-level on the output template), verified by diff against both copies.
- Back-ports into `qa-gates` / `implement-task` family: gate-semantics surface changed 2026-07-23. Mitigation: reconcile against `50e7419`'s batched-review topology, not the forks' frozen text.
- Codex sync after minting: prune transition of generated twins. Mitigation: `-DryRun` first, always.

**Non-breaking (Low)**
- Fallback-pattern additions to the ~15 skills (additive prose; exemplars already in production).
- `recipes/` dir creation + INVENTORY entry.
- Contract-doc/Check-11 extensions (tightening, not loosening).

**Unknown — investigate during planning**
- The 24 unread command bodies (tail misclassification risk for the extraction list).
- cc-looper's consumer-side assertions (`plan.json` content, Recommendation regex) — relevant only if a back-port touches an artifact the runner reads.
- Whether any `~/.claude`-external consumer (Codex `.system`, other machines) assumes the current generated-twin set.

## 7. Clarifying questions

All four blocking questions were answered (§ Decisions D1–D4). Remaining open items are the plan-time gray areas in §5 — none block the plan phase from starting.

---

**Next phase:** `refactor-plan` (Phase 3 of the refactor-techdebt flow; this audit skips the formal Phase-2 review unless requested) — input: this document, reviewed. Suggested first slices for the planner to weigh: (a) the ~15 fallback edits (lowest risk, immediately useful), (b) `document-workflow` extraction (highest value, highest care), (c) back-ports, (d) `recipes/`.
