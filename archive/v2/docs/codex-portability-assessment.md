# Codex Portability Assessment

> **Superseded 2026-08-31.** This assessment is a historical decision and runtime record. The
> current implementation is the common two-root sync and provider-overlay contract described in
> the [root README](../README.md), [analysis](../linux_portability_cross_agent_coupling_analysis.md),
> [technical specification](../linux_portability_cross_agent_coupling_techspec.md),
> [tasks](../linux_portability_cross_agent_coupling_tasks.md), and
> [Codex adapter mechanics](../adapters/codex/README.md). Its decision-history body is preserved
> verbatim below; old generated populations and provider-private install paths are not current
> instructions.

> **Date:** 2026-05-17 · **Scope:** can ai-kit's commands / skills / agents / templates be
> driven by **OpenAI Codex CLI** as well as Claude Code, from **one canonical source + per-tool
> adapters**? · **Deliverable:** assessment only (no implementation; next steps are listed, not
> executed) · **Confidence: 92%** (see §7).
>
> **Decision log (updated 2026-05-17):** §3a now carries a committed direction — strategy **B
> dropped**; **C + externalised verdict-contract + A-default**, with `review-artifact`
> **quarantined**. Implementation 2026-05-17 (Category-1): packaging fork resolved to
> **junction** (Codex plugin bundle deferred); model-tier abstraction **deferred** (Category-2
> — see §4); §4 absolute-path defect **fixed**; **Codex adapter built** —
> `adapters/codex/{sync.ps1,sync.sh,AGENTS.md,README.md}`, exposes 34 skills (per-skill
> junction) + 18 agents (generated as explicit-only Codex skills) into `~/.codex/skills`,
> canonical tree pristine (Claude provably unaffected), `review-artifact` frozen, no kit
> harness. Strategy C realized as instruction in `adapters/codex/AGENTS.md`.
>
> **Decision-log addendum (2026-05-17, post-build):** the §2 "orchestrators become
> orchestrating skills" row is now **realized within Category-1**. The adapter additionally
> **generates 8 Codex-only skills** from `commands/` — the 5 family orchestrators
> (`full-bug-fix-workflow`, `integration-feature-dev`, `refactor-techdebt-dev`,
> `full-incident-response`, `greenfield-dev`) + 3 per-task executors (`implement-task`,
> `gf-implement-task`, `implement-bug-fix`) — `implicit_invocation:false`. Reads `commands/`,
> writes only Codex's root; canonical `commands/` is **never modified** (still Category-1,
> Claude provably unaffected). The ~25 thin shims are deliberately **not** generated (their
> skill is already junctioned). `AGENTS.md` gained a *Generated orchestrator / executor
> skills* section (the `/x` → `$skill` interpretation map). Driven by user Q (2026-05-17):
> commands ≠ skills (3 distinct primitives; the Claude-side reason to keep `commands/` is
> zero always-on context cost + no implicit auto-trigger — recorded in §2 reading notes).
>
> **Decision-log addendum (2026-05-18):** ai-kit gained the `lay-of-the-land` skill
> (Phase-0 pre-workflow recon; supersedes the `trigger-discovery-phase` command) and
> **retired** `discovery-agent` (built-in `Explore` covers recon fan-out). Net Codex
> exposure unchanged at **60** — skills **34 → 35**, agents **18 → 17**, 8
> orchestrators/executors unchanged. `sync.ps1`'s `-Prune` was corrected to resolve
> agent existence by frontmatter `name` (not `<name>.md`) — it had mis-flagged
> `code-reviewer` / `integration-review-agent` / `integration-validator-agent` as
> orphans. Still Category-1 (canonical tree pristine; Claude provably unaffected).
> Standing rule: re-run `adapters/codex/sync.ps1` for any new skill/agent (skills
> auto-discover; agents/orchestrators regenerate; `-Prune -Force` removes true orphans).
>
> **Decision-log addendum (2026-05-19):** a **Cursor CLI** companion adapter was
> built on the same Category-1, additive, canonical-untouched contract —
> `adapters/cursor/{sync.sh,sync.ps1,AGENTS.md,README.md}` +
> `docs/cursor-portability-assessment.md`. It reuses this assessment's
> 8-orchestrator allowlist and the `review-artifact`-frozen / feedback-loop-Anchored
> decisions verbatim; it is *smaller* (Cursor has native `SKILL.md` + a native
> subagent primitive, so no `openai.yaml`/validator/agent-as-skill workaround).
> The Codex facts below are unchanged.
>
> **Decision-log addendum (2026-07-10) — deployed on the primary Windows machine, codex-cli
> `0.144.1`:** `sync.ps1` applied clean — **65 exposed** (38 junctioned skills + 17 agent
> skills + 10 command skills), 0 issues (advisory `quick_validate.py` still skipped — host
> Python broken, kit-independent). Two `[verify on installed binary]` items **RESOLVED
> v0.144.1**: the **global `AGENTS.md` read-location is `~/.codex/AGENTS.md`** (official
> docs; `AGENTS.override.md` in the home dir takes precedence when present; deployed there
> as a **copy** — file-symlink needs elevation, hardlink would silently detach on git
> checkout) and **`project_doc_max_bytes` defaults to 32 KiB** (combined instruction-chain
> cap; kit `AGENTS.md` is ~6.3 KB). Feature flags re-checked: `multi_agent` stable/on,
> `enable_fanout` + `multi_agent_v2` still under-development/off — the §3a decision holds
> unchanged. **Live-verified end-to-end:** junctioned skills are discovered and visible
> in-session (probe from `C:\ai-kit`, now `trust_level = "trusted"` in
> `~/.codex/config.toml`); generated implicit-off skills are — by design — absent from the
> session skill list yet **resolve on explicit `$name` mention** (confirmed with
> `$bug-investigation-agent`: read-only sandbox, zero shell escapes, exact
> name+description returned). **New scripting caveat:** `codex exec` appends piped stdin
> to the prompt and blocks until EOF ("Reading additional input from stdin…") — in any
> non-TTY/background pipe it hangs forever; scripted calls must close stdin
> (`cmd /c "codex exec … < NUL"`, POSIX `… </dev/null`). Still **[verify]**:
> `$ARGUMENTS`/`$1` arg-mapping, `agents.max_depth` counting, hook field-level parity,
> structured-question tool absence.
>
> **Verification log — installed binary, Codex CLI `0.130.0`, 2026-05-17:** several
> `[verify on installed binary]` tags are now **resolved** (skills root, `SKILL.md` spec, agent
> binding format, the named feature flags, `codex mcp-server`, MCP TOML, plugin system, **and
> `codex exec --json`/`--output-schema`/`--output-last-message`** — confirmed in `codex exec
> --help`) — these read **VERIFIED v0.130.0** below. Items not directly probed
> (`$ARGUMENTS`/`$1` arg mapping, `agents.max_depth` counting
> semantics, hook field-level parity) **keep the [verify]
> tag**; `project_doc_max_bytes` and the `AGENTS.md` global read-location were later
> **RESOLVED v0.144.1** (2026-07-10 addendum above). **Caveat:** Codex's own `quick_validate.py` could **not** be run live on this host
> (`C:\Python311` segfaults `0xC0000005`, kit-independent) — canonical skills were
> **statically** validated (frontmatter keys within the allowed set; no `<`/`>` in any
> `description`); live validator pass is deferred to a working-Python / Codex env.
>
> Companion to `model-assignments.md`. Codex facts are dated 2026-05-17 from official docs
> (`developers.openai.com/codex`, `github.com/openai/codex`) — Codex ships weekly; every
> still-unverified version-sensitive fact below is tagged **[verify on installed binary]**.

