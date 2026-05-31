---
description: Refresh EXISTING workflow docs against the current code — commit-diff-driven staleness detection + targeted in-place updates that preserve the document-workflow format. Use when workflow docs already exist and the code has moved on since they were generated.
argument-hint: Optional docs scope — a dir (`workflows/web`), a glob, a single doc, or a service name. Omit to be asked.
---

# Update Workflow Docs

Refresh **existing** `document-workflow` docs so they match the current code, without regenerating from scratch. This is the update counterpart to `/document-workflow`: it reuses each doc's own `Generated From` SHA + `## Source Files` table to detect exactly what drifted, re-traces only the changed paths, and updates the doc in place.

> **Use this** when docs already exist and the code changed since they were written. **For a brand-new workflow** that has no doc yet, use `/document-workflow`. **To inventory a service** and emit fresh per-endpoint tasks for undocumented handlers, use `docs-tasks-creator`. This command never changes the doc *schema* — only its content and metadata; if the template itself changed, re-run `/document-workflow`.

## Input

`$ARGUMENTS` (all optional) may name a docs scope: a directory (`workflows/web`), a glob, a single doc path, or a service name. If omitted, you'll ask in Step 0.

## Step 0 — Locate the docs AND the code (ask first)

The workflow docs and the source code they describe **may live in different repositories** — e.g. the docs get moved into a knowledge-base repo while the code stays put. Do **not** assume they're co-located. Before anything else, establish both with `AskUserQuestion` (offer the detected default as the first option, recommended):

1. **Docs location** — the directory tree holding the workflow `*.md` files. Default: `./workflows/` in the current repo, if present.
2. **Code repository** — the repo whose history + source files the docs were generated from. Default: the current repo. This is where `git log` / `git rev-parse` run and where each doc's `## Source Files` paths resolve. The `Generated From` SHAs are commits in **this** repo, even when the docs live elsewhere.
3. **Scope** — if not given in `$ARGUMENTS`: all docs, one service subtree, or a named list.

If docs and code are the same repo, both default and you only confirm scope. Record the resolved **docs root** and **code root**; every path below is relative to one of them — always be explicit which. Write only inside the docs root; read source only from the code root.

## Process

- Create a todo list for all steps.
- Inventory → detect drift → report buckets → update stale docs (confidence-gated) → final report.
- For non-trivial drift in a doc, you may launch 1–3 specialized agents and must reach **≥95% confidence** before writing, same bar as `/document-workflow`.

## Instructions

### 1. Inventory the docs

Glob the docs root for `*.md` files that contain a `## Summary` table. **Skip** generation artifacts: `_*.md` (e.g. `_docs-tasks.md`, `*_qa.md`, `*_close.md`), `project-overview.md`, `README`. For each real doc, capture: title, `Generated From` short SHA, `Last Updated`, `Mode`, and the full ordered `## Source Files` path list.

### 2. Detect drift (per doc) — the staleness query

In the **code repo**, for each doc run a **single** Bash call (the exact query the `## Source Files` note documents):

```
git log --oneline <generated-from>..HEAD -- <source path 1> <source path 2> …
```

Bucket each doc:

- **Current** — empty output: no traced path changed since `Generated From`. **Leave it untouched** — do not bump dates for a no-op.
- **Stale** — non-empty: at least one traced path changed. Mark for update and keep the commit list as the change evidence.
- **Unverifiable** — `Generated From` is `unknown` / `[TODO: verify SHA]`, the SHA isn't in history, or `## Source Files` is empty/missing. Flag it; offer a full re-trace (`/document-workflow` semantics) instead of a diff.

Also note **removed sources**: if a `## Source Files` path no longer exists in the code repo, flag the doc as possibly describing a deleted workflow — surface it, never auto-delete. Detecting brand-new *undocumented* workflows is out of scope → `docs-tasks-creator`.

**Report the buckets before editing** so the user sees scope and can narrow it.

### 3. Update each stale doc (confidence-gated)

Follow `/document-workflow`'s Instructions and Output Format as the canonical contract — but **scoped to what changed**:

- Re-read the changed source paths (and anything newly reachable from them) with Read / Grep / Glob; for non-trivial drift, launch 1–3 agents and require ≥95% confidence.
- Update **only** the sections the change touches: Sequence of Calls, Flow Description, Data Inventory, Business Rules, Configuration, Dependencies, Complex Logic, and `## Source Files`. Preserve every unaffected section **verbatim** — this is an in-place edit, not a regenerate. Do not drop content, tables, or `[[wikilinks]]` / cross-references you aren't actively changing.
- **Metadata** (per document-workflow update rules): keep `Created`; set `Last Updated` = **today** (fetch the current date, don't hardcode); advance `Generated From` to the code repo's current short SHA — run `git rev-parse --short HEAD` **once for the whole run** and reuse it; keep `Schema` at `v1`; refresh `## Source Files` rows for any paths you newly traced or that disappeared.
- Append **exactly one** `## Change Log` row: `<today> | <what changed> | <why — driving commit subjects/SHAs from step 2>`. Group all edits for this doc into that single row.

**Prefer `Edit` (targeted deltas) over `Write` (full overwrite)** so unaffected sections can't be silently lost. If you must `Write`, re-include the entire doc and re-verify all cross-references afterward.

### 4. Report

One table: `doc | bucket (Current / Updated / Unverifiable / Removed?) | Generated From old→new | one-line change`. State the counts. List every Unverifiable / Removed? doc with the recommended follow-up (full `/document-workflow` re-trace, or confirm deletion).

## Guidelines

- **Don't touch Current docs at all.** An unchanged `Generated From` / `Last Updated` is a feature — it tells the next run nothing drifted. Bumping dates on no-ops destroys that signal.
- Stay tech-agnostic and match each doc's existing voice — this is the same corpus `/document-workflow` produced.
- One `git rev-parse --short HEAD` per run (the new `Generated From` = "state verified against now"); one `git log …` per doc for drift.
- Never change `Schema` or the section structure — that's `/document-workflow`'s job. If the template itself changed shape, re-run that instead.
- Flag anything you can't verify with `[TODO: verify]` rather than guessing.
- This command updates only the published `workflows/*` docs; it does not touch `_docs-tasks.md` generation artifacts or flip task status.

## Confidence

State a confidence score for each updated doc (same factors as `/document-workflow`). Below 95%, keep tracing or flag the uncertain section with `[TODO: verify]` rather than committing a guess.
