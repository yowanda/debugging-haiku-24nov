#!/usr/bin/env python3
"""Write one haiku about debugging to $MAKEFUN_OUTPUT_DIR/entry.txt.

Deterministic, no network, writes only inside the output directory.
"""

import os
import re

HAIKU = (
    # 5-7-5 syllables; 78 characters including newlines, plain text.
    "Cursor blinks past three\n"
    "the log swears the code is fine\n"
    "and the bug was mine\n"
)

EXPECTED_SYLLABLES = (5, 7, 5)
MAX_CHARS = 200

_VOWELS = "aeiouy"


def _syllables_in_word(word: str) -> int:
    """Heuristic syllable count: vowel groups, minus a trailing silent 'e'."""
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = len(re.findall(r"[aeiouy]+", w))
    # Silent trailing 'e' (e.g. code, fine, mine) does not add a syllable.
    if w.endswith("e") and groups > 1 and not w.endswith("le"):
        groups -= 1
    return max(groups, 1)


def _syllables_in_line(line: str) -> int:
    return sum(_syllables_in_word(word) for word in line.split())


def validate_haiku(text: str) -> None:
    """Runtime validation: non-empty, 3 lines, 5-7-5 shape, <= 200 chars."""
    if not text or not text.strip():
        raise ValueError("haiku is empty")
    if len(text) > MAX_CHARS:
        raise ValueError(f"haiku is {len(text)} chars, exceeds {MAX_CHARS}")
    lines = text.rstrip("\n").split("\n")
    if len(lines) != 3:
        raise ValueError(f"haiku must have 3 lines, got {len(lines)}")
    for i, (line, expected) in enumerate(zip(lines, EXPECTED_SYLLABLES), start=1):
        if not line.strip():
            raise ValueError(f"line {i} is empty")
        got = _syllables_in_line(line)
        if got != expected:
            raise ValueError(
                f"line {i} has {got} syllables, expected {expected}: {line!r}"
            )


def main() -> None:
    validate_haiku(HAIKU)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Deterministic byte write: exact bytes, no timestamps or randomness.
    with open(path, "wb") as f:
        f.write(HAIKU.encode("utf-8"))


if __name__ == "__main__":
    main()
