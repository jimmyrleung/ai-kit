# Linux portability and cross-agent coupling — technical specification

Date: 2026-08-31
Mode: refactor
Input: `linux_portability_cross_agent_coupling_analysis.md` (`## Review` approved 2026-08-31)
Repository revision designed against: `76d6bd97c3`

## Review

- **Review date:** 2026-08-31
- **Post-review confidence:** 96%
- **Recommendation:** Approved with notes
- **Review scope:** one independent layer-scoped reviewer traced canonical skill → common sync →
  ownership manifest → both managed roots → provider discovery/rollback; the coordinator then
  re-grounded every finding against current source, local topology, and the Agent Skills standard.
- **Corrections applied:** baseline-preserving rollback and interruption recovery; contextual
  29-file Phase 3 map; strict-YAML dependency boundary; complete metadata profile; unrelated-skill
  whole-root migration guard; exact wrapper mapping; current source revision and counts.
- **Notes:** Windows/macOS link behavior and provider runtime presentation remain implementation-time
  CI/manual acceptance items; they do not leave a design decision open.

## Summary

Replace the four independent adapter sync implementations with one standard-library Python engine
at `scripts/sync-skills.py`, exposing every canonical skill through exactly
`~/.claude/skills` and `~/.agents/skills` while proving ownership before any link is changed.
Then make surgical provider-neutral edits across the 29 context-verified canonical skills and the
live documentation, backed by a strict portability checker and a Linux/macOS/Windows CI matrix.

The planned repository blast radius is **53 production/support files and 2 test files** across the
deployment, canonical-skill, policy, documentation, and automation layers. External apply mode also
writes per-skill links in two user-home roots plus one ownership manifest under the already-anchored
`~/.claude/ownership/` store. **Risk level: HIGH. Recommendation: IMPLEMENT WITH CAUTION.**

## Approach

Use an **incremental branch-by-abstraction refactor**:

1. introduce and prove the common engine without changing canonical skill behavior;
2. make the repository's metadata and authoring checks provider-profile aware;
3. neutralize only behavior-bearing provider vocabulary in canonical skills;
4. switch public/provider documentation to the common surface and apply it locally.

The common engine is Python 3.12+ because one implementation must run natively on Windows, Linux,
and macOS; Bash cannot provide native Windows parity, and PowerShell is not available on the current
Linux machine. It uses only the Python standard library. Windows junction creation is the sole
platform branch (`cmd /c mklink /J`); enumeration, preflight, ownership, reporting, and state are
shared.

Net-new mechanisms are limited to those forced by observed failures:

| Mechanism | Forcing observation / requirement |
| --- | --- |
| Common Python engine | Four implementations drifted; Codex POSIX still runs retired v1 generation. |
| Ownership + baseline manifest | Existing force paths can replace a same-name link without proof, while rollback must distinguish created, adopted, and retargeted entries. |
| Prepared transaction record | A process can stop between filesystem actions and manifest finalization; retry must recover without guessing provenance. |
| `--check` completeness mode | Existing scripts can exit successfully after skipping real-directory collisions. |
| Manifest-guarded `--uninstall` | Refactor rollback must restore pre-apply discovery, not merely erase every recorded entry. |
| Strict portability checker | Four skills carry provider-only frontmatter and population/docs counts drifted. |
| Three-OS CI matrix | Windows, macOS, PowerShell, and junction behavior cannot be proved on this Linux host. |
| Codex invocation policy for `teach` | Cursor's frontmatter flag is not Codex's explicit-invocation mechanism. |

The design reuses the canonical one-directory-per-skill model, dry-run/force/prune vocabulary,
managed instruction blocks, strict YAML policy, and additive provider adapters. It does **not**
build a plugin, copy-based installer, provider-specific skill twins, runtime deduplication layer,
new loop runner, background retry daemon, or compatibility cleanup service.

## Scope

### In scope

- One common sync CLI for `~/.claude/skills` and `~/.agents/skills`.
- POSIX symlinks and Windows directory junctions with equivalent classification and safety.
- Ownership proof, full preflight, dry-run, completeness check, and guarded orphan handling.
- Thin compatibility entry points at the four current adapter script paths.
- Provider-profile-aware frontmatter checks and strict YAML parsing.
- Surgical neutralization of 29 context-verified canonical `SKILL.md` files from the analysis's
  30-file audit envelope; `teach/SKILL.md` remains unchanged.
- Provider-mechanics and public documentation reconciliation.
- Automated Linux/macOS/Windows assurance and final migration of this Linux computer.

### Out of scope

| Item | Why out of scope | Where to revisit |
| --- | --- | --- |
| Moving `~/.claude` observations, improvements, ownership, or audit state | Explicit preserved contract. | A separate maintenance-store proposal. |
| Cleaning `~/.codex/skills` or `~/.cursor/skills` | Legacy roots must remain untouched without separate approval. | A later discovery-root cleanup proposal. |
| Cursor deduplication or precedence logic | Cursor scans both required roots and documents no precedence hook. | Revisit when Cursor documents or exposes root controls. |
| Provider-specific transformed skill copies | Would break the one-canonical-source contract. | Only if a provider stops accepting the shared skill body. |
| Reorganizing `skills/`, renaming skills, or changing workflow order | No requirement forces those changes. | Separate refactor with caller closure. |
| Copy-based primary installation | Breaks immediate propagation from the git checkout. | Documented fallback only. |
| Rewriting archived v1 material or `claude_guide_loop_engineering.md` | Historical evidence must remain intact. | Never, unless a live doc incorrectly treats it as current. |
| Installing Cursor or PowerShell locally | Not required to implement; CI supplies cross-OS proof. | Optional local conformance work. |

## Production-delta map

| Surface | Reuse | Modify | Add |
| --- | --- | --- | --- |
| Canonical skills | Existing 31 `skills/<name>/SKILL.md` directories | 29 context-verified `SKILL.md` targets; preserve names and section structure; leave `find-skills` and `teach` bodies unchanged | `skills/teach/agents/openai.yaml` only |
| Deployment | Per-skill links, dry-run/force/prune concepts | Four adapter scripts become wrappers | `scripts/sync-skills.py` |
| Assurance | Strict YAML rule and Codex advisory validator | `.gitattributes`, `.gitignore`, authoring/audit policy | Portability checker, two test suites, CI, locked JS dependency |
| Documentation | README/inventory/rules/adapters/assessments | Provider-neutral install and historical boundaries | No new narrative document |
| User-home state | Existing roots and anchored ownership store | Adopt exact current links; add links only after clean preflight | One versioned JSON ownership manifest |

## Patterns reused

| Pattern | Verified source | Usage here |
| --- | --- | --- |
| Skills-only sorted enumeration | `adapters/cursor/sync.sh` → `for s in "$SKILLS_SRC"/*/` (≈:78) | Enumerate canonical directories once and require readable `SKILL.md`; Phase 2 checks `name == directory`. |
| Dangling-entry visibility | `adapters/cursor/sync.sh` → `Prune (kit-owned orphans)` plain-entry loop (≈:153) | Classify dangling links without following them. |
| Reparse-point inspection | `adapters/cursor/sync.ps1` → `Test-Entry()` / `Get-ReparseTarget()` (≈:98–105) | Windows tests must inspect junction entries even when targets are missing. |
| Resolved target comparison | `adapters/codex/sync.ps1` → `Get-ReparseTarget()` and `Resolve-Path` (≈:107–126) | Compare normalized resolved targets rather than raw link strings. |
| Managed private-instruction block | `adapters/codex/README.md` → `kit-mechanics` include-point contract (≈:45) | Provider adapters keep mechanics additive and never overwrite private conventions. |
| Neutral user-question wording | `skills/qa-gates/SKILL.md` → `ask the user; record their confirm` (≈:172) | Replace named harness question tools with capability wording. |
| Neutral baseline skill | `skills/find-skills/SKILL.md` → two-key frontmatter and capability wording | Keep this file unchanged as the portability reference. |
| Strict YAML validation | `docs/rules/skill-authoring.md` → `Validate frontmatter with a strict YAML parser` | Automate the rule with `js-yaml` instead of replacing it with a regex parser. |
| Historical/live boundary | `docs/model-assignments.md` → `HISTORICAL (pre-2026-08 kit refactor)` (≈:3) | Supersede old assessments with banners; do not rewrite their decision history. |
| LF guard | `.gitattributes` → `*.sh text eol=lf` (≈:3) | Extend LF enforcement to the new `.py` and `.mjs` executable sources. |

