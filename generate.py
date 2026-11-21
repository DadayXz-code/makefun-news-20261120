#!/usr/bin/env python3
"""Generate entry.png: an original illustrated front page summing up the world news of
Friday 20 November 2026. Every picture on the page is drawn here with code (flat
vector-style illustrations) -- no photographs, no copied artwork. Story facts were
checked against same-day reporting (Kyiv bridges, Cyclone Akvan, Poland, Wall Street,
UK-EU deal, COP31, US Senate). Run: python3 generate.py  ->  writes entry.png (1024x1024).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (163, 18, 18)
BLUE = (31, 58, 95)
GREY = (110, 106, 96)
LIGHT = (233, 227, 210)
GOLD = (176, 132, 40)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, maxw):
    """Greedy word wrap; returns list of lines that fit maxw."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, maxw, text, font, fill=INK, leading=None, max_lines=None):
    """Draw wrapped text; returns y just below the last line."""
    lh = leading if leading is not None else int(font.size * 1.22)
    lines = wrap(d, text, font, maxw)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def hline(d, x0, x1, y, wdt=1, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)


def paste_ill(img, fn, x, y, w, h):
    """Render an illustration on its own layer, clipped to its box, then paste."""
    layer = Image.new("RGB", (w, h), PAPER)
    dl = ImageDraw.Draw(layer)
    fn(dl, 0, 0, w, h)
    img.paste(layer, (x, y))


def kicker(d, x, y, text, color=RED):
    d.text((x, y), text, font=F(SANS_B, 13), fill=color)
    return y + 18


# ---------------- illustrations (all drawn, original) ----------------

def ill_bridge(d, x, y, w, h):
    """Dusk sky, river, a bridge over the Dnipro, explosion bursts."""
    for i in range(h):
        t = i / h
        d.line([(x, y + i), (x + w, y + i)],
               fill=(int(44 + 60 * t), int(52 + 55 * t), int(84 + 60 * t)))
    d.rectangle([x, y + h - 46, x + w, y + h], fill=(38, 54, 74))  # river
    for i in range(5):  # river glints
        d.line([(x + 20 + i * 90, y + h - 30), (x + 70 + i * 90, y + h - 30)],
               fill=(120, 140, 170), width=2)
    d.rectangle([x, y + h - 96, x + w, y + h - 88], fill=(20, 20, 26))  # deck
    for px in (0.18, 0.5, 0.82):  # piers
        bx = x + int(w * px)
        d.rectangle([bx - 5, y + h - 88, bx + 5, y + h - 46], fill=(20, 20, 26))
    for bx, by, s, col in ((0.30, 0.30, 46, (255, 176, 32)),
                           (0.62, 0.22, 60, (255, 120, 20)),
                           (0.80, 0.38, 34, (255, 200, 90))):  # bursts
        cx, cy = x + int(w * bx), y + int(h * by)
        for k in range(10):
            a = k * math.pi / 5
            d.line([(cx, cy), (cx + int(s * math.cos(a)), cy + int(s * math.sin(a)))],
                   fill=col, width=5)
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 226, 140))
    for sx, sy, r in ((0.42, 0.16, 20), (0.52, 0.10, 26), (0.72, 0.30, 16)):  # smoke
        d.ellipse([x + int(w * sx) - r, y + int(h * sy) - r,
                   x + int(w * sx) + r, y + int(h * sy) + r], fill=(90, 88, 92))


def ill_radar(d, x, y, w, h):
    """Air-defence radar screen at night."""
    d.rectangle([x, y, x + w, y + h], fill=(12, 34, 22))
    cx, cy = x + w // 2, y + h // 2
    for r in (14, 28, 42, 54):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(60, 160, 90), width=1)
    d.line([(cx, cy), (cx + 40, cy - 36)], fill=(120, 220, 130), width=2)
    for bx, by in ((0.30, 0.62), (0.68, 0.30), (0.76, 0.66)):
        d.ellipse([x + int(w * bx) - 5, y + int(h * by) - 5,
                   x + int(w * bx) + 5, y + int(h * by) + 5], fill=(255, 80, 60))
    d.text((x + 8, y + 6), "AIR DEFENCE // 03:30", font=F(SANS_B, 11), fill=(140, 230, 150))


