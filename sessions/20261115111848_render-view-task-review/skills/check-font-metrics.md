---
name: check-font-metrics
description: "Reads a .woff2 or .ttf font with fonttools to answer layout questions with numbers: which characters a subset has, the width of one ch, how many characters fit in a CSS measure. Use when a design sets a measure in ch, ships a font subset, or writes non-ASCII characters (arrows, marks) that may fall back to another font. Choosing fonts belongs to ui-process."
---

# check-font-metrics (draft)

Goal: replace guesses such as "66ch is about 66 characters" or "the subset has the arrows" with measured
values from the font file the page ships.

## Steps

1. Write the script below to the session scratch folder (not the repository).
2. Run it with uv, isolated: `uv run --no-project --with fonttools --with brotli python -I <script> <font files>`.
   `brotli` is needed for `.woff2`.
3. Change `sample` to a real paragraph of the page and `chars` to the characters the page writes (grep the
   build script and assets for non-ASCII: `grep -oP "[^\x00-\x7F]" <file> | sort | uniq -c`).
4. Report: the `ch` width in px at the body size, the measure in px, characters per line for the sample, and
   each missing character with its code point.

```python
import sys
from fontTools.ttLib import TTFont

sys.stdout.reconfigure(encoding="utf-8")
size, measure_ch = 16, 66
sample = "Replace this with a real paragraph from the page, with its usual mix of words and numbers."
chars = "↳←→✕⇠−–—·§…✓✗"
for path in sys.argv[1:]:
    font = TTFont(path)
    upm = font["head"].unitsPerEm
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    zero = hmtx[cmap[ord("0")]][0]
    avg = sum(hmtx[cmap[ord(c)]][0] for c in sample if ord(c) in cmap) / len(sample)
    print(path, "| 1ch =", round(size * zero / upm, 2), "px |", measure_ch, "ch =",
          round(measure_ch * size * zero / upm), "px | chars per line =", round(measure_ch * zero / avg))
    missing = [c for c in chars if ord(c) not in cmap]
    print("  missing:", " ".join(f"{c} U+{ord(c):04X}" for c in missing) or "none")
```

## Notes

- `ch` is the advance width of "0" in the element's font. In fonts with wide figures (Geist: 0.663em) a
  `ch`-based measure holds far more than that number of characters: `66ch` in Geist at 16px is 700px, about
  95 characters.
- On Windows, printing non-ASCII without `sys.stdout.reconfigure(encoding="utf-8")` fails with a cp1252
  `UnicodeEncodeError`.
- A missing character that works as an icon should become an inline SVG; a missing text character falls back
  to the next font in the stack and only needs listing.
