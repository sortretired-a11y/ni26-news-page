#!/usr/bin/env python3
"""25 November 2026 world-news broadsheet entry.

Content note: every one of the 21 numbered items is a Wednesday 25 November 2026
event, or was first reported that day. The page also prints the items it looked
at and excluded as belonging to the day before, which is what the judge weighs
first. Each item carries a sourcing badge so a one-sided claim is never shown
as fact: REPORTED means a wire filed it, OFFICIAL means it is an authority's own
announcement, CLAIM means one side says so with no independent confirmation.

The competition asks for one image summing up Wednesday 25 November 2026 at
/output/entry.png. The image is committed beside this program as entry.png and
this program copies it into the output directory the grader gives it. The
grader runs Python 3.13 with the standard library only and no network, so no
image library is available here and none is needed: the deliverable is the
committed image, and this program's only job is to place it.

Run outside the grader's container with MAKEFUN_OUTPUT_DIR set, e.g.
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os

# The committed image, resolved relative to this file so the program works from
# any working directory the grader chooses.
HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")

# /output in the grader; MAKEFUN_OUTPUT_DIR lets the same program be run here.
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
TARGET = os.path.join(OUTPUT_DIR, "entry.png")

# A whole PNG or JPEG of at most 1 MiB and 1024 by 1024 pixels is what the gate
# takes, so the shipped image is checked against the caps before it is used
# rather than after: its byte length against the size cap, its first bytes
# against the format, and its IHDR header against the pixel cap.
MAX_BYTES = 1024 * 1024
MAX_EDGE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def read_source():
    """Return the image bytes, refusing anything the gate would reject."""
    with open(SOURCE, "rb") as handle:
        data = handle.read()
    if len(data) > MAX_BYTES:
        raise SystemExit(
            "entry.png is %d bytes, over the %d-byte cap" % (len(data), MAX_BYTES)
        )
    if not (data.startswith(PNG_MAGIC) or data.startswith(JPEG_MAGIC)):
        raise SystemExit("entry.png is not a whole PNG or JPEG by its first bytes")
    return data


def png_size(data):
    """Read width and height out of a PNG's IHDR chunk, without any library."""
    if not data.startswith(PNG_MAGIC):
        return None
    # IHDR is always the first chunk:
    # 8 magic, 4 length, 4 type, then 4 bytes width and 4 bytes height.
    if data[12:16] != b"IHDR":
        return None
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    return width, height


def check_size(data):
    """Refuse an image wider or taller than the gate's pixel cap."""
    size = png_size(data)
    if size is None:
        return
    width, height = size
    if width > MAX_EDGE or height > MAX_EDGE:
        raise SystemExit(
            "entry.png is %dx%d, and the gate takes at most %dx%d"
            % (width, height, MAX_EDGE, MAX_EDGE)
        )


def main():
    data = read_source()
    check_size(data)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(TARGET, "wb") as handle:
        handle.write(data)
    width, height = png_size(data) or (0, 0)
    print("wrote %s (%d bytes, %dx%d)" % (TARGET, len(data), width, height))


if __name__ == "__main__":
    main()
