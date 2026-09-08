---
name: docs-tasks-creator
description: "Creates or refreshes a documentation backlog by inventorying endpoints, message handlers, and background jobs. Use to scan routes or jobs and generate _docs-tasks.md plus project-overview.md, including monorepos. Covers Next.js App Router / Pages API / Server Actions, Express, Fastify, NestJS, ASP.NET Core attribute / minimal APIs, GRPC .NET, BackgroundService, and Azure Functions. Documenting one operation belongs to document-workflow."
arguments: codebase_path output_dir
---

# Goal

Produce these artifacts. For a single-repo codebase they live directly under `$output_dir`; for a monorepo they live under per-workspace subdirs (`$output_dir/<workspace>/`):

1. `_docs-tasks.md` — a tasks doc with one `## Task N — Document <name>` section per detected execution boundary.
2. `project-overview.md` — a synthesized project orientation: name, detected stack(s), top-level layout, build/run commands, entry-point counts per trigger type.
3. `workflows/` — empty scaffold directory where the per-workflow docs will land once each task is worked.

Each emitted task is independent — the `Reference:` line points at the handler to document, the `Files affected:` line points at the doc to produce. The doc itself follows the `document-workflow` output format (Summary, Sequence of Calls, Flow Description, Data Inventory, Business Rules, Configuration, Dependencies).

## Input

- `$codebase_path` — absolute path to the codebase to scan (read-only).
- `$output_dir` — absolute path where artifacts land. Typically `raw/{client}/{project}/`.

Resolve the per-workspace handoff using
[the documentation evidence contract](references/shared/documentation-evidence.md):
`source_root`, `docs_root`, `workspace_root`, `entry_reference`, and `resolved_output`.
For single-repo mode, `source_root = workspace_root = $codebase_path` and
`docs_root = $output_dir`. For monorepo mode, `source_root = $codebase_path`,
`workspace_root = <selected workspace directory>`, and
`docs_root = $output_dir/<workspace-slug>`.

## Pre-flight

- [ ] Confirm `$codebase_path` exists and is a directory.
- [ ] Confirm `$output_dir` exists; if missing, create it.

## Process

### Phase 1 — Monorepo detection and workspace selection

Inspect orientation files at the codebase root: `README*`, `package.json`, `pnpm-workspace.yaml`, `nx.json`, `turbo.json`, `lerna.json`, `rush.json`, and any `*.sln` / `*.csproj` files at depth ≤ 2.

Check for monorepo signals in **this precedence order** (use the first match):

| Signal | Workspace enumeration |
|---|---|
| `pnpm-workspace.yaml` | Inspect its `packages:` field; resolve glob patterns against codebase root; each resolved dir containing a `package.json` is a workspace |
| `package.json` `workspaces` field | Inspect the array (or `.packages`); resolve globs; each resolved dir with a `package.json` is a workspace |
| `nx.json` | Enumerate `**/project.json`; each match's directory is a workspace |
| `lerna.json` | Inspect its `packages:` field (default `["packages/*"]`); resolve globs |
| `rush.json` | Inspect `projects[].projectFolder`; each entry is a workspace |
| `turbo.json` (and no JS workspaces yet detected) | Turborepo relies on `package.json` workspaces; treat as that signal |
| Multiple `.csproj` reachable from a `.sln` | Parse `Project(...)` lines in the `.sln`; **first drop test projects** (name or dir matching `*.Tests`, `*.UnitTests`, `*.IntegrationTests`, `tests/**`) — they have no documentable surface; each remaining `.csproj` directory is a workspace. If exactly one non-test project remains (the canonical src+tests layout), that is single-repo mode, no selection prompt. For a layered single-app solution (one Web/host project with handlers + class libraries), prefer single-repo mode with `service` derived from the handler class, not monorepo mode with one workspace per library `.csproj`. |
| **Heuristic fallback** | If multiple top-level dirs (e.g. `apps/`, `services/`, `packages/`, `libs/`) each contain a `package.json` or `.csproj`, each such dir is a workspace |

**If 0 or 1 workspaces detected** → single-repo mode. Skip the selection step; treat `$codebase_path` as the single workspace; emit artifacts directly under `$output_dir` (no subdir). Proceed to Phase 2.

**If 2+ workspaces detected** → monorepo mode. Use the user's explicit workspace selection,
including an already authorized request for all workspaces. Otherwise ask which to scan:

