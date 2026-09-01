# Linux portability and cross-agent coupling — analysis

Date: 2026-08-31
Mode: refactor
Input: `linux_portability_cross_agent_coupling_lay-of-the-land.md`
Repository revision analyzed: `8122041eaf`

## Review

**Review date:** 2026-08-31

**Post-review confidence:** **96%** — the two-root requirement, current deployment paths,
link/junction behavior, canonical coupling counts, and documentation closure were independently
re-grounded against the live repository and local filesystem.

**Recommendation:** **Approved with notes** — the reference map is sound after corrective edits.
The techspec must explicitly resolve Cursor's overlapping discovery roots, migration from an
existing whole-root Claude link/junction, ownership proof for force/reconciliation behavior, and
population-based acceptance checks. PowerShell, Windows, macOS, and Cursor runtime behavior remain
unverified on this computer.

## Overview

This refactor moves skill deployment from a Claude-primary, per-provider adapter posture to one
provider-neutral sync surface while preserving the 31 canonical skill directories and their
workflow contracts. It also makes surgical provider-neutral edits where current wording or
metadata carries real Claude Code, Codex, Cursor, Windows, or Unix assumptions, and adds a
repository-owned portability assurance surface.

**Complexity:** High · **Risk:** High · **Scope:** Large

## Confidence score

- Confidence score: **96%** — requirements clarity 40/40, codebase understanding 38/40,
  change-path clarity 18/20.
- 4% uncertainty — the repo has no existing automation host to follow; PowerShell, Windows,
  macOS, and Cursor runtime behavior could not be exercised on this Linux machine; the common
  sync implementation language and compatibility treatment of the old scripts remain design
  decisions.

## Scope definition

### In scope

- One common skill-sync surface for exactly two managed discovery roots:
  `~/.claude/skills` and `~/.agents/skills`.
- Per-skill symbolic links on Linux/macOS and directory junctions on Windows, keeping the git
  checkout as the single source.
- Equal Windows, Linux, and macOS support through that common surface.
- Surgical provider-neutral edits in canonical skills: invocation wording, instruction-file
  terminology, named harness tools, provider/model assumptions, loop routing, OS-specific paths,
  and frontmatter compatibility.
- Existing provider-specific files where genuine Codex/Cursor/Claude mechanics still need a
  narrow home; they cease to be the center of skill deployment.
- Automated checks for sync behavior, link ownership, frontmatter compatibility, shell/platform
  parity, and skill-count/documentation drift.
- Final migration and verification of this Linux computer against both managed roots.

### Out of scope

- Moving or renaming anchored `~/.claude` maintenance-data stores such as observations,
  improvements, ownership records, and audit state. This exclusion does not make
  `~/.claude/CLAUDE.md` the provider-neutral conventions contract.
- Reorganizing the `skills/` tree or rewriting complete prose sections whose purpose is not
  provider-specific.
- Changing skill names, workflow order, artifact names, approval gates, or confidence gates.
- Copy-based skill installation as the primary deployment model.
- Automatically deleting existing ai-kit links under `~/.codex/skills` or
  `~/.cursor/skills`.
- Reworking archived v1 source except where a live document treats it as current.
- Installing Cursor or PowerShell on this computer solely for verification.
- Rewriting the captured provider source `claude_guide_loop_engineering.md`; it remains a
  historical input rather than a canonical convention surface.

### Gray areas — design decision required

- The common script's language and repository location.
- Whether the four current adapter sync scripts become thin compatibility entry points or are
  marked retired while remaining in place.
- Whether frontmatter assurance uses one common subset, provider profiles, or both.
- Whether Codex's installed validator remains advisory or becomes one release gate among several.
- The new automation runner and CI file location; no live repo precedent exists.
- Whether the two old portability assessments receive historical banners or new superseding
  records while preserving their durable decisions.
- Later cleanup of legacy `~/.codex/skills` links; this is approval-gated and not part of the
  common sync's automatic behavior.
- How Cursor's compatibility scan of `~/.claude/skills` and `~/.codex/skills` is reconciled with
  the requested `~/.agents/skills` population. Current docs and a prior live probe show overlapping
  roots can duplicate skills; precedence and deduplication are not established on this machine.
- How an existing whole-root `~/.claude/skills` symlink or Windows junction transitions to the
  requested per-skill layout without being mistaken for a successful populated root.
- Local migration handling for the two empty real directories currently occupying
  `~/.agents/skills/find-skills` and `~/.agents/skills/teach`; replacing filesystem entries is
  approval-gated even when they are empty.

## Preserved contracts

