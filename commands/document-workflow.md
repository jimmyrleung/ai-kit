---
description: Deep-dive documentation for a specific workflow operation.
argument-hint: A method/handler name, a file path, or a descriptive reference.
---

# Document Workflow

Deep-dive documentation for a specific workflow operation.

## Input

$ARGUMENTS should be one of:

- A method/handler name: `DeleteCreditCard`, `ProcessOrderHandler`
- A file path: `src/Users.Api/Services/UsersServiceV1.cs`
- A descriptive reference: `"the GRPC call that deletes credit cards"`
- A full-stack reference: `"the full order submission workflow end-to-end"`

## Mode

The skill has two modes:

- **Backend mode (default)** — entry point is a handler/worker/job. Used for endpoints, message consumers, scheduled jobs. This is the default and covers ~90% of uses.
- **Full-stack mode (opt-in)** — entry point is a user/client action; the workflow is traced across the client/server boundary. Produces a single source-of-truth doc for an end-to-end flow.

**Full-stack mode activates ONLY when `$ARGUMENTS` explicitly signals it**, via one of:

- Phrases: `"full workflow"`, `"end-to-end"`, `"e2e"`, `"fullstack"`, `"full-stack"`, `"from the client"`, `"from the user"`
- A client-side entry point (screen name, user action, device event): `"the Place Order button"`, `"order submission from the mobile app"`

Otherwise, default to backend mode. If it's ambiguous, ask before switching modes.

In full-stack mode, ask the user to name the **client** (e.g. "web app", "iOS app", "POS device", "partner integration") so the doc is anchored. The skill stays tech-agnostic — do not assume a framework, language, or platform on either side.

## Process

- Create todo list for all steps
- Launch 1-3 specialized agents to follow the instructions described in the [Instructions] section
- Consolidate their findings identifying where they converge and where they diverge
- Calculate confidence score based on their results
- If too much divergence, do another round - we need **AT LEAST 95% of confidence** to proceed
- Once confident enough, consolidate their findings in a document with the structure from the [Output Format]

## Instructions

### 1. Locate the entry point

Find the workflow trigger point in the codebase.

**Backend mode:**

- REST controller action
- GRPC service method
- Message/event handler (Service Bus, RabbitMQ, etc.)
- Scheduled job/cron handler

**Full-stack mode:** the entry point is always a **client action**, not a handler. Identify:

- The client (web app, mobile app, device, CLI, partner integration — whatever initiates the action)
- The client-side location of the trigger (screen, view, route, command — in whatever terms the codebase uses)
- The user/system action that fires it (tap, submit, scan, message received, etc.)

The backend handler becomes a downstream step, not the root of the flow.

If $ARGUMENTS is ambiguous, list candidates and ask for clarification before proceeding.

### 2. Trace the execution path

Follow the happy path (all validations pass, all conditions match) through:

- Request handlers / use cases
- Domain services
- External clients (HTTP, GRPC, SDK calls)
- Repository/data access
- Message publishing

**Monorepo cross-service tracing:** When you hit an external boundary (HTTP call, GRPC call, message published), check if the target service exists in this repository. If it does, continue tracing into that service and document the full cross-service flow. Mark the service boundary clearly in the sequence diagram.

**Full-stack mode — trace upward too:** start from the client action and trace _into_ the client code (whatever it is) until you reach the call that crosses the network. Treat the client/server boundary the same way you treat monorepo service boundaries — mark it with `── [<client-name>] ──` / `── [<service-name>] ──` in the sequence tree. Continue into the backend handler and downward as in backend mode.

Stop tracing only when you hit true external boundaries (services outside this repo, third-party APIs, databases).

### 3. Identify branching logic

Note where the flow diverges:

- Validation failures (what gets short-circuited)
- Conditional dependencies (when is X called vs skipped)
- Error handling that changes the flow

**Full-stack mode — also cover client-side divergence and failure modes:**

- Client-side validation that short-circuits before any network call
- Network failures mid-flow (timeout, connection drop, offline)
- Duplicate submission (double-tap, retry, back-and-forward)
- Auth/session expiry during the flow
- Stale local state vs. server state

### 4. Flag complex business logic

While tracing, flag any logic that requires deeper explanation:

- Calculations (pricing, scoring, aggregations)
- Query builders with conditional filters/joins
- State machines or status transitions
- Multi-step validations with interdependencies
- Algorithms (sorting, matching, prioritization)
- Domain-specific rules that aren't self-evident from the code

For each flagged section, note the location and a brief description of why it's complex.

### 5. Catalog the data inventory

Identify all data that flows through or is touched by this workflow:

- **Request/Response contracts** — input DTOs, query parameters, response shapes, GRPC message types
- **Database tables and fields** — which tables are read from, written to, or joined; note the specific columns that matter for the workflow logic
- **Events/Messages** — published or consumed message schemas (Service Bus, RabbitMQ, etc.)
- **External API contracts** — request/response shapes for outbound HTTP/GRPC calls

For each item, note whether it's read, written, or both.

**Full-stack mode — also catalog:**

