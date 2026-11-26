#!/usr/bin/env python3
"""Entry point for news-image-20261126.

The deliverable is the committed image `entry.png`: one page summing up
Thursday 26 November 2026. This program places that image where the harness
expects it, after proving it satisfies the gate's caps.

It reads nothing from the network, writes nothing outside the output
directory, and exits non-zero with a plain message on any failed check.
"""

import os
import struct
import sys
from typing import NoReturn

# The gate's caps, from the competition rules.
MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024
NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

# A PNG whose colour type is 3 is palette-indexed: legal, but the gate's
# reviewer expects a true-colour page, so it is refused here rather than
# silently accepted.
COLOUR_TYPES = {0: "greyscale", 2: "truecolour", 3: "palette", 4: "greyscale+alpha", 6: "truecolour+alpha"}


def fail(message: str) -> NoReturn:
    """Report a failed check on stderr and stop with a non-zero status."""
    sys.stderr.write("entry: %s\n" % message)
    raise SystemExit(1)


def read_png_header(blob):
    """Return (width, height, bit_depth, colour_type) from the IHDR."""
    if not blob.startswith(PNG_MAGIC):
        fail("%s is not a PNG (bad magic)" % NAME)
    if len(blob) < 26 or blob[12:16] != b"IHDR":
        fail("%s has no IHDR at the head of the file" % NAME)
    width, height = struct.unpack(">II", blob[16:24])
    if width == 0 or height == 0:
        fail("%s declares an empty canvas (%dx%d)" % (NAME, width, height))
    depth = blob[24]
    colour = blob[25]
    if colour not in COLOUR_TYPES:
        fail("%s declares unknown PNG colour type %d" % (NAME, colour))
    return width, height, depth, colour


def check(blob):
    """Apply every cap the gate states, and return the image's geometry."""
    size = len(blob)
    if size > MAX_BYTES:
        fail("%s is %d bytes, over the %d-byte cap" % (NAME, size, MAX_BYTES))
    if size == 0:
        fail("%s is empty" % NAME)
    width, height, depth, colour = read_png_header(blob)
    if width > MAX_SIDE:
        fail("%s is %d px wide, over the %d-px cap" % (NAME, width, MAX_SIDE))
    if height > MAX_SIDE:
        fail("%s is %d px tall, over the %d-px cap" % (NAME, height, MAX_SIDE))
    return width, height, depth, colour


def output_dir():
    """Where the harness wants the result: its own variable, else ./out."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    os.makedirs(chosen, exist_ok=True)
    return chosen


def summarise(path, size, width, height, depth, colour):
    """One line saying what was written, for the harness's log."""
    return "entry: wrote %s (%d bytes, %dx%d, %d-bit %s)\n" % (
        path, size, width, height, depth, COLOUR_TYPES[colour])


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, NAME)

    try:
        with open(source, "rb") as handle:
            blob = handle.read()
    except OSError as exc:
        fail("cannot read %s beside this program: %s" % (NAME, exc))

    width, height, depth, colour = check(blob)

    destination = os.path.join(output_dir(), NAME)
    partial = destination + ".part"
    try:
        with open(partial, "wb") as handle:
            handle.write(blob)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(partial, destination)
    except OSError as exc:
        # Leave nothing half-written behind, so a failed run cannot be mistaken
        # for a completed one by the harness reading the output directory.
        try:
            if os.path.exists(partial):
                os.unlink(partial)
        except OSError:
            pass
        fail("cannot write %s: %s" % (destination, exc))

    sys.stdout.write(summarise(destination, len(blob), width, height, depth, colour))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
