---
name: docs-tasks-creator
description: "Create or refresh a documentation backlog by scanning a codebase to inventory endpoints, message handlers, and background jobs. Emits one document-workflow task per detected workflow in _docs-tasks.md plus project-overview.md, with workspace selection for monorepos. Covers Next.js (App Router, Pages API, Server Actions), Express, Fastify, NestJS, ASP.NET Core (attribute and minimal API), GRPC .NET, .NET BackgroundService, and Azure Functions. Use to inventory routes or jobs and generate documentation tasks; the output is consumer-agnostic."
arguments: codebase_path output_dir
---

# Goal

Produce these artifacts. For a single-repo codebase they live directly under `$output_dir`; for a monorepo they live under per-workspace subdirs (`$output_dir/<workspace>/`):

1. `_docs-tasks.md` — a tasks doc with one `## Task N — Document <name>` section per detected handler.
2. `project-overview.md` — a synthesized project orientation: name, detected stack(s), top-level layout, build/run commands, entry-point counts per trigger type.
3. `workflows/` — empty scaffold directory where the per-workflow docs will land once each task is worked.

Each emitted task is independent — the `Reference:` line points at the handler to document, the `Files affected:` line points at the doc to produce. The doc itself follows the `document-workflow` output format (Summary, Sequence of Calls, Flow Description, Data Inventory, Business Rules, Configuration, Dependencies).

## Input

- `$codebase_path` — absolute path to the codebase to scan (read-only).
- `$output_dir` — absolute path where artifacts land. Typically `raw/{client}/{project}/`.

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

**If 2+ workspaces detected** → monorepo mode. Ask the user which to scan:

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
| Next.js App Router | `next.config.{js,ts,mjs}` present AND `app/**/route.{ts,tsx,js,jsx}` exists |
| Next.js Pages API | `next.config.{js,ts,mjs}` present AND `pages/api/**` exists |
| Next.js Server Actions | `'use server'` directive found in any `.ts`/`.tsx` file under `app/` or `src/` |
| Express | `package.json` has `express` in `dependencies` |
| Fastify | `package.json` has `fastify` in `dependencies` |
| NestJS | `package.json` has `@nestjs/core` in `dependencies` |
| ASP.NET Core (attribute) | `.csproj` references `Microsoft.AspNetCore.App` framework AND any `.cs` file contains `[ApiController]` |
| ASP.NET minimal API | `.csproj` references `Microsoft.AspNetCore.App` AND any `.cs` file contains `WebApplication.CreateBuilder` |
| GRPC .NET | `.csproj` references `Grpc.AspNetCore` OR `.proto` files exist in the source tree |
| .NET background workers | Any `.cs` file declares a class inheriting `BackgroundService` or implementing `IHostedService` |
| Azure Functions (.NET isolated / in-process) | `.csproj` references `Microsoft.Azure.Functions.Worker` (isolated) OR `Microsoft.NET.Sdk.Functions` (in-process) |

**Never enter these directories during scan**: `node_modules`, `bin`, `obj`, `dist`, `build`, `.next`, `.git`, `vendor`, `target`, `__pycache__`, `.venv`, `.cache`, `out`.

### Phase 3 — Per-detector entry-point scan

For each active detector in the current workspace, find entry points using the recipe below. Use file enumeration, text search, and file inspection only — no shell recursion, no shell expansion.

Consult [references/detectors.md](references/detectors.md) for the active detectors identified in Phase 2 before scanning. Run every matching detector; the capture contract below still applies.

#### Per-entry-point captures

