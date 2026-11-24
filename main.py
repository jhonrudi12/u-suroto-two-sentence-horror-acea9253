#!/usr/bin/env python3
"""Two-Sentence Horror — make.fun entry (u-suroto-two-sentence-horror-acea9253).

Writes the entry story to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).
Python 3 standard library only, deterministic, no network access.

The story is exactly two sentences and under 400 characters, so it passes
the sealed gate (UTF-8 text, 1-400 characters, not only white space).
"""

import os
import re
import sys

STORY = (
    "Before we moved in, the previous tenants taped a list of house rules "
    "inside the cupboard, and the first one said never to answer the door "
    "after midnight. Tonight someone knocked three times, and when I went "
    "to check the list, a new rule had been added in my handwriting: let "
    "them in."
)

MAX_CHARS = 400


def count_sentences(text):
    """Count sentences by splitting on sentence-terminating punctuation."""
    parts = [p for p in re.split(r"[.!?]+", text) if p.strip()]
    return len(parts)


def validate(text):
    """Return a list of validation errors (empty means valid)."""
    errors = []
    if not text.strip():
        errors.append("story is empty or only white space")
    if len(text) > MAX_CHARS:
        errors.append("story is %d characters, over the 400 limit" % len(text))
    n = count_sentences(text)
    if n != 2:
        errors.append("story has %d sentences, expected exactly 2" % n)
    return errors


def main():
    errors = validate(STORY)
    if errors:
        for error in errors:
            print("error: %s" % error, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the gate counts characters, and the file is the
    # story exactly as written.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(STORY)
    # Read the file back and verify it round-trips exactly: a grader that
    # reads entry.txt must see the same validated story, byte for byte.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != STORY:
        print("error: entry.txt does not match the validated story",
              file=sys.stderr)
        return 1
    if validate(written):
        print("error: written entry failed re-validation", file=sys.stderr)
        return 1
    print("wrote %s (%d characters, %d sentences)"
          % (path, len(STORY), count_sentences(STORY)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