- **Client state** — data the client holds locally before, during, and after the call (form inputs, selected items, cached entities, in-flight flags). Describe _what_ it holds, not the mechanism used to hold it.
- **Wire contract** — the exact over-the-network contract between client and server: endpoint/method (or equivalent for non-HTTP clients), auth requirements, idempotency expectations, and a mapping of response status/outcome → client-visible outcome.
- **Async push-back channels** — any channel that updates the client _after_ the initial response returns (websocket, polling, webhook, push notification, MQTT, email/SMS, etc.). List the channel, the trigger, and what the client does on receipt.

### 6. Extract business rules

Separate the **business intent** from the technical implementation. For each rule:

- State what the business expects to happen, in language a PM or domain expert would recognize and validate
- Avoid referencing code, classes, or implementation details
- Focus on rules that would matter in a requirements review — not every `if` statement

Examples of good business rules:

- "A user can only have one active subscription at a time"
- "Orders over $500 require manager approval before processing"
- "Expired cards are excluded from the default payment method selection"

### 7. Extract configuration

Find settings that affect this workflow:

- Environment variables
- App settings / configuration files
- Feature flags

### 8. Client-visible outcomes _(full-stack mode only)_

For each possible backend outcome (success, each error class, timeout, partial failure), describe what the client presents or does. Stay tech-agnostic — describe the outcome, not the rendering mechanism:

- What the user perceives (confirmation, error message, redirect, no-op, device signal, etc.)
- What the client does internally (clear state, retry, navigate, surface error, etc.)

### 9. Cross-cutting concerns _(full-stack mode only)_

Things that silently break full-stack flows and are worth capturing once:

- Auth/session lifecycle across the boundary (how the session is established, carried, refreshed, and what happens when it expires mid-flow)
- Feature flags that gate client behavior, backend behavior, or both
- Analytics/tracking events fired during the flow
- Any other concern that spans both sides (rate limits, i18n, a11y touchpoints)

## Output Format

**Backend mode:** create the documentation in `/workflows/<service-name>/<workflow-name>.md`.

**Full-stack mode:** create the documentation in `/workflows/_fullstack/<workflow-name>.md`, since no single service owns the flow. Link back from the per-service docs if they exist.

