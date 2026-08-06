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
