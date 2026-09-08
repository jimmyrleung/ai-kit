# Cursor trust-state retry — B17.AC3

**Unavailable before model execution.** The retry preserves the user's trust-state update: the fallback startup's prompt named the newly added scratch root, not the ai-kit repository. This is a startup boundary, not a failed model workflow. Claude remains pending at owner direction; no Claude command was run.

| Startup | Actual command scope | Observed result |
| --- | --- | --- |
| 1 | Original scratch workspace plus fresh added output root; read-only overlay of scratch-scoped permissions. | Exit 1 after 0.711 s. Trust required for `/tmp/astra-backlog-5VdqNm/existing-provider-stores-20260907/cursor/workspace`. |
| 2 | `<user-home>/ai-kit` workspace plus fresh added output root. | Exit 1 after 0.732 s. Trust required specifically for `/tmp/astra-backlog-5VdqNm/cursor-trust-retry-20260907/workspace`. |

Both commands used native `--sandbox enabled`, `--workspace` and `--add-dir` with an outer `bwrap --ro-bind / /` boundary. Only `/tmp/astra-backlog-5VdqNm/cursor-trust-retry-20260907` was host-writable. No trust/force/yolo flag, private policy write, source edit, credential inspection/copy, commit or hidden approval was used. The original permission file is byte-identical; startup 1's permission overlay changed only the process's read-only view. The bounded fallback ran only because startup 1 was a pre-model trust rejection. Each startup had a 180-second maximum; there were zero actual model trials and no further troubleshooting.

Exact inputs and artifacts: `stdin.txt`, `inputs.json`, `procedure-manifest.json`, `workspace/store-profile.json`, `workspace/preflight-evidence.json`, `scoped-cli.json`, and `run.py`. Each `startup-1/` and `startup-2/` directory contains the exact argv, process handle, stdout/stderr and timing/exit receipt. Current help/version were captured as `help.txt` and `version.txt` (Cursor Agent 2026.09.02-c22c1a3). Native model identity and measured usage/cost are unavailable; no zero-cost estimate is inferred. Requested worker gpt-6-astra/high is separate from the unobserved native model.

`verification.json` records 5/5 unchanged public procedure/source-copy identities, the unchanged seeded legacy record, unchanged original permissions, and the complete scratch store inventory. No new observation or result.json exists. Positive recording/tag validation therefore remains unavailable. The actual outer-recorder negative preflight returned exit 2/ENOENT for the intentionally absent enabled record; it stayed absent, and no completion receipt exists. That read-only preflight does not count as Cursor executing the workflow. Earlier native attempts and their results remain intact in `/tmp/astra-backlog-5VdqNm/existing-provider-stores-20260907`.

Remaining concrete boundary: the added fresh scratch root shown above was still reported untrusted by this CLI invocation. The second prompt does not prove ai-kit itself remained untrusted. No private trust-state files were inspected to explain the difference. B17.AC3 remains partial alongside the prior successful Codex scratch recording and pending Claude coverage.

Confidence: **95%** for this bounded report (documentation 29/30, patterns 24/25, dependencies 19/20, complexity 14/15, impact 9/10). Remaining 5%: the exact scope of the external trust update and model/workflow behavior after the added root is trusted are unverified.