---

## Verdict

**ai-kit is highly portable to Codex, and "one canonical set + adapters" is the right shape —
but the strongest version of that goal is not "Claude-native source + a Codex transform." It is
"the canonical source *is* the emerging cross-agent open standard (`SKILL.md` + `AGENTS.md`),
which Claude Code and Codex both natively consume," with a thin adapter only for the genuinely
tool-shaped layers.**

This is a bigger update than expected. As of Q1–Q2 2026 Codex adopted the **same `SKILL.md`
spec** (frontmatter + body + progressive disclosure, implicit *and* explicit invocation), the
**`AGENTS.md`** instruction standard, **native subagents** (GA 2026-03-14), and a **hooks engine
that deliberately reuses Claude Code's field names** (`PreToolUse`, `SessionStart`,
`additionalContext`, `decision: block`). The kit's crown jewel — ~28 methodology skill bodies —
is ~90% tool-agnostic English and ports with minimal body changes. Only **two** capabilities are
genuine no-analog redesigns, and the kit's actual exposure to both is **smaller than the raw
file count suggests**.

The feedback loop stays Claude-anchored exactly as you scoped it: `close`/`improve` write to the
fixed path `~/.claude/…`, which is filesystem-absolute and tool-independent, so running `/close`
*from Codex* and feeding `~/.claude` works with no rework — only cosmetic prose touch-ups.

---

## 1. Target architecture — canonical = the cross-agent standard