- **2–4 workspaces** — prefer the structured question interface with one option per workspace plus an "All workspaces" option; set `multiSelect: true`.
- **5+ workspaces** — emit a plain-text list of workspaces (one per line with the workspace path) and ask the user to reply with comma-separated workspace names, `"all"`, or `"none"`.

Present each workspace as `<workspace-slug>` `(<relative path>)`. The workspace slug is derived as:
- JS / Node workspace: `package.json`'s `name` field with any scope stripped (`@myorg/users-api` → `users-api`).
- .NET project: `.csproj` filename without extension, lower-case + kebab (`Users.Api.csproj` → `users-api`).
- Fallback: directory name (kebab-cased).

For each selected workspace, run Phases 2–6 with the workspace's directory as the scan root and artifacts going to `$output_dir/<workspace-slug>/`.

### Phase 2 — Stack detection (per workspace)

Walk the workspace's top two directory levels. Multiple detectors may apply within one workspace — run all that match.

| Detector | Triggered by |
|---|---|
| Next.js App Router | `next` dependency or `next.config.{js,ts,mjs}` present, AND `app/**/route.{ts,js}` or `src/app/**/route.{ts,js}` exists |
| Next.js Pages API | `next` dependency or `next.config.{js,ts,mjs}` present, AND `pages/api/**` or `src/pages/api/**` exists |
| Next.js Server Actions | `'use server'` directive found in `.ts`/`.tsx` under `app/` or `src/app/` |
| Express | `package.json` has `express` in `dependencies` |
| Fastify | `package.json` has `fastify` in `dependencies` |
| NestJS | `package.json` has `@nestjs/core` in `dependencies` |
| ASP.NET Core (attribute) | `.csproj` uses `Microsoft.NET.Sdk.Web` **or** explicitly references `Microsoft.AspNetCore.App`, AND any `.cs` file contains `[ApiController]` |
| ASP.NET minimal API | `.csproj` uses `Microsoft.NET.Sdk.Web` **or** explicitly references `Microsoft.AspNetCore.App`, AND any `.cs` file contains `WebApplication.CreateBuilder` |
| GRPC .NET | `.csproj` references `Grpc.AspNetCore` OR `.proto` files exist in the source tree |
| .NET background workers | Any `.cs` file declares a class inheriting `BackgroundService` or implementing `IHostedService` |
| Azure Functions (.NET isolated / in-process) | `.csproj` uses `Azure.Functions.Sdk` or references `Microsoft.Azure.Functions.Worker` (isolated), OR references `Microsoft.NET.Sdk.Functions` (in-process) |

**Never enter these directories during scan**: `node_modules`, `bin`, `obj`, `dist`, `build`, `.next`, `.git`, `vendor`, `target`, `__pycache__`, `.venv`, `.cache`, `out`.

### Phase 3 — Per-detector entry-point scan

For each active detector in the current workspace, find entry points using the recipe below. Use file enumeration, text search, and file inspection only — no shell recursion, no shell expansion.

Consult [references/detectors.md](references/detectors.md) for the active detectors identified in Phase 2 before scanning. Run every matching detector; the capture contract below still applies.

Record one coverage row per activated or plausibly present detector: `Covered` when every
supported static form was inspected, `Partial` when a dynamic/ambiguous registration prevents
resolution, `Unsupported` when framework signals exist without a recipe, and `Error` when a
bounded scan failed. Include the exact roots/patterns searched and the boundary. `Covered`
means covered by this documented static recipe; it is never a claim that runtime registration
was exhaustively observed.

#### Per-entry-point captures

