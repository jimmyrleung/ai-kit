# Techspec - [meaningful name]

## Summary

[2-3 sentences explaining the technical solution, including main architectural decisions, implementation strategy, blast radius, and any other important fact that should be known ahead of time]

## Approach

[Write the chosen approach and why it won here; what's reused, what's net-new, what is explicitly _not_ being built. A reader sees the YAGNI decisions up front.]

## Confidence score

[Write the confidence score breakdown, including: factors, evidence, effective threshold, uncertainty consequences and next checks]

## Out-of-scope

[Indicate what's out of scope, why it's out of scope, and where to revisit (if applicable). If beyond two items, add it as a table.]

## Architecture

[Provide an overview of each components/element to be added, modified, or removed:

- Name/path of the component and their role
- Relationship between components
- Implementation Workflow(s)
- Data flow(s)]

## Design

### Patterns reused

[Write a table of patterns reused in the following format `| Pattern | Source | Usage here |`. where every citation is **verified, not guessed — and anchored on a stable token** (symbol name / unique literal / nearest heading), with the line number a _hint that drifts_: write `AppContext.tsx → useAuth() (≈:55)`, never a bare `:NN`. Re-locate and re-verify any inherited citation against current source before relying on it — never reuse one verbatim.]

### Interfaces

[When applicable, define the main interfaces, always respecting the repos patterns, standards, and programming language. Each one should have at most 20 lines.

```
ServiceName
  methodName(input) -> output
```

]

### Implementation map

[Create an implementation map, file-by-file, including the following.

- path + Create/Modify
- What changes and why (one sentence)
- before/after snippets for non-trivial edits with the real names (no placeholder `[NewThing]`)
- which §4 pattern each follows
- associated test-file]

### Anti-overengineering breakdown

[Document here the outcome of the anti-overengineering step]

### Data models

If applicable, document **each** entity or contract using the template below: a dedicated subsection, a field table, and a representative example in the format adopted by the project. Variants, degraded states, error envelopes, mappings, and fixed parameters should have their own blocks, as demonstrated below.

If there are JSON contracts between the backend and UI, they should be ready for display. [Complete the feature-specific context. Fields missing from the source should be normalized to `null` when that is the project convention.]

#### `[TypeName]` — [short description]

| Field     | Type     | Required | Description   |
| --------- | -------- | -------- | ------------- |
| `[field]` | `[type]` | yes/no   | [Description] |

```text
{
  "[field]": "[realistic value]"
}
```

[Repeat the pattern above for each main entity or contract: aggregated payload, input types, error types, etc.]

> **[Variant/degraded state (if applicable)]:** [Explain when it occurs and what impact it has on the payload.]

```text
{
  "[affected_section]": null
}
```

#### `[ErrorName]` — error envelope (if applicable)

| Code     | HTTP       | Meaning       |
| -------- | ---------- | ------------- |
| `[code]` | `[status]` | [Description] |

#### Mapping [external source] → contract (if applicable)

| Source ([API/source]) | Destination (contract) |
| --------------------- | ---------------------- |
| `[source_field]`      | `[destination_field]`  |

#### Fixed source parameters (if applicable)

| API            | Main parameters                    |
| -------------- | ---------------------------------- |
| **[API Name]** | `[param1=value]`, `[param2=value]` |

[If applicable, document database schemas using the same pattern: subsection, table, and example in JSON or SQL.]

### Endpoints mapping

[If the work to be done involves exposing or consuming APIs, document each endpoint according to the following model, covering all relevant scenarios: success, empty responses, validation, errors, and partial degradation. Register non-obvious behaviors in a blockquote `>`. If a given payload was already documented in the data model, just reference it instead of duplicating it.]

#### Overview

| Method           | Route        | Description         |
| ---------------- | ------------ | ------------------- |
| `[GET/POST/...]` | `[/api/...]` | [Brief description] |

---

#### `[METHOD] [/api/route]`

[Brief description of the endpoint's purpose.]

**Query parameters** (or **request body** for POST/PUT/PATCH)

| Parameter | Type     | Default                | Rules                  |
| --------- | -------- | ---------------------- | ---------------------- |
| `[param]` | `[type]` | `[default value or —]` | [Validation and rules] |

**Responses**

| Status  | Body             | When                         |
| ------- | ---------------- | ---------------------------- |
| `[200]` | `[ResponseType]` | [Success condition]          |
| `[400]` | `[ErrorType]`    | [Validation error condition] |
| `[502]` | `[ErrorType]`    | [Upstream failure condition] |

**Example — success**

```http
[METHOD] /api/route?param=value
```

```text
{
  "[field]": "[realistic value]"
}
```

**Example — [alternative scenario, e.g., no matches]**

```http
[METHOD] /api/route?param=value
```

```text
{
  "[body]": []
}
```

> [Note about frontend/client behavior, if applicable.]

**Example — [error scenario]**

```http
[METHOD] /api/route
```

```text
{
  "error": {
    "code": "[code]",
    "message": "[message]"
  }
}
```

[Repeat the pattern above for each endpoint, separating them with `---`.]

## Sequence

[Describe the implementation sequence for each component/functionality.

- For each item, include **why** they should be done in that given order position
- Map dependencies
- Prefer doing the implementation first and tests later. If the implementation involve multiple repos, prefer implementation + tests for repo 1, then implementation + tests for repo 2, [...] as they will probably go in separate PRs]

## Integration points [external]

[When applicable, document external integration points, including:

- External APIs or services and their availability
- Authentication, Authorization, or any other Infrastructure requirements
- Error handling strategy]

## Test plan

According to the QA-scenario pass, document the testing approach for this functionality.

- Conventions: prefix unit tests with `UT-`, integration test with `IT-`, and e2e tests with `E2E-`
- Each test scenario should have an associated acceptance criteria
- Also register as `not applicable` any layer that doesn't make sense for the solution

### Unit Tests (if applicable)

| ID    | Test Case Name   | Acceptance Criteria | Expected Result   |
| ----- | ---------------- | ------------------- | ----------------- |
| UT-01 | [test case name] | [AC-01]             | [expected result] |

[Describe the unit testing strategy:

- Main components to be tested
- Use mocks only for external services
- Critical test scenarios]

### Integration Tests (if applicable)

| ID    | Test Case Name   | Acceptance Criteria | Expected Result   |
| ----- | ---------------- | ------------------- | ----------------- |
| IT-01 | [test case name] | [AC-01]             | [expected result] |

[If necessary, describe:

- Components to be tested together
- Test data requirements]

### E2E Tests (if applicable)

| ID     | Test Case Name   | Acceptance Criteria | Expected Result   |
| ------ | ---------------- | ------------------- | ----------------- |
| E2E-01 | [test case name] | [AC-01]             | [expected result] |

[If necessary, describe how to test the UI together with the involved services using the browser tool available in the environment.]

## Monitoring and observability

[If applicable, describe the monitoring approach using the existing infrastructure:

- Metrics or health checks to be exposed
- Main events to register and their respective level]

## Technical Considerations

### Key Decisions

[Document the key technical decisions:

- Chosen approach and rationale
- Trade-offs considered
- Alternatives that were rejected and why]

### Known Risks

[List the technical risks:

- Potential challenges
- Mitigation approaches
- Areas requiring further research]

### Compliance with AGENTS.md and Rules

[Confirm that `AGENTS.md` and all rules under `.agents/rules/` have been reviewed. Document any constraints and decisions relevant to this specification.]

### Compliance with Skills

[List only the project skills (`.agents/skills`) that are applicable to this specification.]

### Relevant and Dependent Files

[List all relevant and dependent files.]
