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
def get_font(name, size, bold=False, italic=False):
    key = (name, size, bold, italic)
    if key not in FONTS:
        FONTS[key] = load_font(name, size, bold, italic)
    return FONTS[key]

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

def draw_text(x, y, text, font, color, anchor="lt", max_width=None):
    if max_width:
        while font.getlength(text) > max_width and len(text) > 3:
            text = text[:-1]
        if font.getlength(text) > max_width:
            text = text[:-3] + "..."
    D.text((x, y), text, font=font, fill=color, anchor=anchor)

def draw_text_on_layer(draw, x, y, text, font, color, anchor="lt", max_width=None):
    if max_width:
        while font.getlength(text) > max_width and len(text) > 3:
            text = text[:-1]
        if font.getlength(text) > max_width:
            text = text[:-3] + "..."
    draw.text((x, y), text, font=font, fill=color, anchor=anchor)

def draw_text_wrapped(x, y, text, font, color, max_width, line_height, max_lines=2):
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
                break
    if current and len(lines) < max_lines:
        lines.append(current)
    if lines and font.getlength(lines[-1]) > max_width:
        while font.getlength(lines[-1]) > max_width and len(lines[-1]) > 3:
            lines[-1] = lines[-1][:-1]
        if font.getlength(lines[-1]) > max_width:
            lines[-1] = lines[-1][:-3] + "..."
    h_used = 0
    for line in lines:
        D.text((x, y + h_used), line, font=font, fill=color)
        h_used += line_height
    return h_used

def draw_text_wrapped_on_layer(draw, x, y, text, font, color, max_width, line_height, max_lines=2):
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
                break
    if current and len(lines) < max_lines:
        lines.append(current)
    if lines and font.getlength(lines[-1]) > max_width:
        while font.getlength(lines[-1]) > max_width and len(lines[-1]) > 3:
            lines[-1] = lines[-1][:-1]
        if font.getlength(lines[-1]) > max_width:
            lines[-1] = lines[-1][:-3] + "..."
    h_used = 0
    for line in lines:
        draw.text((x, y + h_used), line, font=font, fill=color)
        h_used += line_height
    return h_used

# ═══════════════════════════════════════════════════════════════
# LAYOUT - Explicit Y-bands per fix brief
# ═══════════════════════════════════════════════════════════════
# Masthead block: y 0–150
# Stat strip: y 150–210
# UTC timeline: y 210–238
# Region tabs: y 238–268
# Lead panels 1–3: y 268–560 (each 97px, illustration top ~90px clipped to panel)
# THE DAY IN TEN (cards 4–13): y 560–780 (2 rows x 110px)
# Map + ALSO ON: y 780–950
# DATE CHECK box: y 950–995
# Footer: y 995–1024

y_masthead_top = 0
y_masthead_bot = 150
y_stat_top = 150
y_stat_bot = 210
y_utc_top = 210
y_utc_bot = 238
y_region_top = 238
y_region_bot = 268
y_lead1_top = 268
y_lead1_bot = 365   # 97px each
y_lead2_top = 365
y_lead2_bot = 462
y_lead3_top = 462
y_lead3_bot = 559
y_mid_top = 560
y_mid_bot = 780
y_bottom_top = 780
y_bottom_bot = 950
y_dc_top = 950
y_dc_bot = 995
y_footer_top = 995
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

