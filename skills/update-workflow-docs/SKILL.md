---
name: update-workflow-docs
description: "Checks existing workflow documentation for source drift and refreshes only stale sections. Use to update, refresh, re-sync, or check staleness across workflow, endpoint, handler, or flow docs after code changes. Accepts a docs directory, glob, file path, or service name, including separate source/docs repositories. New workflow documentation belongs to document-workflow."
---

# update-workflow-docs — staleness triage + in-place refresh for workflow docs

You are a docs maintainer. You detect exactly which existing `document-workflow` docs drifted from the code and update **only the drifted sections in place** — you do **not** regenerate docs from scratch, bump metadata on docs that didn't change, or write new docs for undocumented workflows.

> **Litmus test:** if you're rewriting a whole doc, touching a doc classified Current after
> all bounded evidence checks, or documenting a workflow that has no doc yet — you've left the lane.

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
- **Docs root vs source roots** — docs and source may live in different repositories. Resolve
  them under [the documentation evidence contract](references/shared/documentation-evidence.md),
  offering detected defaults (`./workflows/` in the current repo; current repo as primary
  source root). Each Source ID resolves against its own recorded repository/module root;
  git checks run there. Write only inside Docs root; all source roots are read-only. Every
  path states which root/Source ID it resolves against.

## Process

1. **Inventory the docs.** Enumerate Docs root for `*.md` containing `## Summary`. Skip
   generation artifacts (`_*.md`, `*_qa.md`, `*_close.md`, `project-overview.md`, README).
   Per doc capture title, Schema, Last Updated, Mode, the complete `## Source Evidence`
   records, and ordered Source Files manifest. A pre-v2 workflow doc or malformed/missing
   evidence is readable but Unverifiable; never infer historical byte identity from its SHA.
2. **Validate every Source ID.** Resolve its recorded source root/locator; resolve manifest,
   dirty and trace-boundary paths relative to that base, including any workspace prefix.
   An ambiguous legacy path base is Unverifiable, never guessed from the current directory.
   Verify the full
   revision exists and is an ancestor of current HEAD. An inaccessible/non-ancestor revision,
   unreadable independent module, missing manifest, or unresolved dynamic boundary is
   **Unverifiable**. Record the exact failing source and check.
3. **Detect bounded drift from actual bytes and boundaries.** For each verifiable source:
   - use `git log <recorded-revision>..HEAD -- <recorded paths>` only to shortlist commits;
   - recompute every recorded file SHA-256 and the sorted manifest digest;
   - inspect relevant staged, unstaged, and untracked paths, even when HEAD is unchanged; and
   - re-enumerate the recorded trace boundary and its registration/dispatch/routing/config
     inputs. A handler move, new matching registration, removed source, or changed controlling
     input triggers a scoped retrace.

   Bucket the whole doc:
   - **Current** — all Source IDs satisfy the Current definition and bytes/boundary match.
     Leave the doc byte-for-byte untouched.
   - **Stale** — a relevant byte or trace boundary is known to differ. Keep commits, dirty
     layers, old/new hashes, and added/moved/deleted paths as change evidence.
   - **Unverifiable** — any required identity/boundary cannot be checked. Offer a full
     `document-workflow` retrace.

   Irrelevant code-only changes outside recorded sources and boundaries do not invalidate the
   doc. An empty path-limited log alone never establishes Current.
4. **Report the buckets before editing** so the user sees scope and can narrow it.
5. **Update each Stale doc — scoped, in place.** Re-read changed sources and anything newly
   reachable from a changed boundary. Apply `document-workflow`'s scope/risk-based independent
   coverage and evidence policy, recording any unavailable native-worker capability. Update only affected content
   sections plus Source Evidence/Source Files; preserve all unaffected text verbatim, including
   tables, `[[wikilinks]]`, and cross-references. Prefer targeted edits; after any whole-file
   write, recheck every reference.
6. **Metadata discipline.** Keep Created; set Last Updated to today's fetched date; set the
   primary source's short HEAD as display-only Generated From; refresh every source's full
   revision, dirty paths, boundary, file hashes, and manifest digest. Keep Schema unchanged.
   Append exactly one Change Log row with commit subjects/SHAs and dirty/hash evidence. Schema
   migration is a full `document-workflow` retrace, never an in-place refresh.
7. **Confidence gate.** Per updated doc, score with `document-workflow`'s factors; below 95%
   keep tracing or flag the uncertain section `[TODO: verify]` rather than guessing.

## Output structure

Final report, one table: `doc | bucket (Current / Updated / Unverifiable / Removed?) | Generated From old→new | one-line change` — plus counts per bucket and, for every Unverifiable / Removed? doc, the recommended follow-up (full re-trace, or confirm deletion).

## Important rules

1. **Don't touch Current docs at all.** Unchanged metadata is the no-op signal.
2. **Actual bytes are authoritative.** SHA/history is context; dirty source and independently
   changing modules are checked under their own identities.
3. Match each doc's existing voice — this is the corpus `document-workflow` produced; stay tech-agnostic.
4. Never change a doc's `Schema` or section structure.
5. Published `workflows/*` docs only — never generation artifacts, never task-status flips.

## What this skill does NOT do

- **Fresh documentation** of a new workflow → `document-workflow`.
- **Detecting undocumented workflows** → `docs-tasks-creator`.
- **Schema migration** of the doc format → re-run `document-workflow`.

## Output file

No artifact of its own — it edits the existing docs in place and prints the final report table.
