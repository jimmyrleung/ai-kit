# Cursor CLI Portability Assessment

> **Superseded 2026-08-31.** This assessment preserves the historical Cursor duplicate-root
> observation and its dated runtime evidence. The current implementation is the common two-root
> sync plus provider-specific adapter mechanics described in the [root README](../README.md),
> [analysis](../linux_portability_cross_agent_coupling_analysis.md),
> [technical specification](../linux_portability_cross_agent_coupling_techspec.md),
> [tasks](../linux_portability_cross_agent_coupling_tasks.md), and
> [Cursor adapter mechanics](../adapters/cursor/README.md). The body below is preserved verbatim;
> its old discovery paths and counts are historical, not current common-install instructions.

> **Date:** 2026-05-19 · **Scope:** can ai-kit's skills / agents / commands be
> driven by the **Cursor CLI** (`cursor-agent`) as well as Claude Code and
> Codex, from **one canonical source + per-tool adapters**? · **Deliverable:**
> assessment + Category-1 adapter (built same session) · **Confidence: 90%**
> (see §6).
>
> Companion to `codex-portability-assessment.md` and `model-assignments.md`.
> Cursor facts dated 2026-05-19 from official docs (`cursor.com/docs`,
> `cursor.com/llms.txt`, changelog) **and probed live on the user's
> `cursor-agent`**. Cursor ships near-daily; version-sensitive facts are tagged
> **[verify on installed binary]**.

---

## Verdict

**ai-kit is highly portable to the Cursor CLI — more cleanly than to Codex.**
Cursor natively consumes the **same `SKILL.md` Agent-Skills standard** Claude
Code and Codex do, *and* has a **native subagent primitive**, *and* treats
explicit slash-commands as skills (`disable-model-invocation: true`). So the
adapter is **purely additive and smaller than the Codex one**: no `openai.yaml`
interface manifests, no validator step, no agent-as-skill workaround. Only the
8 orchestrator/executor commands need generation; skills and agents map to
first-class Cursor primitives.

The headline finding is not a format gap — it is an **environment gap**: the
kit's skills were invisible in `cursor-agent` purely because the user runs
`cursor-agent` **under WSL** while the kit's `~/.claude` junctions live in the
**Windows** home (`C:\Users\…`). WSL `$HOME=/home/<user>` has no `.claude`, so
Cursor's compat loader found nothing. This was proven, not theorised (below).

---

## 1. Empirical findings (probed on the installed binary)

| Probe | Result | Implication |
|---|---|---|
| `cursor-agent` `/skills` under WSL, before fix | 0 ai-kit skills (13 built-in only) | Not a format problem — see next rows |
| WSL `$HOME` | `/home/<user>`; **no `~/.claude`** (Windows junctions are in `C:\Users\<user>\.claude`) | **Root cause** of "lists nothing" — environment, not incompatibility |
| WSL symlinks `~/.claude/{skills,agents,commands}` → `/mnt/c/ai-kit/*` created; `ls -L` resolves | 30 skill dirs, 17 agents, commands all readable | Symlinks sound; not a link defect |
| Claude Code installed in WSL (native, 2.1.144), reads same symlinks | **All three listed** (skills + agents + commands) | Proves the symlinks are sound and the path is correct ⇒ Cursor's omission is a genuine CLI parity gap |
| `cursor-agent` `/skills` after WSL `~/.claude/skills` reachable | **30 ai-kit skills listed** | Cursor reads `~/.claude/skills` natively (compat root) — skills need **no adapter** |
| `cursor-agent` `/` (commands) | ai-kit commands **not** listed | Cursor CLI does not read `~/.claude/commands` — **gap** |
| `cursor-agent` "list subagents" (after generating `~/.cursor/agents/`) | only built-ins (`generalPurpose`, `cursor-guide`, `best-of-n-runner`) | **Staff-acknowledged parity bug #160426** (ack 2026-05-13, no fix date): Cursor CLI loads only *project-level* `.cursor/agents/`, **not** user-level `~/.cursor/agents/`. `/create-subagent` confirmed on-machine to write project-scoped. |
| Removed diagnostic `~/.claude/{skills,agents,commands}` WSL symlinks; restart | skills 81 → 51 (dupes gone) | **Duplicate-discovery-roots gotcha**: Cursor reads `~/.claude/skills` (compat) *and* `~/.cursor/skills` (native); both present ⇒ every skill listed 2× + command files leak as malformed skills. The adapter must own exactly one root (`~/.cursor`); the diagnostic `~/.claude` symlinks must be torn down. |

The IDE shows all three because its plugin/Claude-compat loader is broader; the
CLI's is narrower and was a known, feature-flagged parity gap in early May 2026
(forum-confirmed). Targeting Cursor's **native** roots (`~/.cursor/skills`,
`~/.cursor/agents`) sidesteps the flaky compat path entirely.

---

## 2. Portability map