```markdown
# <Workflow Name>

## Summary

|                  |                                                   |
| ---------------- | ------------------------------------------------- |
| Created          | YYYY-MM-DD                                        |
| Last Updated     | YYYY-MM-DD                                        |
| Generated From   | `<short-sha>` (commit at gen/update time)         |
| Schema           | v1                                                |
| Mode             | Backend / Full-stack                              |
| Trigger          | GRPC / REST / Service Bus / Cron / Client action  |
| Client           | _(full-stack only)_ web app / mobile / device / … |
| Entry Point      | `Namespace.Class.Method` or client location       |
| Success Response | Empty / DTO / Event published                     |
| Cross-Service    | Yes/No — list services if applicable              |
| Business Rules   | Yes/No — see dedicated section if applicable      |
| Complex Logic    | Yes/No — see dedicated section if applicable      |

## Sequence of Calls

<WorkflowTrigger>
├── HandlerOrService.Method
│   ├── DependencyA.Operation
│   └── DependencyB.Operation
│       └── NestedDependency.Call
│
├── ── [Orders.Api] ── ── ── ── ── ── ──
│   │
│   └── OrdersServiceV1.GetOrder
│       └── OrderRepository.Find

Use `── [ServiceName] ──` to mark service boundaries in monorepos. In full-stack mode, the root node is a client action (e.g. `User taps "Place Order"`) and `── [<client-name>] ──` / `── [<service-name>] ──` markers delimit the client/server boundary.

## Flow Description

1. **[Entry point]** — What initiates this and what input it receives
2. **[Step name]** — What happens, key validations
   - _If [condition]_: [what happens differently]
3. **[Step name]** — Continue through the happy path
4. **[Completion]** — What gets returned/published/persisted

## Complex Logic Breakdown

> Include this section only if complex business logic was flagged during tracing.

### <Descriptive Name>

**Location:** `Namespace.Class.Method` (lines ~X-Y)

**What it does:**
Brief explanation of the logic's purpose.

**How it works:**
Step-by-step breakdown of the logic:

1. First, it checks/calculates...
2. Then, based on [condition]...
3. Finally, it returns/applies...

**Key rules:**

- Rule or condition that matters
- Another business rule
- Edge case handling

**Example scenario:**

> Optional: A concrete example that illustrates the logic
> "If a user has 3 expired cards and 1 active, the prioritization returns..."

---

Repeat for each flagged complex logic section.

## Data Inventory

### Request / Response

| Direction | Type          | Description     |
| --------- | ------------- | --------------- |
| Input     | `RequestDto`  | What it carries |
| Output    | `ResponseDto` | What it returns |

### Database

| Table          | Fields                  | Access     | Origin             |
| -------------- | ----------------------- | ---------- | ------------------ |
| `schema.table` | `field1`, `field2`, ... | Read/Write | External / Derived |

> **Origin**: _External_ = received from caller, event, or upstream service. _Derived_ = computed, transformed, or assembled within this workflow.

### Events / Messages

| Event/Message | Schema       | Direction          |
| ------------- | ------------ | ------------------ |
| `EventName`   | `MessageDto` | Published/Consumed |

### External APIs

| Service       | Operation       | Direction |
| ------------- | --------------- | --------- |
| `ServiceName` | `GET /endpoint` | Outbound  |

> Omit any subsection that doesn't apply to this workflow.

### Client State _(full-stack mode only)_

| Item     | Description   | Lifetime                 |
| -------- | ------------- | ------------------------ |
| `<item>` | What it holds | Before/during/after call |

### Wire Contract _(full-stack mode only)_

| Field       | Value                                     |
| ----------- | ----------------------------------------- |
| Endpoint    | `POST /path` (or equivalent for non-HTTP) |
| Auth        | What the client must present              |
| Idempotency | Expected or not; how it's enforced        |

**Response → client outcome mapping:**

| Response        | Client-visible outcome                        |
| --------------- | --------------------------------------------- |
| `200 / success` | What the user perceives, what the client does |
| `4xx <class>`   | …                                             |
| `5xx / timeout` | …                                             |

### Async Push-Back _(full-stack mode only)_

| Channel     | Trigger       | Client action on receipt |
| ----------- | ------------- | ------------------------ |
| `<channel>` | What fires it | What the client does     |

## Client-Visible Outcomes _(full-stack mode only)_

> One entry per possible outcome of the flow, covering success and every failure mode identified in branching analysis. Stay tech-agnostic — describe what the user/client perceives and does, not the rendering mechanism.

- **[Outcome name]** — What the user perceives + what the client does internally
- **[Outcome name]** — …

## Cross-Cutting Concerns _(full-stack mode only)_

- **Auth/session** — How the session is established, carried, refreshed, and what happens on expiry mid-flow
- **Feature flags** — Flags that gate client behavior, backend behavior, or both
- **Analytics** — Events fired during the flow
- **Other** — Rate limits, i18n, a11y, etc.

## Business Rules

> State each rule in plain language — no code references, no class names. These should be readable and validatable by a PM or domain expert.

- **[Rule name]** — What the business expects to happen
- **[Rule name]** — Another business rule
- **[Rule name]** — Include conditions and edge cases that matter from a business perspective

## Configuration

| Setting       | Purpose          |
| ------------- | ---------------- |
| `Section:Key` | What it controls |

## Dependencies

- **DependencyA** — Brief description of what it provides
- **DependencyB** — Brief description

## Source Files

> Machine-readable list of every source path traced when this doc was written. Used by staleness-detection tooling: `git log <generated-from>..HEAD -- <paths>` reveals exactly what's drifted since `Last Updated`. List one row per distinct path; use the `Role` column to label what it contributes (`Entry point`, `Handler`, `Service`, `Repository`, `External client`, `Message handler`, `Client UI`, etc.).

| Role            | Path                                              |
| --------------- | ------------------------------------------------- |
| Entry point     | `src/Foo.Api/Controllers/BarController.cs`        |
| Handler         | `src/Foo.Api/Handlers/BarHandler.cs`              |
| Service         | `src/Foo.Domain/Services/BarService.cs`           |
| Repository      | `src/Foo.Infra/Data/BarRepository.cs`             |
| External client | `src/Foo.Infra/Clients/PaymentHttpClient.cs`      |

## Change Log

| Date       | Change                     | Reason        |
| ---------- | -------------------------- | ------------- |
| YYYY-MM-DD | Initial documentation pass | First version |

> On future updates: bump `Last Updated` in the Summary table, append one row per update (group related edits into a single row), and leave `Created` alone. If the underlying workflow no longer matches the doc, that's the signal it's stale — compare `Last Updated` against the source file's most recent commit on the traced paths.
```

## Guidelines

- Prefer component names over descriptions in the sequence tree
  - ✓ `TrapHttpClient.GetCreditCards`
  - ✗ `Calls trap to get credit cards`
- Keep descriptions scannable — this will be used in refinement sessions
- Flag anything unclear with `[TODO: verify]` rather than guessing
- If the workflow is exceptionally complex (10+ decision points), suggest breaking the doc into sections or separate flows
- For complex logic sections, optimize for "could I explain this in a refinement session using just this doc?"
- On first generation, set both `Created` and `Last Updated` to today's date (YYYY-MM-DD) and add one initial Change Log row (`Initial documentation pass` / `First version`). If a doc already exists at the target path and you're updating it: keep `Created`, bump `Last Updated`, append one row to the Change Log.
- Populate `Generated From` with the short SHA of `HEAD` at the time of generation/update — run `git rev-parse --short HEAD` once at the start. Advance it on every update (it represents "the state of the codebase this doc was last verified against," not "first generation"). If the call fails or is denied (no git, no permission, detached state), set `Generated From: unknown` with a `[TODO: verify SHA]` marker rather than blocking the doc. `Schema` is the doc-template version — keep it at `v1` until this template itself materially changes shape.
- Populate `## Source Files` with every distinct path traced during the writing pass — entry point + every handler/service/repository/external client/message handler/client UI you read while building Sequence of Calls. This is the input to automated staleness detection; missing paths = silent drift later.