def ill_cyclone(d, x, y, w, h):
    """Cyclone spiral over the sea, coastline below."""
    d.rectangle([x, y, x + w, y + h], fill=(58, 96, 128))
    cx, cy = x + int(w * 0.55), y + int(h * 0.45)
    maxr = min(92, h // 2 - 6)
    for r in range(14, maxr + 1, 12):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=560,
              fill=(235, 240, 245), width=7)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(255, 255, 255))
    d.polygon([(x, y + h), (x, y + int(h * 0.72)), (x + int(w * 0.30), y + int(h * 0.80)),
               (x + int(w * 0.42), y + h)], fill=(222, 196, 140))
    for i in range(14):  # rain
        rx = x + 12 + i * 32
        d.line([(rx, y + 8), (rx - 8, y + 34)], fill=(200, 220, 235), width=2)


def ill_chart(d, x, y, w, h):
    """Falling market chart."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    for gy in range(1, 4):
        yy = y + int(h * gy / 4)
        d.line([(x + 6, yy), (x + w - 6, yy)], fill=(225, 225, 225), width=1)
    pts = [(0.05, 0.25), (0.20, 0.30), (0.35, 0.22), (0.50, 0.45),
           (0.62, 0.42), (0.75, 0.62), (0.88, 0.72), (0.97, 0.86)]
    xy = [(x + int(w * px), y + int(h * py)) for px, py in pts]
    d.line(xy, fill=(163, 18, 18), width=4, joint="curve")
    d.polygon(xy + [(xy[-1][0], y + h - 4), (xy[0][0], y + h - 4)], fill=(232, 190, 190))
    lbl = "NASDAQ  -2%"
    d.text((x + w - 10 - d.textlength(lbl, font=F(SANS_B, 15)), y + 8), lbl,
           font=F(SANS_B, 15), fill=(163, 18, 18))
    d.text((x + 10, y + h - 24), "7TH STRAIGHT FALL", font=F(SANS_B, 11), fill=GREY)


def ill_flags(d, x, y, w, h):
    """Union Jack (simplified) beside the EU circle of stars."""
    hw = w // 2
    d.rectangle([x, y, x + hw - 4, y + h], fill=(18, 40, 90))  # UK
    d.rectangle([x, y + h // 2 - 7, x + hw - 4, y + h // 2 + 7], fill=(255, 255, 255))
    d.line([(x, y), (x + hw - 4, y + h)], fill=(255, 255, 255), width=10)
    d.line([(x + hw - 4, y), (x, y + h)], fill=(255, 255, 255), width=10)
    d.rectangle([x, y + h // 2 - 4, x + hw - 4, y + h // 2 + 4], fill=(200, 16, 46))
    d.line([(x, y), (x + hw - 4, y + h)], fill=(200, 16, 46), width=4)
    d.line([(x + hw - 4, y), (x, y + h)], fill=(200, 16, 46), width=4)
    ex = x + hw + 4  # EU
    d.rectangle([ex, y, ex + hw - 4, y + h], fill=(0, 51, 153))
    ccx, ccy = ex + (hw - 4) // 2, y + h // 2
    for k in range(12):
        a = -math.pi / 2 + k * math.pi / 6
        sx, sy = ccx + int(30 * math.cos(a)), ccy + int(30 * math.sin(a))
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 204, 0))


def ill_summit(d, x, y, w, h):
    """Climate summit: globe, rising thermometer, flags."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 226))
    r = min(52, h // 2 - 4)
    cx, cy = x + int(w * 0.30), y + h // 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 180))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(31, 58, 95), width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360,
          fill=(90, 170, 110), width=max(3, r // 5))
    d.arc([cx - r // 2, cy - r, cx + r // 2, cy + r], 0, 360,
          fill=(90, 170, 110), width=max(3, r // 6))
    tx = x + int(w * 0.74)  # thermometer
    top, bot = y + 8, y + h - 22
    d.rectangle([tx - 7, top, tx + 7, bot], fill=(255, 255, 255),
                outline=(163, 18, 18), width=2)
    d.rectangle([tx - 4, top + (bot - top) // 2, tx + 4, bot], fill=(220, 60, 40))
    d.ellipse([tx - 13, bot - 4, tx + 13, bot + 18], fill=(220, 60, 40))
    if h >= 100:
        for i, col in enumerate(((31, 58, 95), (163, 18, 18), (176, 132, 40), (70, 130, 110))):
            fx = x + 12 + i * 24
            d.polygon([(fx, y + h - 6), (fx, y + h - 34), (fx + 16, y + h - 27),
                       (fx, y + h - 20)], fill=col)


# ---------------- content: Friday 20 November 2026 ----------------

LEAD = {
    "kicker": "UKRAINE  ·  KYIV",
    "headline": "Russia hits three Kyiv bridges in huge overnight barrage",
    "dek": ("More than 400 drones and 110 missiles, 27 of them ballistic, struck "
            "Ukraine overnight, killing at least eight and knocking out power "
            "across ten regions."),
    "ill": ill_bridge,
    "caption": "Illustration: a bridge over the Dnipro under attack. Drawn, not a photograph.",
}

ROW2 = [
    {"kicker": "POLAND  ·  NATO", "region": "Eastern Europe",
     "headline": "Russian missiles land in Poland; NATO calls it a grave violation",
     "body": ("Two missiles and a suspected drone came down in south-east Poland "
              "during drills nearby. Warsaw called it a deliberate provocation; "
              "NATO jets were airborne."),
     "ill": ill_radar},
    {"kicker": "INDIA  ·  CYCLONE AKVAN", "region": "South Asia",
     "headline": "Cyclone Akvan makes landfall; 300,000 moved to safety",
     "body": ("The storm crossed the Odisha coast near Gopalpur, cancelling 28 "
              "trains. Odisha aimed for zero casualties as Akvan weakened over land."),
     "ill": ill_cyclone},
]

GRID = [
    {"kicker": "MARKETS  ·  WALL STREET", "region": "Americas",
     "headline": "AI sell-off deepens: Nasdaq falls for a seventh day",
     "body": ("Nasdaq down about 2%, S&P 500 about 1%; Anthropic 63% below its "
              "IPO price."),
     "ill": ill_chart},
    {"kicker": "BRITAIN  ·  EUROPE", "region": "Western Europe",
     "headline": "UK and EU close reset deal on food, carbon and youth",
     "body": ("Food checks end March 2028; carbon markets linked; youth scheme "
              "for 100,000."),
     "ill": ill_flags},
    {"kicker": "CLIMATE  ·  COP31", "region": "Climate",
     "headline": "COP31 draft drops fossil fuels as talks run late",
     "body": ("In Antalya, a France- and Panama-led group called the text "
              "insufficient."),
     "ill": ill_summit},
]

BRIEFS = [
    ("Americas", "Senate votes 51–48 to block Iran war-powers limits"),
    ("Eastern Europe", "Kerch Bridge hit for the third time in four days"),
    ("East Asia", "Trump, Xi and Putin meet in Shenzhen — a first"),
    ("Eastern Europe", "Zelensky: 'He's a killer' after Trump calls Putin a friend"),
    ("Climate", "EU warns COP31 risks becoming a 'fossil summit'"),
    ("Western Europe", "Miliband: EU deal does not depend on tuition fees"),
    ("Western Europe", "Burnham: UK to explore even closer ties with EU"),
    ("Western Europe", "European Commission confirms cyberattack"),
    ("Western Europe", "Burnham: Europe ready for Ukraine peace talks"),
    ("Western Europe", "Cost-of-living protests sweep the continent"),
    ("Eastern Europe", "Lviv rail station struck; two killed outside Kyiv"),
    ("South Asia", "Odisha: no major damage as Akvan weakens"),
    ("Eastern Europe", "Polish defences scrambled at 3:30 a.m.; no injuries"),
    ("Climate", "Nearly 200 nations debate fossil-fuel wording"),
    ("Americas", "Wall Street heads for worst week since April 2025"),
]

TICKER = "400+ DRONES  ·  110+ MISSILES  ·  300,000 EVACUATED  ·  NASDAQ −2%  ·  100,000/YR YOUTH MOBILITY"
DATE_LINE = "FRIDAY, 20 NOVEMBER 2026"
DAY = "Friday 20 November 2026"


def main():
    stories = [LEAD, *ROW2, *GRID]
    regions = {"Eastern Europe", "South Asia"}
    for s in ROW2 + GRID:
        regions.add(s["region"])
    for r, _ in BRIEFS:
        regions.add(r)
    n_stories = 1 + len(ROW2) + len(GRID) + len(BRIEFS)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 26  # margin
    X1 = W - M

    # masthead
    d.text((M, 16), DATE_LINE, font=F(SANS_B, 14), fill=INK)
    meta = f"{n_stories} STORIES · {len(regions)} REGIONS"
    d.text((X1 - d.textlength(meta, font=F(SANS_B, 14)), 16), meta,
           font=F(SANS_B, 14), fill=INK)
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=F(SERIF_B, 62))) / 2, 34), title,
           font=F(SERIF_B, 62), fill=INK)
    sub = "FRIDAY 20 NOVEMBER 2026  ·  LATE EDITION  ·  THE DAY'S NEWS IN ONE PAGE"
    d.text(((W - d.textlength(sub, font=F(SANS_B, 13))) / 2, 104), sub,
           font=F(SANS_B, 13), fill=GREY)
    hline(d, M, X1, 126, 3)
    hline(d, M, X1, 131, 1)

    # ticker strip
    d.text(((W - d.textlength(TICKER, font=F(SANS_B, 13))) / 2, 140), TICKER,
           font=F(SANS_B, 13), fill=RED)
    hline(d, M, X1, 162, 1)

    # lead story
    y = 176
    ill_w, ill_h = 470, 218
    paste_ill(img, LEAD["ill"], M, y, ill_w, ill_h)
    d.text((M, y + ill_h + 6), LEAD["caption"], font=F(SERIF, 12), fill=GREY)
    tx = M + ill_w + 20
    tw = X1 - tx
    yy = kicker(d, tx, y, LEAD["kicker"])
    yy = block(d, tx, yy + 2, tw, LEAD["headline"], F(SERIF_B, 35), leading=40)
    block(d, tx, yy + 8, tw, LEAD["dek"], F(SERIF, 17), leading=23)
    hline(d, M, X1, 424, 1)

    # row 2: two stories, illustration left, text right
    y = 440
    col_w = (X1 - M - 24) // 2
    for i, s in enumerate(ROW2):
        x = M + i * (col_w + 24)
        iw, ih = 168, 118
        paste_ill(img, s["ill"], x, y, iw, ih)
        tx2 = x + iw + 12
        tw2 = col_w - iw - 12
        yy = kicker(d, tx2, y, s["kicker"])
        yy = block(d, tx2, yy + 1, tw2, s["headline"], F(SERIF_B, 19), leading=23,
                   max_lines=3)
        block(d, tx2, yy + 4, tw2, s["body"], F(SERIF, 13.5), leading=17, max_lines=4)
        if i == 0:
            d.line([(M + col_w + 12, y), (M + col_w + 12, y + 168)], fill=GREY, width=1)
    hline(d, M, X1, 622, 1)

    # grid: three stories, illustration on top
    y = 638
    gw = (X1 - M - 48) // 3
    for i, s in enumerate(GRID):
        x = M + i * (gw + 24)
        paste_ill(img, s["ill"], x, y, gw, 70)
        yy = kicker(d, x, y + 78, s["kicker"])
        yy = block(d, x, yy + 1, gw, s["headline"], F(SERIF_B, 18), leading=21,
                   max_lines=2)
        block(d, x, yy + 4, gw, s["body"], F(SERIF, 13.5), leading=16, max_lines=2)
        if i < 2:
            d.line([(x + gw + 12, y), (x + gw + 12, y + 168)], fill=GREY, width=1)
    hline(d, M, X1, 822, 1)

    # briefs: two columns, one line each
    y = 838
    d.text((M, y), "THE DAY IN BRIEF", font=F(SANS_B, 15), fill=INK)
    d.text((X1 - d.textlength(DAY, font=F(SERIF, 13)), y + 2), DAY,
           font=F(SERIF, 13), fill=GREY)
    hline(d, M, X1, y + 24, 1)
    by = y + 34
    bw = (X1 - M - 24) // 2
    for idx, item in enumerate(BRIEFS):
        col, row = idx % 2, idx // 2
        x = M + col * (bw + 24)
        yy = by + row * 16
        d.text((x, yy), "▪", font=F(SANS_B, 11), fill=RED)
        d.text((x + 14, yy), item[1], font=F(SERIF, 12.5), fill=INK)
    foot = "Events reported on 20 November 2026. All pictures are original drawings, not photographs."
    d.text(((W - d.textlength(foot, font=F(SERIF, 12))) / 2, 1004), foot,
           font=F(SERIF, 12), fill=GREY)

    img.save("entry.png", optimize=True)
    print(f"saved entry.png {n_stories} stories, {len(regions)} regions")


if __name__ == "__main__":
    main()