Three facts make a shared-standard canonical layer (not a Claude-native one) the lowest-drift
choice:

1. **Codex consumes the same `SKILL.md` format Claude Code does** — **VERIFIED v0.130.0**:
   `~/.codex/skills/.system/*/SKILL.md` natives carry the identical spec (`name`/`description`
   frontmatter + markdown body + progressive disclosure via `references/`/`scripts/`/`assets/`).
   The two roots are **scopes, not alternatives**: `~/.codex/skills/<name>/` = user/home (the
   adapter target — mirrors today's `~/.claude` junction), `.agents/skills/<name>/` = repo-scoped.
   [`developers.openai.com/codex/skills`]
2. **The canonical-source + symlink precedent already exists in your setup.** The README
   documents junctioning `ai-kit/{skills,commands,agents}` into `~/.claude/`; the
   `cc-looper-symlink-topology` memory records loop skills already being symlinks to a canonical
   copy. Adding a Codex consumer extends an established pattern — it does not invent one.
3. **`AGENTS.md` ≈ `CLAUDE.md`** in concept and nested-cascade behavior (Codex even reads
   deprecated `CLAUDE_PLUGIN_*` env vars — intentional compat, not coincidence).

**Resulting layout (recommendation, not yet built):**

```
ai-kit/                         # canonical, single source of truth
  skills/<name>/SKILL.md        # shared SKILL.md spec — consumed by BOTH tools
  agents/<name>.md              # canonical agent spec (Claude form; adapter emits a thin
                                #   per-skill agents/openai.yaml — VERIFIED v0.130.0, NOT TOML)
  commands/<name>.md            # Claude-only UX layer (see §2 — Codex needs no separate layer)
  templates/                    # plain markdown — already tool-agnostic
  adapters/
    claude/ -> junction ~/.claude/{skills,commands,agents}     (today's mechanism)
    codex/  -> junction ~/.codex/skills + per-skill agents/openai.yaml + AGENTS.md
             #  packaging = junction (decided 2026-05-17); Codex-plugin bundle deferred
```

The "adapter" is therefore deliberately *thin*: a deterministic build/junction step, not a
re-authoring of methodology. The whole point of putting methodology in `SKILL.md` is that
`SKILL.md` is now the shared currency.

---

## 2. Portability map (the core deliverable)

Transfer classes: **Clean** (same standard, no change) · **Mechanical** (deterministic
transform, scriptable) · **Semantic** (idiom changes, needs judgment) · **Redesign** (no Codex
analog) · **Anchored** (stays Claude by your explicit call).

| ai-kit primitive | Evidence (repo-wide grep) | Codex target | Class | Effort |
|---|---|---|---|---|
| **Skills** (`skills/*/SKILL.md`, ~28) | methodology is ~90% tool-agnostic prose (`qa-gates`, `triage`, `bug-investigation` read end-to-end) | Native skills, **same `SKILL.md` spec** (**VERIFIED v0.130.0**), implicit+explicit invocation | **Clean** | **Low** |
| **Templates** (`templates/**`) | plain markdown | copied as-is | **Clean** | **None** |
| **`CLAUDE.md` confidence/convention refs** | ~2–3 refs in workflow skills | `AGENTS.md` (same concept, nested cascade) | **Mechanical** | **Low** |
| **Command frontmatter + args** | `$ARGUMENTS`/`argument-hint`/`arguments:` — **97 occ / 55 files** | `$ARGUMENTS`/`$1`/`$KEY` map ~1:1 | **Mechanical** | **Low** |
| **Thin per-phase commands** (`investigate-bug.md` = 5-line shim → skill) | ~25 of ~34 commands are shims | **collapse into the skill** — a Codex skill is directly invokable (`$name`/implicit); the shim's job disappears | **Semantic** | **Low** |
| **Orchestrator commands** (`full-bug-fix-workflow`, `integration-feature-dev`, …) | ~5 multi-phase; "create a todo list", phase gates | become **orchestrating skills** (skills may sequence phases, invoke skills/subagents) | **Semantic** | **Med** |
| **Tool-name refs in bodies** (`Bash`/`Grep`/`Read`/`TodoWrite`) | only **5 literal `TodoWrite`/`AskUserQuestion` tokens / 5 files**; rest is soft prose | `shell`/`apply_patch`/`update_plan` (1:1; `update_plan` *is* TodoWrite) | **Mechanical** | **Low** |
| **Subagent *definitions*** (`agents/*.md`, 18) | `name`/`description`/`model`/`tools`/`color` frontmatter + (mostly) thin "follow the skill" bodies | **VERIFIED v0.130.0:** thin per-skill **`agents/openai.yaml`** interface manifest (`display_name`/`short_description`/icons/`default_prompt` + optional `dependencies.tools`). **No body transform** — SKILL.md body is consumed natively (NOT TOML, NOT `developer_instructions`) | **Mechanical** | **Low** |
| **Coordinator/worker *fan-out idiom*** ("the skill launches 1–3 `@x-agent` for breadth, then consolidates") | `@x-agent`/sub-agent — **63 occ / 41 files**; core to `review-artifact`, `bug-investigation` M-path, the `*-reviewer` agents | **no autonomous-spawn analog** — Codex subagents are explicit-by-name only; `max_depth=1` default kills nesting | **Redesign** | **High** |
| **`AskUserQuestion` structured-choice** | light in *bodies* (soft "ask the user"); but mandated by global `CLAUDE.md` clarification rule | **no native analog** — degrade to plain-text Q&A / `/plan` review / custom MCP | **Redesign** | **Med** |
| **Feedback loop** (`close`/`close-tasks`/`improve`/`audit-skills`) | path/tool refs — **131 occ / 24 files**, concentrated here (improve 24, audit-skills 16, close 8) | writes to fixed `~/.claude/…` — **runs from Codex unchanged**; minor prose touch-ups (`/compact`, `Skill`/`Agent` names) | **Anchored** | **None** (by your call) |
| **MCP servers** (e.g. `migrate-notion`) | Notion MCP | `[mcp_servers.<n>]` TOML; stdio+HTTP parity | **Mechanical** | **Low** |
| **settings.json hooks** (secret-scan is a *git* hook — already tool-agnostic) | git pre-commit is portable as-is | Codex hooks deliberately Claude-shaped (`hooks.json`/`[hooks]`, `command`-only, regex matchers) | **Mechanical** | **Low** (if/when needed) |

**Reading the map:** everything above the subagent-fan-out row is Clean/Mechanical/low-Semantic
— i.e. a deterministic adapter. The portability problem reduces to **exactly two Redesign rows**,
covered next.

---

## 3. The two genuine gaps

### 3a. Autonomous multi-agent fan-out — the one real architectural gap

The kit's signature idiom: a skill, *mid-execution*, decides to launch 1–3 `@bug-investigation-agent`
/ `@{reviewer_agent}` workers "for breadth", then consolidates (consensus / disagreement /
confidence-weighted). This is the most-coupled pattern in the kit (**63 occ / 41 files**) and
it has **no Codex analog**: Codex subagents exist and are first-class, but the model does **not
autonomously spawn** them — they're referenced by name and Codex orchestrates; `agents.max_depth`
defaults to **1**, so orchestrator→skill→subagent chains don't nest. [`/codex/subagents`]
**VERIFIED v0.130.0** (`codex features list`): `multi_agent` = **stable/on** (named subagents
available — strategy C is viable today); `enable_fanout` **exists but is under-development/off**
and `multi_agent_v2` is under-development — i.e. a native fan-out primitive is being built but is
not yet usable, so the no-autonomous-spawn gap holds for stable use **and may close natively
later** (does not change the recorded decision; `agents.max_depth` counting still **[verify]**).

Three substitution strategies were on the table; the decision is now recorded (see **Decision** below):

- **A. Degrade to single-thread** in the Codex adapter — the skill does the breadth pass itself
  on the main thread. Lowest effort; loses the multi-perspective consolidation that
  `review-artifact`'s "> 30% → re-run" heuristic depends on.
- **B. `codex exec` fan-out** — the coordinator shells out N parallel `codex exec --json`
  processes as workers, parses structured output, consolidates. Closest behavioral match;
  needs an orchestration harness.
- **C. Explicit named subagents** — pre-declare `bug-investigation-agent.toml` etc.; the skill
  instructs Codex to "consult the X, Y, Z agents." Native, but the *number* of workers (1–3 by
  breadth) becomes static, and consolidation logic moves into the skill prose.

Affected components are enumerable (the `review-artifact` callers + the `*-reviewer`/`*-agent`
set); this is bounded redesign, not open-ended.

#### Decision (recorded 2026-05-17)

**Constraint set by the user:** no kit-owned fan-out harness — rely on the native harness
(Claude / Codex subagents) or a runner *on top of* the native CLI (cc-looper-class), never an
orchestration script embedded in a skill. **⇒ strategy B is dropped.**

The kit has **two different fan-out shapes**; they do not take the same answer:

| Shape | Sites | Decision | Loss vs Claude today |
|---|---|---|---|
| **Divergent + fixed roster** | `integration-techspec`, `refactor-plan`, all 3-way explorers | **C** — native subagents, fixed named roster, one-shot consolidation | none |
| **Convergent + stateful** | `review-artifact`, `bug-investigation` (M), `qa-loop`/`review-checkpoint` | **C** for the parallel independent passes; the multi-round loop *leaves the kit* — the skill emits a structured verdict (`OK` / `NEEDS_RERUN:<who>,<reason>` / `ESCALATE:<reason>`) consumed by a human (interactive) or a cc-looper-class runner (headless) | multi-round becomes external, not native — but **no kit harness** |
| **Small / skip-checked** | `review-artifact` Step-0 / small-bug paths | **A** (single-thread) default | ~none — skip-checks already short-circuit these |

- **Dynamic 1–3 worker count is recoverable without a harness:** native subagents are invoked
  by name *in the prompt*, so the count is a conditional keyed off the S/M/L/XL classifier the
  orchestrators already compute (`if M → consult reviewer-1..3; if S → reviewer-1`). Static
  *definitions*, model-chosen *invocation*.

**Claude-impact boundary (load-bearing — this is *why* the rollout is staged):**

- **Category 1 — purely additive Codex artifacts** (Codex agent defs, the adapter/junction,
  Codex-side A-vs-C selection): files Claude never reads. **Claude provably unaffected.** The
  3-way explorers via C are entirely this category.
- **Category 2 — the convergent-review verdict-contract refactor:** `review-artifact` and
  `bug-investigation` are **one physical canonical file each, junctioned into `~/.claude/`**
  (`cc-looper-symlink-topology`). Under the one-canonical-set decision there is *no Codex-only
  copy by construction* — editing them edits what Claude runs now. "Claude unaffected" is then
  achievable only as a **behaviour-invariant, regression-gated** property, never automatic.

**`review-artifact` is quarantined.** It is the quality gate for 4 of 5 families (bugfix;
feature-addition ×2 — analysis + techspec; refactoring-tech-debt; incident-response) plus the
`review-investigation` / `review-techspec` / `review-diagnosis` wrappers. A broken gate does
not crash — it *passes work it should have caught*, i.e. silent quality erosion across the
kit. Therefore its canonical file is **frozen for this initiative**: Codex runs it from the
*unchanged* file in C-mode (independent reviewer subagents; verdict surfaced; the human drives
any re-run interactively — which collapses into the skill's existing "confirm the change set
with the user / ask if OK to proceed" steps). The verdict-contract refactor is **re-homed to
the future cc-looper-class runner effort** (it is only needed for *headless* multi-round
automation = that effort's scope), done later in isolation, gated by a Claude golden-transcript
regression check. `bug-investigation` is a lesser case (one phase, one family, itself gated
downstream by `review-artifact`) but takes the same rule — no convergent-review verdict
refactor in near-term scope.

### 3b. `AskUserQuestion` — real gap, small actual surface

No native Codex structured multiple-choice tool [`/codex/cli/features`]. **But the kit's
exposure is small:** only 5 literal-token occurrences; the skills overwhelmingly say "ask the
user clarifying questions" / "let the user pick" as tool-agnostic prose, which degrades
gracefully to free-text Q&A. The binding constraint is **not the kit** — it's the *global*
`CLAUDE.md` rule "prefer using the ASK USER QUESTIONS TOOL." The adapter fix is a Codex-conditional
clause in `AGENTS.md` ("Codex has no structured-choice tool — ask as a numbered plain-text
list"), not 28 skill rewrites.

---

## 4. Pre-existing defects the canonical layer must fix anyway

Independent of Codex — surfaced by this assessment, aligned with the `ai-kit-is-public`
path-hygiene rule:

- **Hard-coded absolute paths in skill bodies. — FIXED 2026-05-17.**
  `skills/bug-investigation/SKILL.md:33` and `skills/refactor-audit/SKILL.md:34` referenced
  templates by absolute Windows path (`C:\ai-kit\templates\…`); both are documentation pointers
  ("see X for the shape"), now kit-relative (`templates/…`) — behavior-invariant for Claude,
  tool-agnostic for Codex. No other `C:\ai-kit\…` leaks remain in non-meta skill bodies (grep
  confirmed). (`improve`/`audit-skills`/`close`/`close-tasks` still use `C:\ai-kit\…` — meta-skills
  that operate on the repo itself; lower priority, **still pending**, same fix.)
- **Model pins are vendor-specific. — DEFERRED 2026-05-17 (Category-2, out of near-term scope).**
  `model: opus|sonnet` in 18 agents + the entire `model-assignments.md` methodology is
  Claude-vendor. For a canonical set, abstract to **capability tiers** ("deep-reasoning" /
  "fast-structured"); each adapter maps tier→vendor model (Claude: opus/sonnet; Codex: `model`
  + `model_reasoning_effort`, inherits if omitted). This makes `model-assignments.md` a tier
  policy, not a Claude artifact. **§4 grouped this with the path fix as "lowest-risk," but it
  edits 18 agent files junctioned into `~/.claude/` — that is Category-2 (Claude-affecting),
  which the §3a recorded decision keeps out of near-term scope.** Re-homed as a tracked
  follow-up, behind the same regression discipline as the verdict-contract refactor.

---

## 5. What the adapter actually does (transform inventory)

Deterministic unless marked:

1. **Skills:** symlink/junction `ai-kit/skills` → **`~/.codex/skills`** (**VERIFIED v0.130.0** —
   user/home root, mirrors today's `~/.claude` junction; `.agents/skills` is the repo-scoped root).
   No body transform (shared spec). Frontmatter `allowed-tools`-style restriction, if ever added,
   moves to `agents/openai.yaml` `dependencies.tools`.
2. **Commands:** *do not* port to `~/.codex/prompts/` (deprecated **and** user-only, no project
   scope). The ~25 thin shims collapse into their (already-junctioned) skill — not generated.
   The 5 family orchestrators + 3 per-task executors **are generated as Codex-only
   orchestrating skills** (BUILT 2026-05-17 post-build addendum; implicit-off; reads
   `commands/`, canonical `commands/` never modified). Claude Code keeps `commands/` for its
   `/x` UX via the existing junction — at zero always-on context cost (a command body is not
   in-context until run; a skill description always is — they are *not* interchangeable).
3. **Agents:** **VERIFIED v0.130.0** — generate a thin per-skill **`<skill>/agents/openai.yaml`**
   (`interface:` → `display_name`/`short_description`/`icon_*`/`default_prompt`; optional
   `dependencies.tools`). `name`/`description` map directly; **the SKILL.md body is consumed
   natively — no body transform, no `developer_instructions`, no `<name>.toml`**; `model` → §4
   tier policy (deferred); drop `color`. *(Semantic where the body assumes autonomous spawn —
   see §3a.)*
4. **Instructions:** emit/junction `AGENTS.md` from the `CLAUDE.md` conventions; add the
   Codex-conditional `AskUserQuestion` clause (§3b).
5. **In-body tool names:** mechanical remap (`Bash`→`shell`, `TodoWrite`→`update_plan`, …) — or,
   better, neutralize to capability prose in the canonical copy so neither adapter needs it.
6. **Paths:** fix the §4 absolute paths; `~/.claude/…` feedback-loop paths stay (Anchored).
7. **MCP / hooks:** JSON→TOML / `settings.json`→`hooks.json` mechanical mapping, only if/when you
   want them on the Codex side (out of scope for the feedback-loop-stays-Claude decision).

Community prior art (unofficial — evaluate before trusting): `zuharz/ccode-to-codex` already
classifies Claude→Codex conversion as MECHANICAL/MANUAL/REFACTOR (the same tiering as this
assessment); `ariccb/sync-claude-skills-to-codex` is symlink-based and mirrors your existing
`cc-looper-symlink-topology` approach.

---

## 6. Risks & open decisions

- **§3a decision — RESOLVED 2026-05-17** (see §3a "Decision"): B dropped (no kit harness);
  C for explorers, C + externalised verdict-contract for convergent, A for skip-checked. The
  *new* residual risk is the **deferred verdict-contract refactor of `review-artifact`** — the
  kit's quality gate (4 of 5 families); failure mode is *silent quality erosion*, not a crash.
  Until it is done (re-homed to the cc-looper-runner effort, in isolation, behind a Claude
  golden-transcript regression gate) `review-artifact`'s canonical file stays frozen and Codex
  runs it in C-mode from the unchanged file.
- **Version drift (high-churn risk) — partially retired 2026-05-17.** The **skills root** is
  resolved (`~/.codex/skills`, VERIFIED v0.130.0) and the agent-binding format correction
  (`openai.yaml` not TOML) is a *fact fix*, not residual risk. Still build-variable and **[verify
  on installed binary]**: `$ARGUMENTS`/`$1` arg mapping,
  `codex exec --json`/`--output-schema` flags, `agents.max_depth` counting, hook field-level
  parity (`project_doc_max_bytes` **RESOLVED v0.144.1**: 32 KiB default — 2026-07-10
  addendum). Does not change the top-line conclusion; does change exact adapter details.
- **Plugin system exists (new — not in the original assessment).** **VERIFIED v0.130.0:**
  `plugins` = stable/on; `.codex-plugin/plugin.json` + `.agents/plugins/marketplace.json` +
  `codex plugin marketplace`; a plugin can bundle `skills/ hooks/ scripts/ mcp`. **Packaging fork
  resolved to junction (decided 2026-05-17)** — least Codex-coupled, extends the existing
  `~/.claude` precedent; a Codex-plugin bundle is a tracked follow-up, not near-term scope.
- **Two-consumer test debt:** any change to a canonical skill must be sanity-checked from *both*
  tools. The symlink topology means "edit once," but verification is now 2×.
- **Codex prompts are deprecated:** committing the command layer to skills (not
  `~/.codex/prompts/`) is the future-proof call but means Claude's `/x` UX and Codex's `$skill`
  invocation diverge in muscle memory.

---

## 7. Confidence

**92%.** The structural conclusions — per-primitive transfer class, the two Redesign gaps, the
shared-standard canonical recommendation, the Anchored feedback loop — are robust: the ai-kit
side is file-grounded (end-to-end reads + repo-wide greps with counts, Appendix), and the Codex
side is from official docs with sources.

**8% uncertainty (reduced 2026-05-17 — structural confidence holds at 92%):** (a) Codex is
version-volatile — skills-root is now **resolved** (`~/.codex/skills`, v0.130.0), but doc-byte-cap,
arg-mapping, `exec --json` flags, `max_depth` counting and hook field parity remain **[verify on
installed binary]** and could shift *exact* adapter details (not the classes); (b) §3a is decided
(B dropped → no kit harness; C + externalised verdict-contract + A-default), so effort is no
longer a wide range — the residual is whether interactive-Codex C-mode for `review-artifact` is
*fully* equivalent to today's Claude human-confirmation points or merely close (a Codex-only,
file-unchanged pilot observation — carries no Claude/gate risk); (c) **RESOLVED** — `codex
mcp-server` exists (Codex *can* act as an MCP server; relevant only if you later expose ai-kit
itself as a tool). Net: the agent-format correction is a *fact fix* (assessment was wrong, the
reality is simpler), not a confidence reduction; structural conclusions are unchanged.

---

## 8. Recommended next steps (decision recorded 2026-05-17; Category-1 implemented)

§3a now carries a committed direction (see §3a "Decision"). Sequenced to keep the only
shared-canonical-file change (the quality gate) out of near-term scope:

1. **Do-now = Category-1 only (provably Codex-only) — DONE 2026-05-17 (adapter built).**
   `adapters/codex/{sync.ps1,sync.sh,AGENTS.md,README.md}`. Mechanism (fresh design, verified
   facts): per-skill **directory junction** `~/.codex/skills/<name>` → canonical (34 skills,
   no body transform); the 18 `agents/*.md` **generated as explicit-only Codex skills**
   (`policy.allow_implicit_invocation:false` — no per-session context bloat) since a skill *is*
   the unit of agent invocation (no `~/.codex/agents`). **The 5 family orchestrators + 3
   per-task executors are also generated** (same mechanism, from `commands/`,
   `implicit_invocation:false`; the ~25 thin shims are not — their skill is junctioned).
   **`openai.yaml` for the 34 canonical
   skills deferred** — recommended-not-required (verified); injecting it would either pollute
   the pristine canonical tree or need privilege-fragile Windows file-symlinks. Strategy C =
   instruction in `AGENTS.md` (no kit harness). Idempotent, canonical tree pristine (Claude
   provably unaffected — canonical `commands/` read-only too), `review-artifact` frozen.
2. **Verify Codex specifics on the installed binary — DONE 2026-05-17 (v0.130.0).** Resolved:
   skills root (`~/.codex/skills`), `SKILL.md` spec (identical), agent binding (`openai.yaml`,
   not TOML), feature flags (`multi_agent` stable, `enable_fanout` under-dev, `hooks`/`plugins`
   stable), `codex mcp-server` exists, MCP TOML, plugin system, `codex exec
   --json`/`--output-schema`/`--output-last-message`. **Still [verify]:**
   arg-mapping, `max_depth` counting, hook field parity (`project_doc_max_bytes` = 32 KiB and
   the global `AGENTS.md` read-location = `~/.codex/AGENTS.md` — **RESOLVED v0.144.1**,
   2026-07-10 addendum).
3. **Fix the §4 pre-existing defects — partially DONE 2026-05-17.** Absolute paths → kit-relative
   **FIXED** (2 primitive bodies; meta-skills still pending). Model pins → capability tiers
   **DEFERRED** (Category-2 — edits 18 junctioned agent files; out of near-term scope).
4. **Pilot `bugfix` on Codex** end-to-end with the *unchanged* `review-artifact` — observe
   C-mode interactive behaviour vs Claude (Codex-only, no gate risk).
5. **Deferred & re-homed (NOT this initiative):** the convergent-review verdict-contract
   refactor (`review-artifact`, then `bug-investigation`) — belongs with the future
   cc-looper-class runner effort (only needed for headless multi-round automation), done in
   isolation behind a Claude golden-transcript regression gate.

---

## Appendix — evidence base

**ai-kit side (this repo, 2026-05-17 greps over `**/*.md`):**

- Subagent / coordinator-worker: `@x-agent | sub-agent | Agent tool` → **63 / 41 files**.
- Frontmatter+args+model pins: `$ARGUMENTS | argument-hint | arguments: | model: opus|sonnet`
  → **97 / 55 files**.
- Claude path/tool-name: `~/.claude | .claude/ | C:\ | CLAUDE.md | Claude Code` → **131 / 24
  files**, concentrated in `improve`(24)/`audit-skills`(16)/`close`(8)/`close-tasks`(9)/README(9).
- Literal interactive tool tokens: `TodoWrite | AskUserQuestion | ExitPlanMode | plan mode`
  → **5 / 5 files** (the rest is tool-agnostic prose).
- Absolute-path leaks in *primitive* bodies: `bug-investigation/SKILL.md:33`,
  `refactor-audit/SKILL.md:34` (template refs) + meta-skills `improve`/`audit-skills`/`close`.
- Files read end-to-end: README, `full-bug-fix-workflow`, `integration-feature-dev`,
  `investigate-bug`, `bug-investigation`, `close`, `improve`, `review-artifact`, `qa-gates`,
  `triage`, `bug-investigation-agent`, `code-reviewer-agent`, `model-assignments.md`,
  `INVENTORY/README.md`.

**Codex side (2026-05-17, official docs unless noted):** skills/`SKILL.md` & `.agents/skills`
[`/codex/skills`]; subagents GA 2026-03-14, TOML, explicit-only, `max_depth=1` [`/codex/subagents`];
`AGENTS.md` cascade [`/codex/guides/agents-md`]; hooks Claude-shaped [`/codex/hooks`]; `$ARGUMENTS`/`$1`
& prompts-deprecated [`/codex/custom-prompts`]; `codex exec --json`/`--output-schema`
[`/codex/noninteractive`]; tool surface incl. `update_plan`, no `AskUserQuestion` analog
[`/codex/cli/features`]; MCP TOML parity [`/codex/mcp`]. Community: `zuharz/ccode-to-codex`,
`ariccb/sync-claude-skills-to-codex` (unofficial).

**Codex side — VERIFIED on installed binary, `codex-cli 0.130.0`, 2026-05-17 (supersedes docs
where they differ):** skills root **`~/.codex/skills`** (home; `.system/` natives present) +
`.agents/skills` (repo scope) — *scopes, not alternatives*; `SKILL.md` spec **identical**
(`name`/`description` + body + `references/`/`scripts/`/`assets/`); agent binding = per-skill
**`agents/openai.yaml`** `interface:` manifest + optional `dependencies.tools` — **NOT
`<name>.toml`, NOT `developer_instructions`** (docs were stale here); `codex features list`:
`multi_agent` stable/on, `multi_agent_v2` & `enable_fanout` under-development/off, `hooks`
stable/on, `plugins` stable/on, `plugin_hooks`/`child_agents_md` under-dev; subcommands incl.
`codex exec`, `codex review --base/--uncommitted`, `codex mcp {add,list,get,remove}`, **`codex
mcp-server`** (Codex-as-MCP-server confirmed), `codex plugin marketplace`; `~/.codex/config.toml`
carries `[mcp_servers.<n>]` TOML (MCP-TOML parity confirmed). Not probed on binary (still
`[verify]`): `$ARGUMENTS`/`$1` mapping, `exec --json`/`--output-schema`
flags, `agents.max_depth` counting, hook field-level names, `AskUserQuestion`-analog absence
(`project_doc_max_bytes` since **RESOLVED v0.144.1** = 32 KiB — 2026-07-10 addendum, which
also resolved the global `AGENTS.md` read-location and live-verified skill discovery +
explicit `$name` mention resolution on the deployed machine).
