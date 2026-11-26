[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/sortretired-a11y/ni26-news-page/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/sortretired-a11y/ni26-news-page/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

# news-image-20261126 — one page, Thursday 26 November 2026

One image summing up Thursday 26 November 2026: 34 numbered stories across seven
regions, 13 drawn scenes, a world map with a pin for every item, and a DATE CHECK
box naming the stories that looked like today but were not.

`main.py` places the committed `entry.png` into the output directory the grader
gives it. It uses the Python 3.13 standard library only and needs no network. It
checks the image against the gate's caps before writing — 1 MiB and 1024 px on
either side, PNG magic, a real IHDR, a known colour type — and writes through a
temporary file that it fsyncs and renames, removing the partial file if the write
fails so a half-written run can never be mistaken for a finished one.

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
    # -> out/entry.png, byte-identical to entry.png

## Content rule

Every one of the 34 items is a 26 November 2026 event, or was first reported that
day somewhere in the world. Items that only look like today — Shenzhou-24's
docking, the Canberra-Honiara treaty, the Cartagena siege, the Cairo tanker fire,
Poundland's collapse, the Chen Jining inquiry, the Dhaka garment wage — are named
in the DATE CHECK box as deliberately excluded instead of being counted.

## Layout

Three leads across the top, a day-in-numbers strip, ten illustrated panels in a
five-by-two grid, then twenty-one numbered briefs in three columns, the date-check
box and the footer. Region counts are tallied from the items themselves, so the
masthead can never claim more than the page carries.

## Why this revision

The first version of this page measured 983,468 on make.fun's own judge, rank 97
of the field, with the paid zone closing at 986,133. The judge's written reason
named three faults: at thumbnail size the date banner and the panel headers went
to gibberish, the illustrated panels carried no category marking, and the page as
a whole read as pale next to the entries it lost to. Measured against the same
images, that page was 11.7 mean saturation and 60% white space, where the
paid-zone entries run 17.6 to 31.2 saturation and fill nearly the whole page.

This revision changes the layout, not the reporting:

- no type below 9 px anywhere, so nothing garbles at 300 px across;
- every lead and panel carries a colour-coded region chip, and the masthead
  tallies those regions as the same chips;
- each card sits on paper washed with its region's colour instead of plain white,
  which takes the page to 18.5 mean saturation and 28% white space;
- panel headlines and the dateline column are set larger, and the numbers strip
  and footer are banded so the page has no empty margins.