1. `skills/<name>/SKILL.md` remains the single workflow source.
2. The 31 skill names and directory-name equality remain unchanged.
3. Skills remain independently discoverable and explicitly invocable by name.
4. Existing input contracts, including the three skills that consume named arguments, remain
   behaviorally available.
5. `teach` remains explicit-only rather than becoming an implicitly triggered teaching workflow.
6. Cross-skill workflow order and artifact filename contracts remain unchanged.
7. `~/.claude` maintenance data remains anchored; its storage location does not make
   `CLAUDE.md` canonical provider-neutral guidance.
8. Non-kit entries in either managed root are never overwritten.
9. Link replacement requires an explicit force path; orphan cleanup remains report-first.
10. A link or junction target is never deleted by sync or cleanup behavior.
11. Dry-run remains non-mutating and supports an isolated home/root for verification.
12. Private user convention files are not overwritten by public kit instructions.
13. Public-repo paths remain generic and do not expose machine- or client-specific details.
14. Existing directory and document section structures remain intact unless an entire block is
    provider-specific.
15. `AGENTS.md` is the provider-neutral conventions contract. Generic/global `CLAUDE.md`
    references move toward that contract; the five literal `~/.claude/CLAUDE.md` workflow targets
    in `improve` require surgical classification rather than automatic preservation or replacement.

## Entry points

### User-facing deployment

| Consumer | Current entry point | Current target | Refactor pressure |
| --- | --- | --- | --- |
| Claude Code | `README.md:56-70` | `~/.claude/skills` | Manual whole-root junction/symlink; described as the baseline |
| Codex POSIX | `README.md:72-81`, `adapters/codex/README.md:32-43` | `~/.codex/skills` | Broken v1 shell path and provider-private root |
| Codex PowerShell | Same docs | `~/.codex/skills` | Current v2 reference, but provider-private root |
| Cursor POSIX | `README.md:83-92`, `adapters/cursor/README.md:40-58` | `~/.cursor/skills` | Current v2 logic, but provider-private root |
| Cursor PowerShell | Same docs | `~/.cursor/skills` | Windows parity for the provider-private root |
| Requested common surface | New entry point | `~/.claude/skills`, `~/.agents/skills` | One provider-neutral population pass |

### Canonical policy entry points

- `skills/write-skills/SKILL.md:31-56,90-91` defines the portable profile, invocation wording,
  and post-authoring sync behavior.
- `skills/audit-skills/SKILL.md:51-70` owns structural frontmatter policy.
- `skills/triage/SKILL.md:82-107,123-126` emits skill/loop routing and names the structured
  question tool.
- `skills/orchestrate/SKILL.md:21-41` owns provider/model, parallel-worker, resume, and tool-grant
  mechanics.
- `skills/close/SKILL.md` and `skills/improve/SKILL.md` own the anchored maintenance loop and
  contain the remaining hard-coded Windows repo path.
- `docs/rules/skill-authoring.md:3-63,107-135` owns strict YAML, deployment topology, and
  population/documentation synchronization.

## Execution flow

### Current deployment flow

1. A canonical `skills/<name>/SKILL.md` is authored or changed.
2. Claude Code relies on a manually established `~/.claude/skills` link.
3. Codex and Cursor each use separate shell/PowerShell scripts to enumerate the same source and
   create per-skill links in provider-private homes.
4. Adapter instructions translate invocation, fan-out, model, question, and loop mechanics.
5. The user restarts the selected agent and manually checks discovery.

This duplicates enumeration, ownership, prune, and documentation behavior across four scripts.
The Codex v2 reconciliation changed PowerShell and its docs without changing the shell peer,
leaving Linux on the retired command-generation path.

### Requested deployment flow

1. The common sync enumerates canonical skill directories once.
2. Each canonical skill is represented by one per-skill filesystem link in each managed root:
   `~/.claude/skills/<name>` and `~/.agents/skills/<name>`.
3. Link ownership, conflict reporting, dry-run, and any explicit cleanup rules are applied
   consistently to both roots.
4. Claude Code reads its native root and Codex reads the shared Agent Skills root. Cursor's current
   compatibility loader reads both managed roots and legacy Codex locations, so its effective
   population and precedence must be treated as an overlapping-root seam rather than assumed to
   come only from `~/.agents/skills`.
5. Provider-specific instruction files cover only mechanics that cannot be expressed neutrally
   in a canonical skill.
6. Repository-owned checks exercise the population and documentation contracts.
7. The final refactor run applies this flow on the current Linux computer and verifies both roots
   plus every locally available agent runtime.

The exact script language, command interface, and compatibility-wrapper shape remain for design.

## Similar features and examples

