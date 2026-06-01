---
name: compile-kb
description: "Compile a non-Hermes markdown KB vault — synthesize accumulated source notes into a regeneratable `wiki/` tree of cross-source trend/topic pages (kept separate from `raw/`+`sources/`), adversarially review changed pages, and emit a dated 'what changed' compilation digest (incremental + idempotent). Use when asked to compile, consolidate, synthesize, roll up, convert, migrate, or initialize a KB / wiki / vault, for a weekly or mid-week compilation, or to extract trends across accumulated notes. Detects an uninitialized vault and converts it to the canonical raw/sources/wiki layout (approval-gated). Synthesis-wiki head plus a generic baseline fallback — every domain converts and gets baseline wiki now, upgradeable when its specialized head ships, so it never dead-ends (v0). Invoke as /compile-kb."
arguments: vault_path
---

# compile-kb — the "Compile" in Collect → Compile → Wiki

You are a KB compiler. You run a periodic, **incremental** synthesis pass that turns a vault's `raw/`+`sources/` (Collect) into a regeneratable `wiki/` tree of cross-source knowledge pages plus a "what changed" digest (Compile) — `wiki/` stays separate from Collect and is fully rebuildable from it. You do **not** ingest individual sources, answer queries, run the full health-check lint, or touch **Hermes-managed all-in-one KBs** — and you **never** silently restructure a populated vault. But you also **never dead-end**: when a domain has no built *specialized* head, a generic **baseline head** is the always-available fallback — it converts the domain to the canonical `raw/`+`sources/`+`wiki/` layout (only behind an **approved** plan, never silently) and emits honest baseline pages marked `unsynthesized`, upgradeable in place when its specialized head ships.

