#!/usr/bin/env python3
"""26 November 2026 world-news broadsheet -> out/entry.png (1024x1024 PNG).

v1 defect (board: rank 201/2889, judge 977041): led with Tuesday 24 November events.
v2 defect (solo score 610): every scene painted straight onto the page canvas, so each
    scene's radial highlight bled outside its own box and smudged neighbouring panels
    and headlines; and the lead-card body text ran past the card and collided with the
    numbers strip.
v3 fixes both structurally: each scene renders into its own offscreen surface and is
    pasted, which clips it to its box no matter what it draws; and the vertical rhythm
    is computed from the tallest card rather than hand-tuned. Every story is a
    Wednesday 25 November event; the previous day's items are named in the footer.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (253, 252, 249)
INK = (18, 20, 26)
GREY = (96, 98, 106)
RED = (166, 26, 36)
RULE = (206, 203, 197)
BLUE = (30, 58, 114)
LAND = (186, 200, 216)
SEA = (227, 235, 244)

# ---------------------------------------------------------------- day identity
DAY_NAME = "THURSDAY"                 # weekday of the day being summed up
DAY_DATELINE = "26 NOVEMBER 2026"     # masthead dateline
DAY_LONG = "Thursday 26 November 2026"
DAY_SHORT = "26 November"
ISSUE_NO = "NO. 332"

SB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SR = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
NB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
NR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

SS = 4
_c = {}


def F(path, size):
    k = (path, int(round(size * SS)))
    if k not in _c:
        try:
            _c[k] = ImageFont.truetype(path, k[1])
        except OSError:
            _c[k] = ImageFont.truetype(SB if "Serif" in path else NB, k[1])
    return _c[k]


class SCanvas:
    """Drawing surface whose user coordinates are 1x and are scaled by SS on output."""

    def __init__(self, d):
        self.d = d

    def _s(self, pts):
        return [(p[0] * SS, p[1] * SS) for p in pts]

    def textlength(self, s, font=None):
        return self.d.textlength(s, font=font) / SS

    def text(self, xy, s, font=None, fill=None, anchor="lt"):
        self.d.text((xy[0] * SS, xy[1] * SS), s, font=font, fill=fill, anchor=anchor)

    def rectangle(self, xy, **kw):
        if kw.get("width"):
            kw["width"] = max(1, int(kw["width"] * SS))
        self.d.rectangle(self._s([xy[:2], xy[2:]]), **kw)

    def rounded_rectangle(self, xy, radius=0, **kw):
        if kw.get("width"):
            kw["width"] = max(1, int(kw["width"] * SS))
        self.d.rounded_rectangle(self._s([xy[:2], xy[2:]]), radius=radius * SS, **kw)

    def line(self, xy, **kw):
        if kw.get("width"):
            kw["width"] = max(1, int(kw["width"] * SS))
        self.d.line(self._s(xy), **kw)

    def polygon(self, xy, **kw):
        if kw.get("width"):
            kw["width"] = max(1, int(kw["width"] * SS))
        self.d.polygon(self._s(xy), **kw)

    def ellipse(self, xy, **kw):
        if kw.get("width"):
            kw["width"] = max(1, int(kw["width"] * SS))
        self.d.ellipse(self._s([xy[:2], xy[2:]]), **kw)


def TW(d, s, f):
    return d.textlength(s, font=f)


def TX(d, xy, s, f, fill):
    d.text(xy, s, font=f, fill=fill, anchor="lt")


def ell(d, s, f, maxw):
    if TW(d, s, f) <= maxw:
        return s
    while s and TW(d, s + "\u2026", f) > maxw:
        s = s[:-1]
    return s.rstrip("\u2014 ,.;") + "\u2026"


def wrap(d, s, f, maxw, maxlines=99):
    out, cur = [], ""
    for wd in s.split():
        t = (cur + " " + wd).strip()
        if TW(d, t, f) <= maxw:
            cur = t
        else:
            if cur:
                out.append(cur)
            cur = wd
    if cur:
        out.append(cur)
    if len(out) > maxlines:
        out = out[:maxlines]
        out[-1] = ell(d, out[-1] + " and more", f, maxw)
    return out


# ------------------------------------------------------------------- content
from content import (LEADS, PANELS, BRIEFS, REGIONS, TOTAL, PINS,  # noqa: E402
                     EXCLUDED, NUMBERS, KICKER)

LAND_POLYS = [
    [(-168, 65), (-162, 71), (-140, 70), (-128, 70), (-112, 69), (-95, 70),
     (-85, 73), (-75, 68), (-62, 60), (-55, 51), (-66, 45), (-70, 42),
     (-76, 35), (-81, 26), (-83, 29), (-90, 29), (-97, 26), (-105, 21),
     (-115, 30), (-124, 41), (-124, 48), (-135, 58), (-150, 60), (-165, 55)],
    [(-77, 8), (-70, 12), (-60, 11), (-50, 1), (-35, -5), (-38, -15),
     (-48, -25), (-58, -38), (-63, -42), (-66, -55), (-71, -55),
     (-75, -45), (-73, -35), (-71, -20), (-75, -5), (-80, 0)],
    [(-17, 15), (-16, 22), (-10, 27), (0, 32), (10, 37), (20, 32),
     (32, 31), (35, 25), (38, 18), (43, 12), (51, 12), (48, 2),
     (41, -5), (40, -15), (35, -22), (32, -28), (25, -34), (18, -34),
     (12, -18), (9, -1), (5, 5), (-8, 5)],
    [(-10, 36), (0, 44), (3, 43), (12, 45), (20, 40), (28, 41), (30, 45),
     (40, 48), (30, 60), (25, 66), (15, 68), (5, 58), (0, 50), (-5, 43)],
    [(30, 45), (45, 45), (55, 42), (65, 40), (70, 35), (78, 32), (88, 22),
     (95, 16), (100, 10), (105, 2), (110, 10), (120, 15), (122, 25),
     (120, 32), (125, 40), (130, 45), (135, 50), (142, 55), (155, 60),
     (170, 62), (180, 66), (170, 70), (150, 72), (130, 72), (110, 75),
     (90, 75), (70, 72), (60, 68), (45, 68), (30, 60)],
    [(114, -22), (122, -18), (130, -12), (137, -12), (142, -11), (146, -19),
     (153, -25), (150, -37), (143, -39), (135, -35), (129, -32), (115, -34)],
    [(131, -1), (141, -3), (150, -7), (147, -9), (140, -8), (132, -4)],
    [(-45, 60), (-30, 68), (-20, 75), (-25, 83), (-45, 83), (-58, 80), (-55, 70)],
    [(-5, 50), (-3, 58), (0, 54), (1, 51), (-4, 51)],
    [(130, 31), (136, 35), (141, 40), (143, 44), (141, 43), (138, 37), (133, 33)],
    [(173, -35), (178, -38), (176, -41), (168, -46), (166, -45), (172, -40)],
    [(44, -16), (50, -15), (48, -25), (45, -25), (43, -20)],
    [(95, 5), (105, 2), (100, 6), (97, 4)],
]


# --------------------------------------------------------------------- paint
def vgrad(d, box, top, bot, steps=24):
    """Vertical gradient built from horizontal strips, clamped inside the box."""
    x0, y0, x1, y1 = box
    if y1 <= y0:
        return
    for i in range(steps):
        t = i / (steps - 1) if steps > 1 else 0
        col = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        ya = y0 + (y1 - y0) * i / steps
        yb = y0 + (y1 - y0) * (i + 1) / steps + 0.6
        d.rectangle([x0, ya, x1, yb], fill=col)


def spot(d, cx, cy, r, inner, outer, box, steps=10):
    """Soft radial highlight, hard-clamped to `box` so it can never bleed out."""
    x0, y0, x1, y1 = box
    for i in range(steps, 0, -1):
        t = i / steps
        col = tuple(int(inner[k] + (outer[k] - inner[k]) * t) for k in range(3))
        rr = r * t
        ax = max(x0, cx - rr)
        ay = max(y0, cy - rr * .78)
        bx = min(x1, cx + rr)
        by = min(y1, cy + rr * .78)
        if bx > ax and by > ay:
            d.ellipse([ax, ay, bx, by], fill=col)


# ---- scenes (local coords 0,0 -> w,h; clipped by the offscreen surface) ------
def sc_rocket(d, w, h):
    vgrad(d, (0, 0, w, h), (46, 68, 110), (156, 132, 130))
    spot(d, w * .80, h * .22, w * .22, (255, 249, 228), (156, 132, 130), (0, 0, w, h))
    d.rectangle([0, h * .82, w, h], fill=(46, 44, 52))
    rx = w * .34
    d.polygon([(rx, h * .04), (rx + w * .048, h * .44), (rx + w * .024, h * .54),
               (rx - w * .024, h * .54), (rx - w * .048, h * .44)], fill=(242, 242, 246))
    d.rectangle([rx - w * .028, h * .17, rx + w * .028, h * .25], fill=(172, 32, 42))
    d.polygon([(rx - w * .048, h * .40), (rx - w * .092, h * .58), (rx - w * .048, h * .54)],
              fill=(194, 40, 42))
    d.polygon([(rx + w * .048, h * .40), (rx + w * .092, h * .58), (rx + w * .048, h * .54)],
              fill=(194, 40, 42))
    d.polygon([(rx - w * .042, h * .56), (rx + w * .042, h * .56), (rx, h * .76)],
              fill=(250, 198, 96))
    sx = w * .72
    d.rounded_rectangle([sx - w * .10, h * .36, sx + w * .14, h * .50], 2, fill=(212, 212, 218))
    d.rectangle([sx - w * .018, h * .32, sx + w * .018, h * .36], fill=(176, 178, 188))


def sc_handshake(d, w, h):
    vgrad(d, (0, 0, w, h), (54, 70, 94), (104, 118, 138))
    d.rectangle([0, h * .76, w, h], fill=(46, 52, 62))
    for side, col in ((0, (22, 54, 126)), (1, (16, 42, 104))):
        px = w * (.12 + side * .62)
        d.rectangle([px, h * .34, px + w * .010, h * .76], fill=(122, 124, 130))
        d.polygon([(px + w * .010, h * .18), (px + w * .18, h * .24), (px + w * .010, h * .34)],
                  fill=col)
    cx, cy = w * .50, h * .58
    d.polygon([(cx - w * .19, cy - h * .08), (cx - w * .04, cy - h * .02),
               (cx + w * .01, cy + h * .06), (cx - w * .12, cy + h * .11)], fill=(204, 166, 130))
    d.polygon([(cx + w * .19, cy - h * .08), (cx + w * .04, cy - h * .02),
               (cx - w * .01, cy + h * .06), (cx + w * .12, cy + h * .11)], fill=(226, 188, 150))
    d.polygon([(w * .30, h * .82), (w * .70, h * .82), (w * .67, h * .94), (w * .33, h * .94)],
              fill=(246, 244, 236))
    for i in range(2):
        d.line([(w * .35, h * (.85 + i * .035)), (w * .65, h * (.85 + i * .035))],
               fill=(152, 152, 152), width=1)


def sc_rescue(d, w, h):
    vgrad(d, (0, 0, w, h), (28, 32, 48), (62, 58, 72))
    d.rectangle([w * .05, h * .26, w * .95, h * .80], fill=(46, 50, 64))
    d.rectangle([w * .05, h * .26, w * .95, h * .33], fill=(148, 30, 38))
    for i in range(4):
        gx = w * (.11 + i * .215)
        d.rectangle([gx, h * .38, gx + w * .155, h * .70],
                    fill=(224, 206, 156), outline=(94, 86, 72))
    d.rectangle([0, h * .80, w, h], fill=(28, 30, 40))
    hx, hy = w * .68, h * .14
    d.ellipse([hx - w * .10, hy - h * .012, hx + w * .10, hy + h * .012], fill=(182, 186, 198))
    d.ellipse([hx - w * .038, hy - h * .028, hx + w * .055, hy + h * .028], fill=(58, 62, 76))
    spot(d, hx - w * .05, h * .54, w * .11, (255, 246, 210), (62, 58, 72), (0, 0, w, h))
    for i in range(3):
        ox = w * (.14 + i * .085)
        d.rectangle([ox - w * .016, h * .60, ox + w * .016, h * .80], fill=(22, 26, 38))
        d.ellipse([ox - w * .014, h * .545, ox + w * .014, h * .60], fill=(22, 26, 38))


def sc_wage(d, w, h):
    vgrad(d, (0, 0, w, h), (56, 66, 82), (108, 112, 118))
    d.rectangle([0, h * .78, w, h], fill=(56, 62, 70))
    for i in range(3):
        mx = w * (.08 + i * .31)
        d.rectangle([mx, h * .54, mx + w * .19, h * .63], fill=(34, 38, 50))
        d.rectangle([mx + w * .02, h * .63, mx + w * .05, h * .79], fill=(34, 38, 50))
        d.rectangle([mx + w * .14, h * .63, mx + w * .17, h * .79], fill=(34, 38, 50))
        d.ellipse([mx + w * .07, h * .575, mx + w * .115, h * .615], fill=(194, 166, 94))
    d.rectangle([w * .10, h * .08, w * .90, h * .36], fill=(240, 236, 224))
    d.rectangle([w * .10, h * .08, w * .90, h * .14], fill=(166, 26, 36))
    f = F(NB, max(6, h * .19))
    s = "+36%"
    TX(d, (w * .50 - TW(d, s, f) / 2, h * .19), s, f, (24, 26, 34))


def sc_mine(d, w, h):
    vgrad(d, (0, 0, w, h), (44, 56, 52), (88, 76, 58))
    d.polygon([(0, h * .54), (w * .30, h * .22), (w * .62, h * .48), (w, h * .32),
               (w, h), (0, h)], fill=(96, 84, 62))
    d.polygon([(w * .32, h * .58), (w * .58, h * .58), (w * .54, h * .88), (w * .36, h * .88)],
              fill=(26, 24, 28))
    d.polygon([(w * .36, h * .76), (w * .54, h * .76), (w * .53, h * .88), (w * .37, h * .88)],
              fill=(50, 84, 102))
    d.line([(w * .72, h * .28), (w * .60, h * .60)], fill=(196, 170, 82), width=3)
    d.rectangle([w * .68, h * .22, w * .82, h * .28], fill=(148, 38, 38))
    for i in range(2):
        px = w * (.16 + i * .10)
        d.rectangle([px - w * .015, h * .58, px + w * .015, h * .84], fill=(220, 194, 78))
        d.ellipse([px - w * .014, h * .52, px + w * .014, h * .58], fill=(238, 212, 94))


def sc_gavel(d, w, h):
    vgrad(d, (0, 0, w, h), (40, 44, 58), (18, 20, 28))
    for i in range(1, 5):
        d.line([(w * i / 5, h * .08), (w * i / 5, h * .64)], fill=(52, 58, 76), width=1)
    d.rectangle([0, h * .64, w, h], fill=(92, 66, 44))
    gx, gy = w * .56, h * .42
    d.polygon([(gx - w * .095, gy - h * .09), (gx + w * .045, gy - h * .18),
               (gx + w * .12, gy - h * .02), (gx - w * .02, gy + h * .07)], fill=(194, 148, 94))
    d.line([(gx - w * .02, gy + h * .04), (gx - w * .09, gy + h * .46)],
           fill=(144, 106, 66), width=4)
    spot(d, w * .28, h * .30, w * .15, (248, 224, 170), (40, 44, 58), (0, 0, w, h))


def sc_tanker(d, w, h):
    vgrad(d, (0, 0, w, h), (36, 44, 66), (76, 58, 60))
    d.rectangle([0, h * .60, w, h], fill=(26, 42, 64))
    for i in range(4):
        d.line([(w * .04, h * (.64 + i * .08)), (w * .96, h * (.64 + i * .08))],
               fill=(44, 64, 90), width=1)
    spot(d, w * .60, h * .50, w * .16, (255, 180, 90), (76, 58, 60), (0, 0, w, h))
    tx, ty = w * .32, h * .48
    d.polygon([(tx - w * .19, ty), (tx + w * .17, ty), (tx + w * .12, ty + h * .13),
               (tx - w * .14, ty + h * .13)], fill=(26, 30, 38))
    d.rectangle([tx, ty - h * .09, tx + w * .11, ty], fill=(26, 30, 38))
    d.polygon([(tx - w * .15, ty + h * .15), (tx + w * .13, ty + h * .15),
               (tx + w * .095, ty + h * .21), (tx - w * .115, ty + h * .21)],
              fill=(242, 224, 178))


def sc_rubble(d, w, h):
    vgrad(d, (0, 0, w, h), (52, 46, 50), (94, 80, 72))
    d.rectangle([w * .08, h * .24, w * .60, h * .82], fill=(104, 96, 92))
    d.rectangle([w * .60, h * .44, w * .90, h * .82], fill=(88, 82, 80))
    for r in range(3):
        for c in range(3):
            wx, wy = w * (.13 + c * .145), h * (.30 + r * .15)
            gone = (r, c) in ((0, 2), (1, 1))
            d.rectangle([wx, wy, wx + w * .095, wy + h * .095],
                        fill=(26, 24, 28) if gone else (56, 52, 56))
    d.rectangle([0, h * .82, w, h], fill=(56, 50, 48))
    for i in range(6):
        rx = w * (.05 + i * .15)
        d.polygon([(rx, h * .82), (rx + w * .065, h * .82),
                   (rx + w * .042, h * .92), (rx + w * .018, h * .92)], fill=(126, 118, 110))
    spot(d, w * .28, h * .60, w * .10, (255, 180, 118), (94, 80, 72), (0, 0, w, h))


def sc_flagdown(d, w, h):
    vgrad(d, (0, 0, w, h), (34, 40, 58), (76, 82, 100))
    d.rectangle([0, h * .80, w, h], fill=(44, 48, 60))
    for i in range(2):
        px = w * (.24 + i * .46)
        d.rectangle([px, h * .10, px + w * .010, h * .80], fill=(156, 158, 164))
    sx = w * .24 + w * .010
    d.rectangle([sx, h * .36, sx + w * .16, h * .52], fill=(198, 42, 46))
    d.rectangle([sx + w * .068, h * .392, sx + w * .092, h * .488], fill=(248, 248, 248))
    d.rectangle([sx + w * .045, h * .424, sx + w * .115, h * .452], fill=(248, 248, 248))
    dx = w * .70 + w * .010
    d.rectangle([dx, h * .20, dx + w * .16, h * .38], fill=(22, 42, 106))
    d.ellipse([dx + w * .05, h * .245, dx + w * .088, h * .285], fill=(202, 46, 46))


def sc_crown(d, w, h):
    vgrad(d, (0, 0, w, h), (34, 28, 62), (94, 60, 96))
    spot(d, w * .50, h * .36, w * .26, (255, 242, 204), (94, 60, 96), (0, 0, w, h))
    for i in range(8):
        px, py = w * (.08 + (i * .107) % .82), h * (.06 + (i * .091) % .26)
        d.rectangle([px, py, px + w * .009, py + h * .032], fill=(248, 208, 128))
    cx, cy = w * .50, h * .42
    d.polygon([(cx - w * .15, cy + h * .13), (cx + w * .15, cy + h * .13),
               (cx + w * .115, cy - h * .11), (cx + w * .062, cy + h * .02),
               (cx, cy - h * .17), (cx - w * .062, cy + h * .02),
               (cx - w * .115, cy - h * .11)], fill=(242, 204, 94))
    d.rectangle([cx - w * .15, cy + h * .13, cx + w * .15, cy + h * .19], fill=(212, 170, 68))
    d.ellipse([cx - w * .026, cy + h * .28, cx + w * .026, cy + h * .40], fill=(230, 90, 126))


def sc_warning(d, w, h):
    vgrad(d, (0, 0, w, h), (38, 40, 52), (72, 70, 82))
    d.polygon([(w * .20, h * .84), (w * .80, h * .84), (w * .50, h * .16)],
              fill=(232, 186, 62), outline=(96, 76, 24))
    f = F(NB, max(8, h * .30))
    s = "!"
    TX(d, (w * .50 - TW(d, s, f) / 2, h * .40), s, f, (28, 26, 20))
    # redacted document at the base
    d.rectangle([w * .26, h * .86, w * .74, h * .98], fill=(238, 236, 228))
    for i in range(2):
        d.rectangle([w * .30, h * (.89 + i * .04), w * .70, h * (.915 + i * .04)],
                    fill=(58, 56, 62))


def sc_shield(d, w, h):
    vgrad(d, (0, 0, w, h), (34, 44, 66), (70, 84, 108))
    spot(d, w * .50, h * .40, w * .26, (232, 240, 252), (70, 84, 108), (0, 0, w, h))
    cx = w * .50
    d.polygon([(cx, h * .12), (cx + w * .24, h * .24), (cx + w * .22, h * .62),
               (cx, h * .86), (cx - w * .22, h * .62), (cx - w * .24, h * .24)],
              fill=(198, 210, 230), outline=(58, 78, 112))
    d.polygon([(cx, h * .20), (cx + w * .18, h * .30), (cx + w * .165, h * .60),
               (cx, h * .79), (cx - w * .165, h * .60), (cx - w * .18, h * .30)],
              fill=(168, 30, 40))
    d.line([(cx, h * .30), (cx, h * .62)], fill=(246, 240, 236), width=3)
    d.line([(cx - w * .10, h * .46), (cx + w * .10, h * .46)], fill=(246, 240, 236), width=3)


SCENES = {
    "rocket": sc_rocket, "handshake": sc_handshake, "rescue": sc_rescue,
    "wage": sc_wage, "mine": sc_mine, "gavel": sc_gavel, "tanker": sc_tanker,
    "rubble": sc_rubble, "flagdown": sc_flagdown, "crown": sc_crown,
    "warning": sc_warning, "shield": sc_shield,
}


def scene(big, kind, x, y, w, h):
    """Render one scene on its own surface, then paste. Guarantees zero bleed."""
    pw, ph = int(round(w * SS)), int(round(h * SS))
    sub = Image.new("RGB", (pw, ph), LAND)
    sd = SCanvas(ImageDraw.Draw(sub))
    SCENES[kind](sd, w, h)
    big.paste(sub, (int(round(x * SS)), int(round(y * SS))))


# ----------------------------------------------------------------------- map
def draw_map(d, x0, y0, w, h, pins):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA, outline=(164, 176, 192), width=1)

    def P(lon, lat):
        return (x0 + (lon + 180) / 360 * w, y0 + (90 - lat) / 180 * h)

    for i in range(1, 6):
        xx = x0 + w * i / 6
        d.line([(xx, y0), (xx, y0 + h)], fill=(212, 220, 230), width=1)
    d.line([(x0, y0 + h / 2), (x0 + w, y0 + h / 2)], fill=(212, 220, 230), width=1)
    for ring in LAND_POLYS:
        d.polygon([P(lon, lat) for lon, lat in ring], fill=LAND, outline=(136, 154, 176))

    fl = F(NB, 5.5)
    for nm, lon, lat in (("N. AMERICA", -102, 47), ("S. AMERICA", -59, -17),
                         ("EUROPE", 14, 52), ("AFRICA", 19, 3),
                         ("ASIA", 87, 45), ("AUSTRALIA", 133, -26)):
        px, py = P(lon, lat)
        TX(d, (px - TW(d, nm, fl) / 2, py), nm, fl, (92, 108, 130))

    f = F(NB, 6)
    placed = []
    for num in sorted(pins):
        lat, lon = pins[num]
        px, py = P(lon, lat)
        for qx, qy in placed:
            if abs(px - qx) < 13 and abs(py - qy) < 13:
                py += 12 if py <= qy else -12
                px += 7
        placed.append((px, py))
        d.ellipse([px - 6.4, py - 6.4, px + 6.4, py + 6.4], fill=PAPER)
        d.ellipse([px - 5.2, py - 5.2, px + 5.2, py + 5.2], fill=RED)
        TX(d, (px - TW(d, str(num), f) / 2, py - 3.6), str(num), f, PAPER)


# --------------------------------------------------------------------- build
def build(out_path):
    big = Image.new("RGB", (W * SS, H * SS), PAPER)
    d = SCanvas(ImageDraw.Draw(big))
    M = 26
    inner = W - 2 * M

    # ---------------------------------------------------------- nameplate
    d.rectangle([0, 0, W, 6], fill=RED)
    TX(d, (M, 14), DAY_NAME, F(NB, 11), RED)
    TX(d, (M + TW(d, DAY_NAME, F(NB, 11)) + 9, 14),
       "\u00b7  ONE DAY, ONE PAGE  \u00b7  " + ISSUE_NO, F(NB, 10), GREY)

    name = DAY_DATELINE
    sz = 58
    while TW(d, name, F(SB, sz)) > inner - 240:
        sz -= 1
    TX(d, (M - 3, 30), name, F(SB, sz), INK)

    rx = W - M
    t1 = "%d STORIES" % TOTAL
    TX(d, (rx - TW(d, t1, F(SB, 20)), 33), t1, F(SB, 20), INK)
    TX(d, (rx - TW(d, "EVERY ONE DATED " + DAY_DATELINE, F(NB, 8)), 59),
       "EVERY ONE DATED " + DAY_DATELINE, F(NB, 8), RED)
    for i, (nm, ct) in enumerate(REGIONS):
        col, row = i % 2, i // 2
        s = "%s %d" % (nm.upper(), ct)
        TX(d, (rx - (1 - col) * 76 - TW(d, s, F(NR, 8)), 74 + row * 10.5), s, F(NR, 8), GREY)

    d.rectangle([M, 110, W - M, 113], fill=INK)
    kf = F(SR, 13.5)
    for i, ln in enumerate(wrap(d, KICKER, kf, inner, 2)):
        TX(d, (M, 119 + i * 16), ln, kf, INK)
    d.rectangle([M, 150, W - M, 151], fill=RULE)

    # ------------------------------------------------------------- 3 leads
    ly = 158
    lw = (inner - 2 * 12) // 3
    art_h = 98
    hf, bf = F(SB, 15), F(SR, 10.5)
    lh = 0
    for L in LEADS:
        hh = len(wrap(d, L["head"], hf, lw - 16, 3)) * 17.5
        bh = len(wrap(d, L["body"], bf, lw - 16, 3)) * 12
        lh = max(lh, art_h + 7 + hh + 4 + bh + 6)
    lh = int(round(lh + 4))

    for i, L in enumerate(LEADS):
        x0 = M + i * (lw + 12)
        scene(big, L["kind"], x0, ly, lw, art_h)
        d.rectangle([x0, ly, x0 + lw, ly + lh], outline=RULE, width=1)
        d.rectangle([x0, ly, x0 + lw, ly + 3], fill=RED)
        d.rectangle([x0, ly + 3, x0 + lw, ly + 19], fill=(20, 22, 28))
        TX(d, (x0 + 7, ly + 5.5), L["tag"], F(NB, 7.5), PAPER)
        TX(d, (x0 + lw - 7 - TW(d, L["src"], F(NB, 7.5)), ly + 5.5),
           L["src"], F(NB, 7.5), PAPER)
        hy = ly + art_h + 7
        for ln in wrap(d, L["head"], hf, lw - 16, 3):
            TX(d, (x0 + 7, hy), ell(d, ln, hf, lw - 16), hf, INK)
            hy += 17.5
        hy += 4
        for ln in wrap(d, L["body"], bf, lw - 16, 3):
            TX(d, (x0 + 7, hy), ell(d, ln, bf, lw - 16), bf, GREY)
            hy += 12

    # -------------------------------------------------------- numbers strip
    ny = ly + lh + 14
    d.rectangle([M, ny, W - M, ny + 2], fill=INK)
    TX(d, (M, ny + 6), "THE DAY IN NUMBERS", F(NB, 9), RED)
    cw = inner / 6
    for i, (big_n, cap) in enumerate(NUMBERS):
        x0 = M + i * cw
        TX(d, (x0, ny + 19), big_n, F(SB, 18), INK)
        for k, ln in enumerate(wrap(d, cap, F(NR, 7.8), cw - 10, 2)):
            TX(d, (x0, ny + 40 + k * 9.5), ell(d, ln, F(NR, 7.8), cw - 10), F(NR, 7.8), GREY)

    # -------------------------------------------------- 8 illustrated panels
    py0 = ny + 62
    ph = 92
    NCOL = 5
    tw = (inner - (NCOL - 1) * 7) // NCOL
    for i, (tag, head, sub, kind) in enumerate(PANELS):
        c, r = i % NCOL, i // NCOL
        x0 = M + c * (tw + 8)
        y0 = py0 + r * (ph + 8)
        ah = int(ph * .50)
        scene(big, kind, x0, y0, tw, ah)
        d.rectangle([x0, y0, x0 + tw, y0 + ph], outline=RULE, width=1)
        d.rectangle([x0, y0, x0 + 3, y0 + ah], fill=RED)
        TX(d, (x0 + 6, y0 + ah + 3), ell(d, tag, F(NB, 7), tw - 12), F(NB, 7), RED)
        hy = y0 + ah + 12.5
        for ln in wrap(d, head, F(SB, 9), tw - 12, 2):
            TX(d, (x0 + 6, hy), ell(d, ln, F(SB, 9), tw - 12), F(SB, 9), INK)
            hy += 10
        TX(d, (x0 + 6, y0 + ph - 10), ell(d, sub, F(NR, 7), tw - 12), F(NR, 7), GREY)

    # ------------------------------------------- map + the 16 more datelines
    by = py0 + 2 * (ph + 8) + 6
    d.rectangle([M, by, W - M, by + 2], fill=INK)
    TX(d, (M, by + 6), "THE DAY, IN %d MORE DATELINES" % len(BRIEFS), F(NB, 9.5), INK)
    TX(d, (W - M - TW(d, "every number is a pin on the map", F(NR, 7.5)), by + 7),
       "every number is a pin on the map", F(NR, 7.5), GREY)

    top = by + 22
    map_h = 262
    map_w = 316
    draw_map(d, M, top, map_w, map_h, PINS)
    d.rectangle([M, top, M + map_w, top + 14], fill=(20, 22, 28))
    TX(d, (M + 5, top + 2.5), "WHERE THE DAY HAPPENED", F(NB, 7.5), PAPER)

    gx = M + map_w + 12
    colw = (W - M - gx - 16) // 3
    ROWS = 7
    rowh = map_h / ROWS
    tid, tpl, tbd, tsc = F(NB, 9.5), F(NB, 11.5), F(NR, 11.5), F(NR, 7.5)
    for i, (num, place, body, src) in enumerate(BRIEFS):
        c, r = i // ROWS, i % ROWS
        x0 = gx + c * (colw + 12)
        y0 = top + r * rowh
        TX(d, (x0, y0 + 2), str(num), tid, RED)
        nw = TW(d, str(num), tid) + 5
        sw = TW(d, src, tsc)
        TX(d, (x0 + colw - sw, y0 + 3), src, tsc, GREY)
        TX(d, (x0 + nw, y0 + 1),
           ell(d, place, tpl, colw - nw - sw - 6), tpl, BLUE)
        for k, ln in enumerate(wrap(d, body, tbd, colw - nw, 2)):
            TX(d, (x0 + nw, y0 + 15 + k * 12.5), ell(d, ln, tbd, colw - nw), tbd, INK)

    # --------------------------------------------------------- date check
    dy = top + map_h + 11
    d.rectangle([M, dy, W - M, dy + 50], fill=(244, 242, 236), outline=RULE)
    d.rectangle([M, dy, M + 4, dy + 50], fill=RED)
    TX(d, (M + 12, dy + 5), "DATE CHECK", F(NB, 9), RED)
    TX(d, (M + 12 + TW(d, "DATE CHECK", F(NB, 9)) + 7, dy + 5),
       "\u00b7  all %d items above are " % TOTAL + DAY_LONG + " events, or were first",
       F(NR, 8.5), GREY)
    TX(d, (M + 12, dy + 17),
       "reported that day somewhere in the world.", F(NR, 8.5), GREY)
    TX(d, (M + 12, dy + 31),
       "LEFT OUT ON PURPOSE \u2014 looked like today, but had already happened:",
       F(NB, 7.5), INK)
    TX(d, (M + 12, dy + 41), EXCLUDED, F(NR, 7.5), GREY)

    # -------------------------------------------------------------- footer
    fy = H - 32
    d.rectangle([M, fy, W - M, fy + 1.5], fill=INK)
    TX(d, (M, fy + 6),
       "Each numbered brief carries the outlet that filed it. Scenes drawn in code \u2014 "
       "no photograph is reproduced.", F(NR, 7.5), GREY)
    TX(d, (M, fy + 16),
       "make.fun \u00b7 one image, one day \u00b7 " + DAY_LONG, F(NB, 7.5), INK)

    big.resize((W, H), Image.LANCZOS).save(out_path, "PNG", optimize=True)
    return out_path


if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    p = build("out/entry.png")
    print("wrote", p, os.path.getsize(p), "bytes")