Transfer classes: **Clean** (same standard) · **Mechanical** (deterministic
transform) · **Semantic** (idiom) · **Redesign** (no analog) · **Anchored**
(stays Claude by decision).

| ai-kit primitive | Cursor target | Class | Effort |
|---|---|---|---|
| **Skills** (35) | native `SKILL.md`, per-skill symlink → `~/.cursor/skills/<name>`; auto-discovered | **Clean** | **None** (symlink) |
| **Templates** | plain markdown | **Clean** | **None** |
| **Thin per-phase commands** (~25) | their (symlinked) skill is directly invokable | **Semantic** | **Low** |
| **Orchestrator/executor commands** (8) | generated Cursor skills, `disable-model-invocation: true` (explicit-only `/name`) | **Semantic** | **Med** |
| **Agent definitions** (17) | generated native Cursor subagents (`name`+`description`+body; `model`/`tools`/`color` dropped) | **Mechanical** | **Low** |
| **Coordinator/worker fan-out idiom** | native subagents, explicit by name; multi-round loop stays interactive (`review-artifact` frozen) | **Semantic** | **Med** (instruction in `AGENTS.md`) |
| **`AskUserQuestion` structured-choice** | no native analog — numbered plain-text degradation in `AGENTS.md` | **Redesign** | **Low** (small surface) |
| **`CLAUDE.md` conventions** | project-root `AGENTS.md`/`CLAUDE.md`; global is **[verify]** | **Mechanical** | **Low** |
| **Feedback loop** (`close`/`improve`/…) | writes fixed `~/.claude/…` — runs from Cursor unchanged | **Anchored** | **None** (by decision) |
| **MCP servers** | `.cursor/mcp.json` / `~/.cursor/mcp.json` | **Mechanical** | **Low** (if/when needed) |

Everything is Clean/Mechanical/low-Semantic. There is **no Redesign-High** row —
unlike Codex (whose autonomous-fan-out gap was High): Cursor *has* native
subagents, so the fan-out idiom degrades to instruction, not redesign.

---

## 3. Design decisions (recorded 2026-05-19)

1. **Skills-unified, not `~/.cursor/commands/`.** Cursor deprecated standalone
   slash-commands (old commands docs 404/redirect to Skills; built-in
   `/migrate-to-skills` converts commands → skills with
   `disable-model-invocation:true`). The 8 orchestrators/executors are generated
   as explicit-only **skills**, unifying onto the primitive already proven
   working in the user's `cursor-agent`. The ~25 thin shims are **not**
   generated (their skill is symlinked) — same rule as Codex.
2. **Agents → native subagents**, not agents-as-skills (Codex needed the latter;
   Cursor has the primitive). `model`/`tools`/`color` dropped → `model:
   inherit`.
3. **Generate into Cursor-native roots** (`~/.cursor/skills`, `~/.cursor/agents`),
   not the `~/.claude` compat roots — self-contained, avoids the
   feature-flagged compat-loader flakiness, and does not depend on the manual
   WSL `~/.claude` symlinks created during diagnosis.
4. **`sync.sh` is operative**; `sync.ps1` is Windows-native parity. The Cursor
   CLI on Windows hard-codes a PowerShell shell with documented cold-start hangs
   (no `--shell` override) — the user runs `cursor-agent` under WSL, so the
   WSL-side `~/.cursor` is what matters.
5. **Agents: native subagents kept, CLI-blocked on upstream bug #160426 —
   wait, do not pivot (recorded 2026-05-19).** Empirically the Cursor CLI does
   not load user-level `~/.cursor/agents/` (staff-ack parity bug #160426, no
   fix date); it works in the IDE and self-heals when fixed. A pivot to
   agents-as-skills (the Codex pattern) *was* designed and offered; the user
   chose to **hold off and monitor** (uses Cursor IDE / cc-looper meanwhile).
   So: keep generating `~/.cursor/agents/` (zero-cost, IDE-working,
   self-healing); **do not** generate agents-as-skills or add a per-project
   `.cursor/agents/` bootstrap (the user runs `cursor-agent` from arbitrary
   repos — a per-repo install is a maintenance chore). **CLI fan-out fallback
   meanwhile:** invoke the worker's *methodology skill* by name (skills are
   user-level and do load) — recorded in `adapters/cursor/AGENTS.md`. Revisit
   when #160426 is fixed (one-line doc flip, no rework).
6. **Own exactly one discovery root.** The diagnostic `~/.claude/{skills,
   agents,commands}` WSL symlinks (created to prove links were sound) caused
   double discovery (81 vs 51) once `~/.cursor/skills` existed; they must be
   torn down. The adapter is self-contained under `~/.cursor`.
7. **`review-artifact` frozen**, feedback loop **Anchored** to `~/.claude/…` —
   identical to the recorded Codex decisions; no re-litigation here.

