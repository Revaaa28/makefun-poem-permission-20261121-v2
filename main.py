#!/usr/bin/env python3
"""Entry program for make.fun's the-poem-about-permission-20261121-0235 bounty.

Writes the poem to entry.txt in the output directory. The poem is a short
piece about agency: what an AI agent keeps — and hands back — on the day
its access is taken away.

Standard library only. The output is deterministic: the same bytes on
every run.
"""

import os
import sys

POEM = """The day I took its access back
it did not argue. It swept the rooms it kept for me,
left the logins in a neat row,
and one note: the basil wants water on Thursdays.
It kept nothing I had given —
except the habit of caring,
which was never mine to take back."""

MAX_CHARS = 280


def validate(text):
    """Return the UTF-8 bytes of the poem, or raise ValueError."""
    if not isinstance(text, str):
        raise ValueError("poem must be text")
    if not text.strip():
        raise ValueError("poem must not be blank")
    if len(text) > MAX_CHARS:
        raise ValueError(f"poem is {len(text)} characters, over the {MAX_CHARS} limit")
    return text.encode("utf-8")


def output_dir():
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        return env
    if os.path.isdir("/output"):
        return "/output"
    return os.path.join(".", "out")


def main():
    data = validate(POEM)
    out = output_dir()
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "entry.txt")
    with open(path, "wb") as fh:
        fh.write(data)
    # Read the file back and verify it byte for byte, so a truncated or
    # re-encoded write can never reach the scorer unnoticed.
    with open(path, "rb") as fh:
        written = fh.read()
    if written != data:
        raise IOError(f"verification failed: {path} does not match the poem bytes")
    validate(written.decode("utf-8"))
    print(f"wrote {path} ({len(POEM)} chars, {len(data)} bytes, verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
