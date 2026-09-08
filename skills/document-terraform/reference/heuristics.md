# document-terraform — Resolution heuristics & worked examples

Progressive-disclosure reference for `SKILL.md`. The SKILL body owns the methodology; this file owns the gnarly detail and the worked examples. **The worked examples use a single synthetic landing-zone repo (an anonymized 3-layer Spacelift/Azure estate) purely to illustrate the heuristics — the skill must NOT be coupled to any layout.** A Terragrunt / TFC / flat-single-root repo exercises the same heuristics with different surface shapes.

---

## Name resolution

Goal: for each resource, emit **both** the raw name template and a best-effort resolved value, each with a confidence score. Never present a guess as a fact; never invent a value you couldn't derive.

### Evaluation scopes and order (per environment)

Terraform has two different input boundaries. Never merge them into one precedence list.

1. **Root-module variables.** Identify the actual execution root. Resolve values in
   Terraform's documented precedence, highest first: observed CLI `-var`/`-var-file` or HCP
   Terraform values; lexically ordered `*.auto.tfvars(.json)`; `terraform.tfvars.json`;
   `terraform.tfvars`; `TF_VAR_*`; then the root variable default. Include an upper tier only
   when its invocation/orchestration evidence was inspected. An arbitrary environment-named
   `.tfvars` file is not active unless execution configuration or a `-var-file` reference
   selects it.
2. **Child-module variables.** Evaluate the `module` block's argument in the **parent's**
   resolved scope, then bind that result to the child's input variable. Use the child's default
   only when the call omits the argument. Root tfvars never assign child inputs directly.
3. **Locals and outputs.** Evaluate them in the module where declared, using that module's
   resolved variables, and pass outputs back to the parent before evaluating dependent calls.
   Repeat at each wrapper/module hop.

A segment you cannot resolve at any tier (orchestrator-injected at runtime, sensitive, computed from an unavailable module) is rendered verbatim as `<var.NAME>` / `<unresolved>` in the resolved value, and the confidence drops accordingly. **Do not** substitute a plausible-looking value.

### Confidence bands for a resolved name

- **90–100%** — every segment resolved from an evidenced root input or explicit parent→child
  argument/default plus provider-doc-confirmed naming rules.
- **70–89%** — resolved, but ≥ 1 segment came from a `default` that an env _could_ override, or a provider name-mangling rule (truncation, lowercasing, no-hyphens) you applied from docs but couldn't observe applied.
- **< 70%** — ≥ 1 segment is `<unresolved>`; show the template and the partial value, list exactly which segment is unknown and why.

### Provider name-mangling

Many provider resources mutate the requested name (lowercase, strip hyphens, length cap, append a generated suffix). Confirm the rule from provider docs (context7 → websearch) and apply it to the resolved value; note in the row that the mangling was doc-derived, not observed. Example: an Azure Container Registry name `acme${env}${region}containers1cg` is already lowercased/hyphen-free _by design_ because the author knew the ACR rule — surface that.

### `count` / `for_each` expansion

When multiplicity resolves, one logical block produces N rows. Otherwise retain the block with unknown multiplicity and list the missing input. Record the expansion factor and index basis:

- `count = length(var.regions)` with `regions = ["centralus","eastus2"]` → emit `[0] centralus`, `[1] eastus2` as separate resolved rows.
- `for_each = var.kv_entries` → one row per key; the **key** is in scope for naming (`each.key`), the **value** is a secret (see _Secrets_).

---

## Secrets

Hard rule: record **key names + value-source class only. Never resolve, read, or print a value.**

For secret-bearing constructs (secret-store entries, `*_secret` resources, secret maps fed via `for_each`):

| Capture                                                                 | Don't capture               |
| ----------------------------------------------------------------------- | --------------------------- |
| Secret key name (`ExternalAcmeApi--Key`)                                | The secret value            |
| Value-source class: `from var` / `from resource output` / `hardcoded ⚠` | The resolved variable value |
| The store it lands in (resolved name + confidence)                      | —                           |

