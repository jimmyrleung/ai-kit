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
- **A study / journal / content-gen / client-technical vault** → those archetypes have their own compile heads (later increments). client-technical delegates page generation to `document-workflow`. STOP and say so.
- **A Hermes-managed / all-in-one KB** (`raw/`+`sources/`+compiled pages maintained together by the Hermes `llm-wiki` cron — e.g. a digest-fed brain-kb; flat, no `wiki/` tree) → out of scope. compile-kb is for **non-Hermes** vaults that keep Collect and a regeneratable `wiki/` separate. Hand off to the Hermes skill.

## Input contract
- `$vault_path` — absolute path to the KB vault (git-backed Obsidian-style markdown). Required.
- Everything else (archetype, cadence, mid-week threshold, target folders, digest dir) comes from the vault's `SCHEMA.md` **Compile** block (see contract below); fall back to defaults when absent.

## Preflight — detect, then orient or guide
Run every invocation, before anything else.

1. Confirm `$vault_path` exists and is a directory.
2. Check for `SCHEMA.md` at the vault root and a `wiki/` tree containing `wiki/index.md` + `wiki/log.md` (the synthesized layer lives under `wiki/`).
3. **All present → orient** (the existing-wiki path): read `SCHEMA.md` (root) in full, read `wiki/index.md`, read the last ~30 lines of `wiki/log.md`. **Hermes guard:** if the vault is Hermes-managed (flat — no `wiki/` tree — with `sources/**` notes whose `creator` is a `*Hermes*` cron, or SCHEMA names an external manager), STOP and hand off; compile-kb manages a `wiki/` tree, Hermes KBs stay flat/all-in-one. Resolve the archetype from the SCHEMA **Compile** block (or a `## Archetype` line); if absent, **infer** — `sources/` + typed `concepts/`+`topics/` folders ⇒ `synthesis-wiki` — record the inference and suggest the user add an explicit `archetype:`. If the archetype is **not** `synthesis-wiki`, STOP: name the archetype, say its compile head isn't built yet, and hand off. Otherwise continue to Process.
4. **`SCHEMA.md` or the `wiki/` tree missing → not initialized.** Classify, then branch — **never auto-restructure**:
   - **Greenfield** (≈0 content `.md` outside `raw/`, `templates/`, `.obsidian/`): offer a **guided init** — ask the archetype + domain (be specific), then write the **segregated synthesis-wiki scaffold**: `SCHEMA.md` (root, with a Compile block) + `raw/`+`sources/` (Collect), and the `wiki/` tree for Compile output (`wiki/index.md`, `wiki/log.md`, `wiki/_meta/`, `wiki/topics/`, `wiki/concepts/`, `wiki/comparisons/`, `wiki/_compilations/`); confirm; suggest first sources. Then stop (nothing to compile yet) unless sources already exist.
   - **Populated but unstructured** (many `.md`, no SCHEMA/3-layer — e.g. a course dump): this is a **migration, not an init**. Do **not** move or rewrite anything. Produce a *proposal*: sample the content, infer the archetype + a draft `SCHEMA.md` + a proposed `raw/ ↔ sources/ ↔ wiki` file mapping for a representative slice; present it for the user to approve/edit; STOP. In a headless run, write the proposal to `init-proposal.md` at the vault root and stop. The heavy migration is a separate guided step (`kb-init`).
   - **Partial** (`SCHEMA.md` present but the `wiki/` tree, `wiki/index.md`, or `wiki/log.md` missing): repair the missing scaffolding from current files — do not clobber the SCHEMA.

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
archetype: synthesis-wiki      # synthesis-wiki | study | journal | content-gen | client-technical
cadence: weekly                # default; mid-week auto-suggested at the threshold
midweek_threshold: 15          # uncompiled source notes that warrant an early compile
compile_targets: [wiki/topics, wiki/concepts, wiki/comparisons]   # the regeneratable Compile tree, separate from raw/ + sources/
digest_dir: wiki/_compilations
```

Defaults when the block is absent: `archetype: synthesis-wiki` (only if inferable, else STOP), `cadence: weekly`, `midweek_threshold: 15`, targets under `wiki/` (`wiki/topics`, `wiki/concepts`, …), digest `wiki/_compilations`. Recommend the user add an explicit block; do not silently edit their SCHEMA without showing the change. **Structure:** root = `SCHEMA.md` + `raw/` + `sources/` (Collect); **everything synthesized lives under `wiki/`** — `wiki/index.md`, `wiki/log.md`, `wiki/_meta/` maps, the pages, and `wiki/_compilations/` — fully regeneratable from Collect. The `wiki/` tree's presence marks a compile-kb-managed vault (Hermes-managed KBs stay flat/all-in-one and are out of scope).

## Important rules
1. **Orient before acting** — read `SCHEMA.md` + `wiki/index.md` + recent `wiki/log.md` every session. Skipping it duplicates pages and misses cross-references.
2. **Incremental + idempotent** — only touch what changed since the last compile; a no-change run writes nothing.
3. **Never auto-restructure a populated vault** — detect → propose → await approval. Migration is `kb-init`'s job.
4. **Never silently resolve contradictions** — keep both claims, lower confidence, flag for review.
5. **Adversarial review is not optional** on changed synthesis pages — don't let weak claims harden.
6. **Never commit `raw/`, media, or secrets** — show the diff, commit curated only, with approval.
7. **The vault's SCHEMA wins** over this skill's defaults.
8. **Ask before mass-updating 10+ existing pages** in one compile.

## What this skill does NOT do
- **Ingest a single source** → the `llm-wiki` skill / Hermes cron (compile-kb consumes the backlog ingest produced).
- **Query / answer questions** → the query operation.
- **Full structural lint** → the lint operation (orphans, broken links, tag audit, log rotation).
- **Study / journal / content-gen / client-technical compiles** → their archetype heads (later); client-technical delegates to `document-workflow`.
- **Heavy migration of a populated uninitialized vault** → emits a proposal; `kb-init` owns the guided migration.
- **Operate on a Hermes-managed all-in-one KB** → the Hermes `llm-wiki` skill owns those (ingest + synthesis in one loop, flat layout, no `wiki/` tree).
- **HTML / rendered views** → a deferred derived view, not this skill.

## Output
Within `$vault_path`: knowledge pages under the `wiki/` tree (per `compile_targets`); `wiki/index.md` + `wiki/_meta` maps refreshed; a `wiki/log.md` `compile` entry appended; the compilation digest under `<digest_dir>/` (default `wiki/_compilations/`). Root keeps only `SCHEMA.md` + `raw/` + `sources/`; never writes `raw/` or `sources/` — Collect is read-only to compile. Commits only curated files, only with approval.
