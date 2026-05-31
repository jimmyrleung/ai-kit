---
name: compile-kb
description: "Compile a non-Hermes markdown KB vault — synthesize accumulated source notes into a regeneratable `wiki/` tree of cross-source trend/topic pages (kept separate from `raw/`+`sources/`), adversarially review changed pages, and emit a dated 'what changed' compilation digest (incremental + idempotent). Use when asked to compile, consolidate, synthesize, or roll up a KB / wiki / vault, for a weekly or mid-week compilation, or to extract trends across accumulated notes. Detects an uninitialized vault and guides setup first. Synthesis-wiki archetype (v0). Invoke as /compile-kb."
arguments: vault_path
---

# compile-kb — the "Compile" in Collect → Compile → Wiki

You are a KB compiler. You run a periodic, **incremental** synthesis pass that turns a vault's `raw/`+`sources/` (Collect) into a regeneratable `wiki/` tree of cross-source knowledge pages plus a "what changed" digest (Compile) — `wiki/` stays separate from Collect and is fully rebuildable from it. You do **not** ingest individual sources, answer queries, run the full health-check lint, or touch **Hermes-managed all-in-one KBs** — and you **never** silently restructure a populated vault.

> **Litmus test:** if you're processing one brand-new source end-to-end (that's *ingest*), answering a question (that's *query*), or reorganizing thousands of files without an approved plan — stop, you've left the lane.

## When to use
- Weekly compilation (default cadence), or a mid-week compilation when a vault accumulates sources fast.
- "Compile / consolidate / synthesize / roll up my KB"; "extract the trends across my digests/notes"; "what's new in the wiki since last time".
- Ad-hoc before a planning/refinement session or a content session, so the wiki layer is fresh for a human or an LLM harness.

## When NOT to use
- **Add one new source** → that's *ingest* (the `llm-wiki` skill / the Hermes cron). compile-kb works the backlog ingest already produced.
- **Answer a question from the KB** → that's *query*.
- **Full structural health-check** (orphans, broken links, tag audit) → that's *lint*. compile-kb runs only the trust checks its own output needs.
- **A vault whose domains are *all* known-but-unbuilt heads** (a pure study / journal / content-gen / client-technical vault) → nothing to compile yet; inventory + defer, don't force it through the synthesis head. (A *mixed* vault with ≥1 synthesis-wiki domain → **do** use compile-kb: it compiles that domain and defers the rest.) client-technical delegates page-gen to `document-workflow`.
- **A Hermes-managed / all-in-one KB** (`raw/`+`sources/`+compiled pages maintained together by the Hermes `llm-wiki` cron — e.g. a digest-fed brain-kb; flat, no `wiki/` tree) → out of scope. compile-kb is for **non-Hermes** vaults that keep Collect and a regeneratable `wiki/` separate. Hand off to the Hermes skill.

## Input contract
- `$vault_path` — absolute path to the KB vault (git-backed Obsidian-style markdown). Required.
- Everything else (archetype, cadence, mid-week threshold, target folders, digest dir) comes from the vault's `SCHEMA.md` **Compile** block (see contract below); fall back to defaults when absent.

## Preflight — detect, then orient or guide
Run every invocation, before anything else.

1. Confirm `$vault_path` exists and is a directory.
2. **Hermes guard — run before any branching.** compile-kb is for **non-Hermes** vaults only; Hermes-managed KBs are owned end-to-end (ingest *and* synthesis) by the Hermes `llm-wiki` cron, so we never init, repair, migrate, or compile them. **If the vault carries a Hermes provenance signal — a `sources/**` note whose `creator` is a `*Hermes*` cron, or a `SCHEMA.md` that names Hermes / an external manager — STOP and hand off.** The all-in-one flat shape (compiled pages maintained alongside `raw/`+`sources/`, no separate `wiki/` tree) *corroborates* but is not alone decisive: a non-Hermes vault can also be flat and merely needs migration (that's step 5, not a handoff). Run this **first** — a Hermes vault is flat (no `wiki/` tree), so it would otherwise fall through to step 5 ("not initialized") and get a `wiki/` tree built over it.
3. Check for `SCHEMA.md` at the vault root and a `wiki/` tree containing `wiki/index.md` + `wiki/log.md` (the synthesized layer lives under `wiki/`).
4. **All present → orient** (the existing-wiki path): read `SCHEMA.md` (root) in full, read `wiki/index.md`, read the last ~30 lines of `wiki/log.md`. Resolve the archetype(s) from the SCHEMA **Compile** block — a single `archetype:`, or a **`domains:` map** (each `raw/`/`sources/` subfolder → its head) for a mixed vault; if absent, **infer** (a `wiki/` tree with `sources/` + typed `wiki/concepts/`+`wiki/topics/` ⇒ `synthesis-wiki`) and suggest an explicit block. Archetypes are an **open set** (rule 9); resolve **per domain** 3 ways: **(a)** built head (`synthesis-wiki` today) → compile that domain into the shared `wiki/`; **(b)** known-but-unbuilt head (`study`/`journal`/`content-gen`/`client-technical`) → skip + report it deferred; **(c)** fits **none** → don't force-fit, don't compile — **propose a new archetype** (name + head sketch + signals) **plus the skill update** (rule 9). Compile every domain with a built head; report the deferred/proposed ones. If **no** domain has a built head, STOP after reporting.
5. **`SCHEMA.md` or the `wiki/` tree missing → not initialized.** Classify, then branch — **never auto-restructure**:
   - **Greenfield** (≈0 content `.md` outside `raw/`, `templates/`, `.obsidian/`): offer a **guided init** — ask the archetype + domain (be specific), then write the **segregated synthesis-wiki scaffold**: `SCHEMA.md` (root, with a Compile block) + `raw/`+`sources/` (Collect), and the `wiki/` tree for Compile output (`wiki/index.md`, `wiki/log.md`, `wiki/_meta/`, `wiki/topics/`, `wiki/concepts/`, `wiki/comparisons/`, `wiki/_compilations/`); confirm; suggest first sources. Then stop (nothing to compile yet) unless sources already exist.
   - **Populated but unstructured** (many `.md`, no SCHEMA/3-layer — e.g. a course dump): this is a **migration, not an init**. Do **not** move or rewrite anything. Produce a *proposal* = **a complete disposition inventory** accounting for **100%** of the vault (every top-level area → a `raw/` **domain** + its head + status — not just one slice), a draft **root** `SCHEMA.md` (with a `domains:` map if mixed), and a `raw/ ↔ sources/ ↔ wiki` mapping for a representative slice; present it, then STOP. **One canonical layout per vault:** root = `SCHEMA.md` + `raw/` + `sources/` + `wiki/`, archetypes as **domains** (`raw/<domain>/`, `sources/<domain>/`) all compiling into the **one shared `wiki/`** — never a per-subtree mini-vault. **Inventory counts:** exclude vendored/build exhaust (`**/repos/**` `node_modules`, lockfiles, `dist/`) and report raw-file vs real-note counts — **but first-party lesson/sample code is a *study* source** (explore it, extract the learning), not exhaust. For a domain whose head is **known-but-unbuilt** (e.g. `study`), inventory + defer it; for one fitting **no** known archetype, propose a new one + its skill update (rule 9). Write the full proposal to `init-proposal.md` at the vault root (the vault-local note), then stop. Executing the migration — seeding root `raw/`+`sources/` from the existing files — is a **guided manual step** (AI-assisted, you-approved) *outside* this skill; compile-kb only consumes Collect once it exists. (A dedicated `kb-init` may be extracted later once the shape is proven; it isn't built yet.)
   - **Partial** (`SCHEMA.md` present, but the `wiki/` tree / `wiki/index.md` / `wiki/log.md` missing): branch on how populated the vault already is. A **sparse half-init** (little or no synthesized content outside `raw/`+`sources/`) is safe to **repair** — recreate the missing `wiki/` scaffolding from current files without clobbering the SCHEMA. A vault **already populated with synthesized pages in a flat layout** (pre-segregation, or a foreign tool's shape) is a **migration, not a repair** — do **not** build a `wiki/` tree over it; route to the *Populated but unstructured* proposal path above (executing the migration is a guided manual step, not this skill), per rule #3.

## Process (synthesis-wiki compile head)
Follow the vault's own `SCHEMA.md` conventions over this skill's defaults wherever they differ (folder names, `domains`/`themes` vs `tags`, page types).

### Phase 1 — Find work (incremental)
- Find the last compile: the most recent `## [YYYY-MM-DD] compile |` entry in `wiki/log.md` (or "never").
- Collect candidate sources: `sources/**/*.md` with `status: summarized` (not yet `integrated`), OR `updated`/`date_consumed` after the last compile, plus any raw files whose `sha256` no longer matches (drift). Harvest each candidate's `## Concepts to Update` list.
- **Idempotent:** if nothing changed since the last compile, report "nothing to compile" and exit without writing. (Honor an explicit "recompile everything" request to override.)

### Phase 2 — Synthesize
- Cluster candidate sources by `domains`/`themes` + content. For each cluster meeting the SCHEMA page-creation threshold (central to one source, or appears across 2+), create or update the target **knowledge page**:
  - **Trend/topic pages are the primary v0 output** — the cross-source synthesis that ingest alone never produces (e.g. rolling many digests into a trend page). Place under the vault's `wiki/` tree per SCHEMA `compile_targets` (`wiki/topics/`, `wiki/concepts/`, …) — the regeneratable Compile layer; never write `raw/` or `sources/`.
  - **Merge without flattening:** when sources disagree, keep both claims with dates + links in a `## Tensions / Contradictions` section, lower `confidence`, set `contested: true`. Never silently pick a winner.
  - **Claim-level provenance:** on pages synthesizing 3+ sources, append `^[sources/<path>]` markers at paragraph granularity so each claim traces back without re-reading the source.
  - Cross-link (≥2 `[[wikilinks]]`), update each page's `## Source Trail`, and bump the consumed source notes to `status: integrated`.
  - Respect ingestion levels; split pages over ~200 lines; don't create pages for passing mentions.

### Phase 3 — Adversarial review (mandatory on changed synthesis pages)
- For each created/updated page, run a second **skeptical** pass (ideally a separate reviewer agent or a fresh critical read) that hunts: overreach, unsupported generalizations, claims not traceable to a cited source, and contradictions with existing pages.
- Apply outcomes: demote `confidence`, set `contested: true` + `contradictions: [page]`, or mark a non-surviving claim's page `status: draft`. This is the concrete guard against hallucinations hardening into wiki fact — meter it to synthesis pages only.

### Phase 4 — Update navigation
- Patch `wiki/index.md`: add new pages under the correct type section; **recompute** the `> Last updated: … | Total pages: N` header (fix drift).
- Update affected `wiki/_meta/*-map.md` MOCs.
- Append `## [YYYY-MM-DD] compile | <one-line summary>` to `wiki/log.md`; rotate to `wiki/log-YYYY.md` if it exceeds 500 entries.

### Phase 5 — Emit the compilation digest
Write the dated digest the user reads and points harnesses at, to `<digest_dir>/YYYY-MM-DD-compile.md` (default `wiki/_compilations/`). Shape:

```markdown
# Compilation — YYYY-MM-DD

> Window: <last-compile-date> → <today> | Sources compiled: N | Pages touched: M

## New & emerging trends
- <trend> — <1-2 lines> ([[trend-page]])

## Pages created / updated
- [[page]] — created|updated — <what changed>

## Newly contested / contradicted
- [[page]] — <the tension, with both sources>

## Now stale / needs attention
- [[page]] — <why> (e.g. no corroboration, >90d old, low confidence)
```

### Phase 6 — Verify & commit
- `git diff --check`; inspect `git diff --stat`; ensure `raw/`, media, and secrets are **not** staged.
- **Show the diff to the user. Commit curated files only, with the user's OK** (or per an automated workflow's explicit expectation). Never auto-commit a vault you were told to leave uncommitted.

### Confidence gate
Score the compile (CLAUDE.md format). Any synthesis page you can't support at ≥ high confidence ships as `confidence: medium|low` and/or `status: draft` — never as asserted fact. If the overall compile is < 90% sound, surface what's uncertain instead of committing.

## SCHEMA `## Compile` contract (the archetype plug)
A vault declares how it wants to be compiled. compile-kb reads this; future archetype heads read the same block. Add it to the vault's `SCHEMA.md`:

```yaml
## Compile
archetype: synthesis-wiki      # single-archetype vault: one head. Known heads (OPEN set — propose a new one, rule 9): synthesis-wiki | study | journal | content-gen | client-technical
domains:                       # OPTIONAL — mixed vault: map each raw/sources subfolder → its head (structural; distinct from a source note's themes/tags)
  discussions: synthesis-wiki  #   raw/discussions/ + sources/discussions/ → synthesis-wiki
  courses: study               #   raw/courses/ + sources/courses/         → study (compiles once that head ships)
cadence: weekly                # default; mid-week auto-suggested at the threshold
midweek_threshold: 15          # uncompiled source notes that warrant an early compile
compile_targets: [wiki/topics, wiki/concepts, wiki/comparisons]   # the shared wiki/ tree, separate from raw/ + sources/
digest_dir: wiki/_compilations
```

Defaults when the block is absent: `archetype: synthesis-wiki` (only if inferable, else STOP), `cadence: weekly`, `midweek_threshold: 15`, targets under `wiki/`, digest `wiki/_compilations`. Recommend the user add an explicit block; do not silently edit their SCHEMA without showing the change. **Structure — one canonical layout per vault:** root = `SCHEMA.md` + `raw/` + `sources/` + `wiki/`. **Archetypes live as domains** — `raw/<domain>/` + `sources/<domain>/` (Collect, domain-foldered, mapped to heads by `domains:`); **everything synthesized lives under the one shared `wiki/`** — `wiki/index.md`, `wiki/log.md`, `wiki/_meta/` maps, the pages, `wiki/_compilations/` — fully regeneratable from Collect. A single-archetype vault just sets `archetype:` and may skip the domain subfolders. The `wiki/` tree's presence marks a compile-kb-managed vault (Hermes KBs stay flat/all-in-one, out of scope).

## Important rules
1. **Orient before acting** — read `SCHEMA.md` + `wiki/index.md` + recent `wiki/log.md` every session. Skipping it duplicates pages and misses cross-references.
2. **Incremental + idempotent** — only touch what changed since the last compile; a no-change run writes nothing.
3. **Never auto-restructure a populated vault** — detect → propose → await approval. Executing the migration is a **guided manual step** outside this skill (a `kb-init` may be extracted later; unbuilt today).
4. **Never silently resolve contradictions** — keep both claims, lower confidence, flag for review.
5. **Adversarial review is not optional** on changed synthesis pages — don't let weak claims harden.
6. **Never commit `raw/`, media, or secrets** — show the diff, commit curated only, with approval.
7. **The vault's SCHEMA wins** over this skill's defaults.
8. **Ask before mass-updating 10+ existing pages** in one compile.
9. **Archetypes are open; heads are not improvised.** Fit a known head, or — when a vault/domain fits none — *propose* a new archetype **and** the concrete compile-kb update to support it. Surface it inline **and** persist it to a vault-local note at the vault root (fold into `init-proposal.md` if you're emitting one, else write `archetype-suggestion.md`). **Never invent a compile for a head that doesn't exist** — propose, then stop. Classification is probabilistic; the safety rails (no auto-restructure, the Hermes provenance gate, idempotency, show-diff-before-commit) stay deterministic.

## What this skill does NOT do
- **Ingest a single source** → the `llm-wiki` skill / Hermes cron (compile-kb consumes the backlog ingest produced).
- **Query / answer questions** → the query operation.
- **Full structural lint** → the lint operation (orphans, broken links, tag audit, log rotation).
- **Study / journal / content-gen / client-technical compiles** → their archetype heads (later); client-technical delegates to `document-workflow`.
- **Heavy migration of a populated uninitialized vault** → emits the proposal/plan only; executing it is a **guided manual step** (AI-assisted, you-approved) outside this skill — a future `kb-init` once proven, unbuilt today.
- **Operate on a Hermes-managed all-in-one KB** → the Hermes `llm-wiki` skill owns those (ingest + synthesis in one loop, flat layout, no `wiki/` tree).
- **HTML / rendered views** → a deferred derived view, not this skill.

## Output
Within `$vault_path`: knowledge pages under the shared `wiki/` tree (per `compile_targets`); `wiki/index.md` + `wiki/_meta` maps refreshed; a `wiki/log.md` `compile` entry appended; the compilation digest under `<digest_dir>/` (default `wiki/_compilations/`). Root layout = `SCHEMA.md` + `raw/` + `sources/` + `wiki/`; compile writes only under `wiki/` — never `raw/` or `sources/` (Collect is read-only to compile). Commits only curated files, only with approval.
