# Skill draft — subset and embed an open-license font

Draft from the 2026-11-15 session. For the owner to review; not a live skill.

**Use when:** a self-contained HTML page must carry its own fonts with no network request.

## Steps

1. **Pick fonts without a reserved font name** under the SIL Open Font License, or plan to rename the
   subset. Check the first lines of the font's `OFL.txt`.
2. **List the characters the page needs.** The standard Google `latin` subset has no → ← ↳ ✓ ≤ ≥ ≠ and no
   box-drawing characters, so a custom list is needed: Latin, Latin-1, general punctuation, the arrows and
   math signs in use, and box drawing (U+2500–257F) for the monospace font only.
3. **Ask before downloading.** Say the files, the source and the size. Then download the TTF files from the
   official repository into a folder that holds nothing else.
4. **Narrow the axes** with `fontTools.varLib.instancer`: weight 400–700, optical size pinned. Keeping the
   optical-size axis costs about three times the size.
5. **Save and reload the instanced font** before subsetting; the subsetter fails on it otherwise.
6. **Subset** with `fontTools.subset`: the character list, features `kern liga calt ccmp locl mark mkmk tnum
   zero case lnum pnum`, flavour `woff2`, no hinting.
7. **Report what is missing** from each subset, so the page does not rely on a missing character.
8. **Embed** as base64 in an `@font-face` rule, and keep the `.woff2` files and the licence texts beside it.

## Notes

- Run with `uv run --no-project --with fonttools --with brotli python -I <script>`; keep the script in a
  different folder from the downloads.
- Geist and Geist Mono came to 34 KB together (46 KB as base64).
- Icons such as check marks are safer as inline SVG than as font characters.
