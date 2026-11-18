#!/usr/bin/env python3
"""Draw "The World Today" — Wednesday 18 November 2026 — as a 1024x1024
serif broadsheet front page (PIL). Deterministic: no randomness, no network,
no timestamps. Run: python3 draw.py  ->  entry.png (next to this file)."""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (22, 22, 22)
RED = (158, 17, 17)
BLUE = (30, 58, 95)
GREY = (90, 86, 76)
LIGHT = (232, 226, 210)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, fnt, fill=INK, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def centered(draw, y, s, fnt, fill=INK, cx=512):
    draw.text((cx, y), s, font=fnt, fill=fill, anchor="ma")


def rule(draw, y, x0=28, x1=996, w=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def kicker(draw, x, y, s):
    text(draw, (x, y), s, font(SANS_B, 13), fill=RED)


def headline(draw, x, y, s, size, max_w):
    fnt = font(SERIF_B, size)
    lines = wrap(draw, s, fnt, max_w)
    for i, line in enumerate(lines):
        text(draw, (x, y + i * (size + 4)), line, fnt)
    return y + len(lines) * (size + 4)


def body(draw, x, y, s, size, max_w, leading=None):
    fnt = font(SERIF, size)
    lh = leading or (size + 5)
    lines = wrap(draw, s, fnt, max_w)
    for i, line in enumerate(lines):
        text(draw, (x, y + i * lh), line, fnt)
    return y + len(lines) * lh


# ---------------------------------------------------------------- icons
def icon_tanker(d, x, y, s=1.0):
    d.rectangle([x, y + 18 * s, x + 44 * s, y + 30 * s], fill=(60, 60, 60))
    d.polygon([(x + 30 * s, y + 18 * s), (x + 40 * s, y + 18 * s),
               (x + 40 * s, y + 8 * s), (x + 36 * s, y + 8 * s)],
              fill=(60, 60, 60))
    d.line([(x, y + 33 * s), (x + 44 * s, y + 33 * s)], fill=BLUE, width=2)
    for fx, fh in ((x + 8 * s, 12 * s), (x + 18 * s, 16 * s)):
        d.polygon([(fx, y + 16 * s), (fx + 5 * s, y + 16 * s - fh),
                   (fx + 10 * s, y + 16 * s)], fill=(214, 90, 20))


def icon_bridge(d, x, y, s=1.0):
    d.line([(x, y + 26 * s), (x + 44 * s, y + 26 * s)], fill=INK, width=3)
    d.arc([x + 4 * s, y + 6 * s, x + 40 * s, y + 30 * s], 180, 360,
          fill=INK, width=2)
    d.line([(x + 8 * s, y + 26 * s), (x + 8 * s, y + 10 * s)], fill=INK,
           width=2)
    d.line([(x + 36 * s, y + 26 * s), (x + 36 * s, y + 10 * s)], fill=INK,
           width=2)
    d.polygon([(x + 20 * s, y + 26 * s), (x + 24 * s, y + 26 * s),
               (x + 22 * s, y + 16 * s)], fill=RED)


def icon_branch(d, x, y, s=1.0):
    d.line([(x + 6 * s, y + 34 * s), (x + 38 * s, y + 6 * s)],
           fill=(74, 110, 50), width=2)
    for lx, ly in ((14, 26), (22, 18), (30, 10), (18, 30), (26, 22)):
        d.ellipse([x + lx * s, y + ly * s, x + (lx + 9) * s,
                   y + (ly + 5) * s], fill=(74, 110, 50))


def icon_globe(d, x, y, s=1.0):
    d.ellipse([x + 4 * s, y + 2 * s, x + 40 * s, y + 38 * s],
              outline=BLUE, width=2)
    d.ellipse([x + 16 * s, y + 2 * s, x + 28 * s, y + 38 * s],
              outline=BLUE, width=1)
    d.line([(x + 4 * s, y + 20 * s), (x + 40 * s, y + 20 * s)], fill=BLUE,
           width=1)
    d.arc([x + 4 * s, y + 8 * s, x + 40 * s, y + 32 * s], 0, 180, fill=BLUE,
          width=1)


def icon_storm(d, x, y, s=1.0):
    d.ellipse([x + 4 * s, y + 4 * s, x + 26 * s, y + 20 * s], fill=GREY)
    d.ellipse([x + 18 * s, y + 8 * s, x + 40 * s, y + 24 * s], fill=GREY)
    d.polygon([(x + 20 * s, y + 22 * s), (x + 14 * s, y + 36 * s),
               (x + 20 * s, y + 36 * s), (x + 16 * s, y + 44 * s),
               (x + 28 * s, y + 26 * s), (x + 22 * s, y + 26 * s)],
              fill=(214, 170, 20))


def icon_chart(d, x, y, s=1.0):
    d.line([(x + 4 * s, y + 30 * s), (x + 14 * s, y + 18 * s),
            (x + 24 * s, y + 24 * s), (x + 34 * s, y + 8 * s),
            (x + 42 * s, y + 12 * s)], fill=RED, width=3)
    d.polygon([(x + 42 * s, y + 12 * s), (x + 36 * s, y + 6 * s),
               (x + 36 * s, y + 14 * s)], fill=RED)
    d.rectangle([x + 4 * s, y + 36 * s, x + 16 * s, y + 42 * s],
                outline=INK, width=1)


def flag_usa(d, x, y, w=46, h=30):
    for i in range(7):
        d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                    fill=(178, 34, 52) if i % 2 == 0 else PAPER)
    d.rectangle([x, y, x + w * 0.4, y + h * 4 / 7], fill=BLUE)