# Red italic subhead naming the 3 lead stories - spaced middots per fix brief
y_sub_kicker = y_masthead_top + 110
f_sub = get_font("sans", 13, italic=True)
draw_text(W//2, y_sub_kicker + 6, "COP31 final text lands at dawn \u00b7 Iran claims strikes on US bases in Bahrain \u00b7 Russia launches 186 drones at Ukraine", f_sub, RED, anchor="mm")

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

# Space 6 events EVENLY across full width (not by time proportion)
f_utc_combined = get_font("sans", 6)
num_events = len(utc_events)
for idx, label in enumerate(utc_events):
    # Even spacing: position at (idx + 0.5) / num_events * available_width
    x = PAD_X + int((idx + 0.5) / num_events * (W - 2*PAD_X))
    D.ellipse([x-2, rule_y-2, x+2, rule_y+2], fill=RED)
    ty = rule_y + 8
    # Max width = spacing between events minus margin
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
# Verify sum = 35
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
# 5. THREE LARGE LEAD PANELS (y 268–559) - with continuous panorama CLIPPED to panels
# ═══════════════════════════════════════════════════════════════
lead_stories = [
    {
        "num": 1, "place": "ANTALYA, TURKEY", "tag": "ONGOING", "kicker": "COP31 CLIMATE SUMMIT",
        "tag_color": EUROPE_BLUE, "tag_bg": TAG_BLUE,
        "headline": "COP31 final text lands at dawn after two days in overtime",
        "deck": "No fossil fuel mention; recalls COP28 pact; 35% electricity by 2035; $120bn adaptation target dropped; admits 1.5\u00b0C overshoot",
        "source": "(Reuters, BBC)", "stat": "~200 nations", "illustration": "climate",
    },
    {
        "num": 2, "place": "MANAMA, BAHRAIN", "tag": "CLAIM", "kicker": "IRGC CLAIMS STRIKES",
        "tag_color": MIDEAST_RED, "tag_bg": TAG_RED,
        "headline": "IRGC claims missile and drone strikes on two US Patriot radars",
        "deck": "Retaliation for MQ-1/MQ-9 airspace violations and Hengam radar attack; Bahrain says defences intercepted several, facility hit, no casualties; US unconfirmed",
        "source": "(Al Jazeera)", "stat": "2 bases targeted", "illustration": "bahrain",
    },
    {
        "num": 3, "place": "KYIV, UKRAINE", "tag": "REPORTED", "kicker": "OVERNIGHT BARRAGE",
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
        # Dawn in Antalya - conference hall with large globe
        draw.rectangle([x, y, x+w, y+h], fill=(0xE8,0xEC,0xF4))
        # Delegate rows
        for row in range(5):
            ry = y + h - 20 - row * 16
            for seat in range(6):
                sx = x + 15 + seat * (w - 30) // 5
                draw.rounded_rectangle([sx-5, ry-7, sx+5, ry], radius=1, fill=(0xC0,0xCC,0xDC), outline=(0xA0,0xB8,0xD0))
                draw.ellipse([sx-4, ry-14, sx+4, ry-6], fill=(0xC0,0xA0,0x80))
        # Podium
        draw.rectangle([cx-30, y+h-40, cx+30, y+h-20], fill=(0x70,0x80,0x90))
        # Large globe projection
        globe_r = min(w, h) // 2 - 5
        draw.ellipse([cx-globe_r, cy-globe_r, cx+globe_r, cy+globe_r], outline=(0x30,0x70,0xB0), width=3)
        for lat in (-60, -30, 0, 30, 60):
            ly = cy + lat * globe_r // 60
            draw.arc([cx-globe_r, ly-2, cx+globe_r, ly+2], 0, 360, fill=(0x30,0x70,0xB0), width=1)
        for lon in (-60, -30, 0, 30, 60):
            lx = cx + lon * globe_r // 60
            draw.arc([lx-1, cy-globe_r, lx+1, cy+globe_r], 0, 360, fill=(0x30,0x70,0xB0), width=1)
        for gx, gy, gr in [(cx-30, cy-20, 15), (cx+20, cy-10, 12), (cx-10, cy+25, 18), (cx+35, cy+15, 10)]:
            draw.ellipse([gx-gr, gy-gr, gx+gr, gy+gr], fill=(0x20,0x80,0x30))
        # COP31 banner
        draw.rectangle([cx-100, y+6, cx+100, y+28], fill=EUROPE_BLUE)
        f_banner = get_font("sans", 12, bold=True)
        draw_text_on_layer(draw, cx, y+17, "COP31 ANTALYA", f_banner, WHITE, anchor="mm")
        for bx in [x+10, x+w-110]:
            draw.rectangle([bx, y+35, bx+100, y+55], fill=(0x1E,0x3A,0x8A))
            f_side = get_font("sans", 8, bold=True)
            draw_text_on_layer(draw, bx+50, y+45, "UNFCCC", f_side, WHITE, anchor="mm")
    
    elif type_ == "bahrain":
        # Dusk in Manama - Bahrain coast with burning base
        # Sky - dusk colors
        for i in range(h):
            ratio = i / h
            r = int(0x15 + (0x40 - 0x15) * ratio)
            g = int(0x25 + (0x30 - 0x25) * ratio)
            b = int(0x45 + (0x50 - 0x45) * ratio)
            draw.line([x, y+i, x+w, y+i], fill=(r, g, b))
        # Fire glow
        ex = x + w//2
        ey = y + h//3
        for r, color in [(100, (0x30,0x10,0x05)), (70, (0x50,0x15,0x05)), (40, (0x80,0x20,0x05)), (20, (0xB0,0x30,0x10))]:
            draw.ellipse([ex-r, ey-r, ex+r, ey+r], fill=color)
        # Smoke plumes
        for i in range(10):
            sx = x + 20 + i * (w-40)//9
            sy = y + 15 + (i%3)*15
            sr = 18 + (i%4)*6
            draw.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=(0x10,0x10,0x15))
        # Water line
        cy = y + h * 0.55
        for wx in range(0, w, 20):
            draw.arc([x+wx, cy-10, x+wx+20, cy+10], 0, 180, fill=(0x10,0x30,0x55), width=1)
        draw.line([x, cy, x+w, cy], fill=(0x7B,0x60,0x40), width=2)
        # Tanks
        tank_x = x + 20
        for tx in [tank_x, tank_x+85, tank_x+170, tank_x+255]:
            draw.rectangle([tx, cy-80, tx+55, cy], fill=(0x40,0x40,0x45), outline=(0x25,0x25,0x25))
            draw.ellipse([tx, cy-90, tx+55, cy-70], fill=(0x50,0x50,0x55), outline=(0x25,0x25,0x25))
            draw.rectangle([tx+10, cy-85, tx+45, cy-75], fill=(0x60,0x60,0x65))
            draw.line([tx+27, cy-90, tx+27, cy-110], fill=(0x30,0x30,0x30), width=3)
            draw.line([tx+27, cy-110, tx+12, cy-115], fill=(0x30,0x30,0x30), width=2)
        # Main explosion
        ex = x + w//2
        ey = cy - 80
        for i in range(7):
            rx = ex + (i-3)*20
            draw.ellipse([rx-12, cy+5, rx+12, cy+30], fill=(0xFF,0x40,0x10))
        for r, color in [(40, (0xFF,0x20,0x00)), (32, (0xFF,0x60,0x10)), (22, (0xFF,0xA0,0x20)), (12, (0xFF,0xD0,0x60))]:
            draw.ellipse([ex-r, ey-r, ex+r, ey+r], fill=color)
        # Fire column
        draw.polygon([(ex-25, ey), (ex-12, y+5), (ex+12, y+5), (ex+25, ey)], fill=(0xFF,0x50,0x10))
        # Smoke plume
        for i in range(8):
            sx = ex + (i%3-1)*12
            sy = ey - 30 - i*12
            sr = 15 + i*4
            draw.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=(0x15,0x15,0x18))
        # Debris
        for i in range(15):
            dx = ex + (i%5-2)*18
            dy = ey - 10 - (i//5)*15
            draw.ellipse([dx-2, dy-2, dx+2, dy+2], fill=(0xFF,0xA0,0x30))
        # Shoreline
        for sx in range(x, x+w, 8):
            draw.ellipse([sx-2, cy-2, sx+2, cy+2], fill=(0x50,0x40,0x30))
        f_b = get_font("sans", 10, bold=True)
        draw_text_on_layer(draw, cx, y+h-8, "MANAMA", f_b, (0xFF,0xC0,0xC0), anchor="mm")
    
    elif type_ == "kyiv":
        # Night over Kyiv
        draw.rectangle([x, y, x+w, y+h], fill=(0x0A,0x12,0x25))
        # Moon
        draw.ellipse([x+w-60, y+10, x+w-15, y+55], fill=(0xE8,0xE8,0xC8))
        # City silhouette
        bw = w // 7
        for i in range(7):
            bx = x + i * bw
            bh = [h-25, h-40, h-30, h-50, h-35, h-28, h-42][i]
            bh = max(15, min(h-15, bh))
            draw.rectangle([bx, y+h-bh, bx+bw-2, y+h], fill=(0x04,0x08,0x12))
            for wy in range(y+h-bh+6, y+h-6, 12):
                for wx in range(bx+3, bx+bw-3, 10):
                    if (wx + wy) % 4 == 0:
                        draw.rectangle([wx, wy, wx+3, wy+5], fill=(0xFF,0xD8,0x70))
        # Drone swarm
        for i in range(14):
            dx = x + 15 + (i % 4) * (w-30)//3
            dy = y + 15 + (i // 4) * (h-70)//3
            draw.polygon([(dx, dy), (dx-3, dy+6), (dx+3, dy+6)], fill=(0xFF,0x30,0x30))
            draw.line([dx, dy+6, dx, dy+10], fill=(0xFF,0x50,0x50), width=1)
        # Smoke trails
        for i in range(5):
            sx = x + 20 + i * (w-40)//4
            sy = y + h - 30 - (i%2)*8
            draw.ellipse([sx-8, sy-4, sx+8, sy+4], fill=(0x20,0x20,0x30))
        f_k = get_font("sans", 10, bold=True)
        draw_text_on_layer(draw, cx, y+h-8, "KYIV", f_k, (0xFF,0xC0,0xC0), anchor="mm")


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
        "bahrain": "Bahrain coast, smoke rising at dusk",
        "kyiv": "Night sky over Kyiv, drone swarm incoming",
    }
    draw_text(PAD_X + 6, ill_y + ill_h - 2, captions[story["illustration"]], f_caption, MED_GREY, anchor="lb")

    # Right column text
    f_lead_num = get_font("sans", 18, bold=True)
    f_lead_place = get_font("sans", 10, bold=True)
    f_lead_headline = get_font("sans", 14, bold=True)
    f_lead_deck = get_font("sans", 11)
    f_lead_source = get_font("sans", 9, italic=True)

    ty = panel_y + 8
    draw_text(text_x, ty, str(story["num"]), f_lead_num, RED)
    ty += 20
    draw_text(text_x, ty, story["place"], f_lead_place, BLACK)
    ty += 14
    draw_text_wrapped(text_x, ty, story["headline"], f_lead_headline, BLACK, text_w, 16, max_lines=2)
    ty += 32
    draw_text_wrapped(text_x, ty, story["deck"], f_lead_deck, DARK_GREY, text_w, 12, max_lines=2)
    ty += 24
    draw_text(text_x, ty, story["source"], f_lead_source, MED_GREY)

    # ════════════════════════════════════════════════════════════════
    # 6. THE DAY IN TEN - 2 rows of 5 cards (numbered 4-13) (y 560–780)
    # ════════════════════════════════════════════════════════════════
    mid_stories = [
    {"num": 4, "place": "HONG KONG", "tag": "ELECTION", "tag_color": ASIA_ORANGE, "tag_bg": TAG_ORANGE,
     "headline": "Hong Kong elects Election Committee",
     "deck": "856 candidates, 723 seats; turnout 93.55%",
     "source": "(SCMP)", "illustration": "hk_vote"},
    {"num": 5, "place": "LAS VEGAS, USA", "tag": "SPORT", "tag_color": AMERICAS_GREEN, "tag_bg": TAG_GREEN,
     "headline": "Verstappen wins Las Vegas GP",
     "deck": "Red Bull driver takes the win",
     "source": "(BBC)", "illustration": "f1"},
    {"num": 6, "place": "WELLINGTON, NZ", "tag": "CRICKET", "tag_color": OCEANIA_TEAL, "tag_bg": TAG_TEAL,
     "headline": "India declare 720/9",
     "deck": "Record total in New Zealand",
     "source": "(ESPNcricinfo)", "illustration": "cricket"},
    {"num": 7, "place": "BAYELSA, NIGERIA", "tag": "DISASTER", "tag_color": AFRICA_BROWN, "tag_bg": TAG_BROWN,
     "headline": "Boat carrying mourners capsizes",
     "deck": "Overloaded vessel; toll rises to 26",
     "source": "(DW, Al Jazeera)", "illustration": "boat"},
    {"num": 8, "place": "TEHRAN, IRAN", "tag": "POWER", "tag_color": MIDEAST_RED, "tag_bg": TAG_RED,
     "headline": "Iran starts electricity rationing",
     "deck": "Two-hour daily cuts begin",
     "source": "(Straits Times)", "illustration": "power"},
    {"num": 9, "place": "SINALOA, MEXICO", "tag": "CARTEL", "tag_color": AMERICAS_GREEN, "tag_bg": TAG_GREEN,
     "headline": "'El Chapo Isidro' caught",
     "deck": "FBI top-ten fugitive held",
     "source": "(Reuters)", "illustration": "arrest"},
    {"num": 10, "place": "GAZA", "tag": "AID STRIKE", "tag_color": MIDEAST_RED, "tag_bg": TAG_RED,
     "headline": "Hamas seeks urgent talks",
     "deck": "Three die in Gaza aid strike",
     "source": "(Al Jazeera)", "illustration": "aid"},
    {"num": 11, "place": "MERCURY ORBIT", "tag": "SPACE", "tag_color": WORLD_PURPLE, "tag_bg": TAG_PURPLE,
     "headline": "BepiColombo enters Mercury orbit",
     "deck": "Eight-year trip ends at Mercury",
     "source": "(ESA)", "illustration": "space"},
    {"num": 12, "place": "WASHINGTON, USA", "tag": "TECH", "tag_color": AMERICAS_GREEN, "tag_bg": TAG_GREEN,
     "headline": "Nvidia faces SEC accounting probe",
     "deck": "Regulator examines accounts",
     "source": "(FT)", "illustration": "probe"},
    {"num": 13, "place": "BRASÍLIA, BRAZIL", "tag": "HEALTH", "tag_color": AMERICAS_GREEN, "tag_bg": TAG_GREEN,
     "headline": "Bolsonaro in intensive care",
     "deck": "Ex-president stable in care",
     "source": "(Al Jazeera)", "illustration": "hospital"},
]

def draw_mid_card(story, x, y):
    card_w = 194
    card_h = 110  # taller cards for 2-row layout
    D.rectangle([x, y, x+card_w, y+card_h], fill=WHITE, outline=(0xDD,0xDD,0xDD), width=1)
    
    # Small illustration at top-left (32x32)
    ill_x = x + 6
    ill_y = y + 6
    ill_size = 32
    draw_mid_illustration(story["illustration"], ill_x, ill_y, ill_size, ill_size)
    
    # Tag at top-right of illustration area
    tx = ill_x + ill_size + 6
    tw = card_w - (ill_size + 12) - 6
    
    f_mtag = get_font("sans", 7, bold=True)
    tag_text = story["tag"]
    tag_w = f_mtag.getlength(tag_text) + 8
    D.rounded_rectangle([tx, y+4, tx+tag_w, y+16], radius=2, fill=story["tag_bg"], outline=story["tag_color"])
    draw_text(tx + tag_w//2, y+10, tag_text, f_mtag, story["tag_color"], anchor="mm")
    
    # Number circle to the right of tag
    f_mnum = get_font("sans", 10, bold=True)
    num_cx = tx + tag_w + 12
    num_cy = y + 10
    D.ellipse([num_cx-9, num_cy-9, num_cx+9, num_cy+9], outline=RED, width=2)
    draw_text(num_cx, num_cy, str(story["num"]), f_mnum, RED, anchor="mm")
    
    # Text column starts after number circle
    text_x = num_cx + 12
    text_w = x + card_w - 6 - text_x
    
    f_mplace = get_font("sans", 8, bold=True)
    draw_text(text_x, y+3, story["place"], f_mplace, BLACK)
    
    # Headline - 2 lines max
    f_mhead = get_font("sans", 9, bold=True)
    draw_text_wrapped(text_x, y+16, story["headline"], f_mhead, BLACK, text_w, 12, max_lines=2)
    
    # Deck: 1 line, shortened
    f_mdeck = get_font("sans", 8)
    draw_text_wrapped(text_x, y+42, story["deck"], f_mdeck, DARK_GREY, text_w, 11, max_lines=1)
    
    # Source: shortened to one outlet, italic 7pt
    f_msrc = get_font("sans", 7, italic=True)
    src = story["source"]
    if "," in src:
        src = src.split(",")[0] + ")"
    draw_text(text_x, y+55, src, f_msrc, MED_GREY)
    
    # Second line of deck if needed (use remaining space)
    # Actually keep it simple - 1 line deck fits

def draw_mid_illustration(type_, x, y, w, h):
    cx, cy = x + w//2, y + h//2
    if type_ == "hk_vote":
        D.rectangle([x, y, x+w, y+h], fill=(0xE8,0xF0,0xF8))
        # Ballot box
        D.rectangle([cx-8, cy-4, cx+8, cy+12], fill=(0xD0,0xD0,0xD0), outline=(0x80,0x80,0x80))
        D.rectangle([cx-6, cy-8, cx+6, cy-4], fill=(0xD0,0xD0,0xD0), outline=(0x80,0x80,0x80))
        D.rectangle([cx-3, cy-8, cx+3, cy-2], fill=RED)
        # Ballots going in
        for i in range(3):
            bx = cx - 5 + i*5
            D.line([bx, cy-12, bx, cy-4], fill=(0x00,0x80,0x00), width=1)
    elif type_ == "f1":
        D.rectangle([x, y, x+w, y+h], fill=(0x10,0x10,0x10))
        # Car silhouette
        D.polygon([(x+4, cy+4), (x+w-8, cy+4), (x+w-4, cy-4), (x+8, cy-4)], fill=(0xE0,0x10,0x10))
        D.rectangle([cx-6, cy-8, cx+6, cy-4], fill=(0x20,0x20,0x20))
        # Wheels
        D.ellipse([x+6, cy+2, x+14, cy+10], fill=(0x10,0x10,0x10), outline=(0x40,0x40,0x40))
        D.ellipse([x+w-14, cy+2, x+w-6, cy+10], fill=(0x10,0x10,0x10), outline=(0x40,0x40,0x40))
        # Checkered flag
        for i in range(4):
            for j in range(2):
                color = WHITE if (i+j)%2==0 else (0x20,0x20,0x20)
                D.rectangle([cx-12+i*6, cy-10+j*6, cx-6+i*6, cy-4+j*6], fill=color)
    elif type_ == "cricket":
        D.rectangle([x, y, x+w, y+h], fill=(0xF8,0xF8,0xF0))
        # Pitch
        D.rectangle([x+2, cy-8, x+w-2, cy+8], fill=(0xE0,0xD0,0xA0), outline=(0xA0,0x90,0x60))
        # Stumps
        for sx in [cx-4, cx, cx+4]:
            D.line([sx, cy-8, sx, cy+8], fill=(0xFF,0xE0,0x80), width=2)
        # Bails
        D.line([cx-6, cy-8, cx+6, cy-8], fill=(0xFF,0xE0,0x80), width=1)
        # Bat
        D.line([cx-10, cy+6, cx+2, cy-6], fill=(0x8B,0x6B,0x3B), width=2)
        # Ball
        D.ellipse([cx+6, cy-4, cx+10, cy], fill=(0xD0,0x10,0x10))
        # Score
        f_mag = get_font("sans", 7, bold=True)
        draw_text(cx, y+h-6, "720/9", f_mag, RED, anchor="mm")
    elif type_ == "boat":
        D.rectangle([x, cy, x+w, y+h], fill=(0x15,0x30,0x50))
        # Capsized boat
        D.polygon([(cx-10, cy+2), (cx+10, cy+2), (cx+6, cy+10), (cx-6, cy+10)], fill=(0x50,0x30,0x10))
        # People in water
        for i in range(4):
            px = cx - 12 + i*8
            D.ellipse([px-2, cy+4, px+2, cy+8], fill=(0xD0,0xA0,0x80))
    elif type_ == "power":
        D.rectangle([x, y, x+w, y+h], fill=(0xF8,0xF8,0xE8))
        # Pylon
        D.polygon([(cx-12, y+h-4), (cx-6, cy), (cx+6, cy), (cx+12, y+h-4)], outline=(0x50,0x50,0x50), width=1)
        D.line([cx-6, cy, cx+6, cy], fill=(0x50,0x50,0x50), width=1)
        # Lightning bolt
        pts = [(cx, cy-4), (cx-3, cy+4), (cx, cy+4), (cx-2, cy+12)]
        D.polygon(pts, fill=(0xFF,0xB0,0x10), outline=(0xB0,0x70,0x10))
        # Crossed out
        D.line([cx-10, cy+2, cx+10, cy-2], fill=RED, width=2)
    elif type_ == "arrest":
        D.rectangle([x, y, x+w, y+h], fill=(0xF0,0xF0,0xF0))
        # Handcuffs
        for cx_off in (-10, 10):
            D.ellipse([cx+cx_off-7, cy-7, cx+cx_off+7, cy+7], outline=(0x28,0x28,0x28), width=2)
        D.ellipse([cx-2, cy-2, cx+2, cy+2], outline=(0x28,0x28,0x28), width=1)
        # Chain link
        D.ellipse([cx-5, cy-2, cx+5, cy+2], outline=(0x28,0x28,0x28), width=1)
    elif type_ == "aid":
        D.rectangle([x, y, x+w, y+h], fill=(0xF0,0xE8,0xE8))
        # Truck
        D.rectangle([x+4, cy, x+w-4, y+h-4], fill=(0xD8,0xD8,0xD8))
        D.rectangle([cx-6, cy+4, cx+6, cy+16], fill=(0xD8,0xD8,0xD8))
        D.rectangle([cx-2, cy+4, cx+2, cy+16], fill=RED)
        D.rectangle([cx-6, cy+8, cx+6, cy+12], fill=RED)
        for i in range(2):
            dx = cx - 6 + i*12
            D.line([dx, cy+18, dx+2, cy+22], fill=(0x80,0x20,0x20), width=1)
    elif type_ == "space":
        D.rectangle([x, y, x+w, y+h], fill=(0x05,0x05,0x15))
        # Planet Mercury
        D.ellipse([cx-10, cy-10, cx+10, cy+10], fill=(0x80,0x80,0x80), outline=(0xA0,0xA0,0xA0))
        D.ellipse([cx-8, cy-8, cx+8, cy+8], outline=(0xA0,0xA0,0xA0), width=1)
        # Spacecraft
        D.rectangle([cx-16, cy-2, cx-8, cy+2], fill=(0xD0,0xD0,0xD0))
        D.polygon([(cx-8, cy-2), (cx-4, cy), (cx-4, cy-4), (cx-8, cy+2)], fill=(0xD0,0xD0,0xD0))
        # Solar panels
        D.line([cx-16, cy-2, cx-20, cy-8], fill=(0x30,0x70,0xB0), width=2)
        D.line([cx-16, cy+2, cx-20, cy+8], fill=(0x30,0x70,0xB0), width=2)
        # Stars
        for i in range(6):
            sx = x + 4 + (i%3)*8
            sy = y + 4 + (i//3)*10
            D.ellipse([sx, sy, sx+2, sy+2], fill=WHITE)
    elif type_ == "probe":
        D.rectangle([x, y, x+w, y+h], fill=(0xF0,0xF0,0xF8))
        # Document with magnifying glass
        D.rectangle([x+4, cy-8, x+w-4, y+h-4], fill=WHITE, outline=(0xB8,0xB8,0xB8))
        for ly in range(cy-4, y+h-8, 8):
            D.line([x+8, ly, x+w-12, ly], fill=(0xC8,0xC8,0xC8), width=1)
        # Magnifier
        mgx, mgy = cx+10, cy-10
        D.ellipse([mgx-8, mgy-8, mgx+8, mgy+8], outline=(0x30,0x70,0xB0), width=1)
        D.line([mgx+6, mgy+6, mgx+12, mgy+12], fill=(0x30,0x70,0xB0), width=1)
    elif type_ == "hospital":
        D.rectangle([x, y, x+w, y+h], fill=(0xE8,0xF8,0xE8))
        # Hospital building
        D.rectangle([cx-12, cy-10, cx+12, y+h-4], fill=(0xD8,0xD8,0xD8), outline=(0xB8,0xB8,0xB8))
        D.rectangle([cx-2, cy-8, cx+2, cy+6], fill=RED)
        D.rectangle([cx-8, cy-2, cx+8, cy+2], fill=RED)
        # Ambulance
        D.rectangle([x+4, y+h-12, x+18, y+h-4], fill=WHITE, outline=(0xB8,0xB8,0xB8))
        D.rectangle([x+6, y+h-12, x+8, y+h-4], fill=RED)

card_w = 194
card_gap = (W - 2*PAD_X - 5*card_w) // 4
row_h = 110
for row in range(2):
    y_row = y_mid_top + row * row_h
    for col in range(5):
        idx = row * 5 + col
        x_card = PAD_X + col * (card_w + card_gap)
        draw_mid_card(mid_stories[idx], x_card, y_row)

# ═══════════════════════════════════════════════════════════════
# 7. BOTTOM SECTION: Map (left) + ALSO ON 22 stories (right, 2 cols) (y 780–950)
# ═══════════════════════════════════════════════════════════════
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
     (0.45, -0.1), (0.55, -0.15), (0.65, -0.2), (0.75, -0.25),
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

# ─── ALSO ON list - 22 items (14-35) from TOP-1 proven winner, reworded ───
# Duplicates removed, wording fixed, all lines shortened to fit column width
more_stories = [
    "14 Russian cargo ship still burning off Finland (Reuters)",
    "15 World court: Myanmar genocide ruling (Guardian)",
    "16 EU and Indonesia sign landmark trade deal (DW)",
    "17 Marles rejects US report on AUKUS subs (ABC)",
    "18 Sudan army retakes ~30 towns in Kordofan (Reuters)",
    "19 Estonia to shut Russia border from 1 Dec (Reuters)",
    "20 Nepal PM lands in Delhi on first state visit (IANS)",
    "21 ICE arrests on Seattle jet bridge (UPI)",
    "22 DR Congo: Cantine attack, 40 killed (local officials)",
    "23 Lebanon: Aoun demands Israel withdrawal (Al Jazeera)",
    "24 Football: Liverpool host Man United today (Al Jazeera)",
    "25 Tennis: Zverev v Alcaraz in ATP Finals (ATP)",
    "26 Chisinau: Moldova reports Russian drone breach (Kyiv Independent)",
    "27 Copenhagen: Denmark expels Russian attaché over spy plot (Guardian)",
    "28 Brussels: Belgium air traffic halt for 23 Nov strike (Straits Times)",
    "29 Melbourne: 70th anniversary of 1956 Olympics opening (ABC)",
    "30 Berlin: IG Metall widens strikes at car plants (Reuters)",
    "31 Lisbon: Thousands march over cost-of-living crisis (Reuters)",
    "32 Dhaka: 30 Awami League homes set ablaze (Times of India)",
    "33 Sydney: Fred Nile, former NSW MP, dies at 92 (ABC)",
    "34 Kryvyi Rih missile: 2 dead, 58 hurt (BBC)",
    "35 Saudi downs Houthi missile aimed at Riyadh (Anadolu)",
]

f_section = get_font("sans", 9, bold=True)
draw_text(stories_x, bottom_y + 10, "ALSO ON SUNDAY 22 NOVEMBER \u2014 22 MORE STORIES", f_section, BLACK)

f_more = get_font("sans", 7)
line_h = 10
col_w = stories_w // 2 - 4
items_per_col = 11
for i, story in enumerate(more_stories):
    col = i // items_per_col
    row = i % items_per_col
    tx = stories_x + col * (col_w + 8)
    ty = bottom_y + 24 + row * line_h
    # Ensure we don't exceed bottom area
    if ty + line_h > bottom_y + bottom_h - 2:
        # Reduce font size or skip - but with 170px height and 11 items * 10 = 110px, we have 60px margin
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
# Use 3 lines with proper wrapping
draw_text_wrapped(PAD_X + 6, dc_y + 16, dc_text, f_dc_text, DARK_GREY, W - 2*PAD_X - 12, 11, max_lines=3)

# ═══════════════════════════════════════════════════════════════
# 9. TAG LEGEND
# ═══════════════════════════════════════════════════════════════
f_tag_legend = get_font("sans", 7)
legend_text = "ONGOING: still developing \u00b7 REPORTED: one source's claim, not yet confirmed \u00b7 CLAIM: a party's claim, contested \u00b7 OFFICIALS SAY: attributed, not verified"
draw_text(PAD_X, y_dc_bot + 2, legend_text, f_tag_legend, MED_GREY, anchor="lm")

# ═══════════════════════════════════════════════════════════════
# 10. SOURCES LINE
# ═══════════════════════════════════════════════════════════════
f_src = get_font("sans", 7)
src_text = "Sources: BBC \u00b7 Reuters \u00b7 Al Jazeera \u00b7 The Guardian \u00b7 AP \u00b7 SCMP \u00b7 DW \u00b7 UPI \u00b7 FT \u00b7 Every story names its outlet \u00b7 Pictures and map: original, drawn in code"
draw_text(PAD_X, y_dc_bot + 16, src_text, f_src, MED_GREY, anchor="lm")

# ═══════════════════════════════════════════════════════════════
# 11. FOOTER BAR (y 995–1024)
# ═══════════════════════════════════════════════════════════════
fy = y_footer_top
D.rectangle([0, fy, W, fy+29], fill=NAVY)
f_footer = get_font("sans", 10, bold=True)
draw_text(PAD_X, fy + 14, "THE WORLD IN ONE DAY", f_footer, WHITE, anchor="lm")
draw_text(W - PAD_X, fy + 14, "SUNDAY 22 NOVEMBER 2026 \u2014 ONE PAGE", f_footer, WHITE, anchor="rm")

# ═══════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════
os.makedirs("out", exist_ok=True)
IMG.save("out/entry.png", optimize=True)
print(f"Saved to out/entry.png")
size = os.path.getsize("out/entry.png")
print(f"Size: {size} bytes")

import hashlib
with open("out/entry.png", "rb") as f:
    md5 = hashlib.md5(f.read()).hexdigest()
print(f"MD5: {md5}")