Current official runtime contracts also constrain the implementation:

- Codex loads user skills from `$HOME/.agents/skills`, supports symlinked skill folders, and may
  show both skills when names collide: <https://learn.chatgpt.com/docs/build-skills>.
- Cursor loads both `~/.agents/skills` and compatibility roots including
  `~/.claude/skills` and `~/.codex/skills`: <https://prod.cursor.com/docs/skills>.

Therefore Cursor duplicate listings cannot be eliminated while satisfying the fixed two-root
requirement. The committed compatibility rule is **source equivalence, not precedence**: every
ai-kit occurrence must resolve to the same canonical `skills/<name>` directory. The kit makes no
claim about which duplicate Cursor presents first.

## Success metrics

| Metric | Baseline verified 2026-08-31 | Minimum acceptable result | Measurement |
| --- | --- | --- | --- |
| Managed population | `~/.claude/skills`: 31 ai-kit links; `~/.agents/skills`: 0 ai-kit links and two real-directory collisions | 31 canonical skills are accounted for in each managed root; the normal-home exception may be 31 managed Claude links plus 29 managed Agents links and 2 explicitly preserved entries | Qualified `python3 scripts/sync-skills.py --check --preserve ...` plus resolved-target enumeration |
| Deployment implementations | Four scripts contain independent enumeration/mutation logic | One implementation; four wrappers contain no link classification or mutation logic | `rg` for enumeration/link primitives outside `scripts/sync-skills.py` |
| Platform assurance | No tracked test or CI host | Same suite green on Ubuntu, macOS, and Windows | GitHub Actions matrix result |
| Ownership safety | Force can replace unproven links | Zero test case changes an unowned entry or target; every replacement is manifest-owned or exact-current adoption | Safety fixture assertions and before/after inode/content checks |
| Invocation wording | 25 descriptions contain case-insensitive `Invoke as /...` | Zero canonical descriptions contain provider-specific invocation suffixes | Portability checker |
| Metadata | Four skills expose five non-standard/provider-overlay field occurrences | All 31 pass declared standard + provider-overlay profiles; no unknown field; `teach` explicit-only in Cursor and Codex | Portability checker + provider metadata assertions |
| Hard-coded repo path | Ten `C:\ai-kit` occurrences across three skills | Zero live canonical skill occurrences | Portability checker / `rg` |
| Convention references | 35 `CLAUDE.md` occurrences across 15 skills | Every occurrence classified as historical/provider-specific or replaced by the `AGENTS.md` contract; zero unclassified generic use | Portability checker classification allowlist |
| Documentation count | README says 30 while tree/inventory contain 31 | Tree, README, inventory, and rule agree on the derived count | Portability checker |
| Local acceptance | Shared root incomplete; installed Cursor unavailable | Common check passes; installed Codex and Claude discovery exercised where attributable; Cursor marked not exercised rather than passed | Final phase evidence log |

## Phases

### Phase 1 — Introduce the common sync behind compatibility entry points

**Value delivered:** removes four-way implementation drift and establishes a safe, testable
deployment contract before canonical skill behavior changes.

#### Files

| Path | Action | Change and reason | Pattern |
| --- | --- | --- | --- |
| `scripts/sync-skills.py` | Create | Implement the common Python 3.12+ CLI and all link/junction behavior. | Sorted enumeration, resolved targets, dangling-entry visibility |
| `tests/test_sync_skills.py` | Create | Exercise state transitions against isolated temporary homes on every OS. | Existing dry-run/home-override seams, expanded into deterministic fixtures |
| `adapters/codex/sync.sh` | Modify | Replace implementation with a deprecation notice plus safe forwarding to the common engine. | Thin additive adapter |
| `adapters/codex/sync.ps1` | Modify | Map the six declared common switches plus `-UserHome`; retain `-CodexHome` only as an exit-2 migration diagnostic. | Thin additive adapter |
| `adapters/cursor/sync.sh` | Modify | Same POSIX wrapper; no Cursor-private deployment remains. | Thin additive adapter |
| `adapters/cursor/sync.ps1` | Modify | Same PowerShell contract; retain `-CursorHome` only as an exit-2 migration diagnostic. | Thin additive adapter |
| `.gitattributes` | Modify | Add LF rules for `*.py` and `*.mjs`. | Existing shell LF guard |

#### Common CLI contract

```text
python3 scripts/sync-skills.py [--dry-run] [--check | --uninstall]
                               [--force] [--prune] [--home <isolated-home>]
                               [--preserve <claude|agents>/<skill-name> ...]
```

- Default home: `Path.home()`; tests always pass `--home`.
- Managed roots: `<home>/.claude/skills` and `<home>/.agents/skills` only.
- Manifest: `<home>/.claude/ownership/ai-kit-skill-sync.json`.
- `--dry-run`: compute and print the complete plan; create no directory, link, or manifest.
- `--check`: read-only; exit zero only when every canonical skill resolves exactly from both roots
  and every finalized record agrees with the filesystem. A prepared transaction is incomplete and
  exits 1 with recovery guidance.
- `--uninstall`: restore the first-managed baseline for every record after one global preflight.
  An entry whose baseline was absent is unlinked; an exact-current entry adopted unchanged is left
  intact and released from management; an entry retargeted by `--force` is restored with its
  original link type and raw target. Targets, roots, ownership directory, unrelated entries, and
  legacy provider-private roots remain untouched. `--dry-run --uninstall` previews each action.
  This operation is approval-gated against a normal home.
- Apply (no mode flag): validate the canonical directory envelope, then preflight both roots and
  every planned action before mutation. Any conflict prevents all mutation. On a clean preflight,
  write a prepared transaction containing every baseline, create/adopt/retarget links, and replace
  the manifest atomically with finalized records.
- `--force`: permits replacement only when the manifest records the entry and the current link or
  junction still matches the recorded old target. It never authorizes changing a real directory or
  unrecorded link.
- `--prune`: report manifest-owned entries whose canonical skill disappeared.
  `--prune --force` runs the same per-entry baseline restoration as uninstall after a global
  preflight; it never follows or changes a target.
- `--preserve <claude|agents>/<skill-name>`: explicitly leave an existing directory or link with
  a canonical skill name outside ai-kit ownership for that invocation. The entry must already
  exist with a readable `SKILL.md`, is validated but never recorded in the manifest, and one flag
  is required per entry. The flags must be repeated for a qualified `--check`; without them,
  apply/check fails closed on the unowned canonical-name entry. Preserve policy does not change
  the canonical source count and is invalid with `--uninstall` or `--prune`; it requires no
  manifest-schema change.
- Exit `0`: complete requested state; `1`: conflicts, incomplete population, or runtime failure;
  `2`: invalid CLI combination/argument.

Invalid combinations are fixed: `--dry-run --check`; `--check` with `--force`, `--prune`, or
`--uninstall`; and `--uninstall` with `--force` or `--prune`. `--dry-run --uninstall` and
report-only `--prune` remain valid; only `--prune --force` mutates orphaned managed entries.

The POSIX wrappers first reject a set `CODEX_HOME`/`CURSOR_HOME`, then forward common CLI arguments
unchanged and preserve the exit code. Each PowerShell wrapper exposes `-WhatIf`, `-Check`,
`-Uninstall`, `-Force`, `-Prune`, `-Preserve`, and `-UserHome`; these map respectively to
`--dry-run`, `--check`, `--uninstall`, `--force`, `--prune`, `--preserve`, and `--home`. It retains `-CodexHome` or
`-CursorHome` only to emit migration guidance and exit 2. Provider-private environment variables
are rejected the same way. Those legacy values mean a directory such as `~/.codex`; they cannot be
derived into the user base containing both `.claude` and `.agents` without an unsafe semantic
guess. Wrapper-side invalid combinations match the common CLI and no wrapper contains link logic.

#### Ownership state

