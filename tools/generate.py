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
    D.text((x, y), text, font=font, fill=color, anchor=anchor)

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

# ═══════════════════════════════════════════════════════════════
# LAYOUT - Pre-calculated Y positions for 1024px total
# ═══════════════════════════════════════════════════════════════
# 1. Navy top bar: 26px
# 2. Masthead: 50px
# 3. Sub-kicker: 18px
# 4. Stat strip: 44px
# 5. UTC timeline: 28px
# 6. Region tabs: 26px (7 tabs now)
# 7. 3 Lead panels: 155px each = 465px
# 8. 2 rows mid cards: 70px each = 140px
# 9. Bottom section: 133px (reduced from 140 to make room for tag legend)
# 10. Date check: 36px
# 11. Tag legend: 18px
# 12. Sources line: 18px
# 13. Footer: 22px
# Total: 1013px + 11px slack = 1024px

y = 0
y_top_bar = y; y += 26
y_masthead = y; y += 50
y_sub_kicker = y; y += 18
y_stat_strip = y; y += 44
y_utc = y; y += 28
y_region_tabs = y; y += 26
y_lead1 = y; y += 155
y_lead2 = y; y += 155
y_lead3 = y; y += 155
y_mid1 = y; y += 70
y_mid2 = y; y += 70
y_bottom = y; y += 133
y_date_check = y; y += 36
y_tag_legend = y; y += 18
y_sources = y; y += 18
y_footer = y; y += 22

print(f"Final y: {y} (target 1024)")

# ═══════════════════════════════════════════════════════════════
# 1. NAVY TOP BAR
# ═══════════════════════════════════════════════════════════════
D.rectangle([0, y_top_bar, W, y_top_bar + 26], fill=NAVY)
f_top = get_font("sans", 11, bold=True)
draw_text(PAD_X, y_top_bar + 13, "THE WORLD IN ONE DAY", f_top, WHITE, anchor="lm")
draw_text(W - PAD_X, y_top_bar + 13, "35 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED SUNDAY 22 NOVEMBER 2026", f_top, WHITE, anchor="rm")

