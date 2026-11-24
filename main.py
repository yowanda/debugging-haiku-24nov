#!/usr/bin/env python3
"""Write one haiku about debugging to $MAKEFUN_OUTPUT_DIR/entry.txt.

Deterministic, no network, writes only inside the output directory.
"""

import os

HAIKU = (
    # 5-7-5 syllables; 78 characters including newlines, plain text.
    "Cursor blinks past three\n"
    "the log swears the code is fine\n"
    "and the bug was mine\n"
)


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(HAIKU)


if __name__ == "__main__":
    main()