```json
{
  "schema_version": 1,
  "repo_root": "/resolved/path/to/ai-kit",
  "roots": {
    "/home/user/.claude/skills": {
      "analyze-work": {
        "managed_target": "/resolved/path/to/ai-kit/skills/analyze-work",
        "managed_kind": "symlink",
        "baseline": {
          "state": "link",
          "kind": "symlink",
          "raw_target": "../../ai-kit/skills/analyze-work",
          "resolved_target": "/resolved/path/to/ai-kit/skills/analyze-work"
        }
      },
      "audit-skills": {
        "managed_target": "/resolved/path/to/ai-kit/skills/audit-skills",
        "managed_kind": "symlink",
        "baseline": { "state": "absent" }
      }
    }
  },
  "transaction": null
}
```

While an operation is in flight, `transaction` replaces `null` with this shape; `before` and
`after` use the same baseline/link-state objects as finalized records:

```json
{
  "operation": "apply",
  "phase": "prepared",
  "actions": [
    {
      "root": "/home/user/.agents/skills",
      "name": "audit-skills",
      "before": { "state": "absent" },
      "after": {
        "state": "link",
        "kind": "symlink",
        "raw_target": "/resolved/path/to/ai-kit/skills/audit-skills",
        "resolved_target": "/resolved/path/to/ai-kit/skills/audit-skills"
      }
    }
  ]
}
```

Only the new common engine and `tests/test_sync_skills.py` consume this schema; no existing adapter
or provider reads it. The four wrappers pass through CLI state only, so the new shape does not widen
an unmodified production consumer.

The manifest is evidence, not unilateral authority. Before changing a recorded entry, the engine
must also prove that the live entry is a link/junction and that its actual target equals the
manifest's recorded target. An unrecorded link resolving exactly to the current canonical target
may be adopted without recreation; its original link type, raw target, and resolved target become
the immutable baseline. A baseline is captured only the first time an entry becomes managed and is
not overwritten by later applies or checkout moves.

Before the first filesystem action, the engine atomically writes `transaction` with operation
(`apply`, `prune`, or `uninstall`), phase `prepared`, and the complete ordered action plan including
baselines. A link replacement durably advances its action from `pending` to
`replacement-authorized` before unlinking. Retry accepts the recorded pre-action state, the exact
planned post-action state, or—only for an action carrying that durable authorization—the absent
replacement transition. Any other state is a conflict. After every action reaches its post-state,
one atomic manifest replacement commits the new finalized records and clears `transaction`. This
covers interruption before replacement, after unlink, between roots, after the last action, and
around finalization without a separate lock or journal file.

The common engine validates canonical directories and readable `SKILL.md` presence using the
Python standard library. It does not parse YAML. Strict frontmatter syntax, duplicate keys,
name/directory equality, and profile validation belong to the Phase 2 `js-yaml` checker, which must
pass before any normal-home apply in Phase 4.

If either managed root itself is a symlink/junction, the engine returns a
`root-layout-conflict` and does not traverse it. Root-layout migration stays an explicit,
approval-gated manual operation. First enumerate every direct child visible through the old root
and record its resolved target/type. If only canonical ai-kit children exist, move the root entry
to a named backup, create a real directory, and run the common sync. If any unrelated child exists,
stop for a per-entry disposition; the safe preservation choice is an unmanaged link/junction in
the new real root to that child's original resolved target, never a data copy. Acceptance compares
the pre/post child-name and resolved-target inventories. Retain the old root backup until acceptance
and rollback checks pass.

#### Non-trivial before/after

```bash
# Before: duplicated raw-link comparison and direct mutation
cur="$(readlink "$link")"
if [ "$cur" = "$tgt" ]; then ...

# After: wrapper only
exec python3 "$REPO_ROOT/scripts/sync-skills.py" "$@"
```

```powershell
# Before: independent junction classifier and mutation path
foreach ($s in $skillDirs) { ... New-Item -ItemType Junction ... }

# After: translate legacy PowerShell switches, then invoke the common CLI
& $python $CommonSync @CommonArgs
exit $LASTEXITCODE
```

#### Deployment and phase acceptance

- Merge code without applying it to normal user roots.
- Run tests in temporary homes on all three CI operating systems.
- Dry-run both compatibility shell families in CI; exercise PowerShell wrappers on Windows.
- Phase success: matrix green and an isolated apply followed by `--check` reports 31/31 in both
  roots.

#### Rollback point

Revert Phase 1 repository files. Normal user roots are unchanged until Phase 4. For an applied
isolated home, preview then run baseline-restoring `--uninstall`; an interrupted run is resumed from
the prepared transaction before the test harness discards its temporary directory. No target data
migration exists.

### Phase 2 — Make portability policy executable

**Value delivered:** converts strict YAML, metadata, population, and coupling rules from prose into
one repeatable check before broad canonical edits land.

#### Files

| Path | Action | Change and reason | Pattern |
| --- | --- | --- | --- |
| `scripts/check-skill-portability.mjs` | Create | Strictly parse and validate the 31-skill corpus, provider overlays, counts, and prohibited coupling. | `docs/rules/skill-authoring.md` strict js-yaml rule |
| `tests/test_skill_portability.mjs` | Create | Fixture-test malformed YAML, unknown fields, provider overlays, count drift, and unclassified coupling. | Structural audit checks |
| `package.json` | Create | Pin Node 24, `js-yaml@5.4.1`, and checker/test commands. | Existing Node + js-yaml validation method |
| `package-lock.json` | Create | Lock the only test dependency for reproducible CI. | npm lock contract |
| `.gitignore` | Modify | Ignore `node_modules/` and Python bytecode caches; preserve existing private-evidence exclusions. | Minimal tool-output exclusion |
| `.github/workflows/portability.yml` | Create | Run shell syntax, strict checker, tests, wrapper dry-runs, and sync fixtures on Ubuntu/macOS/Windows. | New automation host forced by cross-OS requirement |
| `skills/teach/agents/openai.yaml` | Create | Set `policy.allow_implicit_invocation: false` for Codex while keeping Cursor's canonical flag. | Official Codex optional metadata contract |
| `docs/rules/skill-authoring.md` | Modify | Replace stale Windows/v1 topology with common sync, profile rules, and automated commands. | Existing repo-rule location |
| `skills/audit-skills/SKILL.md` | Modify | Audit the provider-neutral corpus, generic paths, and common/provider-overlay profiles. | Existing 12-check structure |
| `skills/write-skills/SKILL.md` | Modify | Make the portable profile the default and point post-authoring checks to common sync/checker. | Existing authoring workflow |

#### Metadata profiles

The checker parses every frontmatter block with `js-yaml`; it does not approximate YAML with a
regex.

| Profile | Fields | Rule |
| --- | --- | --- |
| Agent Skills standard | `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools` | `name`/`description` required; the other fields optional. `allowed-tools` is experimental and its runtime effect is implementation-dependent. |
| Claude overlay | `arguments`, `argument-hint`, `disable-model-invocation` | Allowed only when the skill uses that behavior; not claimed as universally valid. |
| Cursor overlay | `paths`, `disable-model-invocation`, `icon`, `color` | Allowed only with a documented Cursor behavior. |
| Codex overlay | `agents/openai.yaml` | Invocation/tool/UI policy lives outside `SKILL.md` frontmatter. |

The standard-field bounds are explicit: `name` is 1–64 lowercase alphanumeric/hyphen characters
without a leading/trailing hyphen; `description` is non-empty and at most 1,024 characters;
`compatibility` is at most 500 characters; `metadata` is a string-to-string map; and
`allowed-tools` is one space-separated scalar. The checker validates those shapes but reports
provider support separately; a standard field is not evidence that every runtime enforces it.
Source: <https://agentskills.io/specification>.

`compile-kb`, `docs-tasks-creator`, and `document-terraform` retain their `arguments` fields so
their named-input contract does not change. `teach` retains `disable-model-invocation: true` for
Cursor and gains the Codex policy file. The installed Codex validator remains an advisory provider
profile check; expected rejection of a documented foreign-provider extension is reported as a
profile note, while an unknown or unjustified extension fails the repository checker.

The checker also enforces:

- directory name equals `name`; the exact standard name/description/compatibility bounds above;
- derived skill count agrees with README and inventory;
- zero `Invoke as /...` description suffixes;
- zero live `C:\ai-kit` skill-body paths;
- every remaining `CLAUDE.md` token is on a small, reviewed historical/provider-specific allowlist;
- `teach` has both Cursor and Codex explicit-only policy;
- `find-skills` stays unchanged as the neutral reference.

#### Deployment and phase acceptance

- Run the checker against the pre-neutralization corpus first with only structural/profile gates
  enabled; then enable coupling gates in Phase 3.
- CI uses `actions/checkout@v7`, `actions/setup-python@v7`, and `actions/setup-node@v7`, pins
  Python 3.12 and Node 24, disables unneeded package-manager caching, and grants only
  `contents: read`.
- Phase success: malformed fixtures fail for the intended reason; all 31 live skills pass the
  declared metadata profiles; `teach` is explicit-only in both provider contracts.

#### Rollback point

Revert the checker/policy files and remove the CI requirement from the branch. Phase 1 deployment
continues unchanged. No user-home state changes.

### Phase 3 — Neutralize canonical skills surgically

**Value delivered:** the canonical corpus describes capabilities and workflow names without making
Claude Code the vocabulary baseline.

#### Context-verified file map

Modify these **29** `SKILL.md` files. The stable anchor identifies the exact sentence/block to
patch; all other text and heading structure stays byte-for-byte unless the row says otherwise.

| Skill | Stable source anchor and coupling class | Committed delta and preserved contract |
| --- | --- | --- |
| `analyze-work` | frontmatter `description`; `## Subagents`; `### Consolidate the change surface`; `### Confidence gate` | Drop the slash-only suffix; replace provider worker/search/convention terms with capability wording. Preserve three modes, caller-closure algorithm, thresholds, and output filename. |
| `audit-skills` | frontmatter `description`; `## Inputs you read`; `### Check 1`; `### Phase 4` | Neutralize invocation/paths and make the standard + overlay profiles from Phase 2 authoritative. Preserve 12 checks, proposal destinations, thresholds, and approval flow. |
| `breakout-session` | frontmatter `description`; `## When to use`; `## Process` | Remove slash spellings around `teach`/`onboard-me`; preserve the one-question cadence, learning-record offer, and go/no-go verdict. |
| `bug-investigation` | frontmatter `description`; `## Coordinator vs worker`; `### Confidence gate`; `## Output file` | Neutralize skill invocations, `Explore`, and global-convention wording. Preserve evidence tags, incident gate, worker count, and artifact contract. |
| `close-tasks` | frontmatter `description`; `## Inputs`; `### 3a`; `## Notes` | Convert slash-form sibling references to skill names. Preserve harvest marker, observation attribution, SESSION_LOG roll-up, and git limits. |
| `close` | frontmatter `description`; `### 2b`; `### 2c`; `### Phase 3` | Neutralize invocation, planning-tool, generic convention-file, and repo-root spellings while retaining anchored `~/.claude` stores. Preserve offer/approval and commit rules. |
| `compile-kb` | frontmatter `description`; `## Orchestration`; `### Phase 3`; `## Confidence gate` | Neutralize invocation, worker/tool, and convention terms. Preserve vault guards, one-worker-per-domain rule, review requirement, and outputs. |
| `docs-tasks-creator` | `arguments`; `### Phase 1`; `### Phase 3`; `### Phase 6` | Replace `AskUserQuestion`/`Glob`/`Grep`/`Read` names with capability wording. Preserve both named arguments, detector precedence, emitted shapes, and handler granularity. |
| `document-terraform` | `arguments`; `## Coordinator vs worker`; `### Phase 3`; `## Confidence gate` | Neutralize worker/file/shell/convention terms. Preserve all three named arguments, topology and permissioning rules, ≥95% gate, and output schema. |
| `document-workflow` | frontmatter `description`; `## Process`; `## Output` | Remove slash-form invocation/cross-skill wording only. Preserve backend/full-stack mode selection and workflow document shape. |
| `implement-task` | frontmatter `description`; `## Input contract`; `## Process` | Replace slash-form sibling references with skill names. Preserve target resolution, fix lens, scope guard, build/test order, and verify-task handoff. |
| `improve` | frontmatter `description`; `## Inputs you read`; `### Phase 3`; `### Phase 5` | Replace `C:\ai-kit` and universal `CLAUDE.md` assumptions with repo-root/loaded-instruction resolution; neutralize question/search terms. Preserve anchored maintenance stores and per-item approval. |
| `lay-of-the-land` | `## Coordinator vs worker`; `## Process`; `## Output structure` | Replace `Explore` and global `CLAUDE.md` with capability/loaded-convention wording. Preserve evidence ledger, assumptions policy, ≥90% gate, and filename. |
| `onboard-me` | frontmatter `description`; `## How to run the conversation`; `## Important rules` | Remove slash suffix/cross-skill and `Explore`/`Read` spellings. Preserve one-step-per-turn Socratic flow and ownership record. |
| `orchestrate` | frontmatter `description`; `## Model & provider contract`; `## Process` | Replace the provider/model table and named worker tools with the capability rule already committed below. Preserve dispatch, persist-on-arrival, verification tiers, and resume semantics. |
| `post-mortem` | frontmatter `description`; `## Input contract`; `## Output file` | Replace slash-form skill handoffs with names. Preserve metrics, blameless structure, action-item fields, and `postmortem.md`. |
| `qa-gates` | frontmatter `description`; `## Inputs`; `### Gate 1`; `### Gate 5` | Neutralize invocation, `Bash`, question, and convention terms. Preserve all five gates, evidence recording, acceptance reasons, and human go/no-go. |
| `record-decision` | frontmatter `description`; `## Process`; `## Output file` | Remove slash spellings around `close` and the skill itself. Preserve UNREVIEWED labeling, ADR fields, and no-auto-commit rule. |
| `review-artifact` | frontmatter `description`; `### 1`; `### 4`; `### 5` | Neutralize invocation and named spawn/message/question terms. Preserve reviewer constraints, delta lenses, confirmation gate, verdicts, and in-place `## Review`. |
| `review-implementation` | frontmatter `description`; `### 2`; `### 3`; `### 4` | Neutralize invocation, worker, and convention terms. Preserve exactly three reviewers, finding verification/disposition, and stamped review block. |
| `tasks-breakdown` | frontmatter `description`; `## Process`; `## Section contract` | Remove slash-form handoffs and generic convention references. Preserve mode detection, sizing, dependency order, locked decisions, and output filename. |
| `techspec` | frontmatter `description`; `## Subagents guidance`; `### QA-scenario pass`; `## Section contract` | Neutralize invocation and named file/worker tools. Preserve mode/depth gates, 3-way approval rule, QA pass, section contract, and output filename. |
| `triage-learning-content` | frontmatter `description`; `## Process`; `## Output structure` | Remove slash-only invocation. Preserve the three exact consumption modes, rubric, and output contract. |
| `triage` | frontmatter `description`; `### Loop-primitive table`; `### Phase 3` | Move provider-native runner spellings to `docs/loop-recipes.md` and use skill names in routes. Preserve classification order, ≥90% clarification gate, and one-line recommendation. |
| `update-workflow-docs` | frontmatter `description`; `## Input contract`; `## Process` | Remove slash suffix and replace `Glob` with file enumeration. Preserve drift buckets, SHA/path resolution, targeted update behavior, and output shape. |
| `verify-task` | frontmatter `description`; `### Step 1`; `## Observation write`; `## Composition` | Replace slash-form `qa-gates`/`close`/`improve` references with skill names. Preserve gates 1–3 only, per-task inputs, observation count, and task-block write. |
| `walkthrough-implementation` | frontmatter `description`; `## Process`; `## Output file` | Remove slash invocation/cross-skill and global-convention wording. Preserve dependency-ordered tour, rationale classification, and no-commit boundary. |
| `walkthrough` | frontmatter `description`; `## Process`; `## Output file` | Remove slash invocation/cross-skill wording. Preserve one-item-per-turn disposition, batch breaks, confidence, and dated rounds. |
| `write-skills` | frontmatter `description`; `## When NOT to use`; `## Portable profile`; `## Process`; `## Output file` | Make provider-neutral authoring the default; replace fixed paths, named tools/models, and slash syntax with profiles/capabilities. Preserve limits, fresh-context tiers, audit handoff, and authoring contract. |