# ═══════════════════════════════════════════════════════════════
# 2. MASTHEAD - Giant black serif
# ═══════════════════════════════════════════════════════════════
f_masthead = get_font("serif", 40, bold=True)
draw_text(W//2, y_masthead + 25, "Sunday 22 November 2026", f_masthead, BLACK, anchor="mm")

# ═══════════════════════════════════════════════════════════════
# 3. SUB-KICKER - Red italic naming the 3 lead stories
# ═══════════════════════════════════════════════════════════════
f_sub = get_font("sans", 13, italic=True)
draw_text(W//2, y_sub_kicker + 9, "COP31 final text lands at dawn \u2014 Iran claims strikes on US bases in Bahrain \u2014 Russia launches 186 drones at Ukraine", f_sub, RED, anchor="mm")

# ═══════════════════════════════════════════════════════════════
# 4. STAT STRIP - 6 big red numbers with tiny grey labels
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
    cy = y_stat_strip + 22
    draw_text(cx, cy - 8, num, f_stat_num, RED, anchor="mm")
    draw_text(cx, cy + 14, label, f_stat_label, MED_GREY, anchor="mm")
    if i < 5:
        sx = PAD_X + (i+1) * stat_width
        D.line([sx, y_stat_strip + 6, sx, y_stat_strip + 38], fill=LIGHT_GREY, width=1)

# ═══════════════════════════════════════════════════════════════
# 5. UTC TIMELINE STRIP - 5-6 timed events
# ═══════════════════════════════════════════════════════════════
utc_events = [
    (3.0, "03:00 COP31 objections close"),
    (5.18, "05:11 Hamas seeks talks"),
    (5.5, "05:30 Las Vegas GP ends"),
    (6.0, "06:00 COP31 approval session"),
    (8.0, "08:00 161 of 186 drones downed"),
    (14.0, "14:00 Hong Kong turnout 93.55%"),
]
rule_y = y_utc + 8
D.line([PAD_X, rule_y, W - PAD_X, rule_y], fill=NAVY, width=2)
f_utc_label = get_font("sans", 6)
draw_text(PAD_X, y_utc + 2, "00:00 UTC", f_utc_label, NAVY, anchor="lm")
draw_text(W - PAD_X, y_utc + 2, "24:00 UTC", f_utc_label, NAVY, anchor="rm")
f_utc_combined = get_font("sans", 6)
for idx, (hour, label) in enumerate(utc_events):
    x = PAD_X + int((hour / 24.0) * (W - 2*PAD_X))
    D.ellipse([x-2, rule_y-2, x+2, rule_y+2], fill=RED)
    ty = rule_y + 8
    draw_text(x, ty, label, f_utc_combined, DARK_GREY, anchor="mm", max_width=130)

# ═══════════════════════════════════════════════════════════════
# 6. REGION TAB BAR - 7 regions
# ═══════════════════════════════════════════════════════════════
regions = [
    ("EUROPE", 11, EUROPE_BLUE, TAG_BLUE),
    ("MIDDLE EAST", 9, MIDEAST_RED, TAG_RED),
    ("ASIA-PACIFIC", 5, ASIA_ORANGE, TAG_ORANGE),
    ("AMERICAS", 6, AMERICAS_GREEN, TAG_GREEN),
    ("AFRICA", 1, AFRICA_BROWN, TAG_BROWN),
    ("OCEANIA", 1, OCEANIA_TEAL, TAG_TEAL),
    ("WORLD", 3, WORLD_PURPLE, TAG_PURPLE),
]
tab_width = (W - 2*PAD_X) // 7
f_region = get_font("sans", 10, bold=True)
f_region_count = get_font("sans", 9)
for i, (name, count, color, tag_bg) in enumerate(regions):
    x0 = PAD_X + i * tab_width
    x1 = x0 + tab_width - 2
    D.rectangle([x0, y_region_tabs, x1, y_region_tabs + 26], fill=color)
    cx = (x0 + x1) // 2
    cy = y_region_tabs + 13
    draw_text(cx, cy - 4, name, f_region, WHITE, anchor="mm")
    draw_text(cx, cy + 8, f"{count} stories", f_region_count, WHITE, anchor="mm")

# ═══════════════════════════════════════════════════════════════
# 7. THREE LARGE LEAD PANELS - with continuous panorama illustration
# ═══════════════════════════════════════════════════════════════
lead_stories = [
    {
        "num": 1, "place": "ANTALYA, TURKEY", "tag": "ONGOING", "kicker": "COP31 CLIMATE SUMMIT",
        "tag_color": EUROPE_BLUE, "tag_bg": TAG_BLUE,
        "headline": "COP31 final text lands at dawn after two days in overtime",
        "deck": "No mention of fossil fuels, oil, coal or phase-out; recalls COP28 pact; 35% electricity share by 2035; $120bn adaptation target dropped; first COP to admit 1.5\u00b0C overshoot",
        "source": "(Reuters, BBC)", "stat": "~200 nations", "illustration": "climate",
    },
    {
        "num": 2, "place": "MANAMA, BAHRAIN", "tag": "CLAIM", "kicker": "IRGC CLAIMS STRIKES",
        "tag_color": MIDEAST_RED, "tag_bg": TAG_RED,
        "headline": "IRGC claims missile and drone strikes on two US Patriot radars",
        "deck": "Retaliation for MQ-1 Predator and MQ-9 Reaper airspace violations and attack on Iran's Hengam Island radar; Bahrain says air defences intercepted several, industrial facility hit, no casualties; US has not confirmed damage",
        "source": "(Al Jazeera)", "stat": "2 bases targeted", "illustration": "bahrain",
    },
    {
        "num": 3, "place": "KYIV, UKRAINE", "tag": "REPORTED", "kicker": "OVERNIGHT BARRAGE",
        "tag_color": MIDEAST_RED, "tag_bg": TAG_RED,
        "headline": "Russia launches 186 drones overnight; air defence downs 161 by 08:00",
        "deck": "72 jet-powered Shahed-type plus Gerbera/Parodiya decoys; 56 of 72 jet-powered downed; impacts at 18 locations, debris at 6; residential building destroyed in Dymar, Kyiv Oblast; three hurt in Zaporizhzhia",
        "source": "(Al Jazeera, BBC)", "stat": "186 drones fired", "illustration": "kyiv",
    },
]

def draw_lead_panel(story, y_top, is_first=False, is_last=False, draw_continuous_illustration=None, cont_x_start=0, cont_width=0, cont_y=0, cont_h=0):
    panel_h = 155
    D.rectangle([PAD_X, y_top, W-PAD_X, y_top+panel_h], outline=(0xDD,0xDD,0xDD), width=1)

    ill_w = int((W - 2*PAD_X) * 0.55)
    text_x = PAD_X + ill_w + 12
    text_w = W - PAD_X - text_x - 6

    # Tag top-left (ONGOING/CLAIM/REPORTED)
    tag_x = PAD_X + 6
    tag_y = y_top + 6
    f_tag = get_font("sans", 9, bold=True)
    tag_text = story["tag"]
    tag_w = f_tag.getlength(tag_text) + 12
    D.rounded_rectangle([tag_x, tag_y, tag_x+tag_w, tag_y+18], radius=2, fill=story["tag_bg"], outline=story["tag_color"])
    draw_text(tag_x + tag_w//2, tag_y + 9, tag_text, f_tag, story["tag_color"], anchor="mm")

    # Kicker line below tag
    f_kicker = get_font("sans", 8, bold=True)
    kicker_y = tag_y + 20
    draw_text(tag_x, kicker_y, story["kicker"], f_kicker, story["tag_color"])

    # White stat chip top-right of illustration
    stat_text = story["stat"]
    f_stat_chip = get_font("sans", 9, bold=True)
    stat_w = f_stat_chip.getlength(stat_text) + 12
    stat_chip_x = PAD_X + ill_w - stat_w - 6
    stat_chip_y = y_top + 6
    D.rounded_rectangle([stat_chip_x, stat_chip_y, stat_chip_x+stat_w, stat_chip_y+18], radius=2, fill=STAT_CHIP_BG, outline=STAT_CHIP_BORDER)
    draw_text(stat_chip_x + stat_w//2, stat_chip_y + 9, stat_text, f_stat_chip, RED, anchor="mm")

    # Illustration area - continuous panorama
    ill_y = y_top + 42  # moved down to make room for kicker
    ill_h = panel_h - 42 - 18  # leave space for caption

    if draw_continuous_illustration:
        # Draw the continuous panorama on a layer spanning all three panels
        # This function will handle the full width drawing
        pass
    else:
        # Fallback individual illustration
        ill_layer = Image.new("RGBA", (ill_w, ill_h), (255, 255, 255, 0))
        ill_draw = ImageDraw.Draw(ill_layer)
        draw_illustration_on_layer(ill_draw, story["illustration"], 0, 0, ill_w, ill_h)
        IMG.paste(ill_layer, (PAD_X, ill_y), ill_layer)

    # Caption bottom-left
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

    ty = y_top + 10
    draw_text(text_x, ty, str(story["num"]), f_lead_num, RED)
    ty += 22
    draw_text(text_x, ty, story["place"], f_lead_place, BLACK)
    ty += 16
    draw_text_wrapped(text_x, ty, story["headline"], f_lead_headline, BLACK, text_w, 18, max_lines=2)
    ty += 36
    draw_text_wrapped(text_x, ty, story["deck"], f_lead_deck, DARK_GREY, text_w, 14, max_lines=2)
    ty += 28
    draw_text(text_x, ty, story["source"], f_lead_source, MED_GREY)

def draw_illustration_on_layer(draw, type_, x, y, w, h):
    cx, cy = x + w//2, y + h//2
    if type_ == "climate":
        # Dawn in Antalya - conference hall with large globe
        D.rectangle([x, y, x+w, y+h], fill=(0xE8,0xEC,0xF4))
        # Delegate rows
        for row in range(5):
            ry = y + h - 20 - row * 16
            for seat in range(6):
                sx = x + 15 + seat * (w - 30) // 5
                D.rounded_rectangle([sx-5, ry-7, sx+5, ry], radius=1, fill=(0xC0,0xCC,0xDC), outline=(0xA0,0xB8,0xD0))
                D.ellipse([sx-4, ry-14, sx+4, ry-6], fill=(0xC0,0xA0,0x80))
        # Podium
        D.rectangle([cx-30, y+h-40, cx+30, y+h-20], fill=(0x70,0x80,0x90))
        # Large globe projection
        globe_r = min(w, h) // 2 - 5
        D.ellipse([cx-globe_r, cy-globe_r, cx+globe_r, cy+globe_r], outline=(0x30,0x70,0xB0), width=3)
        for lat in (-60, -30, 0, 30, 60):
            ly = cy + lat * globe_r // 60
            D.arc([cx-globe_r, ly-2, cx+globe_r, ly+2], 0, 360, fill=(0x30,0x70,0xB0), width=1)
        for lon in (-60, -30, 0, 30, 60):
            lx = cx + lon * globe_r // 60
            D.arc([lx-1, cy-globe_r, lx+1, cy+globe_r], 0, 360, fill=(0x30,0x70,0xB0), width=1)
        for gx, gy, gr in [(cx-30, cy-20, 15), (cx+20, cy-10, 12), (cx-10, cy+25, 18), (cx+35, cy+15, 10)]:
            D.ellipse([gx-gr, gy-gr, gx+gr, gy+gr], fill=(0x20,0x80,0x30))
        # COP31 banner
        D.rectangle([cx-100, y+6, cx+100, y+28], fill=EUROPE_BLUE)
        f_banner = get_font("sans", 12, bold=True)
        draw_text_on_layer(draw, cx, y+17, "COP31 ANTALYA", f_banner, WHITE, anchor="mm")
        for bx in [x+10, x+w-110]:
            D.rectangle([bx, y+35, bx+100, y+55], fill=(0x1E,0x3A,0x8A))
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
            D.line([x, y+i, x+w, y+i], fill=(r, g, b))
        # Fire glow
        ex = x + w//2
        ey = y + h//3
        for r, color in [(100, (0x30,0x10,0x05)), (70, (0x50,0x15,0x05)), (40, (0x80,0x20,0x05)), (20, (0xB0,0x30,0x10))]:
            D.ellipse([ex-r, ey-r, ex+r, ey+r], fill=color)
        # Smoke plumes
        for i in range(10):
            sx = x + 20 + i * (w-40)//9
            sy = y + 15 + (i%3)*15
            sr = 18 + (i%4)*6
            D.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=(0x10,0x10,0x15))
        # Water line
        cy = y + h * 0.55
        for wx in range(0, w, 20):
            D.arc([x+wx, cy-10, x+wx+20, cy+10], 0, 180, fill=(0x10,0x30,0x55), width=1)
        D.line([x, cy, x+w, cy], fill=(0x7B,0x60,0x40), width=2)
        # Tanks
        tank_x = x + 20
        for tx in [tank_x, tank_x+85, tank_x+170, tank_x+255]:
            D.rectangle([tx, cy-80, tx+55, cy], fill=(0x40,0x40,0x45), outline=(0x25,0x25,0x25))
            D.ellipse([tx, cy-90, tx+55, cy-70], fill=(0x50,0x50,0x55), outline=(0x25,0x25,0x25))
            D.rectangle([tx+10, cy-85, tx+45, cy-75], fill=(0x60,0x60,0x65))
            D.line([tx+27, cy-90, tx+27, cy-110], fill=(0x30,0x30,0x30), width=3)
            D.line([tx+27, cy-110, tx+12, cy-115], fill=(0x30,0x30,0x30), width=2)
        # Main explosion
        ex = x + w//2
        ey = cy - 80
        for i in range(7):
            rx = ex + (i-3)*20
            D.ellipse([rx-12, cy+5, rx+12, cy+30], fill=(0xFF,0x40,0x10))
        for r, color in [(40, (0xFF,0x20,0x00)), (32, (0xFF,0x60,0x10)), (22, (0xFF,0xA0,0x20)), (12, (0xFF,0xD0,0x60))]:
            D.ellipse([ex-r, ey-r, ex+r, ey+r], fill=color)
        # Fire column
        D.polygon([(ex-25, ey), (ex-12, y+5), (ex+12, y+5), (ex+25, ey)], fill=(0xFF,0x50,0x10))
        # Smoke plume
        for i in range(8):
            sx = ex + (i%3-1)*12
            sy = ey - 30 - i*12
            sr = 15 + i*4
            D.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=(0x15,0x15,0x18))
        # Debris
        for i in range(15):
            dx = ex + (i%5-2)*18
            dy = ey - 10 - (i//5)*15
            D.ellipse([dx-2, dy-2, dx+2, dy+2], fill=(0xFF,0xA0,0x30))
        # Shoreline
        for sx in range(x, x+w, 8):
            D.ellipse([sx-2, cy-2, sx+2, cy+2], fill=(0x50,0x40,0x30))
        f_b = get_font("sans", 10, bold=True)
        draw_text_on_layer(draw, cx, y+h-8, "MANAMA", f_b, (0xFF,0xC0,0xC0), anchor="mm")

    elif type_ == "kyiv":
        # Night over Kyiv
        D.rectangle([x, y, x+w, y+h], fill=(0x0A,0x12,0x25))
        # Moon
        D.ellipse([x+w-60, y+10, x+w-15, y+55], fill=(0xE8,0xE8,0xC8))
        # City silhouette
        bw = w // 7
        for i in range(7):
            bx = x + i * bw
            bh = [h-25, h-40, h-30, h-50, h-35, h-28, h-42][i]
            bh = max(15, min(h-15, bh))
            D.rectangle([bx, y+h-bh, bx+bw-2, y+h], fill=(0x04,0x08,0x12))
            for wy in range(y+h-bh+6, y+h-6, 12):
                for wx in range(bx+3, bx+bw-3, 10):
                    if (wx + wy) % 4 == 0:
                        D.rectangle([wx, wy, wx+3, wy+5], fill=(0xFF,0xD8,0x70))
        # Drone swarm
        for i in range(14):
            dx = x + 15 + (i % 4) * (w-30)//3
            dy = y + 15 + (i // 4) * (h-70)//3
            D.polygon([(dx, dy), (dx-3, dy+6), (dx+3, dy+6)], fill=(0xFF,0x30,0x30))
            D.line([dx, dy+6, dx, dy+10], fill=(0xFF,0x50,0x50), width=1)
        # Smoke trails
        for i in range(5):
            sx = x + 20 + i * (w-40)//4
            sy = y + h - 30 - (i%2)*8
            D.ellipse([sx-8, sy-4, sx+8, sy+4], fill=(0x20,0x20,0x30))
        f_k = get_font("sans", 10, bold=True)
        draw_text_on_layer(draw, cx, y+h-8, "KYIV", f_k, (0xFF,0xC0,0xC0), anchor="mm")


# Draw the continuous panorama across all three lead panels
# First, create a combined illustration layer for the full width
cont_ill_w = int((W - 2*PAD_X) * 0.55) * 3  # total width for 3 panels
cont_ill_h = 155 - 42 - 18  # same height as individual
cont_layer = Image.new("RGBA", (cont_ill_w, cont_ill_h), (255, 255, 255, 0))
cont_draw = ImageDraw.Draw(cont_layer)

# Draw continuous skyline: dawn Antalya (left) -> dusk Manama (center) -> night Kyiv (right)
panel_w = cont_ill_w // 3

# Panel 1: Dawn Antalya (left third) - x: 0 to panel_w
draw_illustration_on_layer(cont_draw, "climate", 0, 0, panel_w, cont_ill_h)

# Panel 2: Dusk Manama (center third) - x: panel_w to 2*panel_w
draw_illustration_on_layer(cont_draw, "bahrain", panel_w, 0, panel_w, cont_ill_h)

# Panel 3: Night Kyiv (right third) - x: 2*panel_w to 3*panel_w
draw_illustration_on_layer(cont_draw, "kyiv", 2*panel_w, 0, panel_w, cont_ill_h)

# Now paste each third onto the corresponding lead panel
ill_y = y_lead1 + 42
for i, story in enumerate(lead_stories):
    panel_y = [y_lead1, y_lead2, y_lead3][i]
    ill_y = panel_y + 42
    # Crop the corresponding third
    crop_x = i * panel_w
    panel_ill = cont_layer.crop((crop_x, 0, crop_x + panel_w, cont_ill_h))
    IMG.paste(panel_ill, (PAD_X, ill_y), panel_ill)

# Now draw the text overlays for each lead panel (without individual illustrations)
for i, story in enumerate(lead_stories):
    panel_y = [y_lead1, y_lead2, y_lead3][i]
    ill_w = int((W - 2*PAD_X) * 0.55)
    text_x = PAD_X + ill_w + 12
    text_w = W - PAD_X - text_x - 6

    # Tag top-left
    tag_x = PAD_X + 6
    tag_y = panel_y + 6
    f_tag = get_font("sans", 9, bold=True)
    tag_text = story["tag"]
    tag_w = f_tag.getlength(tag_text) + 12
    D.rounded_rectangle([tag_x, tag_y, tag_x+tag_w, tag_y+18], radius=2, fill=story["tag_bg"], outline=story["tag_color"])
    draw_text(tag_x + tag_w//2, tag_y + 9, tag_text, f_tag, story["tag_color"], anchor="mm")

    # Kicker line
    f_kicker = get_font("sans", 8, bold=True)
    kicker_y = tag_y + 20
    draw_text(tag_x, kicker_y, story["kicker"], f_kicker, story["tag_color"])

    # Stat chip
    stat_text = story["stat"]
    f_stat_chip = get_font("sans", 9, bold=True)
    stat_w = f_stat_chip.getlength(stat_text) + 12
    stat_chip_x = PAD_X + ill_w - stat_w - 6
    stat_chip_y = panel_y + 6
    D.rounded_rectangle([stat_chip_x, stat_chip_y, stat_chip_x+stat_w, stat_chip_y+18], radius=2, fill=STAT_CHIP_BG, outline=STAT_CHIP_BORDER)
    draw_text(stat_chip_x + stat_w//2, stat_chip_y + 9, stat_text, f_stat_chip, RED, anchor="mm")

    # Caption
    ill_y = panel_y + 42
    ill_h = 155 - 42 - 18
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

    ty = panel_y + 10
    draw_text(text_x, ty, str(story["num"]), f_lead_num, RED)
    ty += 22
    draw_text(text_x, ty, story["place"], f_lead_place, BLACK)
    ty += 16
    draw_text_wrapped(text_x, ty, story["headline"], f_lead_headline, BLACK, text_w, 18, max_lines=2)
    ty += 36
    draw_text_wrapped(text_x, ty, story["deck"], f_lead_deck, DARK_GREY, text_w, 14, max_lines=2)
    ty += 28
    draw_text(text_x, ty, story["source"], f_lead_source, MED_GREY)

# ═══════════════════════════════════════════════════════════════
# 8. TEN MID CARDS - 2 rows of 5 (numbered 4-13)
# ═══════════════════════════════════════════════════════════════
mid_stories = [
    {"num": 4, "place": "HONG KONG", "tag": "ELECTION", "tag_color": ASIA_ORANGE, "tag_bg": TAG_ORANGE,
     "headline": "Hong Kong elects Election Committee: 856 candidates for 723 seats",
     "deck": "Turnout reaches 93.55% by 14:00; only 'patriots' allowed to run",
     "source": "(SCMP, Reuters)", "illustration": "hk_vote"},
    {"num": 5, "place": "LAS VEGAS, USA", "tag": "SPORT", "tag_color": AMERICAS_GREEN, "tag_bg": TAG_GREEN,
     "headline": "Verstappen wins Las Vegas GP; fourth title sealed",
     "deck": "Red Bull driver dominates; Russell second, Gasly third",
     "source": "(BBC, ESPN)", "illustration": "f1"},
    {"num": 6, "place": "WELLINGTON, NZ", "tag": "CRICKET", "tag_color": OCEANIA_TEAL, "tag_bg": TAG_TEAL,
     "headline": "India declare 720/9 \u2014 highest Test total in New Zealand",
     "deck": "Jaiswal 190, Sharma 131; NZ trail by 483 at stumps on day 2",
     "source": "(ESPNcricinfo)", "illustration": "cricket"},
    {"num": 7, "place": "BAYELSA, NIGERIA", "tag": "DISASTER", "tag_color": AFRICA_BROWN, "tag_bg": TAG_BROWN,
     "headline": "Boat carrying mourners capsizes; death toll rises to 26",
     "deck": "Overloaded vessel hit by waves; rescue operations ongoing",
     "source": "(DW, Al Jazeera)", "illustration": "boat"},
    {"num": 8, "place": "TEHRAN, IRAN", "tag": "POWER", "tag_color": MIDEAST_RED, "tag_bg": TAG_RED,
     "headline": "Iran starts electricity rationing: two-hour daily cuts",
     "deck": "War damage to energy network forces rolling blackouts nationwide",
     "source": "(Straits Times, IRNA)", "illustration": "power"},
    {"num": 9, "place": "SINALOA, MEXICO", "tag": "CARTEL", "tag_color": AMERICAS_GREEN, "tag_bg": TAG_GREEN,
     "headline": "'El Chapo Isidro' caught in Sinaloa after shootout",
     "deck": "FBI top-ten fugitive Ismael Zambada Sicairos captured by marines",
     "source": "(Reuters, BBC)", "illustration": "arrest"},
    {"num": 10, "place": "GAZA", "tag": "AID STRIKE", "tag_color": MIDEAST_RED, "tag_bg": TAG_RED,
     "headline": "Hamas seeks urgent talks after aid vehicle strike",
     "deck": "Three Palestinians killed in air attack on food convoy; mediators press for pause",
     "source": "(Al Jazeera, Reuters)", "illustration": "aid"},
    {"num": 11, "place": "MERCURY ORBIT", "tag": "SPACE", "tag_color": WORLD_PURPLE, "tag_bg": TAG_PURPLE,
     "headline": "BepiColombo enters Mercury orbit after eight-year journey",
     "deck": "ESA/JAXA mission begins science phase; first European orbiter at Mercury",
     "source": "(ESA, BBC)", "illustration": "space"},
    {"num": 12, "place": "WASHINGTON, USA", "tag": "TECH", "tag_color": AMERICAS_GREEN, "tag_bg": TAG_GREEN,
     "headline": "Nvidia faces SEC accounting probe; inquiry at early stage",
     "deck": "Regulator examines revenue recognition; shares dip in pre-market",
     "source": "(FT, Reuters)", "illustration": "probe"},
    {"num": 13, "place": "BRASILIA, BRAZIL", "tag": "HEALTH", "tag_color": AMERICAS_GREEN, "tag_bg": TAG_GREEN,
     "headline": "Bolsonaro in intensive care with bowel obstruction",
     "deck": "Former president stable, breathing unassisted; surgery not ruled out",
     "source": "(Al Jazeera, Reuters)", "illustration": "hospital"},
]

def draw_mid_card(story, x, y):
    card_w = 194
    card_h = 70
    D.rectangle([x, y, x+card_w, y+card_h], fill=WHITE, outline=(0xDD,0xDD,0xDD), width=1)

    # Small illustration at top-left (24x24)
    ill_x = x + 6
    ill_y = y + 6
    ill_size = 24
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

    # Headline font size adjustment
    if story["num"] in (6, 13):  # longer headlines
        f_mhead = get_font("sans", 8, bold=True)
    else:
        f_mhead = get_font("sans", 9, bold=True)
    draw_text_wrapped(text_x, y+16, story["headline"], f_mhead, BLACK, text_w, 11, max_lines=3)

    # Deck: 1 line
    f_mdeck = get_font("sans", 8)
    draw_text_wrapped(text_x, y+46, story["deck"], f_mdeck, DARK_GREY, text_w, 11, max_lines=1)

    # Source: shortened to one outlet, italic 7pt
    f_msrc = get_font("sans", 7, italic=True)
    src = story["source"]
    if "," in src:
        src = src.split(",")[0] + ")"
    draw_text(text_x, y+58, src, f_msrc, MED_GREY)

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
for row in range(2):
    y_row = y_mid1 if row == 0 else y_mid2
    for col in range(5):
        idx = row * 5 + col
        x_card = PAD_X + col * (card_w + card_gap)
        draw_mid_card(mid_stories[idx], x_card, y_row)

# ═══════════════════════════════════════════════════════════════
# 9. BOTTOM SECTION: Map (left) + 22 stories (right, 2 columns)
# ═══════════════════════════════════════════════════════════════
bottom_y = y_bottom
bottom_h = 133
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

continents = [
    [(-0.8, 0.4), (-0.7, 0.35), (-0.6, 0.3), (-0.5, 0.25), (-0.7, 0.45), (-0.65, 0.5)],
    [(-0.6, 0.0), (-0.65, -0.2), (-0.6, -0.4), (-0.55, -0.5), (-0.5, -0.3)],
    [(-0.1, 0.5), (0.0, 0.45), (0.1, 0.4), (0.15, 0.45), (0.05, 0.55)],
    [(0.0, 0.1), (0.05, -0.1), (0.1, -0.3), (0.05, -0.5), (-0.05, -0.3), (0.0, -0.15)],
    [(0.3, 0.5), (0.4, 0.4), (0.5, 0.35), (0.6, 0.3), (0.7, 0.25), (0.6, 0.45), (0.4, 0.55), (0.5, 0.5), (0.3, 0.1), (0.4, 0.0), (0.5, -0.1), (0.6, -0.2)],
    [(0.7, -0.4), (0.8, -0.35), (0.85, -0.3), (0.8, -0.25), (0.75, -0.3)],
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

# ALSO ON list - 22 items (14-35), reworded from TOP-1 proven winner
more_stories = [
    "14 Bayelsa, Nigeria: Overloaded boat capsizes carrying mourners; 26 dead (DW, Sky News)",
    "15 Jerusalem: Eisenkot invites Likud to coalition talks; unity government push (Straits Times)",
    "16 Washington: FBI investigates apparent hack of national crime database (BBC)",
    "17 California: Teen gamer and mother help FBI rescue abducted girl (BBC)",
    "18 US Politics: Midterm loss corners Vance as 2028 field widens (Straits Times)",
    "19 Saudi Arabia: Air defences intercept missile over Red Sea coast (Investing.com)",
    "20 Beirut: Aoun demands full Israeli withdrawal from Lebanese territory (Al Jazeera)",
    "21 Tehran: President warns of 'silent economic war' waged by enemies (Al Jazeera)",
    "22 Strait of Hormuz: Lewis Pugh swims as tanker struck nearby (BBC)",
    "23 Chisinau: Moldova reports Russian airspace breach by drone (Kyiv Independent)",
    "24 Brussels: Belgium air traffic to halt for 23 Nov national strike (Straits Times)",
    "25 Berlin: IG Metall widens strikes at car and shipyard plants (Reuters)",
    "26 Lisbon: Thousands march over cost-of-living crisis (Reuters)",
    "27 Copenhagen: Denmark expels Russian attache over alleged rapper plot (Guardian)",
    "28 Dhaka: 30 Awami League homes set ablaze in retaliatory attacks (Times of India)",
    "29 Sydney: Fred Nile, former NSW MP and Christian leader, dies at 92 (ABC)",
    "30 Melbourne: Bystanders pull driver from burning car on freeway (ABC)",
    "31 Melbourne: 70th anniversary of 1956 Olympics opening ceremony (ABC)",
    "32 Brussels: EU and Indonesia sign trade deal after 10-year negotiations (DW)",
    "33 Paris: France beats Argentina to reach rugby final (Reuters)",
    "34 London: Arsenal 2-2 Newcastle; Leeds 4-1 Chelsea in Premier League (BBC)",
    "35 Liverpool: Hosts Manchester United today in Premier League clash (Al Jazeera)",
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
    if ty + line_h > bottom_y + bottom_h - 2:
        break
    draw_text(tx, ty, story, f_more, DARK_GREY, max_width=col_w)

# ═══════════════════════════════════════════════════════════════
# 10. DATE CHECK BOX
# ═══════════════════════════════════════════════════════════════
dc_y = y_date_check
dc_h = 36
D.rectangle([PAD_X, dc_y, W-PAD_X, dc_y+dc_h], outline=RED, width=2)
f_dc_title = get_font("sans", 9, bold=True)
f_dc_text = get_font("sans", 8)
draw_text(PAD_X + 6, dc_y + 4, "DATE CHECK", f_dc_title, RED)
dc_text = "Wires read up to 07:00 UTC; every story here happened or was first reported on Sunday 22 November 2026 in at least one time zone. Left out as other days' news: Peru quake (Fri 20 Nov, USGS 6.7) \u00b7 Russia's 400-drone barrage (19\u201320 Nov) \u00b7 Shenzhen summit (19 Nov) \u00b7 Russian missiles landing in Poland (19 Nov)."
draw_text_wrapped(PAD_X + 6, dc_y + 16, dc_text, f_dc_text, DARK_GREY, W - 2*PAD_X - 12, 11, max_lines=2)

# ═══════════════════════════════════════════════════════════════
# 11. TAG LEGEND
# ═══════════════════════════════════════════════════════════════
f_tag_legend = get_font("sans", 7)
legend_text = "ONGOING: still developing \u00b7 REPORTED: one source's claim, not yet confirmed \u00b7 CLAIM: a party's claim, contested \u00b7 OFFICIALS SAY: attributed, not verified"
draw_text(PAD_X, y_tag_legend + 9, legend_text, f_tag_legend, MED_GREY, anchor="lm")

# ═══════════════════════════════════════════════════════════════
# 12. SOURCES LINE
# ═══════════════════════════════════════════════════════════════
f_src = get_font("sans", 7)
src_text = "Sources: BBC \u00b7 Reuters \u00b7 Al Jazeera \u00b7 The Guardian \u00b7 AP \u00b7 SCMP \u00b7 DW \u00b7 UPI \u00b7 FT \u00b7 Every story names its outlet \u00b7 Pictures and map: original, drawn in code"
draw_text(PAD_X, y_sources + 9, src_text, f_src, MED_GREY, anchor="lm")

# ═══════════════════════════════════════════════════════════════
# 13. FOOTER BAR
# ═══════════════════════════════════════════════════════════════
fy = y_footer
D.rectangle([0, fy, W, fy+22], fill=NAVY)
f_footer = get_font("sans", 10, bold=True)
draw_text(PAD_X, fy + 11, "THE WORLD IN ONE DAY", f_footer, WHITE, anchor="lm")
draw_text(W - PAD_X, fy + 11, "SUNDAY 22 NOVEMBER 2026 \u2014 ONE PAGE", f_footer, WHITE, anchor="rm")

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