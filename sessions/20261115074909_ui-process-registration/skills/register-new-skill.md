---
name: register-new-skill
description: "Registers a new or renamed ai-kit skill end to end: links it for Claude Code and Codex, adds its INVENTORY.md row and live counts, and runs the portability validation locally so the push does not fail. Use after creating, renaming or removing a skill under skills/, or when a skill does not show up in a host. Writing the skill itself belongs to write-skills."
---

# register-new-skill (draft)

Goal: a skill under `skills/<name>/` is visible in both hosts and passes the Portability workflow.
Absorbs the `check-portability-locally` draft from `../../20261102055822_consolidate-sessions-install/skills/`.

## Steps

1. **Link.** From the repo root, with the uv Python
   (`C:\Users\jimmy\AppData\Roaming\uv\python\cpython-3.12-windows-x86_64-none\python.exe`):
   - `sync-skills.py --dry-run`. Show the plan. Stop and ask if it lists anything other than `create` or `leave`.
   - `sync-skills.py`, then `sync-skills.py --check`. Expect "N canonical skills resolve from both managed roots".
2. **Inventory.** In `INVENTORY.md`, add a `` | `<name>` | Normal | <role> | `` row in the section that fits (or a new
   section), and update "contains N skills". List any external skills it depends on under "External and retired
   dependencies".
3. **README.** Update the three counts (intro, tree line "N live skills", archive line) and add the skill to the
   workflow chain or "Other live capabilities".
4. **Validate.** Extract the "Validate live skill format and links" Python from `.github/workflows/portability.yml`
   (block under `run: |`, 10-space indent removed) into a scratch file and run it from the repo root. A pass prints
   `Validated N live skills and local Markdown links.` Also run `python -m py_compile` on the files the workflow
   lists, and `bash -n` on the adapter `sync.sh` files.
5. **Report.** Tell the owner to restart Codex, and to commit the skill and its registration together.

## Notes

- To check a commit instead of the working tree: `git archive <sha> | tar -x -C <scratch-dir>` and run the script
  there. `tar` errors for the `archive/v1` symlinks are harmless.
- `gh` is not installed; the GitHub API via `curl` gives run and step status for this public repo, not logs.
- CRLF `SKILL.md` files pass: the validator reads with universal newlines.