| Reference | Pattern available to reuse |
| --- | --- |
| `adapters/cursor/sync.sh:77-113` | Current v2 skills-only enumeration and empty retired-command list |
| `adapters/cursor/sync.sh:150-165` | Plain-entry iteration intended to see dangling links |
| `adapters/cursor/sync.ps1:95-105` | Reparse-point inspection that does not depend on a live target |
| `adapters/codex/sync.ps1:111-140` | Resolved-target comparison and explicit force path; useful mechanics, but not proof that a conflicting reparse point is kit-owned |
| `adapters/codex/README.md:45-50` | Managed instruction-block contract that preserves private conventions |
| `skills/write-skills/SKILL.md:31-40` | Existing cross-tool frontmatter and body profile |
| `skills/find-skills/SKILL.md:1-18` | Two-key frontmatter and capability-oriented wording with no provider hits |
| `skills/qa-gates/SKILL.md:167-172,280-285` | Generic “ask the user” and unprefixed skill-name wording |
| `skills/review-implementation/SKILL.md:38-52` | Generic reviewer fan-out and dual `AGENTS.md / CLAUDE.md` terminology |
| `.gitattributes:1-3` | Existing LF checkout enforcement for shell files |
| `docs/model-assignments.md:1-4` | Historical banner that separates retired material from a live section |
| Commit `bc3e6b7` | Seven-file Cursor v2 reconciliation across scripts, docs, inventory, and EOL rule |
| Commit `bb43f67` | Codex v2 reconciliation whose omission of `sync.sh` exposes the parity risk |
| Commit `97811a3` | Cross-skill rename with enumerated documentation and caller closure |

## Key components and responsibilities

### Canonical skill corpus

All 31 `SKILL.md` files contain the reusable workflows. They are linked directly rather than
transformed, so any canonical edit is immediately visible to all consumers after discovery or
restart.

### Discovery roots

`~/.claude/skills` is the retained Claude Code root. `~/.agents/skills` is the requested shared
Codex/Cursor root and already contains unrelated user skills on this computer, making per-skill
ownership essential; a whole-root replacement would not preserve coexistence.

The public install path currently documents `~/.claude/skills` itself as a whole-root symlink or
Windows junction. That topology and the requested per-skill layout expose different entry types to
a sync. Existing adapter logic can walk through the root link, classify its children as real
directories, and report success without establishing per-skill ownership. This is a migration
contract for existing machines, not merely a fresh-install case.

The local probe found 31 current ai-kit relative links under `~/.claude/skills` and zero ai-kit
links under `~/.agents/skills`. The latter root contains two empty real directories named
`find-skills` and `teach`; they collide with canonical skill names and are visible migration
decisions rather than entries the common sync can silently replace.

### Existing provider adapters

The eight files under `adapters/codex/` and `adapters/cursor/` currently mix two roles:
skill deployment and provider-mechanics explanation. The refactor removes deployment from the
center of these files but retains a narrow place for mechanics that are genuinely provider-only.

### Authoring and audit policy

`write-skills` creates conventions that propagate across the corpus. `audit-skills` validates
those conventions. Their current Claude-specific framing and different metadata allowlists make
them higher-risk than ordinary prose references.

### Automated assurance

No tracked CI workflow, test/spec directory, package runner, Makefile, Justfile, Taskfile,
`pyproject.toml`, or `package.json` was found in the live tree. The four existing sync scripts
nevertheless expose useful test seams: dry-run flags, home overrides, and stable result summaries.
Exit status alone is not a complete acceptance signal: current scripts treat skipped real-directory
collisions as success, even when the requested population is incomplete.

## Architecture insights

| Concern | Current health | Evidence |
| --- | --- | --- |
| Canonical source model | High | 31 one-to-one `skills/<name>/SKILL.md` directories; adapters link rather than transform |
| Workflow structure | High | Skill names, phase order, artifacts, and review gates are centrally documented |
| Provider-neutral language | Low-medium | Claude invocation and harness vocabulary remains widespread |
| Deployment cohesion | Low | Manual Claude link plus four provider-specific scripts and three roots |
| POSIX/PowerShell parity | Low | Codex shell retains ten retired commands while PowerShell has an empty list |
| Link ownership | Low on POSIX | Raw `readlink` comparison rejects equivalent relative targets |
| Force ownership proof | Low on all four scripts | A conflicting link/reparse point is replaceable without proving ai-kit ownership |
| Documentation quality | Medium | Detailed records exist, but counts, topology, and capability facts have drifted |
| Provider-fact freshness | Low-medium | Static adapter prose repeats version-sensitive runtime claims |
| Automated assurance | Low | Only LF attributes and ad-hoc/manual checks exist |

The main structural strength is the one-directory-per-skill source model. The main architectural
liability is not the `adapters/` directory itself; it is that deployment ownership and current
provider facts are duplicated across files that drift independently.

