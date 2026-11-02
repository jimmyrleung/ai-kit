---
name: check-portability-locally
description: "Runs the ai-kit portability validation step on the working tree or a commit before pushing, and reads the real errors when a CI run failed. Use after adding, renaming or removing a skill, or when the Portability workflow failed and its logs are not readable. Fixing the reported docs belongs to the change's owner."
---

# check-portability-locally (draft)

Goal: get the same errors as the "Validate live skill format and links" CI step, without CI logs.

## Steps

1. Extract the step's Python from `.github/workflows/portability.yml` into a scratch file (the block under
   `run: |` of that step, with the 10-space indent removed).
2. For the working tree: run it from the repo root with the uv Python
   (`C:\Users\jimmy\AppData\Roaming\uv\python\cpython-3.12-windows-x86_64-none\python.exe -I <script>`).
3. For a commit: `git archive <sha> | tar -x -C <scratch-dir>`, then run it inside that folder. `tar` errors for the
   `archive/v1` symlinks are harmless.
4. Report the `ERROR:` lines; a pass prints `Validated N live skills and local Markdown links.`

## Notes

- `gh` is not installed; the GitHub API via `curl` gives run and step status for this public repo, not logs.