def flag_chn(d, x, y, w=46, h=30):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.ellipse([x + 6, y + 5, x + 13, y + 12], fill=(255, 222, 0))


def flag_rus(d, x, y, w=46, h=30):
    d.rectangle([x, y, x + w, y + h / 3], fill=(245, 245, 245))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def world_map(d, x, y, w=300, h=170):
    """Stylised world map: continent blobs with numbered story dots."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 228, 212),
                outline=INK, width=1)
    blobs = [  # (cx, cy, rx, ry) in map-local coords
        (55, 30, 50, 20), (70, 58, 22, 8),           # N America, C America
        (95, 100, 16, 24),                           # S America
        (150, 26, 18, 12),                           # Europe
        (160, 80, 24, 32),                           # Africa
        (230, 30, 60, 24), (265, 62, 18, 10),        # Asia, SE Asia
        (260, 116, 22, 10),                          # Australia
        (115, 10, 10, 6),                            # Greenland
    ]
    for cx, cy, rx, ry in blobs:
        d.ellipse([x + cx - rx, y + cy - ry, x + cx + rx, y + cy + ry],
                  fill=(196, 188, 164))
    # lon/lat -> map coords: x: -180..180 -> 0..w ; y: 80..-55 -> 0..h
    def ll(lon, lat):
        return (x + (lon + 180) / 360 * w, y + (80 - lat) / 135 * h)
    dots = [
        (1, 114, 22),    # Shenzhen
        (2, 42, 35),     # Gulf / Crimea / Gaza cluster (labelled 2-4)
        (5, 85, 20),     # Odisha
        (6, 147, -6),    # Papua New Guinea
    ]
    for n, lon, lat in dots:
        px, py = ll(lon, lat)
        label = "2-4" if n == 2 else str(n)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED)
        text(d, (px, py - 1), label, font(SANS_B, 10),
             fill=(255, 255, 255), anchor="mm")


# ---------------------------------------------------------------- page
def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([12, 12, W - 12, H - 12], outline=INK, width=2)

    # Masthead
    centered(d, 26, "THE WORLD TODAY", font(SERIF_B, 60))
    centered(d, 96, "WEDNESDAY  •  18 NOVEMBER 2026  •  ONE DAY, ONE PAGE",
             font(SANS_B, 15), fill=GREY)
    rule(d, 124, w=3)
    rule(d, 129, w=1)

    # ---- LEAD panel
    lx, ly, lw, lh = 28, 140, 968, 158
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=(255, 252, 244),
                outline=INK, width=1)
    kicker(d, lx + 14, ly + 10, "LEAD  —  SHENZHEN, CHINA")
    headline(d, lx + 14, ly + 32,
             "Trump meets Xi and Putin in historic three-way talks",
             29, 640)
    body(d, lx + 14, ly + 100,
         "Donald Trump landed in Shenzhen on Wednesday for the first-ever "
         "trilateral summit with China's Xi Jinping and Russia's Vladimir "
         "Putin at the APEC meeting — nuclear arms and Ukraine on the "
         "agenda. Xi and Putin denounced Western sanctions and "
         "protectionism.", 15, 640)
    fx = lx + 700
    for i, (flag, name) in enumerate(((flag_usa, "UNITED STATES"),
                                      (flag_chn, "CHINA"),
                                      (flag_rus, "RUSSIA"))):
        fy = ly + 14 + i * 48
        flag(d, fx, fy)
        text(d, (fx + 56, fy + 7), name, font(SANS_B, 13))

    # ---- story panels (2 rows x 3)
    panels = [
        ("IRAN WAR", "Iran strikes US bases in the Gulf; Hormuz tanker hit",
         "Iran said its drones struck US Patriot defences at Ali Al Salem "
         "Air Base in Kuwait after the US hit Qeshm Island. Gulf states "
         "intercepted missiles and drones. An ADNOC ship was struck in the "
         "Strait of Hormuz; one crew member is missing.", icon_tanker),
        ("UKRAINE", "Ukraine downs Crimean bridge span; Kyiv bridges hit",
         "Ukrainian strikes destroyed the road span of the bridge linking "
         "Russia and Crimea. Russia hit two Kyiv bridges with seven "
         "ballistic missiles. Britain pledged 1,000+ air-defence missiles "
         "for Ukraine.", icon_bridge),
        ("GAZA", "Board of Peace: Gaza truce may collapse",
         "Trump's Board of Peace warned Israel and Hamas are failing their "
         "commitments to end the war. Israel began a \u201cconcentrated "
         "operation\u201d in central Gaza. A baby died of hypothermia as "
         "floods hit the camps; the UN warns of more cold deaths.",
         icon_branch),
        ("ASIA", "Modi home from ASEAN; Xi pushes open Asia-Pacific",
         "PM Modi returned to Delhi after the ASEAN summit in Manila. At "
         "the APEC summit in Shenzhen, Xi Jinping called for removing "
         "trade barriers and deeper cooperation on AI and digital trade.",
         icon_globe),
        ("STORM & QUAKE", "Cyclone Akvan nears Odisha; M6 quake hits Papua N.G.",
         "Akvan strengthened into a severe cyclonic storm off India's east "
         "coast; shelters opened in Odisha. A magnitude 6 earthquake "
         "struck Papua New Guinea on Wednesday, seismologists said.",
         icon_storm),
        ("MARKETS & TECH", "Nvidia won't bring back Huang; Binance eyes Asia",
         "Nvidia said it will not reinstate ex-chief Jensen Huang as it "
         "reported bumper results. After a $6.3bn crypto heist, Binance "
         "plans to expand into five Asian markets. Gold slid to a "
         "one-year low.", icon_chart),
    ]
    px0, py0 = 28, 310
    pw, ph, gap = 314, 224, 13
    for i, (kick, head, txt, icon) in enumerate(panels):
        col, row = i % 3, i // 3
        x = px0 + col * (pw + gap)
        y = py0 + row * (ph + gap)
        d.rectangle([x, y, x + pw, y + ph], fill=(255, 252, 244),
                    outline=INK, width=1)
        kicker(d, x + 12, y + 9, kick)
        hy = headline(d, x + 12, y + 30, head, 19, pw - 24)
        rule(d, hy + 6, x0=x + 12, x1=x + pw - 12, w=1, fill=GREY)
        body(d, x + 12, hy + 14, txt, 13.5, pw - 24, leading=18)
        icon(d, x + pw - 54, y + ph - 50, s=0.9)

    # ---- bottom band: AROUND THE WORLD + map
    by = 310 + 2 * 224 + 13  # 771
    bh = 996 - by
    # left: list
    lx2, lw2 = 28, 640
    d.rectangle([lx2, by, lx2 + lw2, by + bh], fill=(255, 252, 244),
                outline=INK, width=1)
    kicker(d, lx2 + 12, by + 9, "AROUND THE WORLD  —  ALSO TODAY")
    items = [
        "Israel elects Matan Kahana speaker — a blow to Netanyahu.",
        "Rubio: no evidence US flight, bank and Microsoft outages were cyberattacks.",
        "Russian military plane crashes in Siberia; all 19 aboard killed.",
        "Prince William and Kate to meet PM Modi in Delhi today.",
        "US Army officer held in UK over suspected Russian spying handed to US military.",
        "BBC and Ikea among nearly 200 websites hit by hackers.",
        "Myanmar to review its ASEAN ties, president tells parliament.",
        "Alaska: Democrat Mary Peltola defeats Senator Dan Sullivan.",
        "Kashmir: LeT militant Lateef Bhat killed in Kulgam, says Amit Shah.",
    ]
    fnt = font(SERIF, 13)
    yy = by + 32
    for item in items:
        d.ellipse([lx2 + 14, yy + 5, lx2 + 20, yy + 11], fill=RED)
        lines = wrap(d, item, fnt, lw2 - 40)
        for line in lines:
            text(d, (lx2 + 26, yy), line, fnt)
            yy += 16
        yy += 1
    # right: map
    mx, my = 28 + 640 + 13, by
    mw = 996 - mx
    d.rectangle([mx, my, mx + mw, my + bh], fill=(255, 252, 244),
                outline=INK, width=1)
    kicker(d, mx + 12, my + 9, "WHERE TODAY HAPPENED")
    world_map(d, mx + 12, my + 32, w=mw - 24, h=128)
    text(d, (mx + 12, my + 168),
         "1 Shenzhen  ·  2-4 Gulf, Crimea, Gaza  ·  5 Odisha  ·  6 PNG",
         font(SANS, 11), fill=GREY)
    text(d, (mx + 12, my + 186),
         "Dots mark the datelines on this page.",
         font(SERIF_I, 12), fill=GREY)
    text(d, (mx + 12, my + 204),
         "Sources: AP, Reuters, AFP, IANS, Just Security.",
         font(SANS, 10), fill=GREY)
    return img


def main():
    img = draw_page()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
