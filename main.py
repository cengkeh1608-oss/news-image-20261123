"""Draw the front page for 23 November 2026 and write it to /output/entry.png.

One self-contained program: no network, no randomness, no time. Running it
twice produces a byte-identical PNG. Uses PIL (Pillow) and the DejaVu fonts
that ship with the system, with a Liberation fallback.
"""

import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (250, 246, 236)
INK = (25, 25, 25)
RED = (163, 31, 22)
GRAY = (107, 107, 107)

SERIF_BOLD_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
]
SANS_BOLD_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
SANS_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def load_font(paths, size):
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default(size=size)


def wrap(draw, text, font, max_width):
    """Greedy word wrap measured in pixels; returns a list of lines."""
    lines = []
    current = ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centered(draw, y, text, font, fill):
    x = (W - draw.textlength(text, font=font)) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return y


def rule(draw, y, thickness=1):
    draw.rectangle([30, y, W - 30, y + thickness - 1], fill=INK)


LEAD = {
    "kicker": "CLIMATE SUMMIT - ANTALYA, TURKEY",
    "headline": "COP31 COLLAPSES",
    "deck": (
        "No deal as the EU rejects a pact that never mentions fossil fuels, "
        "ending the longest climate summit in history in failure."
    ),
    "source": "CNN - REUTERS - LE MONDE",
}

# (number, headline, summary, source) - 15 more stories, all reported 23 Nov 2026.
STORIES = [
    ("02", "HORMUZ WAR WIDENS",
     "Iran hits US bases in Bahrain and claims the strait; Houthis fire on Saudi Arabia.",
     "FINWIRE - CNBC"),
    ("03", "SHIP STILL BURNING",
     "Russian cargo ship Sparta II ablaze off Finland days after a drone attack.",
     "REUTERS"),
    ("04", "KYIV REGION HIT",
     "14 missing after a drone hits a building; a supermarket strike kills three.",
     "JAGRAN JOSH"),
    ("05", "DEMOCRATS TAKE HOUSE",
     "At least 258 seats - the largest US House majority since 1992.",
     "ZOT NEWS"),
    ("06", "NEPAL-INDIA TALKS",
     "PM Balendra Shah holds bilateral talks with PM Modi in New Delhi.",
     "OBSERVER VOICE"),
    ("07", "INDIA'S RECORD 720",
     "India posts 720/9 declared in the Wellington Test against New Zealand.",
     "OBSERVER VOICE"),
    ("08", "FACTORY FIRE HORROR",
     "Three dead and dozens missing after a blaze at an Indonesian candy factory.",
     "ARAB NEWS"),
    ("09", "MINISTER QUITS",
     "South Korea's education minister resigns over an AI cheating scandal.",
     "DAILY JAGRAN"),
    ("10", "NVIDIA CHIP ROW",
     "US seeks answers on Nvidia chip sales to China amid a secret diversion network.",
     "DAILY JAGRAN"),
    ("11", "LISBON MARCHES",
     "Thousands protest the cost of living in Portugal's capital.",
     "JAGRAN JOSH"),
    ("12", "MYANMAR HITS BACK",
     "Army-backed government calls an ASEAN decision 'unfair and imbalanced'.",
     "JAGRAN JOSH"),
    ("13", "UN SITE HIT IN SUDAN",
     "Drone attack strikes a UN building in Khartoum, the UN says.",
     "ZOT NEWS"),
    ("14", "LIVERPOOL ROUT UNITED",
     "Liverpool thrash 10-man Manchester United in Pochettino's first match.",
     "ARAB NEWS"),
    ("15", "EBOLA FIGHT DISRUPTED",
     "Fighting near Congo's Ebola outbreak hampers the response, WHO chief says.",
     "ARAB NEWS"),
    ("16", "24 KILLED IN S. SUDAN",
     "SPLA-IO forces attack leaves 24 civilians dead, the UN reports.",
     "ARAB NEWS"),
]


def draw_frontpage():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    title_font = load_font(SERIF_BOLD_PATHS, 56)
    date_font = load_font(SANS_BOLD_PATHS, 24)
    kicker_font = load_font(SANS_BOLD_PATHS, 19)
    lead_font = load_font(SERIF_BOLD_PATHS, 78)
    deck_font = load_font(SANS_PATHS, 24)
    source_font = load_font(SANS_BOLD_PATHS, 13)
    label_font = load_font(SANS_BOLD_PATHS, 15)
    num_font = load_font(SANS_BOLD_PATHS, 20)
    head_font = load_font(SANS_BOLD_PATHS, 18)
    sum_font = load_font(SANS_PATHS, 14)
    src_font = load_font(SANS_BOLD_PATHS, 11)

    # Masthead.
    centered(draw, 26, "THE WORLD IN ONE DAY", title_font, INK)
    centered(draw, 96, "MONDAY - 23 NOVEMBER 2026", date_font, RED)
    rule(draw, 132, 3)
    rule(draw, 138, 1)

    # Lead story.
    centered(draw, 156, LEAD["kicker"], kicker_font, RED)
    centered(draw, 182, LEAD["headline"], lead_font, INK)
    deck_lines = wrap(draw, LEAD["deck"], deck_font, W - 120)
    y = 276
    for line in deck_lines:
        centered(draw, y, line, deck_font, INK)
        y += 30
    centered(draw, y + 6, LEAD["source"], source_font, GRAY)

    rule(draw, 362, 2)
    centered(draw, 376, "THE DAY IN FIFTEEN MORE STORIES", label_font, INK)

    # Story grid: 3 columns x 5 rows.
    col_x = [30, 360, 690]
    col_w = 304
    y0 = 404
    row_h = 116
    for i, (num, headline, summary, source) in enumerate(STORIES):
        x = col_x[i % 3]
        y = y0 + (i // 3) * row_h
        draw.text((x, y), num, font=num_font, fill=RED)
        head_lines = wrap(draw, headline, head_font, col_w)
        hy = y + 26
        for line in head_lines[:2]:
            draw.text((x, hy), line, font=head_font, fill=INK)
            hy += 22
        sum_lines = wrap(draw, summary, sum_font, col_w)
        sy = y + 72
        for line in sum_lines[:2]:
            draw.text((x, sy), line, font=sum_font, fill=INK)
            sy += 17
        draw.text((x, y + 104), source, font=src_font, fill=GRAY)

    # Footer.
    centered(
        draw, 994,
        "Sources: CNN, Reuters, Le Monde, CNBC, Finwire, Arab News, WCMU, Zot News",
        src_font, GRAY,
    )
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    img = draw_frontpage()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, "PNG")
    data = open(path, "rb").read()
    print("wrote %s (%d bytes, sha256 %s)" % (path, len(data),
          hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
