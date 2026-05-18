---
description: Document a Terraform codebase — shipped-infrastructure overview, per-environment resolved-resource inventory, and a confidence-scored map of what is likely handled outside Terraform.
argument-hint: <repo_path> [output_dir] [spec_file]
arguments: repo_path output_dir spec_file
---

# Document Terraform Command

This command is a thin shim: the `document-terraform` skill owns the methodology and output contract.

1. Create a todo list with the steps for this command.
2. Use the `document-terraform` skill with:
   - `$repo_path` as the Terraform repo root (read-only),
   - `$output_dir` for the docs (default `${repo_path}/terraform-docs/`),
   - `$spec_file` (optional) as the infra description.

   The skill handles topology discovery (no flat/symmetric-env assumption), the per-(root, environment) resolved-resource inventory, the producer-index 3-state external-vs-cross-stack map, convention-agnostic private-module resolution (asking you to add sources where needed), consolidation (launching 1–3 `Explore` sub-agents for breadth where useful), the ≥ 95% confidence gate, and writing `overview.md` + the per-(root, env) docs with the staleness-tracking audit header.

When the skill hands back, this command is complete.