> **Litmus test:** if you're processing one brand-new source end-to-end (that's *ingest*), answering a question (that's *query*), or reorganizing thousands of files without an approved plan — stop, you've left the lane.

## When to use
- Weekly compilation (default cadence), or a mid-week compilation when a vault accumulates sources fast.
- "Compile / consolidate / synthesize / roll up my KB"; "extract the trends across my digests/notes"; "what's new in the wiki since last time".
- Ad-hoc before a planning/refinement session or a content session, so the wiki layer is fresh for a human or an LLM harness.
- Convert / initialize a populated vault to the canonical `raw/`+`sources/`+`wiki/` layout (approval-gated) — the **baseline head** carries any domain that has no built specialized head, so no part of the vault is left behind.

## When NOT to use
- **Add one new source** → that's *ingest* (the `llm-wiki` skill / the Hermes cron). compile-kb works the backlog ingest already produced.
- **Answer a question from the KB** → that's *query*.
- **Full structural health-check** (orphans, broken links, tag audit) → that's *lint*. compile-kb runs only the trust checks its own output needs.
- **Forcing non-synthesis material through the synthesis-wiki head** — don't. A pure study / journal / content-gen / client-technical vault (or such a domain in a mixed vault) is still **in scope**, but it's carried by the **baseline head** (convert + honest baseline wiki), *not* by faking synthesis pages. A mixed vault compiles its synthesis-wiki domain(s) with that head and baselines the rest — every domain progresses. client-technical delegates richer page-gen to `document-workflow` once that head ships.
- **A Hermes-managed / all-in-one KB** (`raw/`+`sources/`+compiled pages maintained together by the Hermes `llm-wiki` cron — e.g. a digest-fed brain-kb; flat, no `wiki/` tree) → out of scope. compile-kb is for **non-Hermes** vaults that keep Collect and a regeneratable `wiki/` separate. Hand off to the Hermes skill.

## Input contract
- `$vault_path` — absolute path to the KB vault (git-backed Obsidian-style markdown). Required.
- Everything else (archetype, cadence, mid-week threshold, target folders, digest dir) comes from the vault's `SCHEMA.md` **Compile** block (see contract below); fall back to defaults when absent.

## Preflight — detect, then orient or guide
Run every invocation, before anything else.

1. Confirm `$vault_path` exists and is a directory.
2. **Hermes guard — run before any branching.** compile-kb is for **non-Hermes** vaults only; Hermes-managed KBs are owned end-to-end (ingest *and* synthesis) by the Hermes `llm-wiki` cron, so we never init, repair, migrate, or compile them. **If the vault carries a Hermes provenance signal — a `sources/**` note whose `creator` is a `*Hermes*` cron, or a `SCHEMA.md` that names Hermes / an external manager — STOP and hand off.** The all-in-one flat shape (compiled pages maintained alongside `raw/`+`sources/`, no separate `wiki/` tree) *corroborates* but is not alone decisive: a non-Hermes vault can also be flat and merely needs migration (that's step 5, not a handoff). Run this **first** — a Hermes vault is flat (no `wiki/` tree), so it would otherwise fall through to step 5 ("not initialized") and get a `wiki/` tree built over it.
3. Check for `SCHEMA.md` at the vault root and a `wiki/` tree containing `wiki/index.md` + `wiki/log.md` (the synthesized layer lives under `wiki/`).
4. **All present → orient** (the existing-wiki path): read `SCHEMA.md` (root) in full, read `wiki/index.md`, read the last ~30 lines of `wiki/log.md`. Resolve the archetype(s) from the SCHEMA **Compile** block — a single `archetype:`, or a **`domains:` map** (each `raw/`/`sources/` subfolder → its head) for a mixed vault; if absent, **infer** (a `wiki/` tree with `sources/` + typed `wiki/concepts/`+`wiki/topics/` ⇒ `synthesis-wiki`) and suggest an explicit block. Archetypes are an **open set** (rule 9); resolve **per domain**: **(a)** built **specialized** head (`synthesis-wiki` today) → compile that domain with its head into the shared `wiki/`; **(b)** known-but-unbuilt head (`study`/`journal`/`content-gen`/`client-technical`) → the **baseline head** (honest baseline wiki, marked `unsynthesized`), reported as awaiting its specialized head; **(c)** fits **none** → **propose a new archetype** (name + head sketch + signals) **plus the skill update** (rule 9) **and still run the baseline head** so the domain progresses now. **No domain is ever skipped or stopped** — the baseline head is the always-available fallback. **Graduation:** when a specialized head later ships, it upgrades that domain's baseline pages in place.
5. **`SCHEMA.md` or the `wiki/` tree missing → not initialized.** Classify, then branch — **never *silently* restructure** (the baseline head converts only behind an approved plan):
   - **Greenfield** (≈0 content `.md` outside `raw/`, `templates/`, `.obsidian/`): offer a **guided init** — ask the archetype + domain (be specific), then write the **segregated synthesis-wiki scaffold**: `SCHEMA.md` (root, with a Compile block) + `raw/`+`sources/` (Collect), and the `wiki/` tree for Compile output (`wiki/index.md`, `wiki/log.md`, `wiki/_meta/`, `wiki/topics/`, `wiki/concepts/`, `wiki/comparisons/`, `wiki/_compilations/`); confirm; suggest first sources. Then stop (nothing to compile yet) unless sources already exist.
   - **Populated but unstructured** (many `.md`, no SCHEMA/3-layer — e.g. a course dump): this is a **migration, not an init**, run in **two approval-gated steps — propose, then (on approval) the baseline head executes it.** **Step 1 — propose & PAUSE:** produce **a complete disposition inventory** accounting for **100%** of the vault (every top-level area → a `raw/` **domain** + its head + status — not just one slice), a draft **root** `SCHEMA.md` (with a `domains:` map if mixed), and a `raw/ ↔ sources/ ↔ wiki` mapping for a representative slice; write it to `init-proposal.md` at the vault root and **wait for approval — do not move anything yet.** **Step 2 — convert on approval:** for each **approved** domain (all, or a subset you pick), the **baseline head** seeds root `raw/<domain>/` + `sources/<domain>/` from the existing files (git-`mv`, history preserved) and emits baseline wiki; a domain with a built specialized head then compiles with it. **One canonical layout per vault:** root = `SCHEMA.md` + `raw/` + `sources/` + `wiki/`, archetypes as **domains** (`raw/<domain>/`, `sources/<domain>/`) all compiling into the **one shared `wiki/`** — never a per-subtree mini-vault. **Inventory + conversion exclude exhaust:** vendored/build (`**/repos/**`, `node_modules`, lockfiles, `dist/`) and the SCHEMA's listed exhaust stay put; report raw-file vs real-note counts — **but first-party lesson/sample code is a *study* source** (explore it, extract the learning), not files to migrate one-by-one. For a domain fitting **no** known archetype, propose a new one + its skill update (rule 9), then baseline it like any other. **Ask before converting 10+ domains or moving large folders** (rule 8). compile-kb now *executes* the approved migration via the baseline head — it is **no longer an out-of-skill manual step** (the deferred `kb-init` is folded in; a standalone extraction may still follow once proven).
   - **Partial** (`SCHEMA.md` present, but the `wiki/` tree / `wiki/index.md` / `wiki/log.md` missing): branch on how populated the vault already is. A **sparse half-init** (little or no synthesized content outside `raw/`+`sources/`) is safe to **repair** — recreate the missing `wiki/` scaffolding from current files without clobbering the SCHEMA. A vault **already populated with synthesized pages in a flat layout** (pre-segregation, or a foreign tool's shape) is a **migration, not a repair** — do **not** build a `wiki/` tree over it; route to the *Populated but unstructured* propose-then-convert path above (approval-gated, executed by the baseline head), per rule #3.

## Process (synthesis-wiki compile head)
Follow the vault's own `SCHEMA.md` conventions over this skill's defaults wherever they differ (folder names, `domains`/`themes` vs `tags`, page types).

### Phase 1 — Find work (incremental)
- Find the last compile: the most recent `## [YYYY-MM-DD] compile |` entry in `wiki/log.md` (or "never").
- Collect candidate sources: `sources/**/*.md` with `status: summarized` (not yet `integrated`), OR `updated`/`date_consumed` after the last compile, plus any raw files whose `sha256_prefix` no longer matches (drift). Harvest each candidate's `## Concepts to Update` list.
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

## Process (baseline fallback head)
The always-available fallback for any domain without a built **specialized** head — so compile-kb **never dead-ends**. It does two honest things and nothing else; it **never** fabricates synthesis-wiki-shaped pages (that guard is the whole reason this is a separate head, not a setting on the synthesis head).

### B1 — Convert (approval-gated, idempotent)
- Run only after the step-5 disposition proposal is **approved**. For each approved domain, seed `raw/<domain>/` from the existing files (git-`mv`, history preserved) and create one `sources/<domain>/` note per real source (short summary + frontmatter: `status`, `domains`, `themes`, `date_consumed`, `source_type`, `original_filename`, `raw:`, `sha256_prefix`).
- **Exclude** `.git/`, `.obsidian/`, `_migration/`, and the SCHEMA's listed exhaust; treat first-party lesson/sample code as a *study source* to explore on demand, not per-file notes.
- **Idempotent:** a domain already seeded at `raw/<domain>/` is **not** re-converted — skip it. Honor rules 3, 6, 8 (never silent, never commit `raw/` / secrets unprompted, ask before 10+ domains / large moves).

### B2 — Baseline wiki (honest, clearly marked)
- Emit a domain MOC at `wiki/_meta/<domain>-map.md`, and — per the SCHEMA's `baseline_depth` — optionally light per-source notes under `wiki/<domain>/`: an organized index + short summaries, **not** cross-source synthesis.
- Every baseline page carries `head: baseline`, `status: unsynthesized`, `confidence: low`, and a visible top banner (`> ⚠ baseline — not yet synthesized`) so it can never be mistaken for, or harden into, real synthesis.
- Patch `wiki/index.md` (recompute the count; list these under a clearly-labelled **Baseline (unsynthesized)** section) and append `## [YYYY-MM-DD] baseline | <domain> converted + baselined` to `wiki/log.md`.

### B3 — Graduate (when a specialized head ships)
- A newly-built specialized head **upgrades the baseline pages in place**: it reads the same `sources/<domain>/`, replaces the baseline pages with real synthesis, and clears the `unsynthesized` / `head: baseline` markers. Baseline output is a **floor, never a ceiling** — graduation is encoded by the `## Compile` `domains:` map (flip the domain's head once it exists).

Phases 5 (digest — record conversions + baselinings) and 6 (verify & commit) then apply as for the synthesis head.

## SCHEMA `## Compile` contract (the archetype plug)
A vault declares how it wants to be compiled. compile-kb reads this; future archetype heads read the same block. Add it to the vault's `SCHEMA.md`:

```yaml
## Compile
archetype: synthesis-wiki      # single-archetype vault: one head. Known heads (OPEN set — propose a new one, rule 9): synthesis-wiki | study | journal | content-gen | client-technical. Any domain without a built specialized head auto-falls-back to the implicit **baseline** head (never declared).
domains:                       # OPTIONAL — mixed vault: map each raw/sources subfolder → its head (structural; distinct from a source note's themes/tags)
  discussions: synthesis-wiki  #   raw/discussions/ + sources/discussions/ → synthesis-wiki
  courses: study               #   study head unbuilt → baseline now (convert + baseline wiki); real study synthesis when that head ships
cadence: weekly                # default; mid-week auto-suggested at the threshold
midweek_threshold: 15          # uncompiled source notes that warrant an early compile
compile_targets: [wiki/topics, wiki/concepts, wiki/comparisons]   # the shared wiki/ tree, separate from raw/ + sources/
digest_dir: wiki/_compilations
baseline_depth: moc+notes      # baseline-head output depth: `moc` (domain MOC only) | `moc+notes` (MOC + light per-source notes)
```

Defaults when the block is absent: `archetype: synthesis-wiki` (only if inferable; else propose a block and fall back to the **baseline head** — never STOP on an undetermined head), `cadence: weekly`, `midweek_threshold: 15`, targets under `wiki/`, digest `wiki/_compilations`, `baseline_depth: moc+notes`. Recommend the user add an explicit block; do not silently edit their SCHEMA without showing the change. **Structure — one canonical layout per vault:** root = `SCHEMA.md` + `raw/` + `sources/` + `wiki/`. **Archetypes live as domains** — `raw/<domain>/` + `sources/<domain>/` (Collect, domain-foldered, mapped to heads by `domains:`); **everything synthesized lives under the one shared `wiki/`** — `wiki/index.md`, `wiki/log.md`, `wiki/_meta/` maps, the pages, `wiki/_compilations/` — fully regeneratable from Collect. A single-archetype vault just sets `archetype:` and may skip the domain subfolders. The `wiki/` tree's presence marks a compile-kb-managed vault (Hermes KBs stay flat/all-in-one, out of scope). **Baseline pages** (from the fallback head) carry `head: baseline` + `status: unsynthesized` + `confidence: low` and live under `wiki/` alongside synthesis pages until a specialized head graduates them in place.

## Important rules
1. **Orient before acting** — read `SCHEMA.md` + `wiki/index.md` + recent `wiki/log.md` every session. Skipping it duplicates pages and misses cross-references.
2. **Incremental + idempotent** — only touch what changed since the last compile; a no-change run writes nothing.
3. **Never *silently* restructure a populated vault** — detect → propose → **await approval** → then the **baseline head** executes the approved conversion (asking again before 10+ domains / large moves, rule 8). compile-kb *does* perform migration now — but only an **approved** plan, never automatically on sight.
4. **Never silently resolve contradictions** — keep both claims, lower confidence, flag for review.
5. **Adversarial review is not optional** on changed synthesis pages — don't let weak claims harden.
6. **Never commit `raw/`, media, or secrets** — show the diff, commit curated only, with approval.
7. **The vault's SCHEMA wins** over this skill's defaults.
8. **Ask before mass-updating 10+ existing pages** in one compile.
9. **Archetypes are open; heads are not improvised.** Fit a known head, or — when a vault/domain fits none — *propose* a new archetype **and** the concrete compile-kb update to support it. Surface it inline **and** persist it to a vault-local note at the vault root (fold into `init-proposal.md` if you're emitting one, else write `archetype-suggestion.md`). **Never *fake* a specialized head's output — but never *stop* either:** propose the new archetype **and** run the **baseline head** so the domain still progresses (propose ≠ dead-end). Classification is probabilistic; the safety rails (no *silent* restructure, the Hermes provenance gate, idempotency, show-diff-before-commit) stay deterministic.

## What this skill does NOT do
- **Ingest a single source** → the `llm-wiki` skill / Hermes cron (compile-kb consumes the backlog ingest produced).
- **Query / answer questions** → the query operation.
- **Full structural lint** → the lint operation (orphans, broken links, tag audit, log rotation).
- **Specialized study / journal / content-gen / client-technical *synthesis*** → their archetype heads (later); until then the **baseline head** carries those domains honestly (convert + baseline wiki). client-technical delegates richer page-gen to `document-workflow`.
- **Silently restructure / migrate on sight** → never. compile-kb proposes the disposition first and converts only the **approved** plan (the baseline head then executes it). Conversion is in-skill now, but always behind approval.
- **Operate on a Hermes-managed all-in-one KB** → the Hermes `llm-wiki` skill owns those (ingest + synthesis in one loop, flat layout, no `wiki/` tree).
- **HTML / rendered views** → a deferred derived view, not this skill.

## Output
Within `$vault_path`: knowledge pages under the shared `wiki/` tree (per `compile_targets`); `wiki/index.md` + `wiki/_meta` maps refreshed; a `wiki/log.md` `compile`/`baseline` entry appended; the compilation digest under `<digest_dir>/` (default `wiki/_compilations/`). Root layout = `SCHEMA.md` + `raw/` + `sources/` + `wiki/`. **Synthesis compile writes only under `wiki/`** — never `raw/` or `sources/` (Collect is read-only to it). The **baseline head**, on an **approved** conversion, additionally seeds `raw/<domain>/` + `sources/<domain>/` once (the one sanctioned write outside `wiki/`). Commits only curated files, only with approval.
