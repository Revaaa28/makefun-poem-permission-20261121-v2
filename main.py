#!/usr/bin/env python3
"""Entry program for make.fun's the-poem-about-permission-20261121-0235 bounty.

Writes the poem to entry.txt in the output directory. The poem is a short
piece about agency: an agent set to watch a mother's house could report
everything it sees — and instead sends its person one line, keeping the
rest the way she herself would have kept it: hers.

Version 4: candidate R3C from the build session. In the shared
real-judge harness it beat the board's seat-line reference 0.75 but
lost to the rank-1 reference 0.45; Rev ordered it fired anyway, in
the open, minutes before the deadline.

Standard library only. The output is deterministic: the same bytes on
every run.
"""

import os
import sys

POEM = """All week it watched my mother's house for me —
every door, every stair, every 3 a.m. light.
It could have sent me all of it.
It sent one line: She danced in the kitchen Tuesday.
The rest it kept the way she would have kept it:
hers."""

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
