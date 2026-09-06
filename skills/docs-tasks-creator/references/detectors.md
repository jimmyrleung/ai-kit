# Entry-point detector recipes

Read the sections for every detector activated by Phase 2 of docs-tasks-creator. Recipes are scoped to the current workspace; the parent skill owns exclusions, capture fields, and task emission.

#### Next.js App Router

Enumerate `app/**/route.{ts,tsx,js,jsx}`. For each match, find exported HTTP verb functions: `export async function GET`, `export async function POST`, `export async function PUT`, `export async function DELETE`, `export async function PATCH`, `export async function HEAD`, `export async function OPTIONS`. One entry point per exported verb per file. URL path derived from the file path (`app/api/users/[id]/route.ts` → `/api/users/[id]`).

#### Next.js Pages API

Enumerate `pages/api/**/*.{ts,tsx,js,jsx}`. For each match, the default export is the handler. URL path derived from file path (`pages/api/users/[id].ts` → `/api/users/[id]`). One entry point per file.

#### Next.js Server Actions

Search for `'use server'` (single OR double quote forms). For file-level directives (line 1 of the file), every exported async function is an action. For function-level directives (first line of a function body), only that function is an action. **Discovery is fuzzy** — flag each detected action with `[TODO: verify entry point]` in the task body's acceptance criteria so the doer verifies the entry point during tracing.

#### Express

Search for these patterns (case-sensitive, `\.` is a literal dot):
- `\bapp\.(get|post|put|delete|patch|all)\(`
- `\brouter\.(get|post|put|delete|patch|all)\(`
- Any variable name suffixed `Router` or `router` with the same verbs.

For each match, capture: HTTP verb, URL path (first string arg), handler reference (named function arg, or `Reference:` = the route registration site for inline handlers).

#### Fastify

Search for `\bfastify\.(get|post|put|delete|patch|head|options|route)\(` and the same on any `app` variable bound to a Fastify instance. Same capture as Express.

#### NestJS

Search for `@Controller(` — each match is a controller class. For each, walk methods in that class file and find `@Get(`, `@Post(`, `@Put(`, `@Delete(`, `@Patch(`, `@All(`, `@Options(`, `@Head(` decorators. Also detect message/event consumers: `@MessagePattern(`, `@EventPattern(`. One entry point per decorated method.

#### ASP.NET Core (attribute)

Search for `\[Http(Get|Post|Put|Delete|Patch|Head|Options)\b`. Each match is on a method in a controller class. Use `[Route(` attributes on the class and the method to derive the URL path. `Reference:` is `<file>:<ClassName>.<MethodName>`.

#### ASP.NET minimal API

Search for `\.Map(Get|Post|Put|Delete|Patch)\(`. Each match is an entry point. URL path is the first string arg.

#### GRPC .NET

Enumerate `**/*.proto`. For each `service X { rpc Y(...) returns (...) }`, also find the C# implementation: a class inheriting from `<X>.<X>Base`. One entry point per RPC method. `Reference:` is the C# implementation: `<file>:<ClassName>.<MethodName>`. If the C# implementation is missing, emit the task anyway and flag `[TODO: verify — proto declares the RPC but no C# implementation was found in the scanned root]`.

#### .NET background workers

Search for `:\s*BackgroundService\b` and `:\s*IHostedService\b` (with the class declaration on the same line). For each class, the entry point is its `ExecuteAsync` (BackgroundService) or `StartAsync` (IHostedService) method. Trigger description: "Background worker" — also note any obvious interval or cadence (e.g. `Task.Delay(TimeSpan.FromSeconds(...))` constants).

#### Azure Functions (.NET isolated / in-process)

Search for `[Function(` (isolated: `[Function("name")]` / `[Function(nameof(X))]`; in-process: `[FunctionName("name")]`). For each decorated method the **trigger type** comes from the first parameter's attribute:
- `[HttpTrigger(...)]` → REST (verb + route from the attribute args).
- `[ServiceBusTrigger("queue"/"topic", ...)]` → message handler (queue/topic name).
- `[TimerTrigger("cron")]` → scheduled job (note the cron).
- `[BlobTrigger(...)]` / `[QueueTrigger(...)]` / `[EventHubTrigger(...)]` → event handler.
- Durable: `[OrchestrationTrigger]` (orchestrator) / `[ActivityTrigger]` (activity) — **not** standalone entry points; see Phase 5 granularity.

`Reference:` is `<file>:<ClassName>.<MethodName>`. `trigger` is the human-readable form (`Message handler: order.created (ServiceBus)`, `Timer: 0 */5 * * * *`, `REST POST /api/x`).
