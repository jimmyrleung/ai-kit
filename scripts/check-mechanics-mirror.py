#!/usr/bin/env python3
"""Read-only comparison of a copied public mechanics block; never print private text."""

import argparse
import hashlib
import re
from pathlib import Path


def normalized(text: str) -> str:
    return text.replace("\r\n", "\n").strip() + "\n"


def compare(public: str, private: str) -> tuple[str, str | None, str]:
    starts = list(re.finditer(r"<!--\s*kit-mechanics:begin\b[^>]*-->", private))
    ends = list(re.finditer(r"<!--\s*kit-mechanics:end\s*-->", private))
    expected = hashlib.sha256(normalized(public).encode()).hexdigest()
    if len(starts) != 1 or len(ends) != 1 or starts[0].end() > ends[0].start():
        return "unverified", None, expected
    actual = hashlib.sha256(normalized(private[starts[0].end():ends[0].start()]).encode()).hexdigest()
    return ("current" if actual == expected else "drift"), actual, expected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=("codex", "cursor"), required=True)
    parser.add_argument("--file", type=Path, required=True)
    args = parser.parse_args()
    public_path = Path(__file__).resolve().parents[1] / "adapters" / args.provider / "AGENTS.md"
    try:
        status, actual, expected = compare(public_path.read_text(encoding="utf-8"), args.file.expanduser().read_text(encoding="utf-8"))
    except (OSError, UnicodeError):
        print("UNVERIFIED: input cannot be read; no files changed")
        return 2
    print(f"{status.upper()}: copied={actual or 'unknown'} public={expected}; no files changed")
    return {"current": 0, "drift": 1, "unverified": 2}[status]


if __name__ == "__main__":
    raise SystemExit(main())
