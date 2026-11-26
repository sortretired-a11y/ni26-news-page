# news-image-20261126 — one page, Thursday 26 November 2026

One image summing up Thursday 26 November 2026: 34 numbered stories across seven
regions, 13 drawn scenes, a world map with a pin per item, and a DATE CHECK box
naming the stories that looked like today but were not.

`main.py` copies the committed `entry.png` into the grader's output directory.
It uses the Python 3.13 standard library only, needs no network, and validates
the image against the gate's caps before writing: 1 MiB and 1024 px.

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
    # -> out/entry.png, byte-identical to entry.png

## Content rule

Every one of the 34 items is a 26 November 2026 event or was first reported that
day somewhere in the world. Items that only look like today — Shenzhou-24's
docking, the Canberra-Honiara treaty, the Cartagena siege, the Cairo tanker fire,
Poundland's collapse, the Chen Jining inquiry, the Dhaka garment wage — are named
in the DATE CHECK box as deliberately excluded instead of being counted.

## Source

`build/` holds the renderer that produced `entry.png` (`render.py` for layout,
`content.py` for the stories) so the page can be reproduced or corrected.