`skills/find-skills/SKILL.md` remains the neutral reference. `skills/teach/SKILL.md` also remains
unchanged: its Cursor `disable-model-invocation` and `argument-hint` fields are preserved as-is,
while `skills/teach/agents/openai.yaml` supplies Codex's explicit-only policy.

For every edited row, caller closure is one fixed gate: enumerate the skill name and its current
slash spelling across all live source, compare the result with the reviewed analysis's canonical
caller table, and inspect every changed caller sentence. Frontmatter `arguments`, thresholds,
worker counts/order, artifact names, and headings are snapshotted before the batch and compared
after it. A mismatch blocks the batch.

#### Committed edit rules

| Coupling class | Before | After | Contract preserved |
| --- | --- | --- | --- |
| Description invocation suffix | `Invoke as /techspec.` | Remove the suffix; `name` and trigger wording remain authoritative. | Implicit discovery and explicit invocation by provider-native syntax |
| Cross-skill invocation | `/review-artifact` | `the review-artifact skill` or `invoke review-artifact` | Skill name and workflow order |
| Generic conventions | `global CLAUDE.md format` | `loaded AGENTS.md confidence format` | Same score/gate behavior |
| Named file tools | `Glob` / `Grep` / `Read` | `file enumeration` / `text search` / `full-file read` | Same evidence requirement |
| Named worker tools | `Explore`, `Agent`, `Task`, `SendMessage` | `generic research subagent`, `spawn facility`, `send a follow-up to the same worker` | Same fan-out/resume semantics |
| Named planning/question tools | `TodoWrite`, `AskUserQuestion` | `active plan/todo facility`, `structured question facility with plain-text fallback` | Same phase and clarification gates |
| Shell names | `Bash` / `PowerShell` as universal grants | `a shell capable of the required verification`; provider syntax moves to adapters | Same ability to build/test |
| Model names/providers in canonical orchestration | fixed Opus/Fable/Codex branches | capability-based worker selection; inherit unless the active harness supports an explicit override | Same quality floor without volatile names |
| Hard-coded repository path | `C:\ai-kit\...` | repo-root-relative path discovered from the current workspace | Same target, OS-neutral |

`improve` receives the specific convention-target rule that closes the five literal
`~/.claude/CLAUDE.md` cases: resolve repo conventions from `AGENTS.md`; for user-level conventions,
identify the active harness's loaded private instruction file. If mirrored private files would
diverge, stage one proposal per target and require user approval rather than treating
`~/.claude/CLAUDE.md` as universal.

`triage` no longer embeds provider primitive spellings in its description or output. For recurring
work it recommends the runner category and points to `docs/loop-recipes.md`, where provider-native
spellings belong.

`orchestrate` retains the dispatch/persist/verify workflow but replaces its provider/model table
with a capability rule: use the session model by default; select a stronger worker only when the
active spawn facility supports an explicit override and the task requires it; record the choice.

#### Edit discipline

- Read each target end-to-end immediately before editing it.
- Use sentence/line patches; do not rewrite whole files or alter heading structure.
- Do not change names, artifact filenames, thresholds, approval gates, worker counts, or ordering.
- After every batch, strict-parse all 31 frontmatters and grep every replaced term for echoes.
- Re-run canonical caller closure after changing workflow-name wording.

#### Transitional-state tests

- Phase 2 checker runs with coupling gates warn-only while a batch is in flight.
- After each batch, the already-edited skills and untouched skills must both remain discoverable;
  the sync links expose the same physical files, so no dual implementation exists.
- Before phase completion, promote every coupling gate to failure and require all 31 profiles green.

#### Deployment and phase acceptance

- Land in reviewable batches: descriptions; convention/path terms; tool terms; orchestration/loop
  semantics.
- Run strict checker and trigger-description regression prompts after each batch.
- Phase success: approved coupling metrics reach their targets with zero changes to preserved
  contracts.

#### Rollback point

Each batch is independently revertible. If trigger routing or a workflow gate regresses, revert
that batch while Phase 1/2 remain valid. Links need no rollback because they expose the reverted
canonical files immediately.

### Phase 4 — Reconcile docs/adapters and migrate this Linux computer

**Value delivered:** users enter through the common surface, historical records stop presenting
retired mechanisms as current, and the primary Linux machine reaches the exact two-root state.

#### Files

| Path | Action | Change and reason |
| --- | --- | --- |
| `README.md` | Modify | Provider-neutral identity, derived 31-skill count, common install/sync, provider mechanics links. |
| `INVENTORY.md` | Modify | Keep count and current/historical document status consistent. |
| `AGENTS.md` | Modify | Update the indexed skill-authoring rule description to the common topology. |
| `docs/loop-recipes.md` | Modify | Keep provider-native runners isolated here; add equal-OS scheduler guidance and current capability caveats. |
| `agentic_auto_scheduling_experimental_study_research_action_items.md` | Modify | Replace the single standing Codex sync reference with the common checker/sync path only. |
| `docs/codex-portability-assessment.md` | Modify | Add a `Superseded 2026-08-31` banner pointing to this analysis/spec; preserve the body. |
| `docs/cursor-portability-assessment.md` | Modify | Same; explicitly preserve the prior duplicate-root observation as history. |
| `adapters/codex/README.md` | Modify | Mechanics-only guide; common deployment lives at root README. |
| `adapters/codex/AGENTS.md` | Modify | Current Codex invocation/subagent/goals mechanics; reference common sync, avoid duplicated deployment. |
| `adapters/cursor/README.md` | Modify | Mechanics-only guide and explicit duplicate-equivalence limitation. |
| `adapters/cursor/AGENTS.md` | Modify | Current Cursor invocation/subagent/loop mechanics; reference common sync. |

The two historical assessments are not rewritten. A banner states their date, the mechanisms now
retired, and the superseding artifacts. This follows the repository's preserve-history rule.

#### Local migration playbook

1. Re-verify the two externally owned entries at `~/.agents/skills/find-skills` and
   `~/.agents/skills/teach`; do not move, overwrite, or discard either entry.
2. Run `python3 scripts/sync-skills.py --dry-run --preserve agents/find-skills --preserve agents/teach`;
   the only non-managed results must be those two explicit preserves, with no mutation.
3. Require a complete plan of 31 managed Claude links, 29 managed Agents links, and 2 preserved
   Agents entries. The preserve flags are a per-invocation exception and are not written to the
   manifest.
4. Run apply with the same preserve flags, then run the qualified read-only check with the same
   flags. Also confirm that an unqualified check fails closed rather than accepting the exception.
5. Run the portability checker, both test suites, shell syntax, and repository count probes.
6. Restart/exercise locally installed Codex and Claude. Record Cursor as `not exercised` unless a
   runtime is present. Do not claim source attribution when a legacy root makes it ambiguous.
7. Leave `~/.codex/skills` and any `~/.cursor/skills` entries untouched. Record Cursor duplicates
   as acceptable only when every occurrence resolves to the same canonical source.

#### Deployment and phase acceptance

- Documentation and wrappers land before normal-root apply.
- Apply happens once on this Linux computer after the preserve policy has been confirmed and the
  qualified dry-run is conflict-free.
- Phase success: both roots pass exact population check; repository CI is green; all locally
  available runtime checks are honestly classified as passed, failed, ambiguous, or unavailable.

#### Rollback point

If runtime acceptance fails, keep legacy provider-private roots in service. With explicit user
approval, preview and run baseline-restoring `--uninstall`, confirm the 31 adopted Claude links
remain exactly as they were before apply, confirm the two preserved Agents entries remain untouched,
and revert Phase 4 docs. If a prepared transaction exists, resume it before any manual step. Never
change a target directory or touch an unrecorded entry.

## Testing strategy

The test strategy covers three state classes:

1. **pre-refactor state:** old wrappers still exist, common engine tested only in isolated homes;
2. **transitional canonical state:** neutralized and original skill prose coexist batch-by-batch,
   with structural profiles green and coupling gates warn-only;
3. **end state:** common engine owns both roots, all coupling gates fail closed, and provider docs
   describe only current mechanics.

No performance benchmark is needed: sync enumerates 31 local directories outside a hot path, and
the requirement contains no latency target. A manual regression scenario verifies the CLI remains
comfortable to run, but no invented millisecond threshold is introduced.

