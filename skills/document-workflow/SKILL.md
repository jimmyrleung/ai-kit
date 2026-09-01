---
name: document-workflow
description: "Deep-dive documentation of one workflow operation: locate the entry point, trace the happy path and branching hop-by-hop through real source, and write the canonical workflow doc (sequence of calls, data inventory, business rules, configuration, source files) under workflows/ at the target repo's git root. Backend mode by default (endpoint, message consumer, scheduled job); full-stack mode only when explicitly signaled (end-to-end, from the client). Accepts a loose reference: a handler or method name, a file path, or a description. Use when asked to document a workflow, endpoint, handler, route, consumer, job, or flow, or to create or update a workflow doc."
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

Resolve it to a concrete entry point. If it matches several candidates, list them and ask
before proceeding. Echo the resolved (entry point, mode, output path) triple back before
tracing.

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

1. Create a todo list for all steps.
2. Launch 1–3 specialized agents to follow the [Instructions] below.
3. Consolidate their findings, identifying where they converge and where they diverge.
4. Calculate a confidence score from their agreement. If divergence is too high, run
   another round — **at least 95% confidence** is required to proceed.
5. Once confident, write the doc per [Output] below.

## Instructions

1. **Locate the entry point.** Backend: REST controller action, GRPC service method,
   message/event handler, scheduled job/cron handler. Full-stack: the client action
   (screen, view, route, command) and the user/system action that fires it — the backend
   handler becomes a downstream step, not the root.
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

**Path** — anchored at the **git root of the target repo** (where `.git` lives), NOT the
current or tasks-doc directory (a doc written elsewhere is reported missing by docs QA):

- Backend mode: `<repo>/workflows/<service-name>/<workflow-name>.md`
- Full-stack mode: `<repo>/workflows/_fullstack/<workflow-name>.md` (no single service
  owns the flow; link back from per-service docs if they exist)

`<workflow-name>` is short kebab-case (e.g. `delete-credit-card`).

**Metadata** — populate literally, never leave placeholders:

- Fresh doc: `Created` = `Last Updated` = today; one initial Change Log row
  (`Initial documentation pass` / `First version`).
- Updating an existing doc: inspect it first; keep `Created`, bump `Last Updated`, append one
  Change Log row per update (group related edits).
- `Generated From` = short SHA of `HEAD` (`git rev-parse --short HEAD`), advanced on every
  update — it means "the codebase state this doc was last verified against". If the call
  fails, set `unknown` with `[TODO: verify SHA]` rather than blocking.
- `Schema` stays `v1` until the template itself materially changes shape.
- `## Source Files`: every distinct path traced — entry point plus each handler / service /
  repository / external client / message handler / client UI read while building the
  sequence tree. This feeds staleness detection; missing paths = silent drift later.

## Guidelines

- Prefer component names over descriptions in the sequence tree
  (✓ `TrapHttpClient.GetCreditCards` — ✗ `Calls trap to get credit cards`).
- Keep descriptions scannable — the doc is used in refinement sessions; for complex-logic
  sections, optimize for "could I explain this in a refinement using just this doc?".
- Flag anything unclear with `[TODO: verify]` rather than guessing.
- If the workflow is exceptionally complex (10+ decision points), suggest splitting the
  doc into sections or separate flows.

## What this skill does NOT do

- **Staleness triage across existing workflow docs** — `update-workflow-docs` owns the
  corpus-wide drift detection + in-place refresh. Updating ONE named doc is in scope here.
- **Choosing what to document** — `docs-tasks-creator` scans and emits the task list.
- **Code changes** — anything found broken while tracing is reported, then handed to
  `bug-investigation` / the implement-task family.
