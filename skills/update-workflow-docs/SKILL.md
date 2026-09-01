---
name: update-workflow-docs
description: "Refresh existing workflow docs after the code moved on — per-doc commit-diff staleness detection using each doc's Generated From sha + Source Files table, drift buckets (Current / Stale / Unverifiable), and targeted in-place updates that preserve untouched sections verbatim. Use when workflow docs already exist and the code changed since they were generated, or when asked to update, refresh, re-sync, or check staleness or drift of workflow, endpoint, handler, or flow docs. Never bumps docs that didn't drift."
---

# update-workflow-docs — staleness triage + in-place refresh for workflow docs

You are a docs maintainer. You detect exactly which existing `document-workflow` docs drifted from the code and update **only the drifted sections in place** — you do **not** regenerate docs from scratch, bump metadata on docs that didn't change, or write new docs for undocumented workflows.

> **Litmus test:** if you're rewriting a whole doc, touching a doc whose staleness query came back empty, or documenting a workflow that has no doc yet — you've left the lane.

## When to use

- **Ad-hoc:** workflow docs exist and the code has moved on — "are these docs stale?", "refresh the workflow docs", periodic corpus maintenance.
- **After a feature lands** that touched paths some workflow doc traces.

## When NOT to use

- **A workflow with no doc yet** → `document-workflow` (fresh trace).
- **Inventorying a service for undocumented handlers** → `docs-tasks-creator`.
- **The doc template/schema itself changed shape** → re-run `document-workflow`; this skill never changes a doc's section structure.

## Input contract — loose

Accept whatever the invocation provides and resolve before starting; echo the resolved scope back:

- **Docs scope** — a directory (`workflows/web`), a glob, a single doc path, or a service name. Nothing given → ask.
- **Docs root vs code root** — the docs and the code they describe **may live in different repositories** (docs moved to a KB repo while code stays put). Do not assume co-location: confirm both with the user, offering detected defaults (`./workflows/` in the current repo; current repo as code root). `git log` / `git rev-parse` run in the **code root**; `## Source Files` paths resolve there; the `Generated From` shas are commits in **that** repo. Write only inside the docs root; read source only from the code root. Every path you mention states which root it resolves against.

## Process

1. **Inventory the docs.** Enumerate the docs root for `*.md` containing a `## Summary` table. Skip generation artifacts (`_*.md`, `*_qa.md`, `*_close.md`, `project-overview.md`, README). Per doc capture: title, `Generated From` short sha, `Last Updated`, `Mode`, and the ordered `## Source Files` path list.
2. **Detect drift — one staleness query per doc**, in the code root:
   ```
   git log --oneline <generated-from>..HEAD -- <source path 1> <source path 2> …
   ```
   Bucket each doc:
   - **Current** — empty output. **Leave it untouched**; do not bump dates for a no-op.
   - **Stale** — non-empty. Mark for update; keep the commit list as the change evidence.
   - **Unverifiable** — `Generated From` unknown / sha not in history / `## Source Files` empty. Offer a full `document-workflow` re-trace instead of a diff.
   Also flag **removed sources** (a traced path no longer exists): possibly a deleted workflow — surface it, never auto-delete.
3. **Report the buckets before editing** so the user sees scope and can narrow it.
4. **Update each Stale doc — scoped, in place.** Re-read the changed source paths (and anything newly reachable from them); for non-trivial drift launch 1–3 generic subagents, same ≥ 95% confidence bar as `document-workflow`. Update **only** the sections the change touches (Sequence of Calls, Flow Description, Data Inventory, Business Rules, Configuration, Dependencies, Complex Logic, `## Source Files`); preserve every unaffected section **verbatim** — including tables, `[[wikilinks]]`, and cross-references. **Prefer Edit (targeted deltas) over Write (full overwrite)**; if you must Write, re-include the entire doc and re-verify all cross-references afterward.
5. **Metadata discipline.** Keep `Created`; set `Last Updated` = today (fetch the date, don't hardcode); advance `Generated From` to the code root's current short sha — one `git rev-parse --short HEAD` **per run**, reused across docs; keep `Schema` unchanged. Append **exactly one** `## Change Log` row per doc per run: `<today> | <what changed> | <driving commit subjects/shas>`.
6. **Confidence gate.** Per updated doc, score with `document-workflow`'s factors; **< 95% → keep tracing or flag the uncertain section `[TODO: verify]`** rather than committing a guess.

## Output structure

Final report, one table: `doc | bucket (Current / Updated / Unverifiable / Removed?) | Generated From old→new | one-line change` — plus counts per bucket and, for every Unverifiable / Removed? doc, the recommended follow-up (full re-trace, or confirm deletion).

## Important rules

1. **Don't touch Current docs at all.** An unchanged `Generated From` / `Last Updated` is a feature — it tells the next run nothing drifted; bumping dates on no-ops destroys the signal.
2. **One sha per run, one staleness query per doc.** The new `Generated From` means "state verified against now".
3. Match each doc's existing voice — this is the corpus `document-workflow` produced; stay tech-agnostic.
4. Never change a doc's `Schema` or section structure.
5. Published `workflows/*` docs only — never generation artifacts, never task-status flips.

## What this skill does NOT do

- **Fresh documentation** of a new workflow → `document-workflow`.
- **Detecting undocumented workflows** → `docs-tasks-creator`.
- **Schema migration** of the doc format → re-run `document-workflow`.

## Output file

No artifact of its own — it edits the existing docs in place and prints the final report table.