An independent QA-scenario pass was completed after the first draft. Its initial verdict required
revision because the draft could not roll back live managed entries and treated provider-private
home overrides as if they were common user-home paths. The first correction still erased adopted
links; the later independent artifact review caught that deeper provenance defect. The final
baseline manifest, prepared transaction, explicit override mapping, and scenarios 5–7, 9,
21–26, 29, 32–50, and 51 fold in both passes. Each pass assessed its findings at 96% confidence,
matching the post-review whole-design confidence below.

## Test plan

| # | Scenario | Inputs | Expected | Priority | Automatable |
| ---: | --- | --- | --- | --- | --- |
| 1 | Clean isolated apply | Empty temporary home, 31 readable canonical skill directories | Exactly 62 managed records: 31 links/junctions in each root; every baseline is `absent`; schema-1 manifest contains both roots, normalized `repo_root`, and no transaction/legacy root; exit 0 | High | Yes |
| 2 | Idempotent repeat | Home after scenario 1 | No link, directory, or manifest bytes/timestamps change; all entries report `current`; exit 0 | High | Yes |
| 3 | Dry-run is globally non-mutating | Empty fixture and a separate conflicting fixture, each with `--dry-run` | Complete plan or conflict report; no root, link, or manifest bytes/timestamps change in either fixture | High | Yes |
| 4 | Completeness check is read-only | Complete, missing, conflicting, stale, and manifest-mismatch homes | Complete exits 0; every other state exits 1 with exact names/classes; no mutation | High | Yes |
| 5 | Invalid CLI combinations | Conflicting modes, unsupported options, missing `--home`, and action flag without its guard | Exit 2 with usage-specific diagnostic; no filesystem state changes | High | Yes |
| 6 | Manifest schema and syntax rejection | Malformed JSON, missing keys, unsupported schema, invalid baseline/transaction shape, duplicate or unexpected root, unsafe managed path | Exit 1 with manifest-specific diagnostic; no entry or manifest change | High | Yes |
| 7 | Sync source-envelope validation | Missing, unreadable, or non-file `SKILL.md` in a canonical child | Standard-library preflight fails before either managed root or manifest changes; YAML/name cases are delegated to scenarios 30–32 | High | Yes |
| 8 | Relative target equivalence | Relative symlink resolving to canonical target | Entry is adopted/current, not conflicted or recreated | High | Yes (POSIX) |
| 9 | Cross-root preflight is atomic | One root empty; late-sorted unowned collision in the other | Preflight reports the collision; the empty root remains empty and manifest unchanged | High | Yes |
| 10 | Unowned real-directory collision | Real `teach/` containing a sentinel | Preflight fails; sentinel, all sibling entries, and manifest remain unchanged | High | Yes |
| 11 | Unowned link protection | Live and dangling same-name links to unrelated targets, with and without `--force` | Preflight fails in every case; link objects and targets remain unchanged | High | Yes |
| 12 | Exact-current unrecorded adoption | Existing relative symlink/current junction, no manifest record | Object is not recreated; manifest stores link type plus raw/resolved target as immutable baseline; uninstall later releases it unchanged | High | Yes |
| 13 | Repository checkout moved | Finalized records and both roots point to an old checkout; baselines include absent and adopted entries; new checkout supplied with `--force` | Prepared transaction captures all original baselines before action; 62 managed targets move; contents remain unchanged; uninstall can restore each first-managed state | High | Yes |
| 14 | Owned stale state is report-only by default | Recorded old target and live link still match; no `--force` | Nonzero stale report; neither live entry nor manifest changes | High | Yes |
| 15 | Guarded stale correction | Same fixture as scenario 14 with `--force` | Only proven-owned link/junction entries are recreated at current targets; record changes after live-target revalidation | High | Yes |
| 16 | Ownership record/live mismatch | Manifest target differs from the live link target | Every mutating mode refuses that entry; ownership mismatch is explicit | High | Yes |
| 17 | Dangling owned entry report | Finalized managed target disappeared; no action guards | Entry is visible as orphaned; default/check modes do not change it or its baseline | High | Yes |
| 18 | Guarded orphan action | Owned orphan with absent and link baselines plus action and force guards | After global preflight, absent baseline is restored as absent and link baseline is restored/released; targets and unrelated records remain correct | High | Yes |
| 19 | Unowned dangling neighbor | Owned orphan adjacent to an unrecorded dangling link | Unowned neighbor is reported as conflict and remains byte-for-byte unchanged; no partial action occurs | High | Yes |
| 20 | Managed root itself is link/junction | Either managed root points at another directory | `root-layout-conflict`; engine does not traverse or mutate either root | High | Yes |
| 21 | Preflight-to-action race | Fixture hook swaps a preflighted link or creates a collision immediately before action | Action-time revalidation stops all unsafe changes; no false ownership record is written | High | Yes |
| 22 | Link-replacement interruption recovery | Inject failure after durable replacement authorization, after unlink, and after one exact link action | Nonzero exit; complete baselines remain durable; retry recognizes authorized transition/pre/post states and converges without treating the planned link as a fresh adoption | High | Yes |
| 23 | Manifest finalization interruption recovery | Inject failure before/during the prepared write and final atomic replacement | Manifest is absent, old-valid, prepared-valid, or finalized-valid—never partial; retry resumes or finalizes the fixed plan | High | Yes |
| 24 | Rollback preview | Mixed created/adopted/retargeted fixture plus `--dry-run --uninstall` | Plans unlink/leave/restore actions respectively; no entry, root, target, or manifest bytes/timestamps change | High | Yes |
| 25 | Baseline-restoring rollback | Same mixed fixture plus `--uninstall` | Created entries become absent, adopted entries remain identical, retargeted entries regain original type/raw target; unrelated/legacy roots remain; finalized records clear atomically | High | Yes |
| 26 | Rollback ownership mismatch | One managed entry is swapped before `--uninstall` | Global preflight refuses rollback before preparing a transaction; no managed or unrelated entry changes | High | Yes |
| 27 | Windows junction lifecycle | Windows runner fixture | Create, resolve, check, guarded stale/orphan actions, and rollback use directory junctions without symlink privilege | High | Yes |
| 28 | macOS/Linux symlink lifecycle | macOS and Ubuntu runners | Equivalent classifications and safety outcomes use symlinks | High | Yes |
| 29 | Compatibility wrapper parity | POSIX common args; PowerShell `WhatIf/Check/Uninstall/Force/Prune/UserHome`; both legacy parameters/environments; invalid combinations | Exact mapping and exit-code parity; unsafe overrides exit 2 with guidance; wrappers contain no link logic | High | Yes |
| 30 | Strict YAML and standard bounds | All 31 live frontmatters plus empty/1,024/1,025-char description and 64/65-char name fixtures | Strict parse and exact name/description/compatibility bounds pass/fail at their declared boundaries | High | Yes |
| 31 | Malformed YAML fixtures | Unquoted colon-space, duplicate key, invalid scalar, and non-mapping frontmatter | Checker fails with file/key-specific diagnostic | High | Yes |
| 32 | Metadata profile boundaries | Standard `compatibility`, experimental `allowed-tools`, valid overlays, malformed `openai.yaml`, unknown field, and valid overlay on an unjustified skill | Standard shapes pass with provider-support notes; malformed/unknown/unjustified extensions fail with provider/profile context | High | Yes |
| 33 | Preserved provider contracts | Named-input skills, `teach`, and unchanged `find-skills` | `arguments` and hints remain exact; Cursor and Codex explicit-only policies pass; neutral reference hash/semantic snapshot is unchanged | High | Yes |
| 34 | Codex advisory validator behavior | Live corpus and `teach` policy through installed validator when available | Repository profile remains authoritative; expected foreign-extension note is classified, unexpected load failure fails; unavailable runtime is recorded, never inferred | High | Yes statically; runtime manual |
| 35 | Coupling-gate transition | Pre-Phase-3 corpus, an in-flight batch, and completed corpus | Coupling findings warn during the declared transition only; final mode fails on any remaining finding | High | Yes |
| 36 | Population/document drift | Add/remove fixture skill or alter README, inventory, or rule count | Checker fails until every derived/documented population agrees | High | Yes |
| 37 | Canonical coupling classes | Completed corpus with one fixture for each invocation, path, convention, tool, model/provider, and runner-token class | Zero live prohibited tokens; every allowed historical/provider-specific occurrence is explicitly classified | High | Yes |
| 38 | Workflow-contract regression | Before/after names, headings, worker counts/order, thresholds, named inputs, filenames, approval gates, and caller closure | Mechanical snapshot plus review shows no preserved-contract change | High | Yes + review |
| 39 | High-risk semantic probes | `triage`, `orchestrate`, and `improve` before/after fixtures after their edit batches | Runner routing, dispatch/persist/verify, and convention-target proposal behavior remain equivalent | High | Agent-assisted + review |
| 40 | Trigger-routing regression | Edited descriptions plus near-neighbor prompts | Same intended skill wins; `teach` never triggers implicitly | High | Manual/agent-assisted |
| 41 | Cursor duplicate equivalence | Synthetic and installed occurrences across `.agents`, `.claude`, `.codex`, and `.cursor` roots | Every ai-kit duplicate resolves to one canonical source; divergent target fails; no precedence claim is made | High | Yes mechanically; runtime manual |
| 42 | Documentation/config closure | README, inventory, rule index, adapters, loop recipe, package/lock, ignores, attributes, and workflow | No old live topology or count claim remains; commands/files agree; generated/dependency outputs are correctly classified | High | Yes + review |
| 43 | Whole-root migration procedure | Isolated root link/junction whose target contains canonical plus unrelated children | Engine refuses it; inventory is recorded; migration stops without dispositions; approved unmanaged child links preserve every name/resolved target while old target remains unchanged | High | Manual procedure + automated fixture checks |
| 44 | Local two-root migration | Current Linux home with the two explicitly preserved Agents entries | 31 managed Claude links plus 29 managed Agents links and 2 preserved entries; unrelated entries preserved, legacy roots untouched, qualified common check exits 0 | High | Manual apply + automated check |
| 45 | Runtime acceptance classification | Locally installed Claude/Codex and unavailable or duplicate-ambiguous Cursor | Each provider records passed, failed, ambiguous, or unavailable with evidence; no side-effect is treated as source proof | High | Manual |
| 46 | Local rollback drill | Replica of 31 adopted Claude links plus newly created shared-root links and the preserved-entry policy | Preview classifies adopted vs created; rollback leaves the 31 Claude links byte-identical, clears created managed links, leaves preserved entries untouched, and preserves targets/unrelated entries | High | Isolated automated; normal home manual |
| 47 | Historical-document preservation | Two assessment diffs | Only supersession banners/current cross-links change; decision-history bodies remain byte-identical | Medium | Yes |
| 48 | Private instruction-block preservation | Public adapter/include workflow | Public changes identify manual refresh; no repository script writes a private convention file; copied-block review is explicit | Medium | Yes statically; block review manual |
| 49 | CI/toolchain contract | Workflow source plus Ubuntu/macOS/Windows run artifacts | Read-only permissions; Python 3.12, Node 24, locked install, current pinned action majors, syntax/checker/tests/wrappers all execute on intended hosts | High | Yes |
| 50 | CLI usability smoke | Dry-run/check/apply/rollback summaries on each OS | Root, counts, classifications, conflicts, action, and next step are understandable; no generic performance threshold | Low | Manual |
| 51 | Interrupted rollback recovery | Failure injection before first action, between roots, after last action, and around finalization | Prepared rollback remains durable; retry accepts only exact pre/post states, converges idempotently, and rejects any third-party state | High | Yes |
| 52 | Explicit per-root preservation | Existing real directories or links at canonical names plus `--preserve agents/<skill-name>` | Dry-run/apply/check account for the preserved entries without recording or changing them; missing, invalid, owned, or omitted preserve policy fails closed; uninstall leaves them intact | High | Yes |

