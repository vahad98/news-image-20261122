#!/usr/bin/env python3
"""Render the news-image-20261122 entry: a one-page evening newspaper
summing up the world's news of Sunday 22 November 2026.

Reads the four photo panels from assets/ (generated in this repo, no text
in them) and draws every word of the page with Pillow. Output is
entry.png, 1024x1024, at most 1 MiB. Deterministic: same inputs give the
same bytes on every run.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 40
CONTENT_W = W - 2 * MARGIN  # 944

PAPER = (250, 246, 236)   # warm newspaper white
INK = (18, 18, 18)        # near-black
RED = (176, 30, 36)       # masthead red
GRAY = (110, 108, 100)    # dateline / credit gray
LIGHT_RULE = (190, 184, 172)

FONT_DIR = "/usr/share/fonts/truetype/noto"
SERIF_BLACK = os.path.join(FONT_DIR, "NotoSerif-Black.ttf")
SERIF_BOLD = os.path.join(FONT_DIR, "NotoSerif-Bold.ttf")
SERIF_REG = os.path.join(FONT_DIR, "NotoSerif-Regular.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")
SANS_REG = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def fit_single_line(draw, text, path, start, minimum, max_w):
    """Largest font size (start down to minimum) whose line fits max_w."""
    size = start
    while size > minimum:
        fnt = font(path, size)
        if text_w(draw, text, fnt) <= max_w:
            return fnt
        size -= 1
    return font(path, minimum)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_wrapped(draw, text, path, start, minimum, max_w, max_lines):
    """Largest font size whose wrap fits within max_lines; returns (font, lines)."""
    size = start
    while size >= minimum:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = font(path, minimum)
    return fnt, wrap(draw, text, fnt, max_w)[:max_lines]


def draw_centered(draw, y, text, fnt, fill, x0=MARGIN, x1=W - MARGIN):
    w = text_w(draw, text, fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def cover(im, tw, th):
    """Center-crop the image to the target aspect, then resize (Lanczos)."""
    iw, ih = im.size
    scale = max(tw / iw, th / ih)
    nw, nh = int(round(iw * scale)), int(round(ih * scale))
    im = im.resize((nw, nh), Image.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return im.crop((left, top, left + tw, top + th))


def main():
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)

    # --- top red bar -------------------------------------------------
    draw.rectangle([0, 0, W, 10], fill=RED)

    # --- masthead ----------------------------------------------------
    mast = fit_single_line(draw, "THE WORLD TODAY", SERIF_BLACK, 72, 40, CONTENT_W)
    draw_centered(draw, 26, "THE WORLD TODAY", mast, INK)

    # --- date line ---------------------------------------------------
    date_fnt = font(SANS_BOLD, 21)
    draw_centered(draw, 108, "SUNDAY, 22 NOVEMBER 2026", date_fnt, RED)

    # --- dateline ----------------------------------------------------
    dl_fnt = font(SANS_REG, 15)
    draw_centered(draw, 136, "MANAMA  \u2022  ANTALYA  \u2022  SINALOA  \u2022  SHENZHEN",
                  dl_fnt, GRAY)

    # --- double rule -------------------------------------------------
    draw.line([(MARGIN, 162), (W - MARGIN, 162)], fill=INK, width=2)
    draw.line([(MARGIN, 167), (W - MARGIN, 167)], fill=INK, width=1)

    # --- hero photo --------------------------------------------------
    hero = Image.open(os.path.join(ASSETS, "hero.webp")).convert("RGB")
    hero = cover(hero, CONTENT_W, 208)
    hy = 178
    page.paste(hero, (MARGIN, hy))
    draw.rectangle([MARGIN, hy, W - MARGIN, hy + 208], outline=INK, width=1)

    # chip "THE GULF" bottom-left inside the photo
    chip_fnt = font(SANS_BOLD, 15)
    chip_text = "THE GULF"
    chip_w = int(text_w(draw, chip_text, chip_fnt)) + 24
    chip_h = 30
    chip_y = hy + 208 - chip_h - 10
    draw.rectangle([MARGIN + 10, chip_y, MARGIN + 10 + chip_w, chip_y + chip_h],
                   fill=RED)
    draw.text((MARGIN + 22, chip_y + 6), chip_text, font=chip_fnt, fill=(255, 255, 255))

    # --- hero headline (one line, auto-fit) --------------------------
    head_fnt = fit_single_line(draw, "IRAN HITS US BASES IN BAHRAIN",
                               SERIF_BOLD, 54, 28, CONTENT_W)
    draw_centered(draw, 396, "IRAN HITS US BASES IN BAHRAIN", head_fnt, INK)

    # --- hero deck (two lines, centered) -----------------------------
    deck = ("Tehran claims missiles and drones struck two Patriot radars; "
            "Bahrain says an industrial site burned, with no casualties.")
    deck_fnt, deck_lines = fit_wrapped(draw, deck, SERIF_REG, 22, 16,
                                       CONTENT_W - 40, 2)
    dy = 452
    for line in deck_lines:
        draw_centered(draw, dy, line, deck_fnt, INK)
        dy += int(deck_fnt.size * 1.35)

    # --- market ribbon (full page width) -----------------------------
    ribbon_y, ribbon_h = 506, 42
    draw.rectangle([0, ribbon_y, W, ribbon_y + ribbon_h], fill=RED)
    ribbon_fnt = fit_single_line(
        draw, "MARKETS IN CORRECTION  \u2022  S&P 500 -3.7% AS AI SELL-OFF SPREADS",
        SANS_BOLD, 22, 14, W - 32)
    draw_centered(draw, ribbon_y + 9,
                  "MARKETS IN CORRECTION  \u2022  S&P 500 -3.7% AS AI SELL-OFF SPREADS",
                  ribbon_fnt, (255, 255, 255), x0=0, x1=W)

    # --- three columns ------------------------------------------------
    cols = [
        ("climate.webp", "CLIMATE", "COP31 IN OVERTIME",
         "Antalya talks pass a second day past deadline, deadlocked over fossil fuels."),
        ("mexico.webp", "MEXICO", "CARTEL BOSS SEIZED",
         "Mexico captures FBI most-wanted \u2018El Chapo Isidro\u2019 in Sinaloa; "
         "11 killed in the raid."),
        ("summit.webp", "SUMMIT", "THREE LEADERS, ONE TABLE",
         "Trump, Xi and Putin meet in Shenzhen and agree to talk on nuclear risks."),
    ]
    col_w = 304
    gap = 16
    photo_h = 126
    cy = 564
    for i, (img_name, kicker, headline, deck_text) in enumerate(cols):
        x = MARGIN + i * (col_w + gap)
        im = Image.open(os.path.join(ASSETS, img_name)).convert("RGB")
        page.paste(cover(im, col_w, photo_h), (x, cy))
        draw.rectangle([x, cy, x + col_w, cy + photo_h], outline=INK, width=1)

        kick_fnt = font(SANS_BOLD, 15)
        draw.text((x, cy + photo_h + 10), kicker, font=kick_fnt, fill=RED)

        h_fnt, h_lines = fit_wrapped(draw, headline, SERIF_BOLD, 28, 18,
                                     col_w, 2)
        hy2 = cy + photo_h + 34
        for line in h_lines:
            draw.text((x, hy2), line, font=h_fnt, fill=INK)
            hy2 += int(h_fnt.size * 1.22)

        d_fnt, d_lines = fit_wrapped(draw, deck_text, SERIF_REG, 18, 13,
                                     col_w, 4)
        dy2 = hy2 + 6
        for line in d_lines:
            draw.text((x, dy2), line, font=d_fnt, fill=INK)
            dy2 += int(d_fnt.size * 1.32)

    # --- ALSO TODAY footer -------------------------------------------
    fy = 880
    draw.line([(MARGIN, fy), (W - MARGIN, fy)], fill=LIGHT_RULE, width=1)
    also_fnt = font(SANS_BOLD, 17)
    draw.text((MARGIN, fy + 8), "ALSO TODAY", font=also_fnt, fill=RED)
    draw.line([(MARGIN + 118, fy + 19), (W - MARGIN, fy + 19)], fill=RED, width=2)

    items = [
        "EU and Indonesia sign a trade deal covering 730 million people",
        "Russia hits Zelensky\u2019s hometown, Ukraine hits a Russian ship",
        "Magnitude 6.9 quake shakes Peru\u2019s Andes, no damage reported",
        "GTA VI sets a $3.79bn first-day sales record",
        "Factory fire in Indonesia kills 3, 36 missing",
        "Boat carrying mourners capsizes in Nigeria, 24 dead",
    ]
    col_x = [MARGIN, MARGIN + CONTENT_W // 2 + 8]
    col_w2 = CONTENT_W // 2 - 8
    row_y = [fy + 34, fy + 60, fy + 86]
    for idx, item in enumerate(items):
        cx = col_x[idx // 3]
        ry = row_y[idx % 3]
        it_fnt = fit_single_line(draw, item, SANS_REG, 15, 11, col_w2 - 18)
        draw.rectangle([cx, ry + 4, cx + 9, ry + 13], fill=RED)
        draw.text((cx + 16, ry), item, font=it_fnt, fill=INK)

    # --- credit line -------------------------------------------------
    credit_fnt = font(SANS_BOLD, 13)
    draw_centered(draw, 994, "THE WORLD TODAY  \u2022  SUNDAY, 22 NOVEMBER 2026",
                  credit_fnt, GRAY)

    # --- save: PNG if it fits, else JPEG stepped down ----------------
    page.save(OUT, format="PNG")
    if os.path.getsize(OUT) > 1048576:
        for quality in (92, 88, 84, 80, 76, 72):
            page.save(OUT, format="JPEG", quality=quality, optimize=True)
            if os.path.getsize(OUT) <= 1048576:
                break
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
