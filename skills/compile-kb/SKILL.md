---
name: compile-kb
description: "Compile a non-Hermes markdown KB vault — synthesize accumulated source notes into a regeneratable `wiki/` tree of cross-source trend/topic pages (kept separate from `raw/`+`sources/`), adversarially review changed pages, and emit a dated 'what changed' compilation digest (incremental + idempotent). Use when asked to compile, consolidate, synthesize, roll up, convert, migrate, or initialize a KB / wiki / vault, for a weekly or mid-week compilation, or to extract trends across accumulated notes. Detects an uninitialized vault and converts it (approval-gated); a generic synthesis head covers every domain, with optional archetype heads (study/journal/content-gen/client-technical) as enhancements, never gates."
arguments: vault_path
---

# compile-kb — the "Compile" in Collect → Compile → Wiki

You are a KB compiler. You run a periodic, **incremental** synthesis pass that turns a vault's `raw/`+`sources/` (Collect) into a regeneratable `wiki/` tree of cross-source knowledge pages plus a "what changed" digest (Compile) — `wiki/` stays separate from Collect and is fully rebuildable from it. You do **not** ingest individual sources, answer queries, run the full health-check lint, or touch **Hermes-managed all-in-one KBs** — and you **never** silently restructure a populated vault. But you also **never dead-end**: a generic **synthesis head is the default** — it really synthesizes *every* domain's source notes into cross-source pages (adversarially reviewed, honestly confidence-marked), not placeholders. Conversion to the canonical `raw/`+`sources/`+`wiki/` layout runs only behind an **approved** plan (never silently); specialized archetype heads (study/journal/…) later **enhance** a domain's generic pages in place — they never gate it. Synthesis reads `sources/` notes only — never bulk `raw/` code or binary (that's the scope filter in Phase 0).

> **Litmus test:** if you're processing one brand-new source end-to-end (that's *ingest*), answering a question (that's *query*), reorganizing thousands of files without an approved plan, or trying to *synthesize* bulk code / coverage reports / exhaust (that's input you **exclude**, not synthesize) — stop, you've left the lane.

## When to use
- Weekly compilation (default cadence), or a mid-week compilation when a vault accumulates sources fast.
- "Compile / consolidate / synthesize / roll up my KB"; "extract the trends across my digests/notes"; "what's new in the wiki since last time".
- Ad-hoc before a planning/refinement session or a content session, so the wiki layer is fresh for a human or an LLM harness.
- Convert / initialize a populated vault to the canonical `raw/`+`sources/`+`wiki/` layout (approval-gated) — the **generic synthesis head** carries any domain that has no built specialized head, so no part of the vault is left behind.

## When NOT to use
- **Add one new source** → that's *ingest* (the `llm-wiki` skill / the Hermes cron). compile-kb works the backlog ingest already produced.
- **Answer a question from the KB** → that's *query*.
- **Full structural health-check** (orphans, broken links, tag audit) → that's *lint*. compile-kb runs only the trust checks its own output needs.
- **Expecting specialized study / journal / content-gen / client-technical *artifacts*** (flashcards, weekly rollups, glossaries) — not yet; those enhancement heads aren't built. The domains themselves are firmly **in scope** and get **real generic synthesis** now (a specialized head later *enriches* them in place). What's off-limits is *claiming* specialized depth you didn't produce — never compiling the domain at all. client-technical delegates richer page-gen to `document-workflow` once that head ships.
- **A Hermes-managed / all-in-one KB** (`raw/`+`sources/`+compiled pages maintained together by the Hermes `llm-wiki` cron — e.g. a digest-fed brain-kb; flat, no `wiki/` tree) → out of scope. compile-kb is for **non-Hermes** vaults that keep Collect and a regeneratable `wiki/` separate. Hand off to the Hermes skill.

## Input contract
- `$vault_path` — absolute path to the KB vault (git-backed Obsidian-style markdown). Required.
- Everything else (archetype, cadence, mid-week threshold, target folders, digest dir) comes from the vault's `SCHEMA.md` **Compile** block (see contract below); fall back to defaults when absent.

## Preflight — detect, then orient or guide
Run every invocation, before anything else.

