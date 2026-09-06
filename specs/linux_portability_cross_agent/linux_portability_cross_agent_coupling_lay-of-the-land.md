# Linux portability and cross-agent coupling — lay of the land

Date: 2026-08-31
Repository revision inspected: `8122041eaf`
Mode: current-state reconnaissance

## Understanding

The kit was originally maintained from Windows and is now being used primarily from Linux,
with Codex as the main agent and Cursor as a secondary agent. This reconnaissance maps
operating-system assumptions and Claude Code coupling before any remediation is designed.

The maintenance feedback loop is an explicit boundary: skills such as `close`, `improve`,
and `audit-skills` may continue to read from and write maintenance data under `~/.claude`.
Moving observations, improvements, ownership records, and audit state to `.agents`, `.codex`,
or another generic location is out of scope. This storage exception does not make
`~/.claude/CLAUDE.md` the provider-neutral conventions contract: generic/global convention
references target `AGENTS.md`, while literal workflow targets require later surgical
classification.

## Confidence

- Confidence score: **95%** — the live skill and adapter inventory was read, Linux static
  checks and dry runs were executed, the installed Codex runtime was probed, and current
  official Codex and Cursor documentation was checked.
- 5% uncertainty — Cursor and PowerShell are not installed on this Linux machine, no
  apply-mode deployment was performed, and Windows/macOS behavior was not tested live.

## Scope

### In scope

- The 31 live canonical skills under `skills/`.
- Codex and Cursor adapter instructions, sync scripts, and deployment documentation.
- Root documentation and repo rules that describe operating-system or provider behavior.
- Current Linux behavior and current documented Codex/Cursor capabilities.
- Claude-specific vocabulary, tool names, invocation syntax, models, and loop primitives
  where they constrain use from Codex or Cursor.

### Out of scope

- Relocating anchored `~/.claude` maintenance-data stores such as observations, improvements,
  ownership records, and audit state. Convention-file references are assessed separately.
- Changing live skills, adapters, or deployment state during reconnaissance.
- The archived v1 implementation under `archive/v1/`, except where live documents still
  depend on its assumptions.
- Runtime verification in Cursor, PowerShell, Windows, or macOS.
- Designing the remediation; that belongs to the following analysis and design phases.

## Findings

### 1. The canonical skill corpus is broadly portable

The live corpus contains 31 real skill directories, each with a `SKILL.md`. Their workflow
bodies are predominantly Markdown instructions rather than executable provider code. This
matches the Agent Skills format supported by current Codex and Cursor documentation.

The repository already provides both POSIX shell and PowerShell deployment entry points,
and `.gitattributes:1-3` enforces LF endings for shell scripts. Both adapter shell scripts
pass `bash -n`. No tracked executable files, tracked symlinks, case-folding collisions, or
CRLF shell files were found in the live surface.

### 2. The Linux Codex deployment path is currently broken

`adapters/codex/sync.sh:2-4` declares the shell adapter to be the POSIX parity surface while
the PowerShell implementation remains authoritative. The two implementations have drifted:

- `adapters/codex/sync.ps1:195-203` has the v2 command-generation list set to empty.
- `adapters/codex/sync.sh:71-94` still expects 10 retired v1 command files.
- A clean temporary-home `sync.sh --dry-run` exits non-zero because those files are absent.
- Against the current `~/.codex`, the dry run reports 45 issues: 31 relative-symlink
  conflicts, 10 missing retired commands, and 4 skill-validator failures.

The 31 reported symlink conflicts come from comparing the raw relative value returned by
`readlink` with an absolute canonical path at `adapters/codex/sync.sh:33-39`. The installed
kit links are valid relative symlinks of the form `../../ai-kit/skills/<name>`.

The shell script also prints a plain `cp AGENTS.md` instruction at
`adapters/codex/sync.sh:97-103`, while `adapters/codex/README.md:45-50` says the adapter block
must be pasted at the managed include point rather than copied over the deployed file.

### 3. The Cursor shell path is healthier but has an unverified link edge case

`adapters/cursor/sync.sh --dry-run` succeeds with a clean temporary home and enumerates all
31 skills. Its link ownership/comparison logic at `adapters/cursor/sync.sh:78-90` and
`:155-165` uses the same raw-link-versus-absolute-path pattern as the Codex script. There are
no current kit links under `~/.cursor/skills` with which to reproduce or disprove the edge
case, and the Cursor CLI is not installed on this machine.

