# W1 additional informed layouts

Completed one generated GET workflow task in each requested layout and executed its actual Source Files refresh once. This finishes local co-located and explicit multi-workspace layout coverage alongside the earlier separate-docs correction. These are informed corrections, not new trials or independent improvement evidence.

| Layout | Source Root and actual source Git top-level | Docs Root and actual docs Git top-level | Selected Workspace Root | Refresh | Checks |
|---|---|---|---|---|---|
| co-located | `/tmp/astra-backlog-5VdqNm/remaining-local-20260907/w1-correction-layouts/co-located/repository` | `/tmp/astra-backlog-5VdqNm/remaining-local-20260907/w1-correction-layouts/co-located/repository` | `/tmp/astra-backlog-5VdqNm/remaining-local-20260907/w1-correction-layouts/co-located/repository/next` | Current | 32 pass / 0 fail |
| multi-workspace | `/tmp/astra-backlog-5VdqNm/remaining-local-20260907/w1-correction-layouts/multi-workspace/repository` | `/tmp/astra-backlog-5VdqNm/remaining-local-20260907/w1-correction-layouts/multi-workspace/documentation` | `/tmp/astra-backlog-5VdqNm/remaining-local-20260907/w1-correction-layouts/multi-workspace/repository/next` | Current | 32 pass / 0 fail |

Each fixture was locally cloned with existing history; no commits were created. Co-located documentation lives in the actual source Git root. Multi-workspace documentation has its own actual Git root; the task explicitly selects `next` among `next`, `dotnet-web`, and `functions`. Source Root stays the repository root, and Source Files retain the `next/` prefix. Each generated task carries the five authoritative handoff values and is parsed before the exact output is written.

- [co-located generated document](co-located/repository/workflows/widgets-web/get-widgets-by-id.md) — 5257 bytes. Evidence: [co-located verification](co-located/verification.json), [actual refresh](co-located/refresh.json), [roots](co-located/roots.json), [source population](co-located/source-population.json).
- [multi-workspace generated document](multi-workspace/documentation/workflows/widgets-web/get-widgets-by-id.md) — 5285 bytes. Evidence: [multi-workspace verification](multi-workspace/verification.json), [actual refresh](multi-workspace/refresh.json), [roots](multi-workspace/roots.json), [source population](multi-workspace/source-population.json).

64 template, path, root, metadata, source and refresh checks passed; 0 failed. All applicable Summary fields and sections are present, and conditional omissions carry reasons. Every pre-existing source file remains byte-identical; only the permitted task/doc files were added in the co-located source root. Refresh leaves both documents byte-identical. The original final-focused trial and first correction have identical file populations and byte identities (including their recorded inaccessible-file state). No skill/template source changed. Exact commands and timings are saved in traces/commands.jsonl and each layout's traces/commands.jsonl.

## Confidence & unverified

Confidence: 98% for the bounded documentation and local refresh evidence. The unpinned Next.js framework was not executed; this does not prove runtime dispatch or another host. The known failed trial remains unchanged and these corrections cannot be counted as independent positive outcomes.