`hardcoded ⚠` is itself a finding worth surfacing (a literal secret in HCL is a smell). `from resource output` (e.g. a connection string assembled from another module's output) is documented as a _dependency_, not a value.

Worked: `kv_entries = merge(var.kv_entries, { "AzureServiceBus--FullyQualifiedDomainName" = "${module.service_bus[count.index].name}.servicebus.windows.net" })` → list key `AzureServiceBus--FullyQualifiedDomainName`, class `from resource output` (depends on `module.service_bus`), plus "+ N keys from `var.kv_entries` (orchestrator-injected, values out of scope)". Never attempt the values.

---

## Producer relationships

Replaces the naive "every `data` source = external". A `data` source frequently points at a resource **another root in the same repo creates**, or at one inside a **private module not yet loaded** — neither is "external".

### Build the producer index

Across all roots and every source-resolved module, index each resource by provider source/type,
resolved provider configuration, account/subscription/project, region, and
resolved-or-templated name. Retain producing root + module + `file:line` as provenance. A
structural template or type+name match with unknown/different provider context is a candidate
only; do not merge it or classify it cross-stack until the context also matches. Once context
matches, compare producing and consuming roots to distinguish same-root from cross-root.

### Classify each consumer

For every `data` source / hardcoded external ID / cross-resource reference, resolve its lookup key and pick exactly one:

1. **Internal same-root** — matching producer in the consuming root or its child modules. Record the local edge.
2. **Internal cross-stack** — producer found in _another root_ (or a shared module another root owns). Output a dependency edge `consuming-root ← producing-root/module`. This is the most commonly _mis_-classified case — check the index before ever writing "external".
3. **Out-of-band / external** — no producer anywhere, even after following the chain across roots. Raise confidence with corroborating signals (below).
4. **Indeterminate** — a producer plausibly lives inside an unresolved private/remote module. **Not external.** Flag, and trigger Phase 3 (ask the user to add the module). Re-classify once available.

### Corroborating signals (raise/lower confidence on "external")

- **Explicit ownership comment** adjacent to the `data` block — e.g. `# created by cloud engineering team`. Strongest single signal; quote it as evidence.
- **Naming-convention divergence** — the looked-up name uses a prefix/scheme this repo's resources never produce (a different env-abbreviation, a platform prefix).
- **Different RG / subscription / account / project** than anything this repo creates.
- **Chain termination** — follow the producer chain across roots; if even the "closest" root _also_ reads it via `data`, it's external at the platform level (see worked example 3).

### Worked examples (illustrative — do not couple)

**1 — Cross-stack (mis-classified by the naive rule).** `terraform/modules/scaffold/main.tf:119`: `data "azuread_group" "image_pull"` with `display_name = "${acr}-image-pull"`. Producer index hit: `shared/modules/container_registry/main.tf:24` _creates_ a group with display name `"${module.container_registry.name}-image-pull"`. → **cross-stack**, edge `terraform ← shared/container_registry`, confidence 95%. The naive rule would have wrongly called this external.

**2 — Cross-stack via identity.** `terraform/.../scaffold/main.tf:128`: `data "azurerm_user_assigned_identity" "ado"` (`ADO-${principal}-LZ`). Producer: `shared/modules/ado_connections/main.tf:30` creates `name = "ADO-${principal_name_underscored}-LZ"`. → **cross-stack**, confidence 95%.

**3 — Genuinely out-of-band.** `terraform/.../scaffold/main.tf:107`: `data "azurerm_subnet" "cae"` on VNet `acme-${vnet_prefix}-…-1-vnet`. No producer in `terraform/`. Follow the chain: the `shared` root (`shared/modules/scaffold/main.tf:88`) _also_ reads that VNet via `data` — the chain terminates with no producer in any root. Corroborated by `terraform/.../scaffold/main.tf:84` comment `# acme resource groups - created by cloud engineering team`. → **external / out-of-band**, confidence 88% (chain-terminated + ownership comment; not 100% because a platform-team repo we can't see could still be Terraform-managed elsewhere).

**4 — Indeterminate.** A `data "X"` whose only plausible producer is inside `<host>/<ns>/networking/azurerm` (private module, not in workspace). → **indeterminate**, confidence n/a; emit "producer likely in private module `networking` — add it to confirm (Phase 3)". Never label external.

---

## Module source-shape classification (convention-agnostic)

Classify by the `source` string's shape; resolution differs per class. **Never** hardcode a client's `registry-name → local-path` convention — ask.

| Shape            | Example                                                  | Resolution |
| ---------------- | -------------------------------------------------------- | ---------- |
| Local            | `../key_vault`, `./modules/x`                            | Trace directly. Record it as a local provenance leaf with content identity, even though it has no remote version. |
| Public registry  | `terraform-aws-modules/vpc/aws`                          | Registry/provider docs establish semantics only. Inspect the pinned body before inventorying its resources. |
| Private registry | `<host>/<ns>/<name>/<provider>`                          | Request readable pinned source; propose a location but never assume the naming map. |
| Git              | `git::https://…//modules/vpc?ref=v1`                    | Separate repository/package, `//modules/vpc` subdirectory, and `ref`; inspect that subdirectory's body at the resolved revision. |
| Archive / other  | `https://…/mod.zip`                                      | Request readable unpacked pinned source; otherwise unresolved. |

Record two identities rather than calling every module a repository:

- **Package/repository identity:** normalized remote package or local source repository,
  plus resolved revision/content digest. Several module subdirectories may share it.
- **Module identity:** package identity + package subdirectory + version/ref. Multiple
  wrappers and modules can live in one repository; report distinct repositories, module
  sources, and source@version pairs as separate counts.

Statuses are `source-resolved` (pinned body bytes inspected), `semantics-only` (official
registry/provider prose inspected, body still unavailable), or `unresolved-pending-user`.
Only `source-resolved` supports resource inventory/producers. `semantics-only` supports a
generic provider/module role and leaves resources indeterminate. A local leaf is
`source-resolved` with no invented remote/version.

---

## Module provenance & architectural-role rendering

Schema-v4 ships the provenance tree, evidence-grounded role rendering, and the
Integration & permissioning matrix. The matrix separates declared, deployed, and effective
evidence; it does not turn an HCL observation into a live verdict.

### A. The module-provenance chain + tree

**Per resource — the chain.** Walking the tree (Phase 1) you already cross every hop `caller → module "x" → source`. Tag each hop by the source-shape table above:

| Tag | Actual declaring body |
| --- | --- |
| `[entry]` | The Terraform execution root itself. |
| `[wrap]` | A local module that calls one or more child modules; it may compose several remote or local modules. |
| `[local]` | A local leaf with no child modules. |
| `[priv]` | A pinned remote/registry/Git/archive module body that was inspected. |

The origin tag identifies the body that actually declares the resource or data block. It does
not depend on the block being a lookup. Keep the exact module address/call path; `orchestrator`
is a descriptive role, not an override that turns a child body's origin into `[entry]`.
A root directly calling a remote module therefore has root `[entry]` → remote `[priv]`.

**Render rule (protects the resolved-name tables — do not bloat them):**

- **Full chain once**, in the provenance tree (and, _if_ the layout uses per-module sub-sections, also on the section heading: `### module.key_vault[0] — [wrap]→[wrap] local ../key_vault → [priv] key-vault/azurerm@4.2.0`). The single-table layout — common — carries the full chain in the tree **only**.
- **Per resource row:** only the one-token tag (`[priv]`/`[wrap]`/`[local]`/`[entry]`) in an `Origin` column. Never repeat the whole chain per row.
- **Once per (root,env) doc:** the **provenance tree** near the top — the call skeleton, the wrapper→private hop on its **own indented line**, `count`/`for_each` multiplicity annotated as `(×N)` or `(count=expr=N)` — **never** `module.x[N]`-as-count: square brackets in the tree mean a Terraform **index** only (matching the resource table), so a multi-instance module is `module.networking.cae_subnet (×2)`, not `…[2]` — and inert (`count=0`) modules marked:

```
environments/dev/main.tf
└─ module.main → local ../../modules/scaffold              [wrap] orchestrator: RBAC + wiring
   ├─ module.ad_app_access      → [priv] met-application-security-groups/azuread@2.0.0
   ├─ module.key_vault (×1)     → [wrap] local ../key_vault         (count=len(regions)=1; ×2 in a 2-region root)
   │                              └→ [priv] key-vault/azurerm@4.2.0
   ├─ module.container_app_web   → [wrap] local ../container_app
   │                              ├→ [priv] application-insights/azurerm@4.0.0
   │                              └→ [priv] container-app/azurerm@4.0.0
   └─ module.container_app_pollers (×1) → [wrap] local ../container_app_func   (count = enable_pollers ? len(regions) : 0 — resolve the toggle from HCL at the SHA; never assume inert)
```

An unresolved `[priv]` hop (private module not in workspace, Phase 3) is rendered `[priv?] <source>@<ver> — unresolved`; its would-be resources stay `indeterminate`, never invented into the tree.

### B. The "Role in this architecture" block

Placement is **Option A** (see Phase 1): **one consolidated block per root** when the root is a single orchestrator (one top-level `module` — `module.main`/`module.scaffold`, the common case), scoped to that top-level module with sub-module roles folded into the four parts; **one block per top-level module** only when a root's entrypoint calls several _independent_ top-level modules; **never one-per-sub-module** (fragments the story, bloats the doc). Fixed four-part shape, every clause carrying a `file:line` or a Phase-2 edge ID — **omit a part rather than guess it**:

> **Role in <estate>** — _Provides:_ <what this component is here>. _Consumed by / Consumes:_ <the exact cross-stack edge / output / `data` source, with `file:line`>. _Blast radius:_ <what cannot function if absent>. _Posture:_ <env-specific stance — PII lockdown / prod tier / region count, with `file:line`>.

The hard fence (this is the failure mode to police — it's the one place this skill flirts with the "redesign/opinion" line its litmus test forbids):

| Allowed (it's evidence)                                                                                 | Banned (it's opinion / recall)                            |
| ------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| "Consumed by `module.container_app_web` — Terraform writes the `AzureAd--*` secrets (`container_app/main.tf:64`)" — a producer-index/Phase-2 edge | "central to the security architecture" — no edge          |
| "web app cannot start without it" — follows from a **verified** runtime grant (the matrix row, with its effectiveness verdict) — never from an access policy on an RBAC vault | "follows landing-zone best practice" — recommendation     |
| "`default_action=Deny`, Tier-1 PII (`scaffold:147`)" — quoted HCL                                       | "should probably also have a private endpoint" — redesign |

If a component has no consumer edge in the producer index, say so explicitly ("_Consumed by:_ no in-repo consumer found — terminal/told-to-exist") rather than inventing a purpose. The block **renders Phase-2 output**; it never sources a new dependency.

### Worked example (illustrative — do not couple)

`module.key_vault[0]` in `terraform/dev`. Chain: `environments/dev/main.tf` → `module.main` `[wrap]` (`../../modules/scaffold`) → `module.key_vault` `[wrap]` (`../key_vault`) → `[priv] key-vault/azurerm@4.2.0` → `azurerm_key_vault.vault`. `azuread_group.admin_group` in the same module is tagged `[wrap]` (the local `../key_vault` body creates it; it is _not_ in the upstream `key-vault/azurerm`), making "what did the wrapper add" answerable at a glance. Role block: `terraform/dev` is a single-orchestrator root (`module.main`), so KV does **not** get its own block — its role folds into the **consolidated `module.main`** block as evidence lines: _Provides_ …KV `acme-d-cus-secrets-1-kv`…; _Consumed by_ Terraform-written `AzureAd--*` secrets (`container_app/main.tf:NN`) — the web app's runtime **read** grant is **not asserted here**, it is a row in the Integration & permissioning matrix with its own effectiveness verdict; _Blast radius_ web app cannot start without KV/CAE/ACR; _Posture_ `Deny`+RBAC+purge-protection, Tier-1 PII (`scaffold/main.tf:147-149`). Every token traces to HCL or a Phase-2 edge — zero generic commentary, and no permission claimed without the Rule-9 effectiveness check.

---

## Identity & permissioning (declared ≠ effective)

SKILL **Rule 9**. The deliverable is a mandated per-(root,env) **Integration & permissioning (incident-triage) matrix**: every cross-component link and identity→resource grant, as a row, so that on an infra incident the reader's first question — _"is a link broken / is there a permission gap?"_ — is answered without re-deriving it from prose.

### Matrix columns

`Link / grant · Mechanism · Identity · Target · Exact role/perm · Declared · Deployment · Effective · Evidence`

- **Declared:** `present` (binding exists and matches the target's declared auth mode),
  `ineffective` (a binding exists but inspected configuration proves its mechanism cannot
  apply), `missing` (bounded source inspection found no applicable binding), or
  `indeterminate` (unresolved source/context could contain it).
- **Deployment:** `applied` (state/live evidence), `planned` (a user-supplied saved plan or
  orchestration run proves intent but not apply), or `unknown`.
- **Effective:** `verified` (live evidence confirms the intended identity can use the target),
  `proven failure` (an observed runtime/live denial or failed use), or `unknown`.
- **Deploy-time identity and runtime identity are separate rows.** The principal Terraform authenticates as (writes secrets, creates RGs) is not the app's runtime MI. A green deploy row says nothing about runtime access.
- Surface proven failures first in overview/on-ramp, then incident-relevant unknowns with the
  exact probe/evidence needed. Missing credentials or an unrun probe is `unknown`, not red.

### The effectiveness check (why "declared" is not "effective")

A binding resource in HCL establishes only declared state. Before `Declared: present`, check:

1. **Auth-mode match.** The binding's mechanism must be the one the target honours. Canonical trap: `azurerm_key_vault_access_policy` is **silently inert** on a vault created with `enable_rbac_authorization = true` — Azure ignores access policies in RBAC mode; the operative grant must be an `azurerm_role_assignment` (e.g. `Key Vault Secrets User`). The reverse holds for a non-RBAC vault. (Storage/SQL/etc. have analogous mode splits — verify from provider docs, don't assume.)
2. **Principal actually plumbed.** A module that *can* grant access only does so for principals it is *given*. Trace the producing module's variable: a key-vault module whose RBAC readonly assignment is `for_each = toset(concat(var.read_only, var.default_read_only))` grants **nothing to the app** unless the calling wrapper passes the app principal into `read_only` (and `default_read_only` defaults are often an unrelated platform SP, not the app). Read the wrapper's argument list — absence of the argument is the finding.
3. **Right principal.** System-assigned vs user-assigned MI, the app SP vs the deploy SP. The access policy/role must target the identity the workload actually runs as.

If a declared binding is statically incompatible with the target's configured auth mode, use
`ineffective`; if bounded inspection proves no applicable binding, use `missing`; if the check
is unresolved, use `indeterminate`. Deployment/Effective stay unknown until state/live evidence
says more. Never upgrade from a wiring-shaped input, access-policy block, or worker summary.

### Worked example (illustrative — do not couple)

A web Container App must read secrets from `acme-d-cus-secrets-1-kv` at runtime.

- The container-app private module emits `azurerm_key_vault_access_policy.readonly` (Get/List secrets) for the app's system-assigned MI, gated `var.key_vault.grant_read_permissions` (which the wrapper sets true). **Declared.**
- The vault wrapper sets `enable_rbac_authorization = true` (`modules/key_vault/main.tf:NN`). → the access policy is **inert** (check 1 fails). The vault module *does* have an RBAC path (`azurerm_role_assignment … "Key Vault Secrets User"`, `for_each = toset(concat(var.read_only, var.default_read_only))`), but the wrapper passes **no** `read_only`, and `default_read_only` defaults to an unrelated ADO SP (check 2 fails). No role assignment targets the app MI in any root.
- Matrix row from HCL alone: `Web app → KV read | intended access policy | web CA MI |
  ... | Get/List | ineffective (policy is inert in RBAC mode; no role assignment found) | unknown |
  unknown | hcl: container-app/main.tf:NN; key_vault/main.tf:NN`. If a live access check then
  returns denial, update Effective to `proven failure`; if an out-of-band role is observed and
  access succeeds, set Deployment `applied` and Effective `verified` with live evidence.
- Resolution: missing Terraform may be a real defect or an out-of-band grant may exist. Ask
  which evidence source can close it; do not make unknown green or failed by assumption.

---

## Whole-estate fact ledger

Some facts are **estate-wide** — they hold across roots/envs and flip _real_ behaviour, so the overview and every per-(root,env) doc must state them **identically**. SKILL rule 8 mandates the ledger; this is the how + the canonical failure.

**What goes in the ledger** (resolve each once from bytes identified in Source Evidence):

- A behavioural `variable` default that gates a whole subtree — an `enable_*`/`create_*` toggle whose default decides whether N resources exist at all.
- The backend / state model, per root.
- Each root's environment axis + per-env region count (the topology rule already forbids _assuming_ parity; the ledger additionally forbids _stating it differently in two docs_).
- Each private/remote module's resolution status (`resolved@tag` / `unresolved-pending` / `tag-absent`) — **and** any "is this materially moot?" claim that _depends_ on a toggle: those two ledger facts must agree (a module is only "moot because `count=0`" if the gating toggle actually resolves off).

**Canonical failure (illustrative — do not couple).** Between two runs a root's dirty
`variables.tf` flips a feature default while HEAD stays unchanged, or a resolved sibling module
changes at its own revision. A per-env pass reads new bytes while overview reuses the old value.
The same displayed root SHA then carries contradictory truths. Root cause: one root SHA was used
as identity instead of the per-source byte manifests.

**The rule.** The overview is a roll-up. Build the ledger from per-(root,env) source reads,
bind every fact to Source ID/path/hash, and compare all rendered values. On divergence re-read
those exact bytes; never resolve by recency or majority. An unresolved contradiction is a STOP.

---

## Backend / state model

Classify per root:

- Explicit `backend "s3|azurerm|gcs|…"` → document the backend resource (bucket/container/key), and whether _it_ is created in-repo or is itself external/cross-stack.
- No backend block → **default local backend**. Override this only when inspected execution
  configuration for that exact root proves Terragrunt/HCP Terraform/Spacelift/another system
  supplies the state model. Cite the stack/workspace/root mapping; an orchestrator elsewhere in
  the repository is not enough.

---

## Common idiosyncrasies to handle (not exhaustive)

State-reconstruction `import` blocks / `imports.tf`; multi-region via `count` + splat (`module.x[*].id`); provider aliasing (`providers = { azurerm.alt = azurerm }`); an orchestration root that provisions the pipelines running the workload roots; hardcoded tenant/subscription/account IDs replicated across providers (flag as config smell + an external-infra anchor); `depends_on` between modules (a dependency edge worth documenting). None of these are special-cased in the SKILL body — they fall out of "read it, resolve it, index it, score it".