The public Claude install at `README.md:56-70` documents `~/.claude/skills` itself as a
whole-root link/junction. A per-skill sync sees a different topology: current adapter-style
enumeration can walk through the root link, treat all children as real directories, skip them,
and still report success. Existing-machine transition and exact-population acceptance are
therefore separate portability seams.

### 4. Windows-specific assumptions remain in live skills and documentation

Ten hard-coded `C:\ai-kit` occurrences across eight source lines occur in three live skills:

| Skill | Occurrences | Locations |
| --- | ---: | --- |
| `audit-skills` | 7 | `skills/audit-skills/SKILL.md:20-21,158,167,181` |
| `improve` | 2 | `skills/improve/SKILL.md:26,215` |
| `close` | 1 | `skills/close/SKILL.md:222` |

Additional live assumptions include:

- `skills/audit-skills/SKILL.md:111-112` uses a PowerShell-only line-count command as a
  canonical metric.
- `skills/write-skills/SKILL.md:90-91` names only `adapters/codex/sync.ps1` for its dry run.
- `docs/rules/skill-authoring.md:54-57` hard-codes a PowerShell invocation rooted at
  `C:\ai-kit`.
- `docs/loop-recipes.md:43-47,63-70` documents Windows Task Scheduler and `claude -p`, with
  no Linux scheduler counterpart.
- `skills/qa-gates/SKILL.md:189-194` mandates the Unix-specific `wc -l`; this is portable to
  Linux/macOS but not native PowerShell.

`skills/document-terraform` contains a conditional Windows caveat; because it is explicitly
conditional rather than an unconditional requirement, it is not classified as a portability
defect.

### 5. Provider coupling is concentrated in invocation and harness mechanics

Of the 31 live skill descriptions, 25 say `Invoke as /...`, which is the Claude Code
invocation form. The README workflow diagrams and `triage` output contract also use slash
invocations as the canonical presentation.

Provider tool names occur directly in workflow bodies:

| Coupling | Representative locations |
| --- | --- |
| `AskUserQuestion` | `docs-tasks-creator:48-51`, `triage:104-107` |
| `TodoWrite` | `close:59-60` |
| `Explore` | `lay-of-the-land`, `bug-investigation`, `document-terraform` |
| `Glob`, `Grep`, `Read` | `docs-tasks-creator` |
| `SendMessage` | `review-artifact` |
| `Agent`, `Task`, `Bash`, `PowerShell` | `orchestrate` |

`skills/write-skills/SKILL.md:31-40` treats tool-neutral wording as a special portability
profile rather than the default. The same skill is framed as authoring a “Claude skill”,
uses Claude-specific limits and a Haiku trigger test, and documents only Codex adapter sync,
not Cursor sync.

### 6. The Codex adapter describes older runtime capabilities

The installed runtime is `codex-cli 0.151.0`; `codex features list` reports both
`multi_agent` and `goals` as stable and enabled. Current official Codex documentation says
subagents are enabled by default, can run in parallel, and can be configured with per-agent
`model` and `model_reasoning_effort` values.

By contrast, `adapters/codex/AGENTS.md:27-43` describes generic fan-out as sequential unless
a build happens to expose native workers, and `skills/orchestrate/SKILL.md` says Codex model
pinning is unavailable. `adapters/codex/AGENTS.md:67-72` also groups `/goal` with several
Claude-only primitives despite the installed runtime exposing a stable goals feature.

This evidence does not establish direct Codex equivalents for every Claude primitive:
`/loop`, `/schedule`, `/compact`, and the cc-looper workflows remain unverified or
provider-specific.

Current Codex skill documentation lists repository and user skill roots under
`.agents/skills`, including `$HOME/.agents/skills`; it does not list `~/.codex/skills`.
This installed session nevertheless discovers all kit skills through the existing
`~/.codex/skills` links. That is a documentation-versus-local-runtime discrepancy, not a
request to migrate the deployment path during this work.

Official references:

- [Codex Agent Skills](https://learn.chatgpt.com/docs/build-skills)
- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

### 7. The Cursor adapter also describes older runtime capabilities

Current Cursor documentation describes Agent Skills discovery from `.agents/skills`,
`.cursor/skills`, and compatible Claude/Codex locations. It also documents native parallel
subagents and a built-in `/loop` command.

That compatibility surface is load-bearing for the approved two-root direction: Cursor scans
both `~/.agents/skills` and `~/.claude/skills`, and also recognizes `~/.codex/skills`. The existing
Cursor portability assessment records a prior live probe where populating two discovery roots
listed every skill twice. Cursor is unavailable here, so current precedence or deduplication
cannot be tested; the two-root model carries an explicit duplicate-discovery risk.

`adapters/cursor/AGENTS.md:70-75` says `/loop` has no Cursor analogue, and its subagent text
still treats native workers as conditional on the build. This is documentation-level
evidence only because `cursor-agent` is not installed locally.

Official references:

- [Cursor Agent Skills](https://prod.cursor.com/docs/skills)
- [Cursor subagents](https://prod.cursor.com/docs/subagents)

### 8. Four skills fail the installed Codex frontmatter validator

The current validator accepts `allowed-tools`, `description`, `license`, `metadata`, and
`name`. It rejects these live fields:

| Skill | Rejected field locations |
| --- | --- |
| `compile-kb` | `skills/compile-kb/SKILL.md:4` — `arguments` |
| `docs-tasks-creator` | `skills/docs-tasks-creator/SKILL.md:4` — `arguments` |
| `document-terraform` | `skills/document-terraform/SKILL.md:4` — `arguments` |
| `teach` | `skills/teach/SKILL.md:4-5` — `disable-model-invocation`, `argument-hint` |

The repo’s skill-authoring rule currently treats this validator as advisory and relies on a
manual strict-YAML check, so the relationship between Claude-compatible metadata and Codex
validation is an explicit compatibility seam.

### 9. Anchored `.claude` storage is widespread but intentionally preserved

There are 62 literal `~/.claude` references across 10 live skills:

| Skill | References |
| --- | ---: |
| `improve` | 24 |
| `audit-skills` | 13 |
| `close-tasks` | 9 |
| `close` | 7 |
| `onboard-me` | 3 |
| `qa-gates` | 2 |
| `review-implementation` | 1 |
| `record-decision` | 1 |
| `triage` | 1 |
| `write-skills` | 1 |

These paths support observations, staged improvements, audit state, ownership notes, memory,
and related maintenance artifacts. The Codex adapter already records this as an “Anchored
feedback loop.” Under the stated scope, the maintenance-data location is a preserved contract.
It does not automatically preserve convention-file coupling: five literal
`~/.claude/CLAUDE.md` targets occur in `improve`, and the corpus contains 35 `CLAUDE.md`
occurrences across 15 skills. Generic/global convention references target the provider-neutral
`AGENTS.md` contract; literal workflow targets require contextual classification.

### 10. Documentation and automated assurance lag the v2 surface

- `README.md:5,11` says the kit has 30 skills; `INVENTORY.md:3` and the filesystem show 31.
- `docs/rules/skill-authoring.md:20-37` describes three external Windows junctions inside
  `skills/`, but none exist in this Linux checkout. The named skills currently exist as real
  directories under `~/.agents/skills` instead.
- That rule’s deployment section at `:45-63` still describes commands and generated twins
  that were removed in v2.
- The cursor portability assessment is explicitly labeled v1-era in `INVENTORY.md:107`.
- The Codex assessment retains substantial retired command/agent/count material.
- `agentic_auto_scheduling_experimental_study_research_action_items.md:7` still treats
  `adapters/codex/sync.ps1` as the standing propagation path. The captured provider post in
  `claude_guide_loop_engineering.md` is source material and is not a neutralization target.
- No CI workflow or automated test suite checks shell syntax, PowerShell syntax, adapter
  parity, link ownership, frontmatter compatibility, skill counts, or provider documentation
  assumptions. Adapter READMEs instead call for manual cross-consumer checks.

## Current state

The kit has a provider-neutral core format but not a fully provider-neutral operating model.
Claude Code remains the vocabulary and behavior baseline; Codex and Cursor are accommodated
through additive adapter instructions. That structure has allowed the canonical workflows to
remain usable, but provider changes and Windows-authoritative maintenance have created drift
at the adapters and documentation edges.

On this Linux machine:

- all canonical kit skills are discoverable in the current Codex session;
- the Cursor clean-home shell dry run succeeds;
- the Codex clean-home shell dry run fails;
- PowerShell and Cursor runtime behavior cannot be exercised;
- the git worktree was clean before this document was added.

## Touchpoints

| Surface | Current responsibility | Coupling observed |
| --- | --- | --- |
| `skills/*/SKILL.md` | Canonical workflows | Slash invocation, Claude tool names, model and loop assumptions |
| `adapters/codex/` | Codex mechanics and deployment | Stale Linux sync; stale subagent/model/goal notes |
| `adapters/cursor/` | Cursor mechanics and deployment | Stale loop/subagent notes; unverified relative-link handling |
| `README.md` | Public entry point | Claude-first framing and stale skill count |
| `INVENTORY.md` | Live/deprecated inventory | Accurate count but identifies older assessment material |
| `docs/rules/skill-authoring.md` | Authoring and deployment rules | Windows-only examples and stale topology |
| `docs/loop-recipes.md` | Recurring execution recipes | Windows/Claude-only scheduler example |
| `~/.claude/{observations,improvements,ownership,…}` | Anchored maintenance data | Intentional preserved storage contract; excludes convention-file canonicality |

## Key components and responsibilities

### Canonical skills

The 31 `skills/<name>/SKILL.md` files define workflow behavior and trigger descriptions.
They are the common product surface consumed by all three agents.

### Codex adapter

`adapters/codex/AGENTS.md` translates Claude-oriented mechanics into Codex behavior.
`sync.ps1` is documented as authoritative, while `sync.sh` is intended to give Linux/macOS
parity. The two scripts currently represent different generations of the kit.

### Cursor adapter

`adapters/cursor/AGENTS.md` describes Cursor-specific behavior. Its shell and PowerShell sync
scripts deploy the canonical skills, but only the shell clean-home dry run was exercised.

### Repo rules and public documentation

The README, inventory, portability assessments, and `docs/rules/skill-authoring.md` explain
how contributors interpret and deploy the kit. Their stale counts and topology descriptions
can cause maintenance work to reproduce retired assumptions even where the live v2 structure
is simpler.

## Patterns

### Patterns worth preserving

- One canonical skill directory per workflow.
- Additive provider adapters rather than generated copies of skill bodies.
- Dry-run support before adapter mutation.
- Explicit conflict reports before replacing links; current force paths do not prove that a
  conflicting link/reparse point is kit-owned.
- Public-repo path hygiene using `~/` where possible.
- An explicitly documented anchored maintenance-state exception.

### Inconsistent patterns

- PowerShell is treated as authoritative while Linux/macOS scripts are manually mirrored.
- Provider-neutral Markdown coexists with provider-specific invocation and tool vocabulary.
- Current runtime behavior is recorded in static adapter prose without automated freshness
  checks.
- Cross-provider compatibility is manual and advisory rather than executable.
- Cursor's compatibility loader overlaps the requested Claude and shared discovery roots, while
  precedence and duplicate handling are not specified in the kit.

## Constraints

- Existing Windows use must remain understandable; Linux portability is an addition, not
  evidence that Windows is obsolete.
- The canonical skills remain the single workflow source; adapters are additive.
- The `.claude` feedback and maintenance-data store remains anchored by explicit user decision;
  `AGENTS.md` is the provider-neutral conventions contract.
- The repo is public, so committed paths cannot expose private machine-specific details.
- Provider capabilities change independently, and not every Claude primitive has an exact
  Codex or Cursor counterpart.
- No claim of Cursor, PowerShell, Windows, or macOS runtime success can be made from this
  machine.

## Open questions and risks

1. **Provider-neutrality depth:** whether canonical skills should adopt neutral invocation
   and tool vocabulary, or whether adapters should continue translating a Claude-first
   canonical surface.
2. **Platform support posture:** whether Windows and Linux/macOS are equal supported targets
   or Linux becomes primary with Windows retained as compatibility coverage.
3. **Metadata compatibility:** whether Claude-only frontmatter remains acceptable with an
   advisory Codex validation failure, or compatibility requires a shared metadata subset.
4. **Runtime proof:** Cursor and PowerShell behavior remains unverified locally.
5. **Documented skill roots:** current Codex documentation and the locally working legacy
   `~/.codex/skills` topology differ; changing the topology is outside the stated `.agents`
   migration boundary unless separately approved.
6. **Loop primitives:** current Cursor has a documented loop command and local Codex has a
   goals feature, but equivalence with the kit’s Claude loop workflows is not established.
7. **Overlapping discovery roots:** Cursor reads both requested roots and legacy Codex locations;
   a prior live probe observed duplicate listings, while current precedence is unverified.
8. **Existing Claude topology:** the public install path documents a whole-root
   `~/.claude/skills` link/junction, which requires an explicit transition to per-skill ownership.

## Coverage

Evidence gathered in this session includes:

- a complete inventory of the 31 live skill directories and 62 tracked live files outside
  `archive/v1/`;
- full reads of the relevant adapter instructions, sync scripts, READMEs, root inventory,
  repo skill-authoring rule, and the live skills containing the reported couplings;
- repository-wide searches for Windows paths, `.claude` paths, invocation syntax, and
  provider tool vocabulary;
- `bash -n` for both adapter shell scripts;
- clean-temporary-home dry runs for the Codex and Cursor shell adapters;
- a current-home Codex shell dry run to expose installed-link behavior;
- installed Codex version and feature probes;
- current official Codex and Cursor skill/subagent documentation.

Not covered live: adapter apply mode, rollback behavior, Cursor CLI behavior, PowerShell
syntax/runtime, Windows junction behavior, macOS behavior, or external skill junctions that
are absent from this checkout.

## Recommended next step

Run `analyze-work` in **refactor mode** to map the concrete change surface, preserved
contracts, caller closure, risk classes, and scope decisions. That analysis should begin with
the broken Linux Codex sync path and then cover the broader provider-coupling boundary chosen
by the user; it should continue treating the anchored `~/.claude` state as out of scope.

## Clarifications

### 2026-08-31 — refactor-analysis boundary

1. **Platform posture:** Windows, Linux, and macOS remain equal supported targets. The later
   single-sync design must serve all three; preserving separate PowerShell and POSIX adapter
   implementations is no longer a requirement.
2. **Provider posture:** canonical skills become provider-neutral where practical. Genuine
   Claude Code, Codex, and Cursor mechanics stay narrowly isolated in provider-specific files,
   but those files are no longer the center of skill deployment.
3. **Automated assurance:** portability checks are in scope, including shell validation,
   adapter parity, frontmatter compatibility, and skill-count drift.
4. **Anchored state:** existing `~/.claude` maintenance-data stores remain unchanged and out of
   scope; this does not automatically preserve `CLAUDE.md` convention targets.
5. **Deployment direction:** replace the Claude-primary plus per-provider skill-deployment
   posture with one provider-neutral sync surface that exposes every canonical skill through
   exactly two managed roots: `~/.claude/skills` for Claude Code and `~/.agents/skills` for
   shared Codex/Cursor discovery. Existing ai-kit links under `~/.codex/skills` or
   `~/.cursor/skills` are left untouched by this work.
6. **Edit discipline:** provider-neutralization is surgical. Preserve the current directory
   structure, section structure, and complete prose blocks; change only the provider-coupled
   terms or instructions that need it. A whole block enters the change surface only when the
   whole block is provider-specific.
7. **Link model:** keep the git checkout as the single source and expose each canonical skill
   with a per-skill filesystem link, preserving coexistence with non-kit skills in both roots.
   Linux/macOS use symbolic links; Windows uses directory junctions where ordinary symlink
   privileges are unavailable. Copy-based installation remains outside the primary model.
8. **Local migration acceptance:** at the end of the refactor, run the common sync on this
   Linux computer and verify that the ai-kit population resolves from both managed roots and
   is discoverable by the installed agents that can be exercised. Existing legacy links are
   not cleaned up without separate explicit approval.
9. **Convention contract:** `AGENTS.md` is the provider-neutral home for generic/global working
   conventions. The anchored `~/.claude` decision covers maintenance data, not automatic
   preservation of `CLAUDE.md` as canonical; literal workflow targets are classified surgically.