For each detected entry point, capture:
- `name` — kebab-case workflow name, derived from the handler symbol or URL path. `UsersController.GetById` → `users.get-by-id`. `/api/users/{id}` GET → `users.get-by-id`. Strip route-parameter punctuation (`{id}` → `by-id`, `[id]` → `by-id`).
- `service` — for monorepos, derived from sub-projects within the workspace (a workspace can still contain multiple services). For single-repo, derived from the `.csproj` directory name (e.g. `Users.Api`), the top-level package/workspace dir, or the codebase root's directory name.
- `reference` — `<relative-path-from-workspace-root>:<symbol>` form when a symbol exists. URL-style for inline route handlers (`POST /api/orders`).
- `trigger` — human-readable trigger description (e.g. `REST GET /api/users/{id}`, `Message handler: order.created`, `Background worker: 30s interval`).
- `files_affected` — `workflows/<service>/<name>.md` for backend tasks; **`workflows/_fullstack/<name>.md` for full-stack tasks** (path of the doc that will be produced, **relative to the workspace's output dir**). Keying full-stack docs under `_fullstack/` prevents a full-stack and a backend doc for the *same operation* from resolving to the same path.

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

## Notes

- (Anything unusual flagged during scan: dynamic mounting, custom routing, malformed proto files, etc.)
````

Keep the file under ~200 lines. The goal is orientation, not exhaustive documentation — handlers get their own docs through the per-task workflows.

### Phase 5 — Emit handler tasks

For each entry point captured in Phase 3 (for the current workspace), emit a `## Task N — Document <name>` section. N is positional within the workspace's tasks doc, starting at 1. **Group tasks by service in document order** — all of Service A's tasks first, then Service B's, etc. Service order is alphabetical.

**Multi-`[Function]` workflows — one task per workflow file, not per method.** Where one logical workflow spans several decorated members — **Durable Functions** (trigger + orchestrator + N activities in one file) or an **HTTP-starter + queue-consumer pair** — emit **one task per externally-triggered workflow file** and enumerate the orchestrator + activities inside that task's acceptance criteria, *not* a separate task per `[Function]`. (A durable-heavy repo otherwise explodes: ~100 `[Function]` methods → ~46 useful workflow tasks.)

### Phase 6 — Write the tasks doc

Write `<workspace-output-dir>/_docs-tasks.md` in this exact shape:

````markdown
# Documentation Tasks — <Workspace Name>

> Generated by `docs-tasks-creator` on YYYY-MM-DD from `<workspace path>`.
> Each task below describes one workflow to document. Work them however you like —
> manually, through the workflow skill, in a loop, or in batch. The output doc follows
> the `document-workflow` output format.
> Re-running this skill regenerates the full inventory — manually flip `Status: Done`
> for handlers already documented, or delete those tasks before re-working.

## Tasks overview

| #   | Title                          | Trigger                        | Service        | Status |
| --- | ------------------------------ | ------------------------------ | -------------- | ------ |
| 1   | Document `users.get-by-id`     | REST GET `/api/users/{id}`     | Users.Api      | Todo   |
| 2   | Document `users.create`        | REST POST `/api/users`         | Users.Api      | Todo   |
| …   | …                              | …                              | …              | …      |

## Task 1 — Document `users.get-by-id`

**Status:** Todo
**Reference:** `src/Users.Api/Controllers/UsersController.cs:GetById`
**Files affected:** `workflows/users/get-by-id.md`
**Trigger:** REST GET `/api/users/{id}`

**Acceptance criteria:**
- A workflow doc exists at `workflows/users/get-by-id.md`.
- The doc follows the `document-workflow` output format (Summary, Sequence of Calls, Flow Description, Data Inventory, Business Rules, Configuration, Dependencies).
- Backend mode (no full-stack-mode signals in this task body).

## Task 2 — Document `users.create`

…
````

Also create the empty `<workspace-output-dir>/workflows/` directory.

## Output format — Tasks doc field shapes

Every task section MUST contain, in this order:

- `## Task <N> — Document <name>` heading (`Document` prefix is the convention; `<name>` is the kebab-case workflow name).
- `**Status:** Todo` — picked up by any tasks-doc consumer (manual or tooled).
- `**Reference:** <path>:<symbol>` — points at the entry point to document. URL-style references (`POST /api/orders`) are allowed for inline route handlers where no symbol exists. Matches the input shape `document-workflow` expects.
- `**Files affected:** workflows/<service>/<name>.md` — the doc that will be produced. Path is relative to the workspace's output dir.
- `**Trigger:** <human-readable trigger>` — orientation for a human scanning the doc; not parsed.
- `**Acceptance criteria:**` block — three bullets covering: (1) the produced doc exists at the expected path, (2) it follows the `document-workflow` output format, (3) the mode (Backend by default; Full-stack only if the task body signals it via the keywords `document-workflow` recognizes).

Service grouping in v1 uses no checkpoint headings — the tasks doc is a flat list. The `Service` column in the overview table is the only grouping signal. If you later want to checkpoint per service (e.g., for batch reviewing after each service is done), add the checkpoint headings manually.

## Anti-patterns

- **Do not invent handlers.** If a detector recipe doesn't grep-match, the handler doesn't exist for v1's purposes. The user can manually add tasks for dynamically-mounted or otherwise-undetectable handlers by editing `_docs-tasks.md` after the run.
  When a *statically-detectable* framework is present but has **no detector** (e.g. an `.csproj` with `Microsoft.Azure.Functions.Worker` and the Functions detector is somehow off), surface it in `project-overview.md` Notes as `[unsupported handler framework: N <kind> entry points detected, not emitted as tasks]` — do **not** let "don't invent handlers" absorb it into a silently-thin result.
- **Do not skip monorepo selection.** When 2+ workspaces are detected, always ask the user which to scan — do NOT silently scan all of them. A 30-workspace nx repo would produce 30 tasks docs with hundreds of tasks each; that's overwhelming and rarely what's wanted.
- **Do not emit a single combined tasks doc for monorepos.** One tasks doc per workspace, each under its own subdir. The whole point of monorepo handling is keeping per-workspace concerns separable.
- **Do not emit artifacts for zero-handler workspaces.** If a selected workspace's Phase 3 scan
  finds zero entry points, do not create its output folder / `project-overview.md` / `_docs-tasks.md`
  — list it in the nearest emitted `project-overview.md` Notes as
  `[zero-handler workspace skipped: <name>]`. Empty scaffolds are noise the user deletes by hand.
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
- When a project's surface has grown (new controllers, new workers) and the backlog needs a refresh. Note that v1 re-runs regenerate the full inventory; the user manually reconciles what's already documented (delete or `Status: Done` the existing tasks).
- For a monorepo, run incrementally — scan workspace A this week, workspace B next week, etc. The skill makes that easy by asking which workspaces to scan each time.

## When NOT to use

- For pure libraries / SDKs with no handler surface — there's nothing to detect.
- For pure-frontend apps (Vite / CRA / static React with no API routes or server actions) — no auto-discoverable handlers. Full-stack docs need manually-authored tasks with full-stack-mode-triggering language in the body (`"full workflow"`, `"end-to-end"`, etc.).
- For codebases that use only dynamic / runtime handler registration with no static signal — the scan would produce a misleadingly empty result. Consider manually authoring the tasks doc instead.