## Dependencies

### Internal

- `skills/` directory enumeration and the `name == directory` rule.
- `README.md`, `INVENTORY.md`, and `docs/rules/skill-authoring.md` population contracts.
- `docs/output-filename-contract.md` and cross-skill workflow references.
- Existing adapter dry-run, link ownership, validation, and instruction-placement behavior.
- The anchored maintenance-data contracts plus surgical classification of convention-file
  references against the provider-neutral `AGENTS.md` contract.

### External

- Filesystem symbolic-link support on Linux/macOS.
- Windows directory junction/reparse-point support.
- Claude Code discovery from `~/.claude/skills`.
- Codex discovery from `~/.agents/skills`; Cursor discovery from that root plus its documented
  Claude/Codex compatibility roots.
- The installed Codex validator under the Codex-owned `.system/skill-creator` tree.
- A future automation environment capable of exercising the selected common script on each OS.

Current provider references used for volatile behavior:

- [Codex Agent Skills](https://learn.chatgpt.com/docs/build-skills)
- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Cursor Agent Skills](https://prod.cursor.com/docs/skills)
- [Cursor subagents](https://prod.cursor.com/docs/subagents)

## Observations

### Strengths

- The canonical workflows already use the cross-agent `SKILL.md` shape.
- Provider adapters are additive and do not transform live skill bodies.
- Existing scripts preserve real user directories by default and mark dormant generated entries,
  but their force paths do not prove that a conflicting link/reparse point is kit-owned.
- Dry-run and force/prune concepts already exist across platforms.
- The corpus contains provider-neutral wording patterns that can replace specific terms without
  changing whole blocks.
- The anchored maintenance-store exception is explicit and testable.

### Issues

- `adapters/codex/sync.sh:71-94` still generates ten retired v1 commands and fails a clean-home
  Linux dry run.
- Both POSIX scripts compare raw link strings with absolute targets, so equivalent relative links
  are reported as conflicts.
- `adapters/codex/sync.sh:97-103` prints a copy instruction that contradicts the managed-block
  contract in its README and PowerShell peer.
- Twenty-five skill descriptions contain case-insensitive `Invoke as /...` wording.
- A strict live-skill/primitive slash scan found 297 occurrences across 29 skills; these include
  both invocation contracts and ordinary cross-skill references, so they require classification
  rather than bulk replacement. A looser word-boundary probe returns 300 by also counting three
  path-prefix false positives.
- Fifteen skills contain 35 `CLAUDE.md` references.
- Generic/global convention uses within those references target the provider-neutral `AGENTS.md`
  contract in this refactor. The five literal `~/.claude/CLAUDE.md` targets, all in `improve`,
  require contextual classification and are not covered by the anchored maintenance-data exception.
- Four skills contain provider/model-specific terms, and behavior-bearing tool vocabulary appears
  in routing, questions, fan-out, resume, file discovery, and verification workflows.
- Three skills contain 10 literal `C:\ai-kit` occurrences across eight source lines.
- Four skills carry five extra frontmatter fields rejected by the installed Codex validator.
- The README has two stale 30-skill statements while the tree and inventory contain 31.
- The two portability assessments mix durable decisions with retired v1 counts and mechanisms.
- Current Cursor documentation and the prior live Cursor assessment show that Cursor loads
  `~/.agents/skills` as well as compatibility roots including `~/.claude/skills` and
  `~/.codex/skills`; the requested two-root population therefore has a duplicate-discovery seam.

### Opportunities within the approved boundary

- A common two-root sync surface removes four-way skill-population-script duplication without
  moving canonical skills or the anchored maintenance store; Cursor discovery overlap remains a
  separate design seam.
- Existing neutral phrases allow line- or sentence-level edits instead of document rewrites.
- Dry-run home overrides allow isolated local-machine verification without touching normal roots.
- Current drift classes are mechanically checkable: population count, frontmatter parse/profiles,
  shell syntax, clean-home sync, repeated provider terms, and documentation count consistency.

## Anti-patterns found

| Anti-pattern | Locations | Impact |
| --- | --- | --- |
| One provider treated as the canonical vocabulary | README, 25 descriptions, workflow diagrams | Other agents require translation even when the workflow itself is neutral |
| Duplicated platform implementations without parity enforcement | Four sync scripts | Windows-authoritative changes can leave Linux/macOS broken |
| Raw link-string equality | Both POSIX sync scripts | Correct relative links appear stale; ownership/prune classification is representation-sensitive |
| Force treated as ownership | All four sync scripts | A same-name link can be replaced without evidence that ai-kit created it |
| Overlapping discovery roots | Requested Claude + shared roots; Cursor compatibility loader | One canonical skill can be listed more than once and precedence is unverified |
| Provider facts embedded as durable prose | Both adapter `AGENTS.md` files and READMEs | Runtime releases invalidate instructions independently of repo changes |
| Portable profile treated as an exception | `skills/write-skills/SKILL.md:31-40` | New canonical skills reproduce provider coupling by default |
| Provider-specific metadata accepted as universally valid | `audit-skills`, four exceptional skills | A skill can pass one harness policy and fail another validator |
| Manual population synchronization | README/INVENTORY/rule | The current 30-versus-31 drift escaped the documented process |
| Historical and current claims mixed in one record | Both portability assessments | Readers cannot reliably distinguish decisions from obsolete mechanisms |

## Change surface

The rows below identify landing zones. They do not prescribe exact code or whole-block rewrites.

### Files to Modify

| File or exact group | Purpose | Changes needed at analysis altitude |
| --- | --- | --- |
| `README.md` | Public identity and install entry point | Provider-neutral framing, common two-root sync entry, accurate count |
| `INVENTORY.md` | Population and document status index | Keep count/status closure with README and assessment history |
| `AGENTS.md` | Loaded repo-rule index | Align the rule description with current provider-neutral deployment topology |
| `docs/rules/skill-authoring.md` | Authoring, validation, population, deployment rules | Replace Windows-authoritative/v1 topology and connect automated assurance |
| `docs/loop-recipes.md` | Provider-specific loop/scheduler mapping | Keep provider-only material explicit; cover equal-OS constraints without changing neutral skills wholesale |
| `agentic_auto_scheduling_experimental_study_research_action_items.md` | Live research-action input with a standing Codex-sync instruction | Update the one operational deployment reference surgically; leave the research content intact |
| `docs/codex-portability-assessment.md` | Historical decision record | Separate durable decisions from retired v1/runtime facts |
| `docs/cursor-portability-assessment.md` | Historical decision record | Same historical/current boundary |
| `adapters/codex/{sync.sh,sync.ps1,README.md,AGENTS.md}` | Current Codex deployment plus mechanics | Remove skill-deployment primacy; retain only necessary compatibility/mechanics references |
| `adapters/cursor/{sync.sh,sync.ps1,README.md,AGENTS.md}` | Current Cursor deployment plus mechanics | Same boundary for the shared `.agents` root |
| 25 skill descriptions enumerated below | Skill discovery/invocation | Replace Claude slash-only invocation wording surgically |
| 15 skills with `CLAUDE.md` references | Convention lookup or workflow target | Move generic/global convention language toward `AGENTS.md`; classify five literal `~/.claude/CLAUDE.md` targets in `improve` contextually |
| `skills/{write-skills,audit-skills}/SKILL.md` | Convention creation and structural audit | Make provider-neutral behavior the default and align metadata/assurance policy |
| `skills/{triage,orchestrate,close}/SKILL.md` | Routing, fan-out, context/reset behavior | Isolate genuine provider mechanics while preserving workflow blocks |
| `skills/{improve,docs-tasks-creator,document-terraform,review-artifact,lay-of-the-land,bug-investigation,onboard-me,qa-gates,verify-task,compile-kb,walkthrough-implementation,tasks-breakdown,analyze-work,review-implementation}/SKILL.md` | Behavior-bearing provider/tool/convention references | Classify and make only the necessary line/sentence edits |
| `skills/{compile-kb,docs-tasks-creator,document-terraform,teach}/SKILL.md` | Non-common frontmatter | Preserve argument/explicit-invocation behavior across provider validation |
| `.gitattributes` | LF portability guard | Verification surface; modification only if the chosen common script adds a relevant file class |

The mechanical audit envelope is 30 of 31 skills; this is not a commitment to change all 30.
`skills/find-skills/SKILL.md` is the only no-hit reference and is a neutral example. Every candidate
must be read in context; ordinary words such as “Read” and cross-skill `/name` references are not
automatically defects.

The 25 description targets are: `analyze-work`, `audit-skills`, `breakout-session`,
`bug-investigation`, `close`, `close-tasks`, `compile-kb`, `document-workflow`, `implement-task`,
`improve`, `onboard-me`, `orchestrate`, `post-mortem`, `qa-gates`, `record-decision`,
`review-artifact`, `review-implementation`, `tasks-breakdown`, `techspec`,
`triage-learning-content`, `triage`, `update-workflow-docs`, `walkthrough-implementation`,
`walkthrough`, and `write-skills`.

### Files to Create

| File | Purpose | Type |
| --- | --- | --- |
| New path — techspec decision | Common cross-platform two-root skill sync | Utility/script |
| New path — techspec decision | Automated portability and compatibility checks | Test/validation utility |
| New path if CI is selected — techspec decision | Run portable checks in supported environments | CI configuration |

### APIs Affected

No application or network API is affected. User-facing command flags, environment overrides,
exit status, managed discovery roots, and skill metadata are CLI/filesystem transition contracts.
The safety behavior is preserved above; exact legacy flag/environment compatibility and exit
semantics remain design decisions for the common surface and compatibility entry points.

### Database Changes

No database, schema, state-store, or data-model change is present.

## Mechanical caller and reference closure

### Provenance

The canonical closure was derived by enumerating the 31 real `skills/*/SKILL.md` files, scanning
known skill/primitive slash tokens and provider categories, then counting boundary-matched skill
names in every other canonical body. `archive/` was not part of the population. For the slash
count, the live token set is the 31 directory names plus `goal`, `loop`, `schedule`, `tasks-loop`,
`compact`, and `clear`; the suffix boundary rejects `[a-z0-9-]`. That probe returns 297
occurrences across 29 files. A `\\b` suffix returns 300 because it also matches `/loop` inside
`docs/loop-recipes.md` once and `/close` inside the two `close-tasks-loop` path segments. The
provider/model count uses the case-sensitive alternatives
`Claude Code|Cursor|Codex|Opus|Fable|Haiku`. `CLAUDE.md` occurrences were counted with `rg -o`,
not matching-line count.

Reproducible probe: set `live_skill_tokens` from
`find skills -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | LC_ALL=C sort | paste -sd'|' -`,
then run
`rg -o --pcre2 "/(?:${live_skill_tokens}|goal|loop|schedule|tasks-loop|compact|clear)(?=$|[^a-z0-9-])" skills/*/SKILL.md | wc -l`.
The other aggregate commands are
`rg -o -F 'CLAUDE.md' skills/*/SKILL.md | wc -l` and
`rg -o '\b(Claude Code|Cursor|Codex|Opus|Fable|Haiku)\b' skills/*/SKILL.md | wc -l`.

Key population results:

- 31 canonical skills.
- 25 descriptions with case-insensitive `Invoke as /...`.
- 30 files in the broad lexical audit envelope; `find-skills` is the sole no-hit file.
- 29 files with 297 exact live `/skill` or `/primitive` occurrences; a loose lexical boundary
  returns 300 candidates, including three path-prefix false positives.
- 15 files with 35 `CLAUDE.md` occurrences.
- 4 files with 31 provider/model-name occurrences.
- 3 files with 10 `C:\ai-kit` occurrences across eight lines.
- 4 files with five extra frontmatter fields.

### Canonical skill-name closure

Counts are literal boundary-matched references from other canonical skills, not runtime invocation
telemetry.

| Candidate skill | Referencing skills | Occurrences | Enumerated canonical references |
| --- | ---: | ---: | --- |
| `analyze-work` | 7 | 25 | bug-investigation:1, close:1, lay-of-the-land:5, review-artifact:6, techspec:4, triage:7, write-skills:1 |
| `audit-skills` | 2 | 13 | improve:2, write-skills:11 |
| `breakout-session` | 0 | 0 | — |
| `bug-investigation` | 7 | 26 | analyze-work:1, document-workflow:1, lay-of-the-land:4, post-mortem:4, review-artifact:6, techspec:3, triage:7 |
| `close` | 12 | 66 | audit-skills:6, close-tasks:30, improve:6, qa-gates:4, record-decision:7, review-implementation:1, tasks-breakdown:1, techspec:1, triage:4, update-workflow-docs:1, verify-task:3, write-skills:2 |
| `close-tasks` | 2 | 4 | close:3, improve:1 |
| `compile-kb` | 3 | 4 | close:1, orchestrate:2, triage-learning-content:1 |
| `docs-tasks-creator` | 3 | 7 | document-terraform:1, document-workflow:4, update-workflow-docs:2 |
| `document-terraform` | 2 | 2 | document-workflow:1, triage:1 |
| `document-workflow` | 5 | 22 | compile-kb:2, docs-tasks-creator:9, document-terraform:1, triage:1, update-workflow-docs:9 |
| `implement-task` | 8 | 18 | close:1, close-tasks:2, document-workflow:1, post-mortem:2, review-implementation:3, tasks-breakdown:2, triage:5, verify-task:2 |
| `improve` | 10 | 41 | audit-skills:15, close:3, close-tasks:8, post-mortem:1, qa-gates:2, review-implementation:1, triage:2, verify-task:4, walkthrough:3, write-skills:2 |
| `lay-of-the-land` | 6 | 10 | analyze-work:3, bug-investigation:2, document-workflow:1, tasks-breakdown:1, techspec:1, triage:2 |
| `onboard-me` | 4 | 8 | breakout-session:3, record-decision:1, triage:1, walkthrough-implementation:3 |
| `orchestrate` | 0 | 0 | — |
| `post-mortem` | 5 | 10 | bug-investigation:2, qa-gates:1, review-artifact:1, techspec:1, triage:5 |
| `qa-gates` | 8 | 44 | implement-task:1, post-mortem:5, review-implementation:13, tasks-breakdown:1, triage:4, verify-task:16, walkthrough:2, walkthrough-implementation:2 |
| `record-decision` | 3 | 5 | close:3, onboard-me:1, triage:1 |
| `review-artifact` | 9 | 17 | analyze-work:1, bug-investigation:1, implement-task:1, qa-gates:2, review-implementation:3, tasks-breakdown:3, techspec:2, triage:3, verify-task:1 |
| `review-implementation` | 6 | 17 | implement-task:4, qa-gates:6, review-artifact:1, triage:3, verify-task:1, walkthrough-implementation:2 |
| `tasks-breakdown` | 4 | 12 | qa-gates:1, review-artifact:6, techspec:1, triage:4 |
| `teach` | 1 | 8 | breakout-session:8 |
| `techspec` | 15 | 116 | analyze-work:4, audit-skills:4, bug-investigation:3, close-tasks:1, implement-task:11, lay-of-the-land:2, post-mortem:6, qa-gates:13, record-decision:3, review-artifact:18, review-implementation:2, tasks-breakdown:26, triage:15, verify-task:5, walkthrough-implementation:3 |
| `triage` | 8 | 11 | close-tasks:1, compile-kb:1, document-workflow:1, lay-of-the-land:1, orchestrate:1, triage-learning-content:4, update-workflow-docs:1, write-skills:1 |
| `triage-learning-content` | 0 | 0 | — |
| `update-workflow-docs` | 1 | 1 | document-workflow:1 |
| `verify-task` | 3 | 10 | close-tasks:1, implement-task:2, qa-gates:7 |
| `walkthrough` | 3 | 10 | breakout-session:1, onboard-me:4, walkthrough-implementation:5 |
| `walkthrough-implementation` | 1 | 1 | triage:1 |
| `write-skills` | 2 | 4 | audit-skills:3, close:1 |

`find-skills` has no provider-coupling hit and no canonical caller hit; it remains the reference
example rather than a change candidate.

### Deployment/document reference closure

Probe scope: live source outside `archive/`, `SESSION_LOG.md`, drafts, and the two new analysis
artifacts; each target file was excluded from its own reference list.

| Target | Ref files | Enumerated references |
| --- | ---: | --- |
| `adapters/codex/sync.sh` | 2 | README, Codex README |
| `adapters/codex/sync.ps1` | 6 operational | README, Codex AGENTS, Codex README, Codex assessment, write-skills, loop-engineering action items |
| `adapters/codex/AGENTS.md` | 4 | README, Codex sync.ps1, Codex assessment, Codex README |
| `adapters/codex/README.md` | 2 | both Codex sync scripts |
| `adapters/cursor/sync.sh` | 3 | README, Cursor AGENTS, Cursor README |
| `adapters/cursor/sync.ps1` | 1 | Cursor README |
| `adapters/cursor/AGENTS.md` | 5 | both Cursor scripts, Cursor README, README, Cursor assessment |
| `adapters/cursor/README.md` | 4 | README, INVENTORY, both Cursor scripts |
| `docs/rules/skill-authoring.md` | 3 | AGENTS, INVENTORY, write-skills |
| `docs/loop-recipes.md` | 2 | INVENTORY, triage |
| `docs/codex-portability-assessment.md` | 3 | INVENTORY, Codex README, Codex sync.ps1 |
| `docs/cursor-portability-assessment.md` | 3 | Cursor README, INVENTORY, Codex assessment |
| `INVENTORY.md` | 3 | README, skill-authoring rule, write-skills |

The deployed `/home/jleung/.codex/AGENTS.md` contains a copied kit-mechanics block rather than a
link. A source Codex instruction change therefore has an out-of-repo manual refresh consumer.

## Side effects and impact

- The common sync writes link entries outside the repository in two user-home roots.
- Canonical skill edits become immediately visible through both roots because links share the
  source; agent restart/discovery behavior remains provider-owned.
- Existing unrelated skills under `~/.agents/skills` and `~/.claude/skills` coexist with the kit,
  so ownership classification affects user data safety.
- Existing whole-root Claude links/junctions require an explicit transition disposition before a
  per-skill sync can claim ownership or completion.
- This machine's two empty `.agents` name collisions (`find-skills`, `teach`) prevent a clean
  31-skill shared-root result until they are explicitly resolved; the default safe behavior is to
  report them, not replace them.
- Existing kit links under `~/.codex/skills` remain in place and may temporarily create duplicate
  discovery until separately reviewed and, with approval, cleaned up.
- Cursor also scans `~/.claude/skills` and `~/.codex/skills` for compatibility, so populating
  `~/.agents/skills` can duplicate every kit skill even without a `~/.cursor/skills` population.
- Adapter instruction edits do not automatically update private copied include blocks.
- Frontmatter changes can change explicit invocation or argument behavior even when the body text
  is untouched.
- Local-machine acceptance must verify the exact 31-skill population in each managed root rather
  than trust exit status. Installed Codex/Claude discovery can be exercised, but legacy Codex roots
  confound source attribution unless the design supplies a disambiguating check. Cursor discovery
  remains unavailable unless the runtime is present by refactor completion.
- No application API, database, network service, or business-data side effect exists.

## Risks and considerations

| Severity | Risk | Affected surface |
| --- | --- | --- |
| Critical | None identified | — |
| High | Common link ownership misclassifies a non-kit entry | Both managed roots and any force/cleanup path |
| High | Cursor loads both requested roots and legacy compatibility roots, duplicating skill discovery or making precedence ambiguous | Cursor runtime and local acceptance |
| High | Cross-platform logic works on Linux but fails on Windows junctions or macOS links | New common sync and automation matrix |
| High | Metadata normalization drops arguments or `teach` explicit-only behavior | Four exceptional skills plus audit/write policy |
| High | Provider-neutral wording changes subagent, model, resume, or loop semantics | orchestrate, triage, close, provider instruction files |
| High | Broad mechanical replacement alters workflow prose unnecessarily | 30-file lexical envelope; surgical-edit constraint |
| Medium | Legacy provider-private links cause duplicate discovery | Current `~/.codex/skills`; possible Cursor legacy state |
| Medium | Existing whole-root Claude link/junction is mistaken for a complete per-skill deployment | Cross-machine migration and acceptance |
| Medium | Empty local real directories block two shared-root links | `~/.agents/skills/find-skills`, `~/.agents/skills/teach` |
| Medium | Skipped collisions still produce a successful sync exit status | Population completeness checks |
| Medium | Compatibility entry points drift from the common sync | Four existing adapter scripts |
| Medium | Historical assessment cleanup erases durable decisions | Both portability assessments |
| Medium | External validators change independently | Installed Codex `.system` validator and provider runtimes |
| Medium | Private instruction include blocks stay stale | Deployed Codex/Cursor user convention files |
| Low | Public skill count or examples drift again | README, INVENTORY, authoring rule |
| Low | LF guarantee misses a new script type | `.gitattributes` and automation checks |
| Unknown | Exact automation host and cross-OS runner | No existing repository convention |
| Unknown | Cursor runtime conformance on this machine | `cursor-agent` absent during analysis |

## Essential files

### Core requirements and output

- `linux_portability_cross_agent_coupling_lay-of-the-land.md`
- `linux_portability_cross_agent_coupling_analysis.md`

### Deployment and provider mechanics

- `README.md`
- `adapters/codex/{sync.sh,sync.ps1,README.md,AGENTS.md}`
- `adapters/cursor/{sync.sh,sync.ps1,README.md,AGENTS.md}`
- `.gitattributes`

### Canonical policy and documentation

- `INVENTORY.md`
- `AGENTS.md`
- `docs/rules/skill-authoring.md`
- `docs/loop-recipes.md`
- `agentic_auto_scheduling_experimental_study_research_action_items.md`
- `claude_guide_loop_engineering.md` — captured provider source, explicitly preserved verbatim
- `docs/output-filename-contract.md`
- `docs/{codex,cursor}-portability-assessment.md`
- `docs/model-assignments.md`

### Highest-risk canonical skills

- `skills/{write-skills,audit-skills,triage,orchestrate,close,improve}/SKILL.md`
- `skills/{compile-kb,docs-tasks-creator,document-terraform,teach}/SKILL.md`
- The caller-closure table above for the remaining surgical audit envelope.

### External verification dependency

- `~/.codex/skills/.system/skill-creator/scripts/quick_validate.py` — current installed Codex
  validator; external and version-owned, not a repository source file.

## Recommended next step

Proceed to `techspec`. It can decide the common script language/location, compatibility treatment
of the current adapter scripts, metadata compatibility model, automation host, overlapping-root
handling, ownership proof, and exact local-machine migration checks without reopening the scope or
the preserved contracts above.
