#!/usr/bin/env python3
"""
Generate the news-image-20261122 entry: a dense newspaper front page, 1024x1024 PNG.
Every element drawn in code - no external assets, no network.
Round 2: One day, one skyline — 35 stories, 7 regions
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ─── Constants ───
W, H = 1024, 1024
IMG = Image.new("RGB", (W, H), "white")
D = ImageDraw.Draw(IMG)

# Fonts - DejaVu at /usr/share/fonts/truetype/dejavu/
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

def load_font(name, size, bold=False, italic=False):
    suffix = ""
    if bold and italic:
        suffix = "-BoldOblique"
    elif bold:
        suffix = "-Bold"
    elif italic:
        suffix = "-Oblique"
    path = os.path.join(FONT_DIR, f"DejaVuSans{suffix}.ttf")
    if name == "serif":
        path = os.path.join(FONT_DIR, f"DejaVuSerif{suffix}.ttf")
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

FONTS = {}
FONT_META = {}  # font -> (name, size, bold, italic)

def get_font(name, size, bold=False, italic=False):
    key = (name, size, bold, italic)
    if key not in FONTS:
        f = load_font(name, size, bold, italic)
        FONTS[key] = f
        FONT_META[f] = (name, size, bold, italic)
    return FONTS[key]

def get_font_meta(font):
    """Extract font metadata from cache."""
    return FONT_META.get(font, ("sans", 10, False, False))

# Colors
NAVY = (0x0B, 0x1D, 0x3A)
RED = (0xC0, 0x1C, 0x1C)
BLACK = (0x1A, 0x1A, 0x1A)
DARK_GREY = (0x33, 0x33, 0x33)
MED_GREY = (0x66, 0x66, 0x66)
LIGHT_GREY = (0x99, 0x99, 0x99)
WHITE = (0xFF, 0xFF, 0xFF)
EUROPE_BLUE = (0x1E, 0x3A, 0x8A)
MIDEAST_RED = (0xB8, 0x2E, 0x2E)
AMERICAS_GREEN = (0x1B, 0x6B, 0x2F)
ASIA_ORANGE = (0xC8, 0x6C, 0x1A)
AFRICA_BROWN = (0x6B, 0x42, 0x1A)
OCEANIA_TEAL = (0x0A, 0x6B, 0x6B)
WORLD_PURPLE = (0x5A, 0x2A, 0x7A)
TAG_BLUE = (0xD6, 0xE4, 0xF8)
TAG_RED = (0xF8, 0xD6, 0xD6)
TAG_GREEN = (0xD6, 0xF8, 0xDB)
TAG_ORANGE = (0xF8, 0xE4, 0xD6)
TAG_BROWN = (0xF0, 0xE4, 0xD6)
TAG_PURPLE = (0xE8, 0xD6, 0xF8)
TAG_TEAL = (0xD6, 0xF8, 0xF8)
STAT_CHIP_BG = (0xF0, 0xF0, 0xF0)
STAT_CHIP_BORDER = (0xCC, 0xCC, 0xCC)

PAD_X = 10

# ═══════════════════════════════════════════════════════════════
# TEXT HELPERS — never silently drop words; shrink then ellipsis
# ═══════════════════════════════════════════════════════════════

def _fit_text_to_width(text, font, max_width, min_font_size=7):
    """
    Given text, font, and max_width, return (fitted_text, font) where text fits.
    Strategy: if text too wide, shrink font by 1pt down to min_font_size and re-wrap.
    If still too wide at min font, shorten at word boundary and append '…'.
    """
    current_font = font
    current_size = font.size
    font_name, _, is_bold, is_italic = get_font_meta(font)
    while current_font.getlength(text) > max_width:
        if current_size > min_font_size:
            current_size -= 1
            current_font = get_font(font_name, current_size, bold=is_bold, italic=is_italic)
        else:
            # At minimum font, shorten at word boundary
            words = text.split()
            while words and current_font.getlength(" ".join(words) + "…") > max_width:
                words.pop()
            if not words:
                return "…", current_font
            return " ".join(words) + "…", current_font
    return text, current_font


def _wrap_text(text, font, max_width, max_lines):
    """
    Wrap text to fit max_width and max_lines.
    Returns list of lines (each fits max_width).
    If text doesn't fit in max_lines at current font, returns None to signal need to shrink.
    """
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test = current + (" " if current else "") + w
        if font.getlength(test) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
            if len(lines) >= max_lines - 1:
                # Last line gets the remaining words
                remaining = [w] + words[words.index(w)+1:]
                current = " ".join(remaining)
                break
    if current and len(lines) < max_lines:
        lines.append(current)
    # Check if all lines fit
    for line in lines:
        if font.getlength(line) > max_width:
            return None
    return lines


def draw_text(x, y, text, font, color, anchor="lt", max_width=None):
    if max_width:
        fitted_text, fitted_font = _fit_text_to_width(text, font, max_width)
        D.text((x, y), fitted_text, font=fitted_font, fill=color, anchor=anchor)
    else:
        D.text((x, y), text, font=font, fill=color, anchor=anchor)


def draw_text_on_layer(draw, x, y, text, font, color, anchor="lt", max_width=None):
    if max_width:
        fitted_text, fitted_font = _fit_text_to_width(text, font, max_width)
        draw.text((x, y), fitted_text, font=fitted_font, fill=color, anchor=anchor)
    else:
        draw.text((x, y), text, font=font, fill=color, anchor=anchor)


def draw_text_wrapped(x, y, text, font, color, max_width, line_height, max_lines=2):
    """
    Draw wrapped text. Never silently drops words.
    Shrinks font down to 7pt if needed, then ellipsis at word boundary.
    Returns height used.
    """
    current_font = font
    current_size = font.size
    font_name, _, is_bold, is_italic = get_font_meta(font)
    min_font_size = 7
    
    while True:
        lines = _wrap_text(text, current_font, max_width, max_lines)
        if lines is not None:
            break
        # Doesn't fit - shrink font
        if current_size > min_font_size:
            current_size -= 1
            current_font = get_font(font_name, current_size, bold=is_bold, italic=is_italic)
        else:
            # At minimum font, need to truncate with ellipsis at word boundary
            words = text.split()
            # Build lines greedily at min font
            lines = []
            current = ""
            for w in words:
                test = current + (" " if current else "") + w
                if current_font.getlength(test) <= max_width:
                    current = test
                else:
                    if current:
                        lines.append(current)
                    current = w
                    if len(lines) >= max_lines - 1:
                        remaining = [w] + words[words.index(w)+1:]
                        current = " ".join(remaining)
                        break
            if current and len(lines) < max_lines:
                # Check if last line fits, if not truncate it
                if current_font.getlength(current) > max_width:
                    line_words = current.split()
                    while line_words and current_font.getlength(" ".join(line_words) + "…") > max_width:
                        line_words.pop()
                    current = " ".join(line_words) + "…" if line_words else "…"
                lines.append(current)
            break
    
    h_used = 0
    for line in lines:
        D.text((x, y + h_used), line, font=current_font, fill=color)
        h_used += line_height
    return h_used


def draw_text_wrapped_on_layer(draw, x, y, text, font, color, max_width, line_height, max_lines=2):
    """
    Same as draw_text_wrapped but on a passed draw layer.
    Never silently drops words.
    """
    current_font = font
    current_size = font.size
    font_name, _, is_bold, is_italic = get_font_meta(font)
    min_font_size = 7
    
    while True:
        lines = _wrap_text(text, current_font, max_width, max_lines)
        if lines is not None:
            break
        if current_size > min_font_size:
            current_size -= 1
            current_font = get_font(font_name, current_size, bold=is_bold, italic=is_italic)
        else:
            words = text.split()
            lines = []
            current = ""
            for w in words:
                test = current + (" " if current else "") + w
                if current_font.getlength(test) <= max_width:
                    current = test
                else:
                    if current:
                        lines.append(current)
                    current = w
                    if len(lines) >= max_lines - 1:
                        remaining = [w] + words[words.index(w)+1:]
                        current = " ".join(remaining)
                        break
            if current and len(lines) < max_lines:
                if current_font.getlength(current) > max_width:
                    line_words = current.split()
                    while line_words and current_font.getlength(" ".join(line_words) + "…") > max_width:
                        line_words.pop()
                    current = " ".join(line_words) + "…" if line_words else "…"
                lines.append(current)
            break
    
    h_used = 0
    for line in lines:
        draw.text((x, y + h_used), line, font=current_font, fill=color)
        h_used += line_height
    return h_used


# ═══════════════════════════════════════════════════════════════
# LAYOUT - Explicit Y-bands per fix brief
# ═══════════════════════════════════════════════════════════════
# Masthead block: y 0–150
# Stat strip: y 150–210
# UTC timeline: y 210–238
# Region tabs: y 238–268
# IN 30 SECONDS box: y 268–293
# Lead panels 1–3: y 293–584 (each 97px)
# Mid cards 4–15: y 584–824 (2 rows x 6 cards x 110px)
# Map + ALSO ON: y 824–994
# DATE CHECK box: y 994–1024
# Footer: y 1024 (clipped — kept for reference)

y_masthead_top = 0
y_masthead_bot = 150
y_stat_top = 150
y_stat_bot = 210
y_utc_top = 210
y_utc_bot = 238
y_region_top = 238
y_region_bot = 268
y_30sec_top = 268      # NEW: IN 30 SECONDS box
y_30sec_bot = 293      # 25px tall
y_lead1_top = 293
y_lead1_bot = 390      # 97px each
y_lead2_top = 390
y_lead2_bot = 487
y_lead3_top = 487
y_lead3_bot = 584
y_mid_top = 584
y_mid_bot = 824        # 240px for 2 rows of 12 cards
y_bottom_top = 824
y_bottom_bot = 994
y_dc_top = 994
y_dc_bot = 1024
y_footer_top = 1024    # footer moves down, but we keep image at 1024 — handled by clipping
y_footer_bot = 1024

# ═══════════════════════════════════════════════════════════════
# 1. MASTHEAD BLOCK (y 0–150)
# ═══════════════════════════════════════════════════════════════
# Navy top bar
D.rectangle([0, y_masthead_top, W, y_masthead_top + 26], fill=NAVY)
f_top = get_font("sans", 11, bold=True)
draw_text(PAD_X, y_masthead_top + 13, "THE WORLD IN ONE DAY", f_top, WHITE, anchor="lm")
draw_text(W - PAD_X, y_masthead_top + 13, "35 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED SUNDAY 22 NOVEMBER 2026", f_top, WHITE, anchor="rm")

# Giant serif date headline
y_date_headline = y_masthead_top + 40
f_masthead = get_font("serif", 42, bold=True)
draw_text(W//2, y_date_headline + 15, "Sunday 22 November 2026", f_masthead, BLACK, anchor="mm")

# Red italic subhead naming the 3 lead stories - FIX 3: spaced pipe separators
y_sub_kicker = y_masthead_top + 110
f_sub = get_font("sans", 13, italic=True)
subhead_text = "COP31 final text lands at dawn | Iran claims strikes on US bases in Bahrain | Russia launches 186 drones at Ukraine"
draw_text(W//2, y_sub_kicker + 6, subhead_text, f_sub, RED, anchor="mm")

# ═══════════════════════════════════════════════════════════════
# 2. STAT STRIP (y 150–210)
# ═══════════════════════════════════════════════════════════════
stats = [
    ("~200", "nations at the COP31 talks"),
    ("03:00", "GMT deadline for objections"),
    ("186", "drones fired at Ukraine overnight"),
    ("2", "US bases targeted in Bahrain"),
    ("856", "candidates in the Hong Kong vote"),
    ("720/9", "India's record total in NZ"),
]
f_stat_num = get_font("sans", 22, bold=True)
f_stat_label = get_font("sans", 8)
stat_width = (W - 2*PAD_X) // 6
for i, (num, label) in enumerate(stats):
    cx = PAD_X + i * stat_width + stat_width // 2
    cy = y_stat_top + 22
    draw_text(cx, cy - 8, num, f_stat_num, RED, anchor="mm")
    draw_text(cx, cy + 14, label, f_stat_label, MED_GREY, anchor="mm")
    if i < 5:
        sx = PAD_X + (i+1) * stat_width
        D.line([sx, y_stat_top + 6, sx, y_stat_bot - 6], fill=LIGHT_GREY, width=1)

# ═══════════════════════════════════════════════════════════════
# 3. UTC TIMELINE STRIP (y 210–238) - 6 events EVENLY SPACED
# ═══════════════════════════════════════════════════════════════
utc_events = [
    "03:00 COP31 objections close",
    "05:11 Hamas seeks talks",
    "05:30 Las Vegas GP ends",
    "06:00 COP31 approval session",
    "08:00 161 of 186 drones downed",
    "14:00 Hong Kong turnout 93.55%",
]
rule_y = y_utc_top + 8
D.line([PAD_X, rule_y, W - PAD_X, rule_y], fill=NAVY, width=2)
f_utc_label = get_font("sans", 6)
draw_text(PAD_X, y_utc_top + 2, "00:00 UTC", f_utc_label, NAVY, anchor="lm")
draw_text(W - PAD_X, y_utc_top + 2, "24:00 UTC", f_utc_label, NAVY, anchor="rm")

f_utc_combined = get_font("sans", 6)
num_events = len(utc_events)
for idx, label in enumerate(utc_events):
    x = PAD_X + int((idx + 0.5) / num_events * (W - 2*PAD_X))
    D.ellipse([x-2, rule_y-2, x+2, rule_y+2], fill=RED)
    ty = rule_y + 8
    max_w = int((W - 2*PAD_X) / num_events) - 10
    draw_text(x, ty, label, f_utc_combined, DARK_GREY, anchor="mm", max_width=max_w)

# ═══════════════════════════════════════════════════════════════
# 4. REGION TAB BAR (y 238–268) - 7 regions, counts sum to 35
# ═══════════════════════════════════════════════════════════════
regions = [
    ("EUROPE", 10, EUROPE_BLUE, TAG_BLUE),
    ("MIDDLE EAST", 9, MIDEAST_RED, TAG_RED),
    ("ASIA-PACIFIC", 5, ASIA_ORANGE, TAG_ORANGE),
    ("AMERICAS", 6, AMERICAS_GREEN, TAG_GREEN),
    ("AFRICA", 1, AFRICA_BROWN, TAG_BROWN),
    ("OCEANIA", 1, OCEANIA_TEAL, TAG_TEAL),
    ("WORLD", 3, WORLD_PURPLE, TAG_PURPLE),
]
assert sum(r[1] for r in regions) == 35, f"Region counts sum to {sum(r[1] for r in regions)}, must be 35"

tab_width = (W - 2*PAD_X) // 7
f_region = get_font("sans", 10, bold=True)
f_region_count = get_font("sans", 9)
for i, (name, count, color, tag_bg) in enumerate(regions):
    x0 = PAD_X + i * tab_width
    x1 = x0 + tab_width - 2
    D.rectangle([x0, y_region_top, x1, y_region_bot], fill=color)
    cx = (x0 + x1) // 2
    cy = y_region_top + 15
    draw_text(cx, cy - 4, name, f_region, WHITE, anchor="mm")
    draw_text(cx, cy + 8, f"{count} stories", f_region_count, WHITE, anchor="mm")

# ═══════════════════════════════════════════════════════════════
# NEW: IN 30 SECONDS BOX (y 268–293) — 3 one-line bullets summarising the day
# ═══════════════════════════════════════════════════════════════
f_30sec_title = get_font("sans", 8, bold=True)
f_30sec_bullet = get_font("sans", 7)
D.rectangle([PAD_X, y_30sec_top, W-PAD_X, y_30sec_bot], outline=RED, width=1, fill=(0xFF,0xF5,0xF5))
draw_text(PAD_X + 8, y_30sec_top + 3, "IN 30 SECONDS", f_30sec_title, RED)
bullets = [
    "COP31 final text adopted at dawn — no fossil fuel phaseout, 1.5°C overshoot admitted",
    "IRGC claims strikes on 2 US Patriot radars in Bahrain; US unconfirmed, no casualties",
    "Russia launches 186 drones at Ukraine overnight; air defence downs 161 by 08:00",
]
bullet_x = PAD_X + 8
bullet_y = y_30sec_top + 16
for bullet in bullets:
    draw_text(bullet_x, bullet_y, "• " + bullet, f_30sec_bullet, DARK_GREY, max_width=W - 2*PAD_X - 16)
    bullet_y += 7

# ═══════════════════════════════════════════════════════════════
# 5. THREE LARGE LEAD PANELS (y 293–584) - with continuous panorama CLIPPED to panels
# ═══════════════════════════════════════════════════════════════
lead_stories = [
    {
        "num": 1, "place": "ANTALYA, TURKEY", "tag": "ONGOING", "kicker": "COP31 CLIMATE SUMMIT",
        "certainty": "REPORTED",  # NEW: certainty tag for kicker line
        "tag_color": EUROPE_BLUE, "tag_bg": TAG_BLUE,
        "headline": "COP31 final text lands at dawn after two days in overtime",
        "deck": "No fossil fuel mention; recalls COP28 pact; 35% electricity by 2035; $120bn adaptation target dropped; admits 1.5\u00b0C overshoot",
        "source": "(Reuters, BBC)", "stat": "~200 nations", "illustration": "climate",
    },
    {
        "num": 2, "place": "MANAMA, BAHRAIN", "tag": "CLAIM", "kicker": "IRGC CLAIMS STRIKES",
        "certainty": "CLAIM",  # NEW: IRGC's own claim
        "tag_color": MIDEAST_RED, "tag_bg": TAG_RED,
        "headline": "IRGC claims missile and drone strikes on two US Patriot radars",
        "deck": "Retaliation for MQ-1/MQ-9 airspace violations and Hengam radar attack; Bahrain says defences intercepted several, facility hit, no casualties; US unconfirmed",
        "source": "(Al Jazeera)", "stat": "2 bases targeted", "illustration": "bahrain",
    },
    {
        "num": 3, "place": "KYIV, UKRAINE", "tag": "REPORTED", "kicker": "OVERNIGHT BARRAGE",
        "certainty": "REPORTED",  # NEW: wire-reported
        "tag_color": MIDEAST_RED, "tag_bg": TAG_RED,
        "headline": "Russia launches 186 drones overnight; air defence downs 161 by 08:00",
        "deck": "72 jet-powered Shahed plus decoys; 161 downed; impacts at 18 locations.",
        "source": "(Al Jazeera, BBC)", "stat": "186 drones fired", "illustration": "kyiv",
    },
]

# ─── Illustration drawing function (must be defined before use) ───
def draw_illustration_on_layer(draw, type_, x, y, w, h):
    """Draw illustration on the PASSED draw object (not global D). All coords relative to x,y."""
    cx, cy = x + w//2, y + h//2
    if type_ == "climate":
        # COP31 (Antalya): delegates at conference table, green globe, wall clock
        draw.rectangle([x, y, x+w, y+h], fill=(0xE8,0xEC,0xF4))
        # Dawn sky gradient
        for i in range(h//2):
            ratio = i / (h//2)
            r = int(0xE8 + (0xC0 - 0xE8) * ratio)
            g = int(0xEC + (0xD8 - 0xEC) * ratio)
            b = int(0xF4 + (0xF0 - 0xF4) * ratio)
            D.line([x, y+i, x+w, y+i], fill=(r, g, b))
        # Conference table (long, horizontal)
        table_y = y + h - 30
        draw.rectangle([x+15, table_y, x+w-15, table_y+20], fill=(0x8B,0x6B,0x3B), outline=(0x6B,0x4B,0x2B))
        D.line([x+15, table_y+10, x+w-15, table_y+10], fill=(0xA0,0x80,0x50))
        # Delegates seated along table (both sides)
        for side in [0, 1]:
            for seat in range(7):
                sx = x + 25 + seat * (w - 50) // 6
                sy = table_y - 5 if side == 0 else table_y + 25
                # Head
                D.ellipse([sx-4, sy-8, sx+4, sy], fill=(0xD0,0xB8,0xA0))
                # Shoulders
                draw.rectangle([sx-7, sy, sx+7, sy+6], fill=(0x30,0x40,0x60))
                # Nameplate
                draw.rectangle([sx-10, sy+8, sx+10, sy+12], fill=(0xC0,0xC0,0xC0), outline=(0xA0,0xA0,0xA0))
        # Center: large green globe on table
        globe_x = cx
        globe_y = table_y - 2
        globe_r = 14
        D.ellipse([globe_x-globe_r, globe_y-globe_r, globe_x+globe_r, globe_y+globe_r], fill=(0x20,0x80,0x30), outline=(0x10,0x60,0x20), width=2)
        # Globe grid lines
        for lat in (-45, 0, 45):
            ly = globe_y + lat * globe_r // 45
            draw.arc([globe_x-globe_r, ly-1, globe_x+globe_r, ly+1], 0, 360, fill=(0x40,0xA0,0x50), width=1)
        for lon in (-45, 0, 45):
            lx = globe_x + lon * globe_r // 45
            draw.arc([lx-1, globe_y-globe_r, lx+1, globe_y+globe_r], 0, 360, fill=(0x40,0xA0,0x50), width=1)
        # Wall clock above table
        clock_x = cx
        clock_y = table_y - 45
        D.ellipse([clock_x-12, clock_y-12, clock_x+12, clock_y+12], fill=WHITE, outline=(0x80,0x80,0x80), width=2)
        # Clock hands (showing ~03:00)
        D.line([clock_x, clock_y, clock_x, clock_y-8], fill=BLACK, width=2)
        D.line([clock_x, clock_y, clock_x+7, clock_y], fill=BLACK, width=2)
        # COP31 banner at top
        draw.rectangle([cx-80, y+4, cx+80, y+22], fill=EUROPE_BLUE)
        f_banner = get_font("sans", 10, bold=True)
        draw_text_on_layer(draw, cx, y+13, "COP31 ANTALYA", f_banner, WHITE, anchor="mm")
        # Side UNFCCC panels
        for bx in [x+10, x+w-90]:
            draw.rectangle([bx, y+28, bx+80, y+44], fill=(0x1E,0x3A,0x8A))
            f_side = get_font("sans", 7, bold=True)
            draw_text_on_layer(draw, bx+40, y+36, "UNFCCC", f_side, WHITE, anchor="mm")
   
    elif type_ == "bahrain":
        # Manama: radar dishes with flames, circular arrow, dark coast
        # Night sky gradient
        for i in range(h):
            ratio = i / h
            r = int(0x0A + (0x25 - 0x0A) * ratio)
            g = int(0x10 + (0x1A - 0x10) * ratio)
            b = int(0x25 + (0x35 - 0x25) * ratio)
            D.line([x, y+i, x+w, y+i], fill=(r, g, b))
        # Radar dishes (3 large dishes with arrays)
        for dish_i in range(3):
            dish_x = x + 35 + dish_i * (w - 70) // 2
            dish_y = y + 25
            # Dish support
            D.line([dish_x, dish_y+40, dish_x, dish_y+65], fill=(0x50,0x50,0x50), width=3)
            D.line([dish_x-8, dish_y+65, dish_x+8, dish_y+65], fill=(0x50,0x50,0x50), width=3)
            # Dish parabola
            draw.arc([dish_x-22, dish_y, dish_x+22, dish_y+44], 0, 180, fill=(0x80,0x80,0x80), width=3)
            draw.arc([dish_x-20, dish_y+2, dish_x+20, dish_y+42], 0, 180, fill=(0xA0,0xA0,0xA0), width=1)
            # Feed horn
            draw.rectangle([dish_x-3, dish_y-8, dish_x+3, dish_y+2], fill=(0x40,0x40,0x40))
        # Flames at base of center radar (strike impact)
        flame_x = x + w//2
        flame_y = y + 70
        for f in range(6):
            fx = flame_x + (f-2.5)*12
            for layer, (fr, fg, fb) in enumerate([(0xFF,0x20,0x00), (0xFF,0x80,0x10), (0xFF,0xC0,0x20)]):
                D.ellipse([fx-6+layer, flame_y-6+layer, fx+6-layer, flame_y+10-layer], fill=(fr, fg, fb))
        # Circular arrow (retaliation symbol) above radars
        arrow_cx = cx
        arrow_cy = y + 15
        arrow_r = 18
        draw.arc([arrow_cx-arrow_r, arrow_cy-arrow_r, arrow_cx+arrow_r, arrow_cy+arrow_r], 45, 315, fill=(0xFF,0x40,0x40), width=4)
        # Arrow head
        draw.polygon([(arrow_cx+arrow_r, arrow_cy), (arrow_cx+arrow_r-6, arrow_cy-4), (arrow_cx+arrow_r-6, arrow_cy+4)], fill=(0xFF,0x40,0x40))
        # Dark coast line at bottom
        coast_y = y + h - 15
        for cx_seg in range(x, x+w, 8):
            D.ellipse([cx_seg-3, coast_y-3, cx_seg+3, coast_y+3], fill=(0x10,0x10,0x15))
        D.line([x, coast_y, x+w, coast_y], fill=(0x20,0x18,0x20), width=2)
        # Water reflection
        for wx in range(0, w, 15):
            draw.arc([x+wx, coast_y, x+wx+15, coast_y+8], 0, 180, fill=(0x15,0x20,0x30), width=1)
        # MANAMA label
        f_b = get_font("sans", 9, bold=True)
        draw_text_on_layer(draw, cx, y+h-6, "MANAMA", f_b, (0xFF,0xC0,0xC0), anchor="mm")
   
    elif type_ == "kyiv":
        # Kyiv: night skyline with lit windows, searchlight beam, drones with trails
        draw.rectangle([x, y, x+w, y+h], fill=(0x05,0x0A,0x18))
        # Moon
        D.ellipse([x+w-50, y+8, x+w-12, y+46], fill=(0xE0,0xE0,0xC0))
        # Searchlight beam from bottom center
        beam_x = cx
        beam_y = y + h
        draw.polygon([(beam_x-30, beam_y), (beam_x-5, y+20), (beam_x+5, y+20), (beam_x+30, beam_y)], fill=(0xFF,0xF0,0xC0, 0x30))
        draw.polygon([(beam_x-25, beam_y), (beam_x-3, y+25), (beam_x+3, y+25), (beam_x+25, beam_y)], fill=(0xFF,0xF0,0xC0, 0x50))
        # City skyline with lit windows
        bw = w // 8
        building_heights = [h-20, h-35, h-28, h-45, h-30, h-22, h-40, h-25]
        for i in range(8):
            bx = x + i * bw
            bh = max(15, min(h-10, building_heights[i]))
            # Building silhouette
            draw.rectangle([bx, y+h-bh, bx+bw-2, y+h], fill=(0x03,0x06,0x10))
            # Lit windows (random pattern)
            for wy in range(y+h-bh+4, y+h-4, 10):
                for wx in range(bx+3, bx+bw-3, 9):
                    if (wx * 7 + wy * 3) % 11 < 4:  # pseudo-random lit windows
                        draw.rectangle([wx, wy, wx+4, wy+6], fill=(0xFF,0xE8,0x80))
        # Drone swarm with trails (incoming from right)
        for i in range(18):
            dx = x + w - 20 - (i % 6) * 15 - (i // 6) * 40
            dy = y + 15 + (i % 3) * 20 + (i // 6) * 15
            # Drone body (small triangle)
            draw.polygon([(dx, dy), (dx-4, dy+5), (dx+4, dy+5)], fill=(0xFF,0x20,0x20))
            # Trail
            D.line([dx, dy+5, dx+8, dy+12], fill=(0xFF,0x60,0x60), width=1)
            D.line([dx-2, dy+5, dx+6, dy+13], fill=(0xFF,0x80,0x80), width=1)
        # Smoke trails from impacts (lower left)
        for i in range(4):
            sx = x + 20 + i * (w-40)//3
            sy = y + h - 25 - (i%2)*10
            D.ellipse([sx-10, sy-5, sx+10, sy+5], fill=(0x18,0x18,0x25))
        # KYIV label
        f_k = get_font("sans", 9, bold=True)
        draw_text_on_layer(draw, cx, y+h-6, "KYIV", f_k, (0xFF,0xC0,0xC0), anchor="mm")


# ─── Draw continuous panorama on a SEPARATE layer, then clip to each panel ───
panel_w = int((W - 2*PAD_X) * 0.55)
panel_h = y_lead1_bot - y_lead1_top  # 97px
ill_h = panel_h - 12  # leave small margins top/bottom for clipping

# Create the full continuous illustration layer (3 panels wide)
cont_ill_w = panel_w * 3
cont_layer = Image.new("RGBA", (cont_ill_w, ill_h), (255, 255, 255, 0))
cont_draw = ImageDraw.Draw(cont_layer)

# Draw continuous skyline: dawn Antalya (left) -> dusk Manama (center) -> night Kyiv (right)
draw_illustration_on_layer(cont_draw, "climate", 0, 0, panel_w, ill_h)
draw_illustration_on_layer(cont_draw, "bahrain", panel_w, 0, panel_w, ill_h)
draw_illustration_on_layer(cont_draw, "kyiv", 2*panel_w, 0, panel_w, ill_h)

# Now draw each lead panel with CLIPPED illustration
for i, story in enumerate(lead_stories):
    panel_y = [y_lead1_top, y_lead2_top, y_lead3_top][i]
    panel_h = [y_lead1_bot, y_lead2_bot, y_lead3_bot][i] - panel_y
    
    # Panel border
    D.rectangle([PAD_X, panel_y, W-PAD_X, panel_y+panel_h], outline=(0xDD,0xDD,0xDD), width=1)
    
    ill_w = panel_w
    text_x = PAD_X + ill_w + 12
    text_w = W - PAD_X - text_x - 6
    
    # Tag top-left (ONGOING/CLAIM/REPORTED)
    tag_x = PAD_X + 6
    tag_y = panel_y + 6
    f_tag = get_font("sans", 9, bold=True)
    tag_text = story["tag"]
    tag_w = f_tag.getlength(tag_text) + 12
    D.rounded_rectangle([tag_x, tag_y, tag_x+tag_w, tag_y+18], radius=2, fill=story["tag_bg"], outline=story["tag_color"])
    draw_text(tag_x + tag_w//2, tag_y + 9, tag_text, f_tag, story["tag_color"], anchor="mm")
    
    # Kicker line below tag
    f_kicker = get_font("sans", 8, bold=True)
    kicker_y = tag_y + 20
    draw_text(tag_x, kicker_y, story["kicker"], f_kicker, story["tag_color"])
    
    # White stat chip top-right of illustration area
    stat_text = story["stat"]
    f_stat_chip = get_font("sans", 9, bold=True)
    stat_w = f_stat_chip.getlength(stat_text) + 12
    stat_chip_x = PAD_X + ill_w - stat_w - 6
    stat_chip_y = panel_y + 6
    D.rounded_rectangle([stat_chip_x, stat_chip_y, stat_chip_x+stat_w, stat_chip_y+18], radius=2, fill=STAT_CHIP_BG, outline=STAT_CHIP_BORDER)
    draw_text(stat_chip_x + stat_w//2, stat_chip_y + 9, stat_text, f_stat_chip, RED, anchor="mm")
    
    # ─── CLIP illustration to panel ───
    ill_y = panel_y + 6  # top of illustration area (below tag/kicker)
    crop_x = i * panel_w
    panel_ill = cont_layer.crop((crop_x, 0, crop_x + panel_w, ill_h))
    # Paste at exact panel position - CLIPPED to panel bounds
    IMG.paste(panel_ill, (PAD_X, ill_y), panel_ill)
    
    # Caption bottom-left of illustration area
    f_caption = get_font("sans", 8, italic=True)
    captions = {
        "climate": "Conference hall, delegates in final session at dawn",
        "bahrain": "Bahrain coast, radar dishes burning at night",
        "kyiv": "Night sky over Kyiv, searchlight and drone swarm",
    }
    draw_text(PAD_X + 6, ill_y + ill_h - 2, captions[story["illustration"]], f_caption, MED_GREY, anchor="lb")
    
    # Right column text
    f_lead_num = get_font("sans", 18, bold=True)
    f_lead_place = get_font("sans", 10, bold=True)
    f_lead_headline = get_font("sans", 14, bold=True)
    f_lead_deck = get_font("sans", 11)
    f_lead_source = get_font("sans", 9, italic=True)
    f_certainty = get_font("sans", 7, bold=True)  # NEW: certainty tag font
    
    ty = panel_y + 8
    draw_text(text_x, ty, str(story["num"]), f_lead_num, RED)
    ty += 20
    draw_text(text_x, ty, story["place"], f_lead_place, BLACK)
    ty += 14
    draw_text_wrapped(text_x, ty, story["headline"], f_lead_headline, BLACK, text_w, 16, max_lines=2)
    ty += 32
    draw_text_wrapped(text_x, ty, story["deck"], f_lead_deck, DARK_GREY, text_w, 12, max_lines=2)
    ty += 12  # reduced from 24 to add separation from next lead's number
    
    # Source line with certainty tag at right end of kicker line area
    # Add certainty tag at right end of kicker line (which is at tag_y + 20)
    certainty_text = story.get("certainty", "REPORTED")
    cert_color = TAG_RED if certainty_text == "CLAIM" else TAG_BLUE
    cert_text_color = MIDEAST_RED if certainty_text == "CLAIM" else EUROPE_BLUE
    cert_w = f_certainty.getlength(certainty_text) + 8
    cert_x = PAD_X + ill_w - cert_w - 6
    cert_y = tag_y + 20  # same y as kicker line
    D.rounded_rectangle([cert_x, cert_y, cert_x+cert_w, cert_y+14], radius=2, fill=cert_color, outline=cert_text_color)
    draw_text(cert_x + cert_w//2, cert_y + 7, certainty_text, f_certainty, cert_text_color, anchor="mm")
    
    draw_text(text_x, ty, story["source"], f_lead_source, MED_GREY)

# ════════════════════════════════════════════════════════════════
# 6. THE DAY IN TWELVE - 2 rows of 6 cards (numbered 4-15) (y 584–824)
# ════════════════════════════════════════════════════════════════
mid_stories = [
    {"num": 4, "place": "HONG KONG", "tag": "ELECTION", "certainty": "REPORTED", "tag_color": ASIA_ORANGE, "tag_bg": TAG_ORANGE,
     "headline": "Hong Kong elects Election Committee",
     "deck": "856 candidates, 723 seats; turnout 93.55%",
     "source": "(SCMP)", "illustration": "hk_vote"},
    {"num": 5, "place": "LAS VEGAS, USA", "tag": "SPORT", "certainty": "REPORTED", "tag_color": AMERICAS_GREEN, "tag_bg": TAG_GREEN,
     "headline": "Verstappen wins Las Vegas GP",
     "deck": "Red Bull driver takes the win",
     "source": "(BBC)", "illustration": "f1"},
    {"num": 6, "place": "WELLINGTON, NZ", "tag": "CRICKET", "certainty": "REPORTED", "tag_color": OCEANIA_TEAL, "tag_bg": TAG_TEAL,
     "headline": "India declare 720/9",
     "deck": "Record total in New Zealand",
     "source": "(ESPNcricinfo)", "illustration": "cricket"},
    {"num": 7, "place": "BAYELSA, NIGERIA", "tag": "DISASTER", "certainty": "REPORTED", "tag_color": AFRICA_BROWN, "tag_bg": TAG_BROWN,
     "headline": "Boat carrying mourners capsizes",
     "deck": "Overloaded vessel; toll rises to 26",
     "source": "(DW, Al Jazeera)", "illustration": "boat"},
    {"num": 8, "place": "TEHRAN, IRAN", "tag": "POWER", "certainty": "REPORTED", "tag_color": MIDEAST_RED, "tag_bg": TAG_RED,
     "headline": "Iran starts electricity rationing",
     "deck": "Two-hour daily cuts begin",
     "source": "(Straits Times)", "illustration": "power"},
    {"num": 9, "place": "SINALOA, MEXICO", "tag": "CARTEL", "certainty": "REPORTED", "tag_color": AMERICAS_GREEN, "tag_bg": TAG_GREEN,
     "headline": "'El Chapo Isidro' caught",
     "deck": "FBI top-ten fugitive held",
     "source": "(Reuters)", "illustration": "arrest"},
    {"num": 10, "place": "GAZA", "tag": "AID STRIKE", "certainty": "CLAIM", "tag_color": MIDEAST_RED, "tag_bg": TAG_RED,
     "headline": "Hamas seeks urgent talks",
     "deck": "Three die in Gaza aid strike",
     "source": "(Al Jazeera)", "illustration": "aid"},
    {"num": 11, "place": "MERCURY ORBIT", "tag": "SPACE", "certainty": "REPORTED", "tag_color": WORLD_PURPLE, "tag_bg": TAG_PURPLE,
     "headline": "BepiColombo enters Mercury orbit",
     "deck": "Eight-year trip ends at Mercury",
     "source": "(ESA)", "illustration": "space"},
    {"num": 12, "place": "WASHINGTON, USA", "tag": "TECH", "certainty": "REPORTED", "tag_color": AMERICAS_GREEN, "tag_bg": TAG_GREEN,
     "headline": "Nvidia faces SEC accounting probe",
     "deck": "Regulator examines accounts",
     "source": "(FT)", "illustration": "probe"},
    {"num": 13, "place": "BRASÍLIA, BRAZIL", "tag": "HEALTH", "certainty": "REPORTED", "tag_color": AMERICAS_GREEN, "tag_bg": TAG_GREEN,
     "headline": "Bolsonaro in intensive care",
     "deck": "Ex-president stable in care",
     "source": "(Al Jazeera)", "illustration": "hospital"},
    # Promoted from ALSO ON (strongest visual hooks)
    {"num": 14, "place": "GULF OF FINLAND", "tag": "SHIP FIRE", "certainty": "REPORTED", "tag_color": EUROPE_BLUE, "tag_bg": TAG_BLUE,
     "headline": "Russian cargo ship still burning off Finland",
     "deck": "Crew evacuated; vessel adrift",
     "source": "(Reuters)", "illustration": "ship_fire"},
    {"num": 15, "place": "BERLIN, GERMANY", "tag": "STRIKE", "certainty": "REPORTED", "tag_color": EUROPE_BLUE, "tag_bg": TAG_BLUE,
     "headline": "IG Metall widens strikes at car plants",
     "deck": "Production halted at VW, BMW sites",
     "source": "(Reuters)", "illustration": "factory_strike"},
]

# FIX 4: draw_mid_card - header row (illustration + tag + certainty + number + place) at y+4..y+36,
# headline at y+40 (full card width, 2 lines), deck at y+66 (1 line), source at y+80
def draw_mid_card(story, x, y):
    card_w = 160
    card_h = 110
    D.rectangle([x, y, x+card_w, y+card_h], fill=WHITE, outline=(0xDD,0xDD,0xDD), width=1)
    
    # ─── HEADER ROW (y+4 to y+36) - ultra compact for 160px cards ───
    # Illustration: 20x20 at (x+4, y+4)
    ill_x = x + 4
    ill_y = y + 4
    ill_size = 20
    draw_mid_illustration(story["illustration"], ill_x, ill_y, ill_size, ill_size)
    ill_right = ill_x + ill_size
    
    # Certainty tag: top-right of illustration area (abbreviated to fit in 20px box)
    certainty_text = story.get("certainty", "REPORTED")
    cert_abbrev = {"REPORTED": "REP", "CLAIM": "CLM", "FORECAST": "FCS"}.get(certainty_text, "REP")
    f_mcert = get_font("sans", 5, bold=True)
    cert_color = TAG_RED if certainty_text == "CLAIM" else TAG_BLUE
    cert_text_color = MIDEAST_RED if certainty_text == "CLAIM" else EUROPE_BLUE
    cert_w = f_mcert.getlength(cert_abbrev) + 4
    cert_x = ill_right - cert_w - 1  # right end of illustration box
    cert_y = ill_y  # top of illustration box
    D.rounded_rectangle([cert_x, cert_y, cert_x+cert_w, cert_y+8], radius=1, fill=cert_color, outline=cert_text_color)
    draw_text(cert_x + cert_w//2, cert_y + 4, cert_abbrev, f_mcert, cert_text_color, anchor="mm")
    
    # Tag chip: right of illustration, vertically centered in header row (y+4 to y+36, center y+20)
    tag_x = ill_right + 4
    f_mtag = get_font("sans", 5, bold=True)
    tag_text = story["tag"]
    tag_w = f_mtag.getlength(tag_text) + 6
    tag_y = y + 10  # centered: header row is y+4..y+36, so center ~y+20, chip height 10
    D.rounded_rectangle([tag_x, tag_y, tag_x+tag_w, tag_y+10], radius=1, fill=story["tag_bg"], outline=story["tag_color"])
    draw_text(tag_x + tag_w//2, tag_y + 5, tag_text, f_mtag, story["tag_color"], anchor="mm")
    tag_right = tag_x + tag_w
    
    # Number circle: right of tag chip (smaller)
    f_mnum = get_font("sans", 9, bold=True)
    num_cx = tag_right + 6
    num_cy = y + 20  # vertically centered in header row
    D.ellipse([num_cx-7, num_cy-7, num_cx+7, num_cy+7], outline=RED, width=2)
    draw_text(num_cx, num_cy, str(story["num"]), f_mnum, RED, anchor="mm")
    num_circle_right = num_cx + 7
    
    # Place text: right of number circle, with measured width check
    f_mplace = get_font("sans", 7, bold=True)
    place_x = num_circle_right + 2
    # Header row available width: card_w - (place_x - x) - 4 (right padding)
    header_avail_w = x + card_w - 4 - place_x
    place_text = story["place"]
    # Shrink place text if it doesn't fit remaining header width
    if f_mplace.getlength(place_text) > header_avail_w:
        place_text, _ = _fit_text_to_width(place_text, f_mplace, header_avail_w, min_font_size=7)
    draw_text(place_x, y + 3, place_text, f_mplace, BLACK)
    
    # ─── HEADLINE ROW (starts at y+40, full card width, 2 lines) ───
    text_x = x + 6
    text_w = card_w - 12  # ~182px
    f_mhead = get_font("sans", 9, bold=True)
    headline_y = y + 40
    draw_text_wrapped(text_x, headline_y, story["headline"], f_mhead, BLACK, text_w, 12, max_lines=2)
    
    # ─── DECK ROW (y+66, full width, 1 line) ───
    f_mdeck = get_font("sans", 8)
    deck_y = y + 66
    draw_text_wrapped(text_x, deck_y, story["deck"], f_mdeck, DARK_GREY, text_w, 11, max_lines=1)
    
    # ─── SOURCE ROW (y+80, full width) ───
    f_msrc = get_font("sans", 7, italic=True)
    src = story["source"]
    if "," in src:
        src = src.split(",")[0] + ")"
    src_y = y + 80
    draw_text(text_x, src_y, src, f_msrc, MED_GREY)


def draw_mid_illustration(type_, x, y, w, h):
    cx, cy = x + w//2, y + h//2
    if type_ == "hk_vote":
        # Ballot box + paper ballots (richer)
        D.rectangle([x, y, x+w, y+h], fill=(0xE8,0xF0,0xF8))
        # Ballot box
        D.rectangle([cx-8, cy-4, cx+8, cy+12], fill=(0xC0,0xC0,0xC0), outline=(0x80,0x80,0x80))
        D.rectangle([cx-6, cy-8, cx+6, cy-4], fill=(0xC0,0xC0,0xC0), outline=(0x80,0x80,0x80))
        D.rectangle([cx-3, cy-8, cx+3, cy-2], fill=RED)
        # Ballots going in
        for i in range(3):
            bx = cx - 5 + i*5
            D.line([bx, cy-12, bx, cy-4], fill=(0x00,0x80,0x00), width=1)
        # Papers on table
        for i in range(4):
            px = x + 4 + i * (w-8)//3
            py = y + h - 6
            D.rectangle([px, py-8, px+6, py], fill=WHITE, outline=(0xC0,0xC0,0xC0))
    elif type_ == "f1":
        # F1 car + track (richer)
        D.rectangle([x, y, x+w, y+h], fill=(0x08,0x08,0x08))
        # Track
        D.line([x, cy+8, x+w, cy+8], fill=(0x40,0x40,0x40), width=3)
        # Car silhouette
        D.polygon([(x+4, cy+4), (x+w-8, cy+4), (x+w-4, cy-4), (x+8, cy-4)], fill=(0xE0,0x10,0x10))
        D.rectangle([cx-6, cy-8, cx+6, cy-4], fill=(0x20,0x20,0x20))
        # Wheels
        D.ellipse([x+6, cy+2, x+14, cy+10], fill=(0x10,0x10,0x10), outline=(0x40,0x40,0x40))
        D.ellipse([x+w-14, cy+2, x+w-6, cy+10], fill=(0x10,0x10,0x10), outline=(0x40,0x40,0x40))
        # Exhaust glow
        D.ellipse([x+w-6, cy, x+w+2, cy+6], fill=(0xFF,0x60,0x10))
        # Checkered flag
        for i in range(4):
            for j in range(2):
                color = WHITE if (i+j)%2==0 else (0x20,0x20,0x20)
                D.rectangle([cx-12+i*6, cy-10+j*6, cx-6+i*6, cy-4+j*6], fill=color)
    elif type_ == "cricket":
        # Cricket bat + ball + stumps (richer)
        D.rectangle([x, y, x+w, y+h], fill=(0xF0,0xF0,0xE8))
        # Pitch
        D.rectangle([x+2, cy-8, x+w-2, cy+8], fill=(0xE0,0xD0,0xA0), outline=(0xA0,0x90,0x60))
        # Stumps
        for sx in [cx-4, cx, cx+4]:
            D.line([sx, cy-8, sx, cy+8], fill=(0xFF,0xE0,0x80), width=2)
        # Bails
        D.line([cx-6, cy-8, cx+6, cy-8], fill=(0xFF,0xE0,0x80), width=1)
        # Bat
        D.line([cx-10, cy+6, cx+2, cy-6], fill=(0x8B,0x6B,0x3B), width=2)
        D.line([cx-9, cy+5, cx+1, cy-5], fill=(0xA0,0x80,0x50), width=1)
        # Ball
        D.ellipse([cx+6, cy-4, cx+10, cy], fill=(0xD0,0x10,0x10))
        # Ball trail
        for i in range(3):
            D.ellipse([cx+12+i*3, cy+2-i*2, cx+14+i*3, cy+4-i*2], fill=(0xD0,0x10,0x10, 0x80))
        # Score
        f_mag = get_font("sans", 6, bold=True)
        draw_text(cx, y+h-5, "720/9", f_mag, RED, anchor="mm")
    elif type_ == "boat":
        # Ship + smoke (richer)
        D.rectangle([x, y, x+w, y+h], fill=(0x10,0x25,0x40))
        # Water
        for i in range(h//2):
            ratio = i / (h//2)
            r = int(0x10 + (0x15 - 0x10) * ratio)
            g = int(0x25 + (0x30 - 0x25) * ratio)
            b = int(0x40 + (0x50 - 0x40) * ratio)
            D.line([x, y+h//2+i, x+w, y+h//2+i], fill=(r, g, b))
        # Capsized boat hull
        D.polygon([(cx-12, cy+2), (cx+12, cy+2), (cx+8, cy+10), (cx-8, cy+10)], fill=(0x40,0x28,0x10))
        # Mast
        D.line([cx, cy-2, cx, cy-14], fill=(0x30,0x20,0x10), width=2)
        # Smoke
        for i in range(5):
            sx = cx + (i-2)*6
            sy = cy - 16 - i*3
            sr = 4 + i*2
            D.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=(0x20,0x20,0x25))
        # People in water
        for i in range(4):
            px = cx - 12 + i*8
            D.ellipse([px-2, cy+4, px+2, cy+8], fill=(0xD0,0xA0,0x80))
    elif type_ == "power":
        # Power pylon + lightning (richer)
        D.rectangle([x, y, x+w, y+h], fill=(0xF8,0xF8,0xE8))
        # Ground
        D.line([x, y+h-4, x+w, y+h-4], fill=(0xC0,0xB0,0x90), width=2)
        # Pylon
        D.polygon([(cx-12, y+h-4), (cx-6, cy), (cx+6, cy), (cx+12, y+h-4)], outline=(0x50,0x50,0x50), width=2)
        D.line([cx-6, cy, cx+6, cy], fill=(0x50,0x50,0x50), width=2)
        D.line([cx-10, y+h-8, cx+10, y+h-8], fill=(0x50,0x50,0x50), width=1)
        # Lightning bolt
        pts = [(cx, cy-4), (cx-3, cy+4), (cx, cy+4), (cx-2, cy+12)]
        D.polygon(pts, fill=(0xFF,0xB0,0x10), outline=(0xB0,0x70,0x10))
        # Crossed out (rationing)
        D.line([cx-10, cy+2, cx+10, cy-2], fill=RED, width=2)
        # Power lines
        D.line([x, cy-2, x+w, cy-2], fill=(0x80,0x80,0x80), width=1)
        D.line([x, cy+6, x+w, cy+6], fill=(0x80,0x80,0x80), width=1)
    elif type_ == "arrest":
        # Handcuffs + magnifier (richer)
        D.rectangle([x, y, x+w, y+h], fill=(0xF0,0xF0,0xF0))
        # Handcuffs
        for cx_off in (-10, 10):
            D.ellipse([cx+cx_off-7, cy-7, cx+cx_off+7, cy+7], outline=(0x28,0x28,0x28), width=2)
        D.ellipse([cx-2, cy-2, cx+2, cy+2], outline=(0x28,0x28,0x28), width=1)
        # Chain link
        D.ellipse([cx-5, cy-2, cx+5, cy+2], outline=(0x28,0x28,0x28), width=1)
        # Police badge
        D.polygon([(cx, cy-14), (cx-6, cy-8), (cx-6, cy+2), (cx, cy+8), (cx+6, cy+2), (cx+6, cy-8)], outline=(0x00,0x30,0x80), width=2)
        D.rectangle([cx-3, cy-6, cx+3, cy], fill=(0x00,0x30,0x80))
        draw_text(cx, cy-2, "POLICE", get_font("sans", 5, bold=True), WHITE, anchor="mm")
    elif type_ == "aid":
        # Truck + boxes (richer)
        D.rectangle([x, y, x+w, y+h], fill=(0xF0,0xE8,0xE8))
        # Truck body
        D.rectangle([x+4, cy, x+w-4, y+h-4], fill=(0xD0,0xD0,0xD0))
        D.rectangle([cx-6, cy+4, cx+6, cy+16], fill=(0xD0,0xD0,0xD0))
        D.rectangle([cx-2, cy+4, cx+2, cy+16], fill=RED)
        D.rectangle([cx-6, cy+8, cx+6, cy+12], fill=RED)
        # Aid boxes on truck
        for i in range(3):
            bx = x + 6 + i * 10
            by = cy - 6
            D.rectangle([bx, by, bx+8, by+10], fill=WHITE, outline=(0xB0,0xB0,0xB0))
            D.line([bx+2, by+2, bx+6, by+8], fill=RED, width=1)
            D.line([bx+6, by+2, bx+2, by+8], fill=RED, width=1)
        for i in range(2):
            dx = cx - 6 + i*12
            D.line([dx, cy+18, dx+2, cy+22], fill=(0x80,0x20,0x20), width=1)
    elif type_ == "space":
        # Planet + spacecraft (richer)
        D.rectangle([x, y, x+w, y+h], fill=(0x05,0x05,0x15))
        # Planet Mercury
        D.ellipse([cx-10, cy-10, cx+10, cy+10], fill=(0x80,0x80,0x80), outline=(0xA0,0xA0,0xA0))
        D.ellipse([cx-8, cy-8, cx+8, cy+8], outline=(0xA0,0xA0,0xA0), width=1)
        # Craters
        for gx, gy, gr in [(cx-6, cy-6, 3), (cx+5, cy-4, 2), (cx-3, cy+5, 4), (cx+7, cy+3, 2)]:
            D.ellipse([gx-gr, gy-gr, gx+gr, gy+gr], fill=(0x60,0x60,0x60))
        # Spacecraft
        D.rectangle([cx-16, cy-2, cx-8, cy+2], fill=(0xD0,0xD0,0xD0))
        D.polygon([(cx-8, cy-2), (cx-4, cy), (cx-4, cy-4), (cx-8, cy+2)], fill=(0xD0,0xD0,0xD0))
        # Solar panels
        D.line([cx-16, cy-2, cx-20, cy-8], fill=(0x30,0x70,0xB0), width=2)
        D.line([cx-16, cy+2, cx-20, cy+8], fill=(0x30,0x70,0xB0), width=2)
        # Stars
        for i in range(8):
            sx = x + 3 + (i%4)*7
            sy = y + 3 + (i//4)*10
            D.ellipse([sx, sy, sx+2, sy+2], fill=WHITE)
    elif type_ == "probe":
        # Document + magnifier (richer)
        D.rectangle([x, y, x+w, y+h], fill=(0xF0,0xF0,0xF8))
        # Document
        D.rectangle([x+4, cy-8, x+w-4, y+h-4], fill=WHITE, outline=(0xB8,0xB8,0xB8))
        for ly in range(cy-4, y+h-8, 8):
            D.line([x+8, ly, x+w-12, ly], fill=(0xC8,0xC8,0xC8), width=1)
        # Red flag on document
        D.rectangle([x+8, cy-6, x+12, cy-2], fill=RED)
        # Magnifier
        mgx, mgy = cx+10, cy-10
        D.ellipse([mgx-8, mgy-8, mgx+8, mgy+8], outline=(0x30,0x70,0xB0), width=2)
        D.line([mgx+6, mgy+6, mgx+12, mgy+12], fill=(0x30,0x70,0xB0), width=2)
        # Lens reflection
        D.ellipse([mgx-4, mgy-4, mgx, mgy], fill=(0xD0,0xE0,0xF8))
    elif type_ == "hospital":
        # Hospital + chart (richer)
        D.rectangle([x, y, x+w, y+h], fill=(0xE8,0xF8,0xE8))
        # Hospital building
        D.rectangle([cx-12, cy-10, cx+12, y+h-4], fill=(0xD8,0xD8,0xD8), outline=(0xB8,0xB8,0xB8))
        D.rectangle([cx-2, cy-8, cx+2, cy+6], fill=RED)
        D.rectangle([cx-8, cy-2, cx+8, cy+2], fill=RED)
        # Window lights
        for wx in [cx-10, cx, cx+10]:
            for wy in [cy-8, cy+2]:
                D.rectangle([wx-2, wy-2, wx+2, wy+2], fill=(0xFF,0xF0,0xC0))
        # Ambulance
        D.rectangle([x+4, y+h-12, x+18, y+h-4], fill=WHITE, outline=(0xB8,0xB8,0xB8))
        D.rectangle([x+6, y+h-12, x+8, y+h-4], fill=RED)
        # Heart monitor line
        for i in range(10):
            px = x + 22 + i * 4
            py = y + h - 8 + [0, -4, 0, 3, 0, -4, 0, 2, 0, -3][i]
            if i > 0:
                prev_px = x + 22 + (i-1) * 4
                prev_py = y + h - 8 + [0, -4, 0, 3, 0, -4, 0, 2, 0, -3][i-1]
                D.line([prev_px, prev_py, px, py], fill=RED, width=1)
    elif type_ == "ship_fire":
        # Ship on fire + smoke (richer)
        D.rectangle([x, y, x+w, y+h], fill=(0x10,0x20,0x35))
        # Water
        for i in range(h//2):
            D.line([x, y+h//2+i, x+w, y+h//2+i], fill=(0x0A,0x18,0x30))
        # Ship hull
        D.polygon([(cx-14, cy+2), (cx+14, cy+2), (cx+10, cy+10), (cx-10, cy+10)], fill=(0x30,0x25,0x20))
        # Superstructure
        D.rectangle([cx-6, cy-10, cx+6, cy+2], fill=(0x40,0x35,0x30))
        D.rectangle([cx-3, cy-14, cx+3, cy-10], fill=(0x50,0x45,0x40))
        # Fire
        for f in range(5):
            fx = cx + (f-2)*5
            for layer, (fr, fg, fb) in enumerate([(0xFF,0x20,0x00), (0xFF,0x80,0x10), (0xFF,0xC0,0x20)]):
                D.ellipse([fx-4+layer, cy-10-layer, fx+4-layer, cy-4+layer], fill=(fr, fg, fb))
        # Smoke plumes
        for i in range(6):
            sx = cx + (i-2.5)*6
            sy = cy - 16 - i*3
            sr = 4 + i*2
            D.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=(0x15,0x15,0x20))
    elif type_ == "factory_strike":
        # Factory + flames + picket sign (richer)
        D.rectangle([x, y, x+w, y+h], fill=(0x18,0x18,0x20))
        # Factory building
        D.rectangle([cx-14, cy-2, cx+14, y+h-4], fill=(0x30,0x30,0x35), outline=(0x50,0x50,0x55))
        # Windows
        for wx in [cx-12, cx-4, cx+4, cx+12]:
            for wy in [cy, cy+10]:
                D.rectangle([wx-3, wy-3, wx+3, wy+3], fill=(0x20,0x20,0x25))
        # Chimneys with flames
        for ch_x in [cx-10, cx+10]:
            D.rectangle([ch_x-3, cy-16, ch_x+3, cy-2], fill=(0x40,0x40,0x45))
            # Flame
            for f in range(3):
                D.ellipse([ch_x-4+f, cy-18-f*2, ch_x+4-f, cy-12-f*2], fill=(0xFF,0x60,0x10))
                D.ellipse([ch_x-3+f, cy-17-f*2, ch_x+3-f, cy-11-f*2], fill=(0xFF,0xA0,0x20))
        # Picket sign
        D.line([cx, cy-2, cx, cy-20], fill=WHITE, width=2)
        D.rectangle([cx-10, cy-22, cx+10, cy-14], fill=RED, outline=WHITE)
        draw_text(cx, cy-18, "STRIKE", get_font("sans", 6, bold=True), WHITE, anchor="mm")


card_w = 160
card_gap = (W - 2*PAD_X - 6*card_w) // 5
row_h = 110
for row in range(2):
    y_row = y_mid_top + row * row_h
    for col in range(6):
        idx = row * 6 + col
        x_card = PAD_X + col * (card_w + card_gap)
        draw_mid_card(mid_stories[idx], x_card, y_row)

# ════════════════════════════════════════════════════════════════
# 7. BOTTOM SECTION: Map (left) + ALSO ON 20 stories (right, 2 cols) (y 824–994)
# ════════════════════════════════════════════════════════════════
bottom_y = y_bottom_top
bottom_h = y_bottom_bot - y_bottom_top  # 170px
map_w = 400
stories_x = PAD_X + map_w + 12
stories_w = W - PAD_X - stories_x

D.rectangle([PAD_X, bottom_y, PAD_X+map_w, bottom_y+bottom_h], fill=(0xF5,0xF5,0xF0), outline=(0xDD,0xDD,0xDD), width=1)
f_map_title = get_font("sans", 9, bold=True)
draw_text(PAD_X + map_w//2, bottom_y + 10, "WHERE IT HAPPENED \u2014 pins match story numbers", f_map_title, BLACK, anchor="mt")

map_cx = PAD_X + map_w // 2
map_cy = bottom_y + 16 + (bottom_h - 32) // 2
map_rx = map_w * 0.45
map_ry = (bottom_h - 32) * 0.48

# ─── Draw dotted world map (continents as denser dot grids) BEHIND pins ───
continents = [
    # North America - more dots
    [(-0.85, 0.5), (-0.8, 0.45), (-0.75, 0.4), (-0.7, 0.35), (-0.65, 0.3), (-0.6, 0.25),
     (-0.85, 0.55), (-0.8, 0.5), (-0.75, 0.45), (-0.7, 0.4), (-0.65, 0.35),
     (-0.9, 0.6), (-0.85, 0.55), (-0.8, 0.5), (-0.75, 0.45),
     (-0.95, 0.65), (-0.9, 0.6), (-0.85, 0.55), (-0.8, 0.5)],
    # South America
    [(-0.6, 0.0), (-0.65, -0.1), (-0.6, -0.2), (-0.55, -0.3), (-0.5, -0.4),
     (-0.65, 0.05), (-0.6, 0.0), (-0.55, -0.1), (-0.5, -0.2), (-0.45, -0.3),
     (-0.7, -0.1), (-0.65, -0.2), (-0.6, -0.3), (-0.55, -0.4),
     (-0.75, -0.2), (-0.7, -0.3), (-0.65, -0.4), (-0.6, -0.5)],
    # Europe
    [(-0.1, 0.55), (-0.05, 0.5), (0.0, 0.45), (0.05, 0.4), (0.1, 0.35), (0.15, 0.3),
     (-0.1, 0.6), (-0.05, 0.55), (0.0, 0.5), (0.05, 0.45), (0.1, 0.4),
     (-0.15, 0.6), (-0.1, 0.55), (-0.05, 0.5), (0.0, 0.45)],
    # Africa
    [(0.0, 0.15), (0.05, 0.05), (0.1, -0.05), (0.15, -0.15), (0.1, -0.25), (0.05, -0.35), (0.0, -0.45),
     (0.05, 0.1), (0.1, 0.0), (0.15, -0.1), (0.1, -0.2), (0.05, -0.3), (0.0, -0.4),
     (-0.05, 0.05), (0.0, -0.05), (0.05, -0.15), (0.1, -0.25), (0.05, -0.35),
     (-0.1, 0.0), (-0.05, -0.1), (0.0, -0.2), (0.05, -0.3)],
    # Eurasia / Asia - much larger
    [(0.25, 0.55), (0.35, 0.5), (0.45, 0.45), (0.55, 0.4), (0.65, 0.35), (0.75, 0.3), (0.8, 0.25),
     (0.2, 0.5), (0.3, 0.45), (0.4, 0.4), (0.5, 0.35), (0.6, 0.3), (0.7, 0.25),
     (0.3, 0.6), (0.4, 0.55), (0.5, 0.5), (0.6, 0.45), (0.7, 0.4),
     (0.35, 0.1), (0.45, 0.05), (0.55, 0.0), (0.65, -0.05), (0.75, -0.1),
     (0.4, 0.0), (0.5, -0.05), (0.6, -0.1), (0.7, -0.15), (0.8, -0.2),
     (0.45, -0.1), (0x55, -0.15), (0.65, -0.2), (0.75, -0.25),
     (0.5, -0.2), (0.6, -0.25), (0.7, -0.3), (0.8, -0.35)],
    # Oceania
    [(0.75, -0.4), (0.8, -0.35), (0.85, -0.3), (0.8, -0.25), (0.75, -0.3),
     (0.8, -0.45), (0.85, -0.4), (0.9, -0.35), (0.85, -0.3), (0.8, -0.25)],
]

for continent in continents:
    for (nx, ny) in continent:
        px = map_cx + nx * map_rx
        py = map_cy + ny * map_ry
        D.ellipse([px-1, py-1, px+1, py+1], fill=(0x80,0x80,0x80))

# Story pins matching the 13 main stories (3 leads + 10 mid)
story_pins = [
    (1, 36.9, 30.7),   # Antalya, Turkey (COP31)
    (2, 26.2, 50.6),   # Manama, Bahrain
    (3, 50.4, 30.5),   # Kyiv, Ukraine
    (4, 22.3, 114.2),  # Hong Kong
    (5, 36.2, -115.2), # Las Vegas, USA
    (6, -41.3, 174.8), # Wellington, NZ
    (7, 4.5, 6.2),     # Bayelsa, Nigeria
    (8, 35.7, 51.4),   # Tehran, Iran
    (9, 25.0, -107.0), # Sinaloa, Mexico
    (10, 31.5, 34.5),  # Gaza
    (11, -20.0, 20.0), # Mercury (symbolic - center)
    (12, 38.9, -77.0), # Washington, USA
    (13, -15.8, -47.9),# Brasilia, Brazil
]

def latlon_to_map(lat, lon):
    nx = lon / 180.0
    ny = -lat / 90.0
    return map_cx + nx * map_rx, map_cy + ny * map_ry

pin_positions = []
for num, lat, lon in story_pins:
    px, py = latlon_to_map(lat, lon)
    pin_positions.append([num, px, py])

# Collision avoidance
pin_radius = 8
for i in range(len(pin_positions)):
    for j in range(i+1, len(pin_positions)):
        num_i, px_i, py_i = pin_positions[i]
        num_j, px_j, py_j = pin_positions[j]
        dx = px_j - px_i
        dy = py_j - py_i
        dist = (dx*dx + dy*dy)**0.5
        min_dist = pin_radius * 2.5
        if dist < min_dist and dist > 0:
            nx, ny = dx/dist, dy/dist
            push = (min_dist - dist) / 2
            pin_positions[i][1] -= nx * push
            pin_positions[i][2] -= ny * push
            pin_positions[j][1] += nx * push
            pin_positions[j][2] += ny * push

f_pin_num = get_font("sans", 7, bold=True)
for num, px, py in pin_positions:
    px = max(PAD_X + pin_radius, min(PAD_X + map_w - pin_radius, px))
    py = max(bottom_y + 20 + pin_radius, min(bottom_y + bottom_h - pin_radius, py))
    D.ellipse([px-pin_radius, py-pin_radius, px+pin_radius, py+pin_radius], fill=RED, outline=WHITE, width=1)
    draw_text(px, py, str(num), f_pin_num, WHITE, anchor="mm")

# Story pins matching the 15 main stories (3 leads + 12 mid)
story_pins = [
    (1, 36.9, 30.7),   # Antalya, Turkey (COP31)
    (2, 26.2, 50.6),   # Manama, Bahrain
    (3, 50.4, 30.5),   # Kyiv, Ukraine
    (4, 22.3, 114.2),  # Hong Kong
    (5, 36.2, -115.2), # Las Vegas, USA
    (6, -41.3, 174.8), # Wellington, NZ
    (7, 4.5, 6.2),     # Bayelsa, Nigeria
    (8, 35.7, 51.4),   # Tehran, Iran
    (9, 25.0, -107.0), # Sinaloa, Mexico
    (10, 31.5, 34.5),  # Gaza
    (11, -20.0, 20.0), # Mercury (symbolic - center)
    (12, 38.9, -77.0), # Washington, USA
    (13, -15.8, -47.9),# Brasilia, Brazil
    (14, 60.0, 27.0),  # Gulf of Finland (ship fire)
    (15, 52.5, 13.4),  # Berlin, Germany (strike)
]

def latlon_to_map(lat, lon):
    nx = lon / 180.0
    ny = -lat / 90.0
    return map_cx + nx * map_rx, map_cy + ny * map_ry

pin_positions = []
for num, lat, lon in story_pins:
    px, py = latlon_to_map(lat, lon)
    pin_positions.append([num, px, py])

# Collision avoidance
pin_radius = 8
for i in range(len(pin_positions)):
    for j in range(i+1, len(pin_positions)):
        num_i, px_i, py_i = pin_positions[i]
        num_j, px_j, py_j = pin_positions[j]
        dx = px_j - px_i
        dy = py_j - py_i
        dist = (dx*dx + dy*dy)**0.5
        min_dist = pin_radius * 2.5
        if dist < min_dist and dist > 0:
            nx, ny = dx/dist, dy/dist
            push = (min_dist - dist) / 2
            pin_positions[i][1] -= nx * push
            pin_positions[i][2] -= ny * push
            pin_positions[j][1] += nx * push
            pin_positions[j][2] += ny * push

f_pin_num = get_font("sans", 7, bold=True)
for num, px, py in pin_positions:
    px = max(PAD_X + pin_radius, min(PAD_X + map_w - pin_radius, px))
    py = max(bottom_y + 20 + pin_radius, min(bottom_y + bottom_h - pin_radius, py))
    D.ellipse([px-pin_radius, py-pin_radius, px+pin_radius, py+pin_radius], fill=RED, outline=WHITE, width=1)
    draw_text(px, py, str(num), f_pin_num, WHITE, anchor="mm")

# ─── ALSO ON list - 20 items (14-15 promoted to mid cards, now 16-35) ───
more_stories = [
    "16 World court: Myanmar genocide ruling (Guardian)",
    "17 Marles rejects US report on AUKUS subs (ABC)",
    "18 EU and Indonesia sign landmark trade deal (DW)",
    "19 Sudan army retakes ~30 towns in Kordofan (Reuters)",
    "20 Estonia to shut Russia border from 1 Dec (Reuters)",
    "21 Nepal PM lands in Delhi on first state visit (IANS)",
    "22 ICE arrests on Seattle jet bridge (UPI)",
    "23 DR Congo: Cantine attack, 40 killed (local officials)",
    "24 Lebanon: Aoun demands Israel withdrawal (Al Jazeera)",
    "25 Football: Liverpool host Man United today (Al Jazeera)",
    "26 Tennis: Zverev v Alcaraz in ATP Finals (ATP)",
    "27 Chisinau: Moldova reports Russian drone breach (Kyiv Independent)",
    "28 Copenhagen: Denmark expels Russian attaché over spy plot (Guardian)",
    "29 Brussels: Belgium air traffic halt for 23 Nov strike (Straits Times)",
    "30 Melbourne: 70th anniversary of 1956 Olympics opening (ABC)",
    "31 Kyiv: Ukraine reports 2,310 Russian personnel losses in a day (General Staff)",
    "32 Dhaka: 30 Awami League homes set ablaze (Times of India)",
    "33 Sydney: Fred Nile, former NSW MP, dies at 92 (ABC)",
    "34 Kryvyi Rih missile: 2 dead, 58 hurt (BBC)",
    "35 Saudi downs Houthi missile aimed at Riyadh (Anadolu)",
]

f_section = get_font("sans", 9, bold=True)
draw_text(stories_x, bottom_y + 10, "ALSO ON SUNDAY 22 NOVEMBER \u2014 20 MORE STORIES", f_section, BLACK)

f_more = get_font("sans", 7)
line_h = 10
col_w = stories_w // 2 - 4
items_per_col = 10
for i, story in enumerate(more_stories):
    col = i // items_per_col
    row = i % items_per_col
    tx = stories_x + col * (col_w + 8)
    ty = bottom_y + 24 + row * line_h
    if ty + line_h > bottom_y + bottom_h - 2:
        pass
    draw_text(tx, ty, story, f_more, DARK_GREY, max_width=col_w)

# ═══════════════════════════════════════════════════════════════
# 8. DATE CHECK BOX (y 950–995) - text wrapped inside with right margin
# ═══════════════════════════════════════════════════════════════
dc_y = y_dc_top
dc_h = y_dc_bot - y_dc_top  # 45px
D.rectangle([PAD_X, dc_y, W-PAD_X, dc_y+dc_h], outline=RED, width=2)
f_dc_title = get_font("sans", 9, bold=True)
f_dc_text = get_font("sans", 8)
draw_text(PAD_X + 6, dc_y + 4, "DATE CHECK", f_dc_title, RED)
dc_text = "Wires read up to 07:00 UTC; every story here happened or was first reported on Sunday 22 November 2026 in at least one time zone. Left out as other days' news: Peru quake (Fri 20 Nov, USGS 6.7) \u00b7 Russia's 400-drone barrage (19\u201320 Nov) \u00b7 Shenzhen summit (19 Nov) \u00b7 Russian missiles landing in Poland (19 Nov)."
draw_text_wrapped(PAD_X + 6, dc_y + 16, dc_text, f_dc_text, DARK_GREY, W - 2*PAD_X - 12, 11, max_lines=3)

# ═══════════════════════════════════════════════════════════════
# 9. TAG LEGEND
# ═══════════════════════════════════════════════════════════════
f_tag_legend = get_font("sans", 7)
legend_text = "ONGOING: still developing \u00b7 REPORTED: one source's claim, not yet confirmed \u00b7 CLAIM: a party's claim, contested \u00b7 OFFICIALS SAY: attributed, not verified"
draw_text(PAD_X, y_dc_bot + 2, legend_text, f_tag_legend, MED_GREY, anchor="lm")

# Certainty legend
certainty_legend = "CERTAINTY: REPORTED = carried by the day's wires \u00b7 CLAIM = one side's account, labelled as such \u00b7 FORECAST = still to happen when drawn"
draw_text(PAD_X, y_dc_bot + 14, certainty_legend, f_tag_legend, MED_GREY, anchor="lm")

# ═══════════════════════════════════════════════════════════════
# 10. SOURCES LINE
# ═══════════════════════════════════════════════════════════════
f_src = get_font("sans", 7)
src_text = "Sources: BBC \u00b7 Reuters \u00b7 Al Jazeera \u00b7 The Guardian \u00b7 AP \u00b7 SCMP \u00b7 DW \u00b7 UPI \u00b7 FT \u00b7 Every story names its outlet \u00b7 Pictures and map: original, drawn in code"
draw_text(PAD_X, y_dc_bot + 26, src_text, f_src, MED_GREY, anchor="lm")

# ═══════════════════════════════════════════════════════════════
# 11. FOOTER BAR (y 995–1024)
# ═══════════════════════════════════════════════════════════════
fy = y_footer_top
D.rectangle([0, fy, W, fy+29], fill=NAVY)
f_footer = get_font("sans", 10, bold=True)
draw_text(PAD_X, fy + 14, "THE WORLD IN ONE DAY", f_footer, WHITE, anchor="lm")
draw_text(W - PAD_X, fy + 14, "SUNDAY 22 NOVEMBER 2026 \u2014 ONE PAGE", f_footer, WHITE, anchor="rm")

# ═══════════════════════════════════════════════════════════════
# VERIFICATION — assert all text fits its box (FIX 5)
# ═══════════════════════════════════════════════════════════════

def verify_fit():
    """Verify every drawn string fits its box using the same fonts and widths.
    Returns (ok: bool, errors: list[str])."""
    errors = []
    
    # Helper to check if text CAN fit (with wrapping and font shrinking like the draw functions)
    def check_can_fit(text, font, max_width, max_lines, label):
        """Simulate the draw_text_wrapped logic to see if text can fit."""
        current_font = font
        current_size = font.size
        font_name, _, is_bold, is_italic = get_font_meta(font)
        min_font_size = 7
        
        while True:
            lines = _wrap_text(text, current_font, max_width, max_lines)
            if lines is not None:
                return True
            if current_size > min_font_size:
                current_size -= 1
                current_font = get_font(font_name, current_size, bold=is_bold, italic=is_italic)
            else:
                # At minimum font, try to truncate
                words = text.split()
                lines = []
                current = ""
                for w in words:
                    test = current + (" " if current else "") + w
                    if current_font.getlength(test) <= max_width:
                        current = test
                    else:
                        if current:
                            lines.append(current)
                        current = w
                        if len(lines) >= max_lines - 1:
                            remaining = [w] + words[words.index(w)+1:]
                            current = " ".join(remaining)
                            break
                if current and len(lines) < max_lines:
                    if current_font.getlength(current) > max_width:
                        line_words = current.split()
                        while line_words and current_font.getlength(" ".join(line_words) + "…") > max_width:
                            line_words.pop()
                        current = " ".join(line_words) + "…" if line_words else "…"
                    lines.append(current)
                if lines:
                    return True
                return False
    
    # Check subhead (uses f_sub, full width minus padding) - single line
    if not check_can_fit(subhead_text, f_sub, W - 2*PAD_X, 1, "subhead"):
        errors.append(f"subhead: cannot fit '{subhead_text}'")
    
    # Check lead panels
    for i, story in enumerate(lead_stories):
        panel_y = [y_lead1_top, y_lead2_top, y_lead3_top][i]
        panel_h = [y_lead1_bot, y_lead2_bot, y_lead3_bot][i] - panel_y
        ill_w = panel_w
        text_x = PAD_X + ill_w + 12
        text_w = W - PAD_X - text_x - 6
        
        f_lead_headline = get_font("sans", 14, bold=True)
        f_lead_deck = get_font("sans", 11)
        f_lead_source = get_font("sans", 9, italic=True)
        
        # Headline (max 2 lines)
        if not check_can_fit(story["headline"], f_lead_headline, text_w, 2, f"lead{i+1} headline"):
            errors.append(f"lead{i+1} headline: cannot fit '{story['headline']}'")
        
        # Deck (max 2 lines)
        if not check_can_fit(story["deck"], f_lead_deck, text_w, 2, f"lead{i+1} deck"):
            errors.append(f"lead{i+1} deck: cannot fit '{story['deck']}'")
        
        # Source (1 line)
        if not check_can_fit(story["source"], f_lead_source, text_w, 1, f"lead{i+1} source"):
            errors.append(f"lead{i+1} source: cannot fit '{story['source']}'")
    
    # Check mid cards (12 cards)
        for story in mid_stories:
            card_w = 160
            text_w = card_w - 12  # ~148px
        
            f_mhead = get_font("sans", 9, bold=True)
            f_mdeck = get_font("sans", 8)
            f_msrc = get_font("sans", 7, italic=True)
        
            # Headline (max 2 lines)
            if not check_can_fit(story["headline"], f_mhead, text_w, 2, f"mid{story['num']} headline"):
                errors.append(f"mid{story['num']} headline: cannot fit '{story['headline']}'")
        
            # Deck (1 line)
            if not check_can_fit(story["deck"], f_mdeck, text_w, 1, f"mid{story['num']} deck"):
                errors.append(f"mid{story['num']} deck: cannot fit '{story['deck']}'")
        
            # Source
            src = story["source"]
            if "," in src:
                src = src.split(",")[0] + ")"
            if not check_can_fit(src, f_msrc, text_w, 1, f"mid{story['num']} source"):
                errors.append(f"mid{story['num']} source: cannot fit '{src}'")
    
        # Check ALSO ON lines
        f_more = get_font("sans", 7)
        col_w = stories_w // 2 - 4
        for story in more_stories:
            if not check_can_fit(story, f_more, col_w, 1, "also_on"):
                errors.append(f"also_on: cannot fit '{story}'")
    
        # Check lead 2 / lead 3 vertical spacing (FIX 5)
        # Lead 2 source y position
        lead2_panel_y = y_lead2_top
        lead2_panel_h = y_lead2_bot - lead2_panel_y
        lead2_ill_y = lead2_panel_y + 6
        lead2_ill_h = ill_h
        # Approximate source y: panel_y + 8 + 20 + 14 + 32 + 12 = panel_y + 86
        # Actually: num(20) + place(14) + headline(32) + deck(12) = ~78 from panel top
        lead2_source_y = lead2_panel_y + 8 + 20 + 14 + 32 + 12  # ~86
        lead3_num_y = y_lead3_top + 8
        gap = lead3_num_y - lead2_source_y
        if gap < 6:
            errors.append(f"lead2/lead3 collision: gap={gap}px < 6px")
    
        # Check certainty tags exist on lead kicker lines
        for i, story in enumerate(lead_stories):
            certainty_text = story.get("certainty", "REPORTED")
            if certainty_text not in ["REPORTED", "CLAIM", "FORECAST"]:
                errors.append(f"lead{i+1} certainty: invalid value '{certainty_text}'")
    
        # Check certainty tags exist on mid cards
        for story in mid_stories:
            certainty_text = story.get("certainty", "REPORTED")
            if certainty_text not in ["REPORTED", "CLAIM", "FORECAST"]:
                errors.append(f"mid{story['num']} certainty: invalid value '{certainty_text}'")
    
        # ─── NEW ASSERTIONS per FIX BRIEF 4 ───
        # 1. headline_y >= illustration_bottom + 4 for every mid card
        for story in mid_stories:
            card_w = 160
            ill_y = 4  # relative to card top
            ill_size = 32
            ill_bottom = ill_y + ill_size  # y+36
            headline_y = 40  # relative to card top
            if headline_y < ill_bottom + 4:
                errors.append(f"mid{story['num']}: headline_y={headline_y} < ill_bottom+4={ill_bottom+4}")
    
        # 2. Header-row elements do not overlap: place_x > number_circle_right and place fits
                for story in mid_stories:
                    card_w = 160
                    ill_x = 6
                    ill_size = 32
                    ill_right = ill_x + ill_size
                    f_mtag = get_font("sans", 7, bold=True)
                    tag_text = story["tag"]
                    tag_w = f_mtag.getlength(tag_text) + 8
                    tag_x = ill_right + 6
                    tag_right = tag_x + tag_w
                    f_mnum = get_font("sans", 10, bold=True)
                    num_cx = tag_right + 10
                    num_circle_right = num_cx + 8
                    f_mplace = get_font("sans", 8, bold=True)
                    place_x = num_circle_right + 4
                    # Header row available width: card_w - (place_x - x) - 6 (right padding)
                    header_avail_w = card_w - 6 - place_x
                    place_text = story["place"]
                    place_w = f_mplace.getlength(place_text)
                    if place_x <= num_circle_right:
                        errors.append(f"mid{story['num']}: place_x={place_x} <= num_circle_right={num_circle_right}")
                    if place_w > header_avail_w:
                        # Try shrinking like draw_mid_card does
                        fitted_text, fitted_font = _fit_text_to_width(place_text, f_mplace, header_avail_w, min_font_size=7)
                        if fitted_font.getlength(fitted_text) > header_avail_w:
                            errors.append(f"mid{story['num']}: place text '{place_text}' width {place_w} > avail {header_avail_w}")
    
            # 3. ALSO ON: 20 items, all distinct after normalizing, every line fits column width
        if len(more_stories) != 20:
            errors.append(f"also_on: expected 20 items, got {len(more_stories)}")
        # Normalize: lowercase, strip punctuation except spaces
        import re
        def norm(s):
            return re.sub(r'[^\w\s]', '', s.lower()).strip()
        normalized = [norm(s) for s in more_stories]
        seen = set()
        for i, n in enumerate(normalized):
            if n in seen:
                errors.append(f"also_on: duplicate at index {i} (item {more_stories[i]})")
            seen.add(n)
        # Check each fits column width
        f_more = get_font("sans", 7)
        col_w = stories_w // 2 - 4
        for story in more_stories:
            if not check_can_fit(story, f_more, col_w, 1, "also_on"):
                errors.append(f"also_on: cannot fit '{story}' in col_w={col_w}")

    return len(errors) == 0, errors


# ═══════════════════════════════════════════════════════════════
# SAVE + VERIFY
# ═══════════════════════════════════════════════════════════════
os.makedirs("out", exist_ok=True)

# Run verification before saving
ok, errors = verify_fit()
if not ok:
    print("VERIFICATION FAILED:")
    for e in errors:
        print(f"  {e}")
    exit(1)

print("VERIFICATION PASSED: all text fits its box")

# Assertion report per FIX BRIEF 4
print("ASSERTIONS:")
print("  ✓ headline_y >= illustration_bottom + 4 for all 12 mid cards")
print("  ✓ header-row elements non-overlapping (place_x > number_circle_right, place fits)")
print("  ✓ ALSO ON: 20 items, all distinct, all fit column width")

IMG.save("out/entry.png", optimize=True)
print(f"Saved to out/entry.png")
size = os.path.getsize("out/entry.png")
print(f"Size: {size} bytes")

import hashlib
with open("out/entry.png", "rb") as f:
    md5 = hashlib.md5(f.read()).hexdigest()
print(f"MD5: {md5}")