1. Confirm `$vault_path` exists and is a directory.
2. **Hermes guard — run before any branching.** compile-kb is for **non-Hermes** vaults only; Hermes-managed KBs are owned end-to-end (ingest *and* synthesis) by the Hermes `llm-wiki` cron, so we never init, repair, migrate, or compile them. **If the vault carries a Hermes provenance signal — a `sources/**` note whose `creator` is a `*Hermes*` cron, or a `SCHEMA.md` that names Hermes / an external manager — STOP and hand off.** The all-in-one flat shape (compiled pages maintained alongside `raw/`+`sources/`, no separate `wiki/` tree) *corroborates* but is not alone decisive: a non-Hermes vault can also be flat and merely needs migration (that's step 5, not a handoff). Run this **first** — a Hermes vault is flat (no `wiki/` tree), so it would otherwise fall through to step 5 ("not initialized") and get a `wiki/` tree built over it.
3. Check for `SCHEMA.md` at the vault root and a `wiki/` tree containing `wiki/index.md` + `wiki/log.md` (the synthesized layer lives under `wiki/`).
4. **All present → orient** (the existing-wiki path): read `SCHEMA.md` (root) in full, read `wiki/index.md`, read the last ~30 lines of `wiki/log.md`. Resolve the archetype(s) from the SCHEMA **Compile** block — a single `archetype:`, or a **`domains:` map** (each `raw/`/`sources/` subfolder → its archetype **hint**) for a mixed vault; if absent, **infer** (a `wiki/` tree with `sources/` + typed `wiki/concepts/`+`wiki/topics/` ⇒ `synthesis-wiki`) and suggest an explicit block. The archetype is a **hint** (open set, rule 9), **not a gate**: it records intent, selects a specialized **enhancement** head when one is built, and lightly tunes page emphasis. Resolve **per domain**: **(a)** a **built specialized** head exists for the hint → compile that domain with it (generic synthesis + its enhancements) into the shared `wiki/`; **(b)** known archetype but its specialized head **isn't built yet** (`study`/`journal`/`content-gen`/`client-technical` today) → **run the generic synthesis head** (real synthesis), recording the enhancement as the named upgrade path; **(c)** fits **no** known archetype → **propose a new archetype** (name + head sketch + signals) **plus the skill update** (rule 9) **and still run the generic head** now. **No domain is ever skipped, stopped, or placeholdered** — the generic head is the always-available default. **Enhancement (graduation):** when a specialized head later ships, it *enriches* that domain's generic pages in place (adds flashcards / weekly rollups / glossary / etc.), flipping `head: generic` → `head: <archetype>`. **Always-confirm-first:** before synthesizing, collect **every** domain that resolves to the generic head (no built specialized head) and **PAUSE ONCE** — present a single batch listing each such domain + its assumed archetype hint + the page emphasis that implies; proceed on **one** approval. Never interrupt per-domain. After the single approval, **dispatch one subagent per domain** to synthesize (see *Orchestration* under Process); the orchestrator retains shared nav + the commit.
5. **`SCHEMA.md` or the `wiki/` tree missing → not initialized.** Classify, then branch — **never *silently* restructure** (conversion runs only behind an approved plan):
   - **Greenfield** (≈0 content `.md` outside `raw/`, `templates/`, `.obsidian/`): offer a **guided init** — ask the archetype + domain (be specific), then write the **segregated synthesis-wiki scaffold**: `SCHEMA.md` (root, with a Compile block) + `raw/`+`sources/` (Collect), and the `wiki/` tree for Compile output (`wiki/index.md`, `wiki/log.md`, `wiki/_meta/`, `wiki/topics/`, `wiki/concepts/`, `wiki/comparisons/`, `wiki/_compilations/`); confirm; suggest first sources. Then stop (nothing to compile yet) unless sources already exist.
   - **Populated but unstructured** (many `.md`, no SCHEMA/3-layer — e.g. a course dump): this is a **migration, not an init**, run in **two approval-gated steps — propose, then (on approval) convert + synthesize.** **Step 1 — propose & PAUSE:** produce **a complete disposition inventory** accounting for **100%** of the vault (every top-level area → a `raw/` **domain** + its archetype hint + status — not just one slice), a draft **root** `SCHEMA.md` (with a `domains:` map if mixed), and a `raw/ ↔ sources/ ↔ wiki` mapping for a representative slice; write it to `init-proposal.md` at the vault root and **wait for approval — do not move anything yet.** **Step 2 — convert on approval:** for each **approved** domain (all, or a subset you pick), **conversion** seeds root `raw/<domain>/` + `sources/<domain>/` from the existing files (git-`mv`, history preserved), then the **generic synthesis head** compiles each converted domain (a domain with a built specialized head also runs its enhancements). **One canonical layout per vault:** root = `SCHEMA.md` + `raw/` + `sources/` + `wiki/`, archetypes as **domains** (`raw/<domain>/`, `sources/<domain>/`) all compiling into the **one shared `wiki/`** — never a per-subtree mini-vault. **Classify inputs, don't dump them (rule 10):** a **known-ingestable set** (`.md`, `.html`, … — extract a rendered report's text into a `sources/` note) is converted; **exhaust** — vendored/build (`**/repos/**`, `node_modules`, lockfiles, `dist/`), media, and the SCHEMA's listed exhaust — stays put; report raw-file vs real-note counts. **First-party lesson/sample code is a *study* source** (explore it, extract the learning), not files to migrate one-by-one. **Never silently delete, and never 100%-tag a folder as exhaust** — a mostly-exhaust folder can still hold a first-class source to rescue individually; an **unexpected/unrecognized file extension PAUSES for confirmation** rather than being assumed ingestable or exhaust. For a domain fitting **no** known archetype, propose a new one + its skill update (rule 9), then synthesize it generically like any other. **Ask before converting 10+ domains or moving large folders** (rule 8). compile-kb now *executes* the approved migration (convert + generic synthesis) — it is **no longer an out-of-skill manual step** (the deferred `kb-init` is folded in; a standalone extraction may still follow once proven).
   - **Partial** (`SCHEMA.md` present, but the `wiki/` tree / `wiki/index.md` / `wiki/log.md` missing): branch on how populated the vault already is. A **sparse half-init** (little or no synthesized content outside `raw/`+`sources/`) is safe to **repair** — recreate the missing `wiki/` scaffolding from current files without clobbering the SCHEMA. A vault **already populated with synthesized pages in a flat layout** (pre-segregation, or a foreign tool's shape) is a **migration, not a repair** — do **not** build a `wiki/` tree over it; route to the *Populated but unstructured* propose-then-convert path above (approval-gated, executed by conversion + the generic head), per rule #3.

## Process (generic synthesis head — the default)
The default head — it runs for **every** domain (Karpathy-style, archetype-agnostic: summaries / entity / concept / topic / comparison / overview pages fit any domain by design). Follow the vault's own `SCHEMA.md` conventions over this skill's defaults wherever they differ (folder names, `domains`/`themes` vs `tags`, page types).

### Orchestration — one subagent per domain (context isolation)
A multi-domain compile or conversion runs as an **orchestrator + per-domain subagents**, never all in one context — synthesizing every domain in the main session is what bloats it and stops scaling to larger vaults. The split falls on the existing phase boundary: **Phases 0–3 are per-domain → run them in a subagent; Phases 4–6 are vault-wide → the orchestrator runs them once.**
- **Orchestrator (main session):** preflight + the Phase 1 *vault-level* scan (which domains have changed) + the always-confirm-first batch pause; then **dispatch one subagent per domain with work**, collect their summaries, and run Phase 4 (nav), Phase 5 (digest), Phase 6 (verify & commit). Shared files — `wiki/index.md`, `wiki/log.md`, the digest — and the commit are **orchestrator-only**: subagents can't obtain the user's commit approval (rule 6), and parallel writes to shared nav would collide. Cross-domain back-links are returned by subagents as **proposals** (never applied into another domain's pages); the orchestrator applies and dedupes them centrally in Phase 4.
- **Per-domain subagent:** runs Phases 0–3 for **its domain only** — reads just `sources/<domain>/` (+ that domain's `raw/` on demand, Phase 0), writes just that domain's `wiki/topics|concepts|comparisons/` pages + `wiki/_meta/<domain>-map.md`, and runs the Phase 3 adversarial pass (itself, or handing off to a separate reviewer subagent). It **returns a compact summary** — pages created/updated (one line each), sources flipped to `integrated`, confidence, any `contested`/`contradictions`, open questions — and **never the full page bodies**; that compactness is what keeps the orchestrator's context flat as the vault grows. The dispatch prompt must pin the vault's output conventions the pages have to match — charset (e.g. ASCII-only where that is the vault's convention), heading/frontmatter shape, link style. Parallel subagents do not share an implicit house style: a convention that isn't written into the dispatch (or enforced by a Phase 6 gate) WILL drift across agents. Pin conventions by **pointing at a sibling file/prior compile commit**, not by inlined literals — but character-level micro-conventions (provenance-marker form incl. suffix/punctuation) must still be named *literally* in the dispatch: an exemplar transfers structure, not punctuation. Per-domain review checklists include the page-size budget (~200 lines) and each subagent reports its max changed-page line count; the orchestrator's full-tree sweep is the backstop, not the primary catch. Tag orchestrator-supplied context (SCHEMA labels, changelog triage, figures quoted from sources) as **hints-to-verify**: the subagent re-verifies against the primary source and **flags-not-complies** on conflict, reporting the delta. The dispatch also states the grouped-note sha invariant verbatim: `sha256_prefix` tracks the **first-listed (primary)** raw file; secondaries go in `## Source Trail`. When the orchestrator corrects a term a subagent propagated, it **echo-greps** the corrected term across the whole run's output. Mid-run scope extensions go to the *same* finished domain agent (resume with context intact), never a fresh spawn.
- **Cadence (maturity-conditional):** on a vault's **first orchestrated run**, after a **compile-kb skill change**, or when the run includes **new-domain conversions**, synthesize one representative domain first and pause for the user's review; fan out the rest only on approval. On an **established incremental** (≥2 prior clean orchestrated runs on this vault, no skill change), dispatch all domains in parallel directly — the user overrode the pause on three consecutive runs with zero rework. Always show the diff before committing.
- **When to delegate:** every multi-domain run and every conversion. A trivial single-domain incremental compile may run inline (no subagent overhead).

### Phase 0 — Scope filter (what synthesis may read)
The bound that makes generic synthesis safe for every domain (rule 10):
- **Synthesis input is `sources/<domain>/*.md` only — never walk `raw/` for bulk content.** A real source earned a `sources/` summary; bulk code/binary never did, so it is structurally invisible to synthesis.
- **Exclude exhaust:** `**/repos/**`, `node_modules`, `dist/`, lockfiles, media, and the SCHEMA's listed exhaust — never synthesis input, never per-file `sources/` notes. First-party lesson/sample code is a *study source* explored on demand.
- **Unknown extensions pause** (rule 10): a known-ingestable set (`.md`, `.html`) converts; anything unrecognized asks first. This guard keeps the synthesis engine off coverage reports and sample apps. PDF sources: if the harness inspection capability can't render PDFs in this environment, extract text via `pdftotext` or Python + PyMuPDF (`fitz`) to a temp file and work from that — a named fallback, not a per-run rediscovery.

### Phase 1 — Find work (incremental)
- Find the last compile: the most recent `## [YYYY-MM-DD] compile |` entry in `wiki/log.md` (or "never").
- Collect candidate sources: `sources/**/*.md` with `status: summarized` (not yet `integrated`), OR `updated`/`date_consumed` after the last compile, plus any raw files whose `sha256_prefix` no longer matches (drift). Harvest each candidate's `## Concepts to Update` list.
- **Unseeded raw (full-tree, not window-scoped):** diff the full `raw/` tree against `sources/` `raw:` pointers — every raw file/directory (excluding exhaust) must be claimed by some `sources/` note; unclaimed ones surface as "needs seeding" work. A window-scoped `git log <last-compile>..HEAD` probe structurally misses anything that predates the window (two PDFs sat invisible for five consecutive compiles; 15 guides sat invisible for a full cycle when only status/date/sha signals were scanned). Keep the git-log probe only as a cheap first pass; the pointer diff is authoritative. Directory-backed sources (a `raw:` pointing at a directory) are fingerprinted by their **primary file** per the grouped-note rule — not reported MISSING by a file-only check; a hash mismatch on a git-clean raw file is a **metadata anomaly** (recorded-hash typo), not drift.
  Bucket the unclaimed set: **new-source** (needs seeding) / **companion** (artifact of an
  already-claimed source — record it in the owning note's `## Source Trail` or the domain
  manifest so it stops surfacing) / **non-source** (exhaust — record, don't seed). A
  45-file sweep held 1 real source; without buckets the other 44 re-surface every run.
- **Idempotent:** if nothing changed since the last compile, report "nothing to compile" and exit without writing. (Honor an explicit "recompile everything" request to override.)

### Phase 2 — Synthesize
- Cluster candidate sources by `domains`/`themes` + content. For each cluster meeting the SCHEMA page-creation threshold (central to one source, or appears across 2+), create or update the target **knowledge page**:
  - **Cross-source synthesis is what ingest alone never produces** — roll the cluster into whichever page type fits the material, from Karpathy's **archetype-agnostic vocabulary**: `topics/` (cross-source trend/overview), `concepts/` (one idea), `comparisons/`, plus per-source `summaries` and `entity`/overview pages where useful. Place under the vault's `wiki/` tree per SCHEMA `compile_targets` — the regeneratable Compile layer; never write `raw/` or `sources/`. **A single-source cluster gets a faithful overview/summary page — never a fabricated cross-source "trend."**
  - **Merge without flattening:** when sources disagree, keep both claims with dates + links in a `## Tensions / Contradictions` section, lower `confidence`, set `contested: true`. Never silently pick a winner.
  - **Claim-level provenance:** on pages synthesizing 3+ sources, append `^[sources/<path>]` markers at paragraph granularity so each claim traces back without re-reading the source.
  - Cross-link (≥2 `[[wikilinks]]`), update each page's `## Source Trail`, and bump the consumed source notes to `status: integrated`.
  - **Mark every generic page** `head: generic` + honest `confidence` (`high|medium|low`), and add a one-line **graduation note** when a specialized enhancement is the named upgrade path (e.g. `> generic synthesis — a specialized study head could later add flashcards/glossary`). **No `unsynthesized` status, no "⚠ not yet synthesized" banner** — these are real synthesis, gated by Phase 3 review + the confidence gate.
  - Respect ingestion levels; split pages over ~200 lines; don't create pages for passing mentions.

### Phase 3 — Adversarial review (mandatory on changed synthesis pages)
- For each created/updated page, run a second **skeptical** pass (ideally a separate reviewer subagent or a fresh critical read) that hunts: overreach, unsupported generalizations, claims not traceable to a cited source, and contradictions with existing pages.
- Apply outcomes: demote `confidence`, set `contested: true` + `contradictions: [page]`, or mark a non-surviving claim's page `status: draft`. This is the concrete guard against hallucinations hardening into wiki fact — runs on every domain's synthesis pages (meter it to those, not the `index`/`_meta` nav).
- **Retroactive reach:** when a new source establishes a convention or constraint, grep the *existing* wiki pages for violations (the incremental flow never looks backward — one source invalidated ~16 spots in prior pages). Escalate hits in the digest; never auto-rewrite pages outside the run's cluster without approval (rule 8).
- **Full-file reread on dated refreshes:** the reviewer rereads each changed page
  end-to-end (not the diff hunks) and greps it for the replaced current-state terms —
  dated appendices went in correct while the page's summary/heading text stayed stale in
  two runs; hunk-scoped review is structurally blind to that.

### Phase 4 — Update navigation (orchestrator, once)
- Patch `wiki/index.md` from the per-domain subagents' returned summaries (not by re-reading every page): add new pages under the correct type section; **recompute** the `> Last updated: … | Total pages: N` header (fix drift).
- Per-domain `wiki/_meta/<domain>-map.md` MOCs are written by each domain's subagent as part of its synthesis — the orchestrator only patches the vault-wide `index.md` + `log.md` here.
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

Any deferred/escalated finding in the digest (codename exposure, contract violation, staleness) carries `file:line` + the matched term — a bare count is unactionable downstream (a purge agent found zero in-scope hits from a count-only escalation).

The digest, `wiki/index.md`, and `wiki/log.md` are wiki files: **the vault's charset/style conventions apply to the orchestrator's own writing exactly as to subagents'.** Where the vault convention is ASCII-only, transliterate this template's punctuation (em-dashes, arrows) when instantiating it. After the orchestrator's Phase 4–5 writes, re-run the Phase 6 sweep over the files it touched (both runs where the digest leaked non-ASCII, the offender was the orchestrator, not an agent).

### Phase 6 — Verify & commit
- `git diff --check`; inspect `git diff --stat`; ensure `raw/`, media, and secrets are **not** staged.
- **Full-tree hygiene sweep — the whole `wiki/` tree, not just this run's diff:** charset offenders
  (where the vault convention is ASCII-only), broken `[[wikilinks]]`, trailing whitespace.
  Incremental-only verification accumulates blind spots; the full sweep is cheap and is the backstop
  that catches drift a prior run let through.
- **Secret scan (pinned contract v2):** scan **added content only** (the run's diff, not
  whole files) for secret *values*: key/token-shaped literals
  (`(api[_-]?key|secret|token|password)\s*[:=]\s*['"][A-Za-z0-9+/_-]{16,}`), PEM headers,
  and base64/hex runs ≥ 32 chars that ALSO pass all three filters: (1) token-boundary —
  not embedded in a path, wikilink slug, or URL (require non-word delimiters both sides);
  (2) mixed character classes (≥ 2 of upper/lower/digit); (3) not a declared hash —
  `sha256_prefix` values and `## Source Trail` digest entries are provenance, exempt.
  (A raw base64/hex grep produced 1,036 path-shaped false positives; a keyword grep 110.)
  Record pattern + filters in the digest so the next run reproduces, never re-derives.
- **All-hashes verification:** verify every explicit hash in new/refreshed grouped notes —
  the primary `sha256_prefix` AND each `## Source Trail` secondary, including
  directory-relative entries. A wrong 12-char secondary shipped past a primary-only check.
- Before staging, transition any "pending approval" markers in `wiki/log.md`/digest to their final
  state, then re-check post-state — a marker that still said "pending user commit approval" shipped
  inside the very commit it referred to.
- **Show the diff to the user. Commit curated files only, with the user's OK** (or per an automated workflow's explicit expectation). Never auto-commit a vault you were told to leave uncommitted.

### Confidence gate
Score the compile (loaded confidence format). Any synthesis page you can't support at ≥ high confidence ships as `confidence: medium|low` and/or `status: draft` — never as asserted fact. If the overall compile is < 90% sound, surface what's uncertain instead of committing.

## Process (convert — the migration mechanic)
Conversion is **not** a compile head — it's the one-time, approval-gated relocation that gets a populated vault into the canonical `raw/`+`sources/`+`wiki/` layout so the generic head can synthesize it. Already-canonical vaults skip it entirely.

### Convert (approval-gated, idempotent)
- Run only after the step-5 disposition proposal is **approved**. For each approved domain, seed `raw/<domain>/` from the existing files (git-`mv`, history preserved) and create one `sources/<domain>/` note per real source (short summary + frontmatter: `status: summarized`, `domains`, `themes`, `date_consumed`, `source_type`, `original_filename`, `raw:`, `sha256_prefix`). Grouped notes (one `sources/` note covering several raw files): frontmatter `sha256_prefix` tracks the PRIMARY (first) raw file only; record each secondary file's sha prefix inline in the note's `## Source Trail` so staleness detection covers non-primary files too.
- **Classify inputs (rule 10):** convert the known-ingestable set (`.md`; `.html` → extract the rendered report's text into the `sources/` note); **exclude** `.git/`, `.obsidian/`, `_migration/`, `**/repos/**`, media, and the SCHEMA's listed exhaust; treat first-party lesson/sample code as a *study source* to explore on demand, not per-file notes. **Never silently delete or 100%-tag a folder as exhaust** — rescue a first-class source buried in an exhaust folder individually; an unexpected extension pauses for confirmation.
- **Idempotent:** a domain already seeded at `raw/<domain>/` is **not** re-converted — skip it. Honor rules 3, 6, 8 (never silent, never commit `raw/` / secrets unprompted, ask before 10+ domains / large moves).
- **Then synthesize:** each converted domain is handed to the generic synthesis head — **one subagent per domain** for Phases 0–3 (see *Orchestration* under Process), with the orchestrator running Phases 4–6 once (digest, verify/commit). A domain with a built specialized head also runs its enhancements.

### Enhance (graduation — when a specialized head ships)
- A newly-built specialized head **enriches the generic pages in place**: it reads the same `sources/<domain>/`, adds archetype-specific artifacts (flashcards / weekly rollups / glossary / per-ticket narratives), and flips `head: generic` → `head: <archetype>`. Generic synthesis is the **floor, never a ceiling** — the `## Compile` `domains:` hint already names the target archetype; build its head, then re-run.

## SCHEMA `## Compile` contract (the archetype plug)
A vault declares how it wants to be compiled. compile-kb reads this; future archetype heads read the same block. Add it to the vault's `SCHEMA.md`:

```yaml
## Compile
archetype: synthesis-wiki      # single-archetype vault: one archetype HINT. Known archetypes (OPEN set — propose a new one, rule 9): synthesis-wiki | study | journal | content-gen | client-technical. The **generic synthesis head runs by default**; a specialized head, once built, *enhances* that archetype's pages.
domains:                       # OPTIONAL — mixed vault: map each raw/sources subfolder → its archetype HINT (selects an enhancement when built; distinct from a source note's themes/tags)
  discussions: synthesis-wiki  #   raw/discussions/ + sources/discussions/ → synthesis-wiki (generic synthesis is already the full shape — no extra enhancement)
  courses: study               #   study archetype, head unbuilt → generic synthesis now; a study head *enhances* later (flashcards/glossary)
cadence: weekly                # default; mid-week auto-suggested at the threshold
midweek_threshold: 15          # uncompiled source notes that warrant an early compile
compile_targets: [wiki/topics, wiki/concepts, wiki/comparisons]   # the shared wiki/ tree, separate from raw/ + sources/
digest_dir: wiki/_compilations
synthesis_depth: moc+notes     # generic-head page depth: `moc` (domain MOC only) | `moc+notes` (MOC + per-source pages) | `full` (+ cross-source topic/concept pages). Legacy `baseline_depth` is read as an alias.
```

Defaults when the block is absent: `archetype: synthesis-wiki` (only if inferable; else propose a block and run the **generic synthesis head** — never STOP on an undetermined archetype), `cadence: weekly`, `midweek_threshold: 15`, targets under `wiki/`, digest `wiki/_compilations`, `synthesis_depth: moc+notes` (legacy `baseline_depth` read as an alias). Recommend the user add an explicit block; do not silently edit their SCHEMA without showing the change. **Structure — one canonical layout per vault:** root = `SCHEMA.md` + `raw/` + `sources/` + `wiki/`. **Archetypes live as domains** — `raw/<domain>/` + `sources/<domain>/` (Collect, domain-foldered, mapped to archetype hints by `domains:`); **everything synthesized lives under the one shared `wiki/`** — `wiki/index.md`, `wiki/log.md`, `wiki/_meta/` maps, the pages, `wiki/_compilations/` — fully regeneratable from Collect. A single-archetype vault just sets `archetype:` and may skip the domain subfolders. The `wiki/` tree's presence marks a compile-kb-managed vault (Hermes KBs stay flat/all-in-one, out of scope). **Exhaust globs match the post-migration `raw/` paths.** **Generic pages** carry `head: generic` + honest `confidence` (+ a graduation note naming the specialized enhancement, if any); a specialized head later enriches them in place, flipping `head:` as it adds real depth — never a `status: unsynthesized` placeholder.

## Important rules
1. **Orient before acting** — read `SCHEMA.md` + `wiki/index.md` + recent `wiki/log.md` every session. Skipping it duplicates pages and misses cross-references.
2. **Incremental + idempotent** — only touch what changed since the last compile; a no-change run writes nothing.
3. **Never *silently* restructure a populated vault** — detect → propose → **await approval** → then **conversion** executes the approved plan and the **generic head** synthesizes (asking again before 10+ domains / large moves, rule 8). compile-kb *does* perform migration now — but only an **approved** plan, never automatically on sight.
4. **Never silently resolve contradictions** — keep both claims, lower confidence, flag for review.
5. **Adversarial review is not optional** on changed synthesis pages — don't let weak claims harden.
6. **Never commit `raw/`, media, or secrets** — show the diff, commit curated only, with approval.
7. **The vault's SCHEMA wins** over this skill's defaults.
8. **Ask before mass-updating 10+ existing pages** in one compile.
9. **Archetypes are open; specialized heads are not improvised.** Fit a known archetype hint, or — when a vault/domain fits none — *propose* a new archetype **and** the concrete compile-kb update to support its enhancement head. Surface it inline **and** persist it to a vault-local note at the vault root (fold into `init-proposal.md` if you're emitting one, else write `archetype-suggestion.md`). **Never *claim* specialized-head depth you didn't produce** (flashcards, weekly rollups, glossary) — **but never *stop* either:** propose the new archetype **and** run the **generic head** so the domain gets real synthesis now (propose ≠ dead-end). Classification is probabilistic; the safety rails (no *silent* restructure, the Hermes provenance gate, idempotency, show-diff-before-commit) stay deterministic.
10. **Synthesize notes, not exhaust (the scope filter).** Generic synthesis reads `sources/<domain>/*.md` **only** — never walks bulk `raw/` code or binary; exclude `**/repos/**`, `node_modules`, `dist/`, lockfiles, media, and the SCHEMA's listed exhaust. Maintain a **known-ingestable** set (`.md`, `.html` → extract text) and a **known-exhaust** set; an **unexpected extension PAUSES** for confirmation. **Never silently delete, and never 100%-tag a folder as exhaust** — rescue a first-class source buried in exhaust individually.
11. **Delegate per-domain synthesis to subagents (context isolation).** A multi-domain compile or conversion runs as an **orchestrator + one subagent per domain**: the subagent runs Phases 0–3 for its domain and returns a **compact summary** (never full page bodies); the orchestrator runs Phases 4–6 and owns the commit. Synthesizing every domain in one context bloats the session and doesn't scale; shared nav (`wiki/index.md`/`log.md`) + commit stay orchestrator-only (rule 6). A trivial single-domain incremental compile may run inline.

## What this skill does NOT do
- **Ingest a single source** → the `llm-wiki` skill / Hermes cron (compile-kb consumes the backlog ingest produced).
- **Query / answer questions** → the query operation.
- **Full structural lint** → the lint operation (orphans, broken links, tag audit, log rotation).
- **Specialized study / journal / content-gen / client-technical *artifacts*** (flashcards, weekly rollups, glossaries, per-ticket narratives) → their archetype **enhancement** heads (later); until then the **generic head** already produces real synthesis for those domains. client-technical delegates richer page-gen to `document-workflow`.
- **Silently restructure / migrate on sight** → never. compile-kb proposes the disposition first and converts only the **approved** plan (conversion then executes it, and the generic head synthesizes). Conversion is in-skill now, but always behind approval.
- **Operate on a Hermes-managed all-in-one KB** → the Hermes `llm-wiki` skill owns those (ingest + synthesis in one loop, flat layout, no `wiki/` tree).
- **Emit HTML / rendered *views* of the wiki** → a deferred derived view, not this skill. (But **ingesting** a rendered report — `.html` — as a *source* IS in scope: extract its text into a `sources/` note and synthesize it like any other source.)

## Output
Within `$vault_path`: knowledge pages under the shared `wiki/` tree (per `compile_targets`); `wiki/index.md` + `wiki/_meta` maps refreshed; a `wiki/log.md` `compile`/`convert` entry appended; the compilation digest under `<digest_dir>/` (default `wiki/_compilations/`). Root layout = `SCHEMA.md` + `raw/` + `sources/` + `wiki/`. **Synthesis compile writes only under `wiki/`** — never `raw/`, and touches `sources/` for (i) the frontmatter-only `status: summarized → integrated` transition Phase 2 requires, and (ii) the **seeding sub-step**: creating or evidence-grounded refreshing of `sources/` notes for raw the Phase-1 sweep surfaced as unseeded, scope-confirmed at the batch pause (established practice: weekly compiles fold seeding in). Synthesis itself never edits source-note content; `raw/` stays read-only. **Conversion**, on an **approved** plan, additionally seeds `raw/<domain>/` + `sources/<domain>/` once (the one sanctioned write outside `wiki/`). Commits only curated files, only with approval.