Tests are **not** needed for application APIs, databases, DI, browser/device behavior, or business
data because this refactor changes none of those surfaces. Full accessibility/security audits are
also not required; the security-relevant filesystem safety is covered directly by ownership and
target-preservation tests.

## Rollback strategy

### Decision tree

```text
All phase criteria pass
  -> continue to the next phase.

Minor canonical wording or documentation defect
  -> fix forward inside the current batch; rerun strict checker and affected scenarios.

Trigger/workflow regression with intact deployment
  -> revert the Phase 3 batch; Phase 1/2 remain deployed.

Ownership, target-preservation, or cross-OS failure
  -> stop rollout; revert common-wrapper activation; keep legacy provider-private roots;
     do not apply to normal homes.

Local runtime failure after apply
  -> recover any prepared transaction, preview and run baseline-restoring --uninstall only with
     explicit approval, verify preserved external entries remain untouched, and continue using
     untouched legacy roots.
```

No phase alters canonical target contents through the sync engine, so rollback never requires data
recovery. Git reverts restore repository behavior; user-home rollback changes only proven
link/junction entries and returns each to its immutable first-managed baseline.

## Contingency and unknowns

| Trigger / unknown | Response |
| --- | --- |
| Windows runner cannot create a junction | Treat Phase 1 as failed; correct the `mklink /J` path or runner permissions before rollout. Do not substitute copy mode. |
| `Path.is_junction()` or target resolution differs by Python patch | Pin the verified Python 3.12 patch in CI and add the observed case to fixtures before changing the algorithm. |
| A prepared transaction contains a third filesystem state | Stop with conflict evidence; do not rewrite the plan or baseline. The user must disposition the unexpected entry. |
| A stored Windows junction baseline target cannot be recreated | Stop rollback before action during global preflight; keep the managed entry and manifest until the original target is available or the user chooses a new disposition. |
| Cursor shows duplicate entries with divergent targets | Fail compatibility acceptance; enumerate every discovery root and correct only ai-kit-owned/common-root entries. Legacy-root cleanup needs separate approval. |
| Cursor later documents precedence/deduplication | Update provider docs/tests; do not change the fixed two-root common sync without a new decision. |
| Installed Codex validator rejects a declared foreign-provider extension | Record the expected profile note; repository checker still fails unknown extensions. If runtime stops loading the skill, open a new compatibility design rather than generating a twin silently. |
| A provider-specific term proves behavior-bearing during Phase 3 | Keep it in the narrow provider adapter/doc and replace the canonical sentence with the capability contract. |
| A `CLAUDE.md` workflow target has no discoverable active-harness equivalent | Stop that edit and ask which private convention file owns the proposal; do not guess. |
| Current external entries are not valid preserved directories or links | Stop local migration; leave them intact and ask the user for a disposition. Repository phases can still complete. |
| CI provider action major changes | Re-verify official action documentation and update the pinned major in a focused automation change. |

## Risks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Unowned entry is replaced | Low after design | Critical user-data loss | Full preflight; manifest + live-target proof; real dirs/unrecorded links never forceable. |
| Preserved exception is omitted or mis-scoped | Low after design | High | Require existing canonical-name entries, validate each root/name pair, keep preserves out of the manifest, and make unqualified apply/check fail closed. |
| Rollback erases or rewrites pre-existing discovery | Low after review | Critical | Immutable first-managed baseline; prepared transaction; created/adopted/retargeted lifecycle tests. |
| Interrupted action loses provenance | Low after review | High | Prepared plan is atomic before action; retry permits only exact pre/post states. |
| Junction operation affects target | Low | High | Windows fixture asserts target inode/content survives relink and orphan paths. |
| Cursor duplicate discovery confuses users | High | Medium | Explicit equivalence contract, enumeration check, no precedence claim, provider docs. |
| Cross-platform behavior diverges | Medium | High | One shared engine and three-OS matrix; wrappers contain no platform mutation logic. |
| Canonical wording changes workflow behavior | Medium | High | Surgical batches, preserved-contract probes, trigger tests, review before rollout. |
| Named-argument or explicit-only metadata regresses | Low-medium | High | Provider overlays retained; dedicated `teach` and named-input scenarios. |
| Historical records are accidentally rewritten | Low | Medium | Banner-only diffs with byte-preservation test. |
| CI infrastructure becomes a maintenance burden | Low | Low | One dependency, locked; no build framework or coverage target. |
| Local acceptance cannot attribute runtime source | High while legacy roots remain | Medium | Report `ambiguous`, not pass; rely on mechanical target proof and official root contract. |
| Private copied instruction blocks stay stale | Medium | Medium | Adapter docs and sync output explicitly surface manual refresh; never overwrite private files. |

