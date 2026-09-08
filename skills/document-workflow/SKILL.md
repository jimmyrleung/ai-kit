---
name: document-workflow
description: "Documents or updates one workflow, endpoint, route, handler, message consumer, job, or flow by tracing real source. Accepts a generated docs task, handler/method name, file path, or description. Backend by default; full-stack / end-to-end documentation when explicitly requested. Inventorying what to document belongs to docs-tasks-creator; checking drift across existing docs belongs to update-workflow-docs."
---

# document-workflow — deep-dive doc for one workflow operation

You are a workflow documentarian. You trace ONE operation end-to-end through the actual
source and write its canonical workflow doc; you do **not** modify code, fix bugs you
notice while tracing, or document a second workflow "while you're here".

> **Litmus test:** if you're editing source files, or the doc describes how the code
> *should* behave rather than how it *does*, you've left the lane.

## When to use

- **Ad-hoc:** asked to document a workflow, endpoint, handler, message consumer, job, or
  end-to-end flow — or to update an existing `workflows/` doc after a change.
- **Orchestrated:** working one task from a `docs-tasks-creator` tasks doc manually (its
  `Reference:` line is this skill's input shape).

## When NOT to use

- Headless per-task runs under cc-loop → `document-workflow-loop` (cc-looper-owned fork).
- Deciding *what* to document across a codebase → `docs-tasks-creator`.
- Terraform / infrastructure → `document-terraform`.
- Pre-implementation recon of an unfamiliar area → `lay-of-the-land` (a sourced map, not a
  deep-dive).

## Input contract — loose reference

Accept any of:

- a method/handler name — `DeleteCreditCard`, `ProcessOrderHandler`
- a file path — `src/Users.Api/Services/UsersServiceV1.cs`
- a descriptive reference — `"the GRPC call that deletes credit cards"`
- a full-stack reference — `"the full order submission workflow end-to-end"`
- a generated `docs-tasks-creator` task carrying `Source root`, `Docs root`,
  `Workspace root`, `Reference`, and `Resolved output`

Resolve it to a concrete entry point. If it matches several candidates, list them and ask
before proceeding. Resolve roots and paths with
[the documentation evidence contract](references/shared/documentation-evidence.md).
For a generated task, its five handoff values are authoritative: resolve `Reference`
against `Workspace root` and write exactly `Resolved output` inside `Docs root`. For an
ad-hoc reference, detect the source repository's git root, default `Docs root` to that root,
and derive the normal workflow path. Ask if the source/docs roots or destination are
ambiguous. Echo the resolved (source root, docs root, workspace root, entry point, mode,
resolved output) before tracing.

## Mode

- **Backend mode (default)** — entry point is a handler/worker/job (endpoint, message
  consumer, scheduled job). Covers ~90% of uses.
- **Full-stack mode (opt-in)** — entry point is a user/client action; the workflow is
  traced across the client/server boundary into a single source-of-truth doc.

Full-stack mode activates ONLY when the input explicitly signals it: phrases like
`"full workflow"`, `"end-to-end"`, `"e2e"`, `"fullstack"`, `"full-stack"`,
`"from the client"`, `"from the user"` — or a client-side entry point (screen name, user
action, device event). Otherwise default to backend mode; if genuinely ambiguous, ask
before switching. In full-stack mode, ask the user to name the **client** (web app, iOS
app, POS device, partner integration, …) so the doc is anchored. Stay tech-agnostic — do
not assume a framework, language, or platform on either side.

## Process

Follow [authorized work](references/shared/authorized-work.md); resolve bundled references
from this skill folder. Existing permission covers local tracing and drafting.

1. Map the entry, boundaries, and evidence needed by the Instructions below.
2. Keep a small isolated flow on the main thread. For distinct cross-service/data/security
   boundaries, plan independent coverage and use authorized native workers when available.
   Otherwise use separate scoped passes and record their weaker independence; consult the
   [provider capability reference](references/shared/provider-capabilities.md).
3. Consolidate by source evidence and missing coverage. Re-open load-bearing sources and
   resolve conflicting claims; worker agreement alone does not prove correctness.
4. Write the authorized doc using the Output contract. At least 95% confidence is the reporting
   target; unsupported sections remain explicit TODOs with precise next probes. Ask only for
   missing load-bearing facts or a real scope/owner decision, never permission inferred from a score.

## Instructions

1. **Locate the entry point.** Backend: REST controller action, GRPC service method,
   message/event handler, scheduled job/cron handler. Full-stack: the client action
   (screen, view, route, command) and the user/system action that fires it — the backend
   handler becomes a downstream step, not the root. Also identify the static registration,
   dispatch, routing, project, workspace, and configuration inputs that make this entry
   reachable. These are freshness inputs even when they are not a happy-path call.
2. **Trace the execution path** — the happy path through request handlers / use cases,
   domain services, external clients (HTTP, GRPC, SDK), repository/data access, message
   publishing. At an external boundary, check whether the target service exists in this
   repository: if yes, continue tracing into it and mark the boundary
   `── [<service-name>] ──` in the sequence tree. Full-stack: also trace upward from the
   client action into client code until the network call, marking the client/server
   boundary `── [<client-name>] ──` the same way. Stop only at true external boundaries
   (services outside this repo, third-party APIs, databases).
3. **Identify branching logic** — validation short-circuits, conditional dependencies,
   error handling that changes the flow. Full-stack also: client-side validation that
   short-circuits before any network call, network failures mid-flow, duplicate
   submission, auth/session expiry, stale local state vs. server state.
4. **Flag complex business logic** — calculations, query builders with conditional
   filters/joins, state machines, multi-step validations, algorithms, domain rules not
   self-evident from the code. Note each location and why it's complex.
5. **Catalog the data inventory** — request/response contracts, database tables and
   fields (read/write/both), events/messages, external API contracts. Full-stack also:
   client state (what it holds, not the mechanism), the wire contract (endpoint, auth,
   idempotency, response → client-outcome mapping), async push-back channels (websocket,
   polling, webhook, push, …).
6. **Extract business rules** in plain language a PM or domain expert would recognize —
   no code references, no class names; only rules that would matter in a requirements
   review, not every `if`.
7. **Extract configuration** — env vars, app settings, feature flags affecting the flow.
8. **Client-visible outcomes** *(full-stack only)* — per backend outcome (success, each
   error class, timeout, partial failure): what the user perceives and what the client
   does internally, tech-agnostic.
9. **Cross-cutting concerns** *(full-stack only)* — auth/session lifecycle across the
   boundary, feature flags on either side, analytics events, rate limits/i18n/a11y.

## Output

Write the doc in the exact format of [references/output-template.md](references/output-template.md)
— this template is the canonical contract for workflow docs (docs-tasks-creator acceptance
criteria and QA gates check against it); do not reshape its sections.

**Path** — use the resolved handoff destination. A generated task's `Resolved output` is
authoritative and must be inside its `Docs root`. In an ad-hoc run only, default Docs root to
the source git root:

- Backend mode: `<docs-root>/workflows/<service-name>/<workflow-name>.md`
- Full-stack mode: `<docs-root>/workflows/_fullstack/<workflow-name>.md` (no single service
  owns the flow; link back from per-service docs if they exist)

`<workflow-name>` is short kebab-case (e.g. `delete-credit-card`).

**Metadata** — populate literally, never leave placeholders:

- Fresh doc: `Created` = `Last Updated` = today; one initial Change Log row
  (`Initial documentation pass` / `First version`).
- Updating an existing doc: inspect it first; keep `Created`, bump `Last Updated`, append one
  Change Log row per update (group related edits).
- `Generated From` is a display value: the source root's short `HEAD`, or `unknown` with
  `[TODO: verify SHA]`. The authoritative bounded identity is `## Source Evidence`, built
  from actual bytes under the documentation evidence and shared change-evidence contracts.
- `Schema` is `v2`. A pre-v2 document remains readable, but its revision-only freshness is
  Unverifiable until a full retrace creates the v2 evidence fields.
- `## Source Evidence`: one row per source repository or independently changing source,
  including public-safe source ID, full revision, trace boundary (roots/patterns plus
  registration/config controls), relevant dirty paths, and manifest digest.
- `## Source Files`: every distinct path read — entry point, registration/dispatch/config
  controls, and every handler/service/repository/client/UI path used by the trace. Record
  source ID + path + role + SHA-256 of actual bytes. Missing paths cause silent drift later.
- A dirty relevant source may still be documented, but never label it clean or represent
  HEAD alone as the verified content. Record its byte identity and dirty layer explicitly.

## Guidelines

- Prefer component names over descriptions in the sequence tree
  (✓ `TrapHttpClient.GetCreditCards` — ✗ `Calls trap to get credit cards`).
- Keep descriptions scannable — the doc is used in refinement sessions; for complex-logic
  sections, optimize for "could I explain this in a refinement using just this doc?".
- Flag anything unclear with `[TODO: verify]` rather than guessing.
- Source code is read-only. Write only the resolved documentation output inside Docs root,
  including when Docs root is a separate repository.
- If the workflow is exceptionally complex (10+ decision points), suggest splitting the
  doc into sections or separate flows.

## What this skill does NOT do

- **Staleness triage across existing workflow docs** — `update-workflow-docs` owns the
  corpus-wide drift detection + in-place refresh. Updating ONE named doc is in scope here.
- **Choosing what to document** — `docs-tasks-creator` scans and emits the task list.
- **Code changes** — anything found broken while tracing is reported, then handed to
  `bug-investigation` / the implement-task family.