**Claude-impact boundary:** every adapter artifact is Category-1 (files Claude
never reads — `~/.cursor/…` generated entries + `adapters/cursor/`). Canonical
`skills/`, `agents/`, `commands/` are read-only inputs. Claude provably
unaffected.

---

## 4. What the adapter does (transform inventory)

Deterministic, idempotent, additive:

1. **Skills:** per-skill symlink (`sync.sh`) / junction (`sync.ps1`)
   `~/.cursor/skills/<name>` → canonical (35). No body transform (shared spec).
2. **Orchestrators/executors (8):** generate `~/.cursor/skills/<cn>/SKILL.md`
   with `name: <cn>` (must equal folder name — Cursor rule), `description` from
   canonical command frontmatter (YAML-quoted/escaped), `disable-model-invocation:
   true`, body = canonical command body verbatim. `.ai-kit-generated` sentinel.
3. **Agents (17):** generate `~/.cursor/agents/<name>.md` — `name`+`description`
   frontmatter + an `ai-kit-generated:` HTML-comment sentinel + body verbatim.
4. **AGENTS.md:** print placement guidance + the "personal conventions do not
   transfer" reminder (never silent — global read-location is **[verify]**).
5. **Prune:** report-only unless `--force`/`-Force`; resolves agent existence by
   frontmatter `name` (not filename), guarded against deleting non-kit entries
   or symlink targets.

No `openai.yaml`, no validator (both Codex-specific — Cursor needs neither).

---

## 5. Pre-existing defects / shared follow-ups

Same as the Codex assessment §4 (not re-opened here): meta-skill absolute paths
(`improve`/`audit-skills`/`close`) still pending; model-pins → capability-tier
abstraction **deferred** (Category-2 — edits 18 junctioned agent files). The
capability-tier work, if/when done, benefits Cursor too (it currently just drops
the pin → `model: inherit`).

---

## 6. Confidence

**95%.** Structural conclusions are robust and now **end-to-end verified on the
user's binary**: skills (51, no dupes) and the 8 explicit-only orchestrators
load and list in `cursor-agent`; the agents gap is root-caused to
staff-acknowledged bug #160426 (not our format — `/create-subagent` writes
project-scoped, confirming the mechanism). The root-cause WSL `$HOME` finding
and the duplicate-discovery-roots gotcha are observed, not inferred.

**5% uncertainty:** (a) Cursor is version-volatile and docs unversioned — the
`AGENTS.md` global read-location and four-skills-dir precedence remain
**[verify on installed binary]** (the adapter depends on neither); (b) **bug
#160426** could be fixed any day — the adapter's `~/.cursor/agents/` generation
is the deliberate self-healing path, so this is upside risk, not breakage; (c)
end-to-end run of a generated *orchestrator* (vs. just listing) not yet
exercised — Cursor-only, no Claude/gate risk.

---

## 7. Recommended next steps

1. **Built 2026-05-19 (Category-1):** `adapters/cursor/{sync.sh,sync.ps1,
   AGENTS.md,README.md}` + this assessment.
2. **Applied + verified 2026-05-19:** `sync.sh` run in WSL; `cursor-agent`
   lists 51 (30 skills + 8 explicit-only orchestrators + 13 built-in), no
   dupes. Subagents **CLI-blocked on bug #160426** (decision §3.5: wait,
   methodology-skill fallback). Diagnostic `~/.claude` symlinks torn down;
   diagnostic WSL Claude Code (`~/.local/bin/claude`) left installed (inert,
   optional cleanup).
3. **Pilot `bugfix` on Cursor** with the *unchanged* `review-artifact`
   (Cursor-only, no gate risk) — observe interactive C-mode vs Claude.
4. **Re-verify on the next Cursor update** the `[verify on installed binary]`
   items in §6 / the adapter README.
5. **Deferred & re-homed (NOT this initiative):** the convergent-review
   verdict-contract refactor — belongs with the future cc-looper-class runner
   effort, behind a Claude golden-transcript regression gate (same as Codex).

---

## Appendix — evidence base

**ai-kit side:** reuses the `codex-portability-assessment.md` Appendix greps
(unchanged canonical tree). 8 orchestrator/executor allowlist identical to the
Codex adapter's `$OrchCmds`.

**Cursor side (2026-05-19, official + probed):** Skills standard & dirs
[`cursor.com/docs/skills`]; `disable-model-invocation` semantics [`/docs/skills`];
subagents primitive + dirs + frontmatter [`cursor.com/docs/subagents`];
slash-commands deprecated/folded + `/migrate-to-skills` [`/docs/skills`,
`cursor.com/llms.txt`]; CLI reads `AGENTS.md`+`CLAUDE.md`+`mcp.json`
[`cursor.com/docs/cli/using`]; Windows-PowerShell-shell hang + WSL `$HOME`
split (forum, known issues). **Probed live on the user's `cursor-agent`**: the
§1 table (skills discovered post-fix; commands+agents not; WSL `~/.claude`
absent; Claude-Code-in-WSL cross-check).
