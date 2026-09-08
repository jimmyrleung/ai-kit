# Entry-point detector recipes

Read the sections for every detector activated by Phase 2 of docs-tasks-creator. Recipes are scoped to the current workspace; the parent skill owns exclusions, capture fields, and task emission.

#### Next.js App Router

Enumerate both `app/**/route.{ts,js}` and `src/app/**/route.{ts,js}`. For each match,
inspect exports for the supported HTTP verbs `GET`, `POST`, `PUT`, `PATCH`, `DELETE`,
`HEAD`, and `OPTIONS`. Cover function declarations with or without `async` and exported
function-valued constants (`export const GET = …`). One entry point per exported verb per
file. Derive the URL from the path after `app/`; omit route-group segments such as `(admin)`
and keep dynamic segments (`[id]`). A re-export, computed export, or non-literal path is a
`Partial` boundary rather than an invented handler.

#### Next.js Pages API

Enumerate `pages/api/**/*.{ts,tsx,js,jsx}` and `src/pages/api/**/*.{ts,tsx,js,jsx}`. For
each match, inspect the default export (declaration, identifier, or expression) as one
handler. Derive the URL with its `/api/` prefix, omit the file extension and a trailing
`index`, and preserve dynamic segments. Do not exclude `_`-prefixed files in Pages API:
`pages/api/_health.ts` with a default handler maps to `/api/_health`. Follow the workspace's
configured `pageExtensions` when present; unresolved configuration is a coverage gap.
A computed/re-exported default whose target cannot be found statically is a `Partial`
boundary. These rules follow the [Next API Routes contract](https://nextjs.org/docs/pages/building-your-application/routing/api-routes).

#### Next.js Server Actions

Search under `app/` and `src/app/` for a directive-prologue string `'use server'` or
`"use server"` (allow comments before a file-level directive). For file-level directives,
capture exported async function declarations and exported async function-valued constants.
For function-level directives, capture only the containing async function. Re-exports,
aliases whose declaration cannot be resolved, and directives outside these forms are a
`Partial` boundary. **Discovery is fuzzy** — flag each detected action with
`[TODO: verify entry point]` in the task acceptance criteria.

#### Express

Search for these patterns (case-sensitive, `\.` is a literal dot):
- `\bapp\.(get|post|put|delete|patch|all)\(`
- `\brouter\.(get|post|put|delete|patch|all)\(`
- Any variable name suffixed `Router` or `router` with the same verbs.

For each match, capture: HTTP verb, URL path (first string arg), handler reference (named function arg, or `Reference:` = the route registration site for inline handlers).

Also inspect literal router mounts such as `app.use('/api', usersRouter)` and trace the
mounted router declaration/import. Compose the mount prefix with each router route. Nested
literal mounts may be composed transitively. Dynamic prefixes, array/regex paths, factory
returns, or a mount target that cannot be resolved are recorded as a `Partial` boundary;
do not emit a guessed public URL.

#### Fastify

Search for `\bfastify\.(get|post|put|delete|patch|head|options|all|route)\(` and the same
on an `app`/instance parameter or variable bound to Fastify. Cover shorthand calls and
`route({ method: <literal-or-literal-array>, url|path: <literal>, handler })`. Inspect
`register(plugin, { prefix: '<literal>' })` and compose nested literal plugin prefixes with
the route URL. Dynamic plugin references/prefixes or route option objects that cannot be
resolved statically are a `Partial` boundary.

#### NestJS

Search for `@Controller(` — each match is a controller class. For each, walk methods in
that class file and find `@Get(`, `@Post(`, `@Put(`, `@Delete(`, `@Patch(`, `@All(`,
`@Options(`, `@Head(` decorators. Compose literal paths as global prefix from
`app.setGlobalPrefix(...)` + controller prefix + method path. Also detect message/event
consumers: `@MessagePattern(` and `@EventPattern(`. One entry point per decorated method.
Dynamic decorator arguments, versioning/host constraints, or conditional global prefixes
that cannot be resolved are a `Partial` boundary.

#### ASP.NET Core (attribute)

Search for `\[Http(Get|Post|Put|Delete|Patch|Head|Options)\b`. Each match is on a method in a controller class. Use `[Route(` attributes on the class and the method to derive the URL path. `Reference:` is `<file>:<ClassName>.<MethodName>`.

#### ASP.NET minimal API

Search for `\.Map(Get|Post|Put|Delete|Patch)\(`. Each match is an entry point. URL path is the first string arg.

Also resolve literal route groups: `var group = app.MapGroup("/prefix")` followed by
`group.MapGet("/path", ...)`, including statically traceable chained/nested `MapGroup`
calls. Compose all literal group prefixes. Dynamic patterns, extension methods that register
routes, or group variables whose assignment cannot be resolved are a `Partial` boundary.

#### GRPC .NET

Enumerate `**/*.proto`. For each `service X { rpc Y(...) returns (...) }`, also find the C# implementation: a class inheriting from `<X>.<X>Base`. One entry point per RPC method. `Reference:` is the C# implementation: `<file>:<ClassName>.<MethodName>`. If the C# implementation is missing, emit the task anyway and flag `[TODO: verify — proto declares the RPC but no C# implementation was found in the scanned root]`.

#### .NET background workers

Search for `:\s*BackgroundService\b` and `:\s*IHostedService\b` (with the class declaration on the same line). For each class, the entry point is its `ExecuteAsync` (BackgroundService) or `StartAsync` (IHostedService) method. Trigger description: "Background worker" — also note any obvious interval or cadence (e.g. `Task.Delay(TimeSpan.FromSeconds(...))` constants).

#### Azure Functions (.NET isolated / in-process)

Search separately for `[Function(` (isolated: `[Function("name")]` /
`[Function(nameof(X))]`) and `[FunctionName(` (in-process). For each decorated method the
**trigger type** comes from its trigger-decorated parameter:
- `[HttpTrigger(...)]` → REST (verb + route from the attribute args).
- `[ServiceBusTrigger("queue"/"topic", ...)]` → message handler (queue/topic name).
- `[TimerTrigger("cron")]` → scheduled job (note the cron).
- `[BlobTrigger(...)]` / `[QueueTrigger(...)]` / `[EventHubTrigger(...)]` → event handler.
- Durable: `[OrchestrationTrigger]` (orchestrator) / `[ActivityTrigger]` (activity) — **not** standalone entry points; see Phase 5 granularity.

`Reference:` is `<file>:<ClassName>.<MethodName>`. `trigger` is the human-readable form
(`Message handler: order.created (ServiceBus)`, `Timer: 0 */5 * * * *`,
`REST POST /api/x`). Attributes supplied through aliases, generated metadata, or trigger
arguments that cannot be resolved to literals are a `Partial` boundary.

#### Coverage boundary common to every detector

After scanning, enumerate the activated detector's exact roots and patterns in the Scan
coverage table. Static recipes do not prove the absence of runtime/plugin/generated routes.
When the scan sees a likely registration form outside the recipe, include its `file:line` and
state `Partial` or `Unsupported`; never report an empty scan as a complete handler inventory.