## Files changed summary

### Production/support files

| Group | Modify | Create | Count |
| --- | ---: | ---: | ---: |
| Root/config (`README`, `INVENTORY`, `AGENTS`, `.gitattributes`, `.gitignore`, research action list) | 6 | 0 | 6 |
| Policy/history docs (`docs/rules/skill-authoring.md`, loop recipes, two assessments) | 4 | 0 | 4 |
| Adapter scripts/docs/instructions | 8 | 0 | 8 |
| Canonical `SKILL.md` files | 29 | 0 | 29 |
| Common engine/checker/package/CI/Teach Codex metadata | 0 | 6 | 6 |
| **Total production/support** | **47** | **6** | **53** |

Created support files are:

- `.github/workflows/portability.yml`
- `package.json`
- `package-lock.json`
- `scripts/check-skill-portability.mjs`
- `scripts/sync-skills.py`
- `skills/teach/agents/openai.yaml`

### Test files

| Path | Action |
| --- | --- |
| `tests/test_sync_skills.py` | Create |
| `tests/test_skill_portability.mjs` | Create |

**Explicit count: 53 production/support files and 2 test files.** Six new production/support
files and two new test files; no application API, database migration, schema, DI, network service,
feature flag, secret, or business-data change.

## Confidence score

**Confidence score: 96% — the reviewed reference map, independent artifact review, current
filesystem baselines, existing adapter patterns, and current standards support a complete phased
design with baseline-safe rollback.**

Factor calculation:

| Factor | Score | Evidence |
| --- | ---: | --- |
| API/docs clarity | 29/30 | Current Codex/Cursor roots, Codex metadata, and the Agent Skills standard checked; Cursor precedence remains undocumented. |
| Similar patterns | 24/25 | Existing enumeration, dry-run, reparse, managed-block, strict-YAML, and history-banner patterns verified. |
| Data-flow understanding | 20/20 | Canonical source → baseline/transaction manifest → two roots → three consumers → rollback is mapped for created, adopted, and retargeted states. |
| Complexity | 14/15 | Broad edits are divided into phases, but filesystem transaction recovery remains the densest implementation area. |
| Cross-system impact | 9/10 | External roots and private instruction copies are enumerated; unavailable Cursor/local Windows execution remains an operational gap. |
| **Total** | **96/100** | |

### Why 96%

- The reviewed analysis was re-grounded against the live 31-skill tree, four adapters, policy docs,
  and current local discovery roots.
- The current machine baselines were re-derived: 31 ai-kit Claude links, zero ai-kit shared-root
  links, and the two externally owned real-directory entries that are now explicitly preserved.
- Every net-new mechanism maps to a named safety, parity, rollback, or assurance requirement.
- Official Codex/Cursor documents confirm the roots and overlap; the Agent Skills standard fixes
  the metadata fields and bounds used by the checker.
- The independent review's six verified findings were corrected in the manifest lifecycle,
  contextual skill map, dependency boundary, migration procedure, and test plan.

### 4% uncertainty

- **Operational, does not block implementation:** Cursor is unavailable locally, so its duplicate
  presentation can be mechanically bounded but not visually/runtime confirmed here.
- **Operational, covered by CI:** Windows junction and macOS symlink paths cannot be exercised on
  this Linux machine before the matrix exists.
- **Minor implementation judgement:** exact CLI diagnostic wording and failure-injection hook shape
  may change during coding while exit semantics and transaction states remain fixed.
- **Does not block repository phases:** local migration still depends on separate approval for the
  normal-home apply and any rollback action; refusal leaves repository work valid but local
  acceptance incomplete.

## Post-review implementation correction — 2026-09-01

The independent review reproduced an interruption between unlink and recreate, proved that the two
preserved normal-home entries were empty rather than discoverable skills, found missing Cursor
overlay value-shape checks, and identified stale completion/CI evidence. The approved correction is:

- each retarget/restore action carries durable `pending` / `replacement-authorized` progress;
- a preserved entry must expose a readable `SKILL.md`, not merely occupy the expected path;
- Cursor `paths`, `icon`, and `color` values follow the documented string/list/string/enum shapes;
- the two live external skills are restored from the provenance already recorded in
  `~/.agents/.skill-lock.json`, with the empty placeholders retained as a dated backup;
- local green checks and hosted matrix evidence are reported separately. The workflow supports
  push, pull-request, and manual dispatch, but Ubuntu/macOS/Windows execution cannot be claimed
  until the workflow is committed, pushed, and run.

This section records the implementation correction without rewriting the earlier dated design and
QA evidence. The normal-home apply is complete; only hosted cross-OS evidence and unavailable
provider runtime attribution remain external.

## Hosted CI compatibility correction — 2026-09-01

The first pushed three-OS matrix run (`33519064448`) passed on Ubuntu and exposed two portability
assumptions before Gate 5 could close:

- the POSIX wrappers used `[[ -v VAR ]]`, which requires Bash 4.2 while the macOS runner provides
  Bash 3.2; wrapper environment detection now uses the Bash-3-compatible `${VAR+x}` expansion;
- the locked `find-skills` digest hashed checkout bytes, so a Windows CRLF checkout changed the
  digest without changing the skill text. The neutral-reference check now normalizes CRLF to LF
  before hashing, while a fixture proves that semantic content changes still fail.

The workflow also syntax-checks each POSIX wrapper in a loop rather than passing the second path as
an argument to the first `bash -n` invocation. These corrections refine scenarios 29, 33, and 49:
wrapper parity includes the oldest supported runner Bash, the neutral-reference lock is textual
rather than checkout-EOL-specific, and hosted success requires a fresh green matrix run.

## Hosted sync-harness correction — 2026-09-01

Subsequent hosted runs moved the remaining macOS and Windows failures into the isolated sync
harness and exposed their tracebacks. The detailed evidence is in
`linux_portability_hosted_ci_investigation.md`; this section records the resulting design
clarifications without rewriting the original phased design.

- **Windows junction command boundary:** `cmd.exe` receives the built-in command and every
  `mklink /J` operand as separate subprocess arguments. The engine does not pre-quote an entire
  command argument and does not enable `shell=True`. This preserves argument boundaries and the
  selected non-privileged junction mechanism.
- **Windows junction identity:** Python exposes a junction's substitution path with a typical
  `\\?\` namespace prefix. Path normalization removes equivalent `\\?\`, `\\?\UNC\`, and
  `\??\` prefixes. Junction states compare normalized raw/resolved targets; symbolic-link states
  retain exact raw-target comparison so relative baseline text remains immutable.
- **Dangling-link identity:** resolved-target classification starts from the stored raw link target,
  joined to the link parent when relative, rather than traversing the live entry. This keeps
  dangling Windows junctions attributable to the canonical tree and preserves the fail-closed
  unowned-neighbor guard during prune/rollback planning.
- **Snapshot consistency:** one `entry_state()` call reads the raw link target once and derives the
  normalized target from that same value. A concurrent external retarget therefore cannot mix two
  link states inside one baseline or transaction comparison.
- **Test-hook portability:** a hook path ending in `.py` is invoked through `sys.executable`.
  Other executable hook types retain direct invocation. This affects only the failure-injection
  surface and not normal sync actions.
- **macOS fixture identity:** temporary paths used for direct equality or relative-symlink
  construction are resolved first so `/var` and `/private/var` aliases cannot change the intended
  target.
- **Adapter test ownership:** Bash wrapper execution belongs to POSIX runners. Windows retains the
  PowerShell syntax/dry-run steps plus the full junction and transaction harness; it does not run a
  second provider surface through Git Bash.
- **Failure observability:** the unittest result emits one bounded GitHub annotation per failure
  during Actions runs. Local output and test behavior are unchanged.

These refinements complete scenarios 31, 33, 34, 49, and 51 only when a new hosted matrix is green.
They do not change ownership records, baseline restoration, preserve semantics, managed roots, or
the explicit exclusion of legacy provider-private roots.