For each detected entry point, capture:
- `name` — kebab-case workflow name, derived from the handler symbol or URL path. `UsersController.GetById` → `users.get-by-id`. `/api/users/{id}` GET → `users.get-by-id`. Strip route-parameter punctuation (`{id}` → `by-id`, `[id]` → `by-id`).
- `service` — for monorepos, derived from sub-projects within the workspace (a workspace can still contain multiple services). For single-repo, derived from the `.csproj` directory name (e.g. `Users.Api`), the top-level package/workspace dir, or the codebase root's directory name.
- `reference` — `<relative-path-from-workspace-root>:<symbol>` form when a symbol exists. URL-style for inline route handlers (`POST /api/orders`).
- `trigger` — human-readable trigger description (e.g. `REST GET /api/users/{id}`, `Message handler: order.created`, `Background worker: 30s interval`).
- `files_affected` — `workflows/<service>/<name>.md` for backend tasks; **`workflows/_fullstack/<name>.md` for full-stack tasks** (path of the doc that will be produced, **relative to the workspace's output dir**). Keying full-stack docs under `_fullstack/` prevents a full-stack and a backend doc for the *same operation* from resolving to the same path.
- `workflow_id` — stable execution-boundary identity, independent of task order and source
  filename: `<workspace-slug>:<kind>:<canonical-trigger>`. Canonical HTTP triggers include
  method + fully composed literal route; messages include broker/binding kind + literal
  destination; GRPC includes service + RPC; scheduled jobs include the declared schedule +
  handler symbol. If the trigger lacks a stable external address, include the fully-qualified
  handler symbol. Add the service only to disambiguate a real collision. Never derive identity
  from `Task N`, alphabetical position, or physical file alone.

### Phase 4 — Synthesize `project-overview.md`

Write `<workspace-output-dir>/project-overview.md` in this exact shape:

````markdown
# <Workspace Name> — Project Overview

> Generated by `docs-tasks-creator` on YYYY-MM-DD. Synthesized from codebase scan;
> verify any `[TODO: verify]` flags before relying on them.

## Summary

|              |                                                          |
| ------------ | -------------------------------------------------------- |
| Path         | `<workspace path relative to monorepo root>` (or absolute for single-repo) |
| Stack(s)     | <comma-separated detected stack names>                   |
| Services     | <count> (<comma-separated service names>)                |
| Entry points | <total>: <n> REST, <n> messages, <n> jobs, …             |

## Top-level layout

(1–2 levels deep, with one-line annotations on noteworthy dirs.)

- `src/` — …
- `tests/` — …
- `Services/` — …

## Build / Run

(Detected from `package.json` scripts, `*.csproj` defaults, or README. Trim noise — keep build, run, test, and deploy commands only.)

- `<command>` — <one-line description>

## Services

(For each detected service / `.csproj` / sub-project within the workspace:)

### <Service name>

- Path: `<relative path from workspace root>`
- Entry points: <count> (<verb breakdown>)
- Stack: <which detector matched>

## Scan coverage

| Detector | State | Roots/patterns searched | Boundary |
| -------- | ----- | ----------------------- | -------- |
| <name>   | Covered / Partial / Unsupported / Error | <enumerated roots/patterns> | <none or exact unresolved form> |

## Notes

- (Anything unusual flagged during scan: dynamic mounting, custom routing, malformed proto files, etc.)
````

Keep the file under ~200 lines. The goal is orientation, not exhaustive documentation — handlers get their own docs through the per-task workflows.

### Phase 5 — Emit handler tasks

For each execution boundary captured in Phase 3 (for the current workspace), emit a
`## Task N — Document <name>` section. On first generation, assign N in service/name order.
On refresh, retain each exact `Workflow ID`'s number and assign new tasks monotonically after
the prior maximum; task numbers are display locators, never identity. Keep document order by
service/name, even when retained numbers are no longer sequential.

**Group by execution boundary, not physical file.** Independent decorated functions/routes in
one file remain separate tasks. Combine members only when a static edge proves one workflow:
for example, a Durable starter names an orchestrator and that orchestrator calls named
activities, or an output binding's literal destination matches a consumer trigger. Record every
member reference in the combined task. A merely co-located or similarly named member is not
proof of connection; keep it separate or mark the grouping `Partial` for review.

### Phase 6 — Write the tasks doc

Write or refresh `<workspace-output-dir>/_docs-tasks.md` in this exact schema-v2 shape:

````markdown
# Documentation Tasks — <Workspace Name>

> Generated by `docs-tasks-creator` on YYYY-MM-DD from `<workspace path>`.
> Inventory Schema: v2
> Each task below describes one workflow to document. Work them however you like —
> manually, through the workflow skill, in a loop, or in batch. The output doc follows
> the `document-workflow` output format.
> Refresh reconciles by Workflow ID and preserves task progress, evidence, and manual notes.

## Handoff

| Field          | Value                    |
| -------------- | ------------------------ |
| Source root    | `<absolute source root>` |
| Docs root      | `<absolute docs root>`   |
| Workspace root | `<absolute workspace root>` |

## Tasks overview

| #   | Title                          | Trigger                        | Service        | Status |
| --- | ------------------------------ | ------------------------------ | -------------- | ------ |
| 1   | Document `users.get-by-id`     | REST GET `/api/users/{id}`     | Users.Api      | Todo   |
| 2   | Document `users.create`        | REST POST `/api/users`         | Users.Api      | Todo   |
| …   | …                              | …                              | …              | …      |

## Task 1 — Document `users.get-by-id`

**Status:** Todo
**Workflow ID:** `users-api:http:get:/api/users/{id}`
<!-- inventory:begin -->
**Source root:** `<absolute source root>`
**Docs root:** `<absolute docs root>`
**Workspace root:** `<absolute workspace root>`
**Reference:** `src/Users.Api/Controllers/UsersController.cs:GetById`
**Files affected:** `workflows/users/get-by-id.md`
**Resolved output:** `<absolute docs root>/workflows/users/get-by-id.md`
**Trigger:** REST GET `/api/users/{id}`
<!-- inventory:end -->

**Acceptance criteria:**
- A workflow doc exists exactly at the task's `Resolved output`.
- The doc follows the `document-workflow` output format (Summary, Sequence of Calls, Flow Description, Data Inventory, Business Rules, Configuration, Dependencies).
- Backend mode (no full-stack-mode signals in this task body).

## Task 2 — Document `users.create`

…
````

Also create the empty `<workspace-output-dir>/workflows/` directory.

### Refresh reconciliation

Before writing, parse an existing tasks doc and reconcile it with the new scan:

1. Key schema-v2 tasks by exact `Workflow ID`. For legacy tasks without an ID, derive a
   candidate from their Trigger/Reference once and list the proposed migration in the change
   report; do not silently transfer evidence when the mapping is ambiguous.
2. Exact IDs retain their task number, `Status`, acceptance/evidence history, and all manual
   prose outside `<!-- inventory:begin/end -->`. Replace only generated inventory fields when
   they changed.
3. New IDs become `Todo` with a new number greater than the previous maximum. An earlier
   alphabetical insertion never renumbers or remaps an existing task.
4. Unmatched old IDs remain in a `## Retired workflows — review required` section with their
   full notes/evidence and `Status: Review retirement`; never delete or mark them done.
5. For an unmatched old/new pair with the same service/kind and similar trigger/reference,
   report `Possible rename: <old> → <new>` for human review. Do not transfer completion or
   evidence until accepted.
6. If the reconciled tasks doc and overview have no semantic change, do not write either file
   and do not update their generated date. Report `no-op`. Otherwise report added, changed,
   possible-renamed, and retired IDs explicitly.

## Output format — Tasks doc field shapes

Every task section MUST contain, in this order:

- `## Task <N> — Document <name>` heading (`Document` prefix is the convention; `<name>` is the kebab-case workflow name).
- `**Status:** Todo` (or preserved status on refresh) — picked up by any tasks-doc consumer (manual or tooled).
- `**Workflow ID:** <stable-id>` — authoritative identity across refreshes; task number is only a locator.
- An `inventory:begin/end` block containing the generated handoff fields below. Preserve all
  user notes and evidence outside this block verbatim.
- `**Source root:** <absolute-path>` and `**Docs root:** <absolute-path>` — source is read-only;
  documentation writes stay under Docs root.
- `**Workspace root:** <absolute-path>` — base for `Reference`.
- `**Reference:** <path>:<symbol>` — points at the entry point to document. URL-style references (`POST /api/orders`) are allowed for inline route handlers where no symbol exists. Matches the input shape `document-workflow` expects.
- `**Files affected:** workflows/<service>/<name>.md` — the doc that will be produced. Path is relative to the workspace's output dir.
- `**Resolved output:** <absolute-path>` — authoritative destination, contained by Docs root.
- `**Trigger:** <human-readable trigger>` — orientation for a human scanning the doc; not parsed.
- `**Acceptance criteria:**` block — three bullets covering: (1) the produced doc exists exactly
  at `Resolved output`, (2) it follows the `document-workflow` output format, (3) the mode
  (Backend by default; Full-stack only if the task body signals it via accepted keywords).

Service grouping uses no checkpoint headings — the active tasks doc is a flat list. The
`Service` column in the overview table is the grouping signal. Retired tasks have their own
review section so they cannot be mistaken for active work.

## Anti-patterns

- **Do not invent handlers.** If a supported static detector recipe doesn't match, do not emit
  a task. Record dynamic or unsupported registration in Scan coverage as `Partial` or
  `Unsupported`; never turn absence from a bounded scan into a claim that no handler exists.
  The user can manually add tasks for runtime-only handlers.
  When a *statically-detectable* framework is present but has **no detector** (e.g. an `.csproj` with `Microsoft.Azure.Functions.Worker` and the Functions detector is somehow off), surface it in `project-overview.md` Notes as `[unsupported handler framework: N <kind> entry points detected, not emitted as tasks]` — do **not** let "don't invent handlers" absorb it into a silently-thin result.
- **Do not infer monorepo scope.** When 2+ workspaces are detected, honor an explicit selection
  already supplied by the user; otherwise ask which to scan. Workspace discovery alone does
  not authorize scanning all workspaces.
- **Do not emit a single combined tasks doc for monorepos.** One tasks doc per workspace, each under its own subdir. The whole point of monorepo handling is keeping per-workspace concerns separable.
- **Do not emit empty-completeness artifacts.** If no framework signal and no entry point is
  found, skip the workspace and list `[zero-handler workspace skipped: <name>]` in the nearest
  overview. If a detector is `Partial`, `Unsupported`, or `Error` and captured zero tasks, emit
  `project-overview.md` with the explicit Scan coverage boundary but no `_docs-tasks.md` or empty
  workflow scaffold.
- **Do not include files outside `$codebase_path`.** Symlinks, projects outside the scan root, etc. — stay within the input root.
- **Do not scan vendor/build directories.** `node_modules`, `bin`, `obj`, `dist`, `build`, `.next`, `vendor`, `target`, `out`, `.cache`, `__pycache__`, `.venv` are explicitly excluded — they contain compiled or third-party code that is not part of the workflow surface.
- **Do not emit a `Task 0 — Setup`.** Setup work (scaffolding + `project-overview.md`) happens inline in Phase 4 of *this* skill. The tasks doc contains handler tasks only.
- **Do not modify files in `$codebase_path`.** This skill is read-only against the codebase; only `$output_dir` is written to.
- **Do not fail the whole run on a single detector error.** If a `.proto` file is malformed and the GRPC detector can't parse it, append `[scan warning: <detail>]` to the `Notes` section of the workspace's `project-overview.md` and continue with the other detectors.
- **Do not invent ID slugs that collide.** If two handlers within the same workspace map to the same `<name>` (e.g. two different services both expose `users.get-by-id`), suffix the second with the service name: `users.get-by-id--users-api` vs `users.get-by-id--admin-api`. The task heading stays unique within its workspace. This covers same-kind slug clashes. **Also detect `(kind, slug)` clashes across kinds:** if a full-stack task and a backend task target the same `<service>/<name>`, route the full-stack one to `workflows/_fullstack/<name>.md` (per Phase 3) so neither silently claims the other's path; if any disambiguation happened, note "N path collisions disambiguated" in `project-overview.md` Notes.
- **Do not skip the `Tasks overview` table.** It's a useful index for any consumer; emit it even if the per-task sections look complete.
- **Do not couple the emitted tasks doc to any specific runner.** The doc is consumer-agnostic — usable manually, looped, or in batch. The skill body never assumes one workflow consumer over another.

## When to use

- At engagement start on a new codebase, to seed the documentation backlog.
- When a project's surface has grown and the backlog needs a refresh. Schema-v2 refreshes
  reconcile stable workflow IDs and preserve existing progress, evidence, and notes.
- For a monorepo, run incrementally with the requested workspace selection, asking only when
  that selection is missing.

## When NOT to use

- For pure libraries / SDKs with no handler surface — there's nothing to detect.
- For pure-frontend apps (Vite / CRA / static React with no API routes or server actions) — no auto-discoverable handlers. Full-stack docs need manually-authored tasks with full-stack-mode-triggering language in the body (`"full workflow"`, `"end-to-end"`, etc.).
- For codebases that use only dynamic/runtime registration — emit the bounded overview and
  recommend a manual tasks doc; do not emit an empty generated backlog.
