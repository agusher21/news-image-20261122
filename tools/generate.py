#!/usr/bin/env python3
"""
Generate the news-image-20261122 entry: a dense newspaper front page, 1024x1024 PNG.
Every element drawn in code - no external assets, no network.
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
WORLD_PURPLE = (0x5A, 0x2A, 0x7A)
TAG_BLUE = (0xD6, 0xE4, 0xF8)
TAG_RED = (0xF8, 0xD6, 0xD6)
TAG_GREEN = (0xD6, 0xF8, 0xDB)
TAG_ORANGE = (0xF8, 0xE4, 0xD6)
TAG_BROWN = (0xF0, 0xE4, 0xD6)
TAG_PURPLE = (0xE8, 0xD6, 0xF8)
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

# ═══════════════════════════════════════════════════════════════
# LAYOUT - Pre-calculated Y positions for 1024px total
# ═══════════════════════════════════════════════════════════════
# 1. Navy top bar: 26px
# 2. Masthead: 50px
# 3. Sub-kicker: 18px
# 4. Stat strip: 44px
# 5. UTC timeline: 28px
# 6. Region tabs: 26px
# 7. 3 Lead panels: 155px each = 465px
# 8. 2 rows mid cards: 70px each = 140px
# 9. Bottom section: 140px
# 10. Date check: 36px
# 11. Sources: 18px
# 12. Footer: 22px
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
y_bottom = y; y += 140
y_date_check = y; y += 36
y_sources = y; y += 18
y_footer = y; y += 22

print(f"Final y: {y} (target 1024)")

# ═══════════════════════════════════════════════════════════════
# 1. NAVY TOP BAR
# ═══════════════════════════════════════════════════════════════
D.rectangle([0, y_top_bar, W, y_top_bar + 26], fill=NAVY)
f_top = get_font("sans", 11, bold=True)
draw_text(PAD_X, y_top_bar + 13, "THE WORLD IN ONE DAY", f_top, WHITE, anchor="lm")
draw_text(W - PAD_X, y_top_bar + 13, "35 STORIES - 6 REGIONS - EVERY ONE DATED SUNDAY 22 NOVEMBER 2026", f_top, WHITE, anchor="rm")

# ═══════════════════════════════════════════════════════════════
# 2. MASTHEAD - Giant black serif
# ═══════════════════════════════════════════════════════════════
f_masthead = get_font("serif", 40, bold=True)
draw_text(W//2, y_masthead + 25, "Sunday 22 November 2026", f_masthead, BLACK, anchor="mm")

# ═══════════════════════════════════════════════════════════════
# 3. SUB-KICKER - Red italic
# ═══════════════════════════════════════════════════════════════
f_sub = get_font("sans", 13, italic=True)
draw_text(W//2, y_sub_kicker + 9, "Climate deal in sight at COP31 - Russia's 400-drone barrage on Ukraine - Iran hits US bases in Bahrain", f_sub, RED, anchor="mm")

# ═══════════════════════════════════════════════════════════════
# 4. STAT STRIP - 6 big red numbers with tiny grey labels
# ═══════════════════════════════════════════════════════════════
stats = [
    ("~200", "nations at the COP31 talks"),
    ("03:00", "GMT deadline for objections"),
    ("400+", "drones fired at Ukraine"),
    ("110", "missiles in the same night"),
    ("7+", "people killed in Kyiv"),
    ("2", "US bases targeted in Bahrain"),
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

# ════════════════════════════════════════════════════════════════
# 5. UTC TIMELINE STRIP - THE UNIQUE TWIST
# ════════════════════════════════════════════════════════════════
utc_events = [
    (3.0, "03:00 COP31 deadline"),
    (6.0, "06:00 Sparta II"),
    (9.0, "09:00 Peru quake"),
    (12.0, "12:00 Oman tankers"),
    (15.0, "15:00 France UN"),
    (19.0, "19:00 Bahrain strikes"),
    (22.0, "22:00 Kyiv barrage"),
]
# Rule higher in utc band; combined labels in two rows BELOW rule, ending before region tabs at 166
rule_y = y_utc + 8  # = 146
D.line([PAD_X, rule_y, W - PAD_X, rule_y], fill=NAVY, width=2)
# UTC endpoints at top of band
f_utc_label = get_font("sans", 6)
draw_text(PAD_X, y_utc + 2, "00:00 UTC", f_utc_label, NAVY, anchor="lm")
draw_text(W - PAD_X, y_utc + 2, "24:00 UTC", f_utc_label, NAVY, anchor="rm")
f_utc_combined = get_font("sans", 6)
# Two rows: row 0 (events 0-3) at rule_y+8=154, row 1 (events 4-6) at rule_y+16=162
for idx, (hour, label) in enumerate(utc_events):
    x = PAD_X + int((hour / 24.0) * (W - 2*PAD_X))
    D.ellipse([x-2, rule_y-2, x+2, rule_y+2], fill=RED)
    row = idx // 4  # 4 per row: 0-3 top row, 4-6 bottom row
    if row == 0:
        ty = rule_y + 8   # 154
    else:
        ty = rule_y + 16  # 162 - baseline at 162, text fits 158-166
    draw_text(x, ty, label, f_utc_combined, DARK_GREY, anchor="mm", max_width=110)

# ═══════════════════════════════════════════════════════════════
# 6. REGION TAB BAR
# ═══════════════════════════════════════════════════════════════
regions = [
    ("EUROPE", 11, EUROPE_BLUE, TAG_BLUE),
    ("MIDDLE EAST", 9, MIDEAST_RED, TAG_RED),
    ("AMERICAS", 6, AMERICAS_GREEN, TAG_GREEN),
    ("ASIA-PACIFIC", 5, ASIA_ORANGE, TAG_ORANGE),
    ("AFRICA", 1, AFRICA_BROWN, TAG_BROWN),
    ("WORLD", 3, WORLD_PURPLE, TAG_PURPLE),
]
tab_width = (W - 2*PAD_X) // 6
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
# 7. THREE LARGE LEAD PANELS
# ═══════════════════════════════════════════════════════════════
lead_stories = [
    {
        "num": 1, "place": "ANTALYA, TURKEY", "tag": "CLIMATE",
        "tag_color": EUROPE_BLUE, "tag_bg": TAG_BLUE,
        "headline": "COP31 climate talks close in on a final deal",
        "deck": "A new package lands after a fight over fossil fuels; delegations have until 03:00 GMT to object before a final plenary.",
        "source": "(Reuters, BBC)", "stat": "~200 nations", "illustration": "climate",
    },
    {
        "num": 2, "place": "KYIV, UKRAINE", "tag": "WAR",
        "tag_color": MIDEAST_RED, "tag_bg": TAG_RED,
        "headline": "Russia fires 400 drones and 110 missiles",
        "deck": "One of the war's largest overnight attacks; at least seven people are killed in Kyiv.",
        "source": "(Al Jazeera)", "stat": "7+ killed", "illustration": "drones",
    },
    {
        "num": 3, "place": "MANAMA, BAHRAIN", "tag": "IRAN WAR",
        "tag_color": MIDEAST_RED, "tag_bg": TAG_RED,
        "headline": "Iran strikes US bases in Bahrain",
        "deck": "An industrial site burns, no injuries; tankers are hit in Hormuz.",
        "source": "(Al Jazeera, CNA)", "stat": "2 bases hit", "illustration": "explosion",
    },
]

def draw_lead_panel(story, y_top):
    panel_h = 155
    D.rectangle([PAD_X, y_top, W-PAD_X, y_top+panel_h], outline=(0xDD,0xDD,0xDD), width=1)
    
    ill_w = int((W - 2*PAD_X) * 0.55)
    text_x = PAD_X + ill_w + 12
    text_w = W - PAD_X - text_x - 6
    
    # Red tag top-left
    tag_x = PAD_X + 6
    tag_y = y_top + 6
    f_tag = get_font("sans", 9, bold=True)
    tag_text = story["tag"]
    tag_w = f_tag.getlength(tag_text) + 12
    D.rounded_rectangle([tag_x, tag_y, tag_x+tag_w, tag_y+18], radius=2, fill=story["tag_bg"], outline=story["tag_color"])
    draw_text(tag_x + tag_w//2, tag_y + 9, tag_text, f_tag, story["tag_color"], anchor="mm")
    
    # White stat chip top-right of illustration
    stat_text = story["stat"]
    f_stat_chip = get_font("sans", 9, bold=True)
    stat_w = f_stat_chip.getlength(stat_text) + 12
    stat_chip_x = PAD_X + ill_w - stat_w - 6
    stat_chip_y = y_top + 6
    D.rounded_rectangle([stat_chip_x, stat_chip_y, stat_chip_x+stat_w, stat_chip_y+18], radius=2, fill=STAT_CHIP_BG, outline=STAT_CHIP_BORDER)
    draw_text(stat_chip_x + stat_w//2, stat_chip_y + 9, stat_text, f_stat_chip, RED, anchor="mm")
    
    # Illustration area - draw on separate RGBA layer to clip to panel
    ill_y = y_top + 28
    ill_h = panel_h - 28 - 18  # leave space for caption
    ill_layer = Image.new("RGBA", (ill_w, ill_h), (255, 255, 255, 0))
    ill_draw = ImageDraw.Draw(ill_layer)
    draw_illustration_on_layer(ill_draw, story["illustration"], 0, 0, ill_w, ill_h)
    # Paste onto main image
    IMG.paste(ill_layer, (PAD_X, ill_y), ill_layer)
    
    # Caption bottom-left
    f_caption = get_font("sans", 8, italic=True)
    captions = {
        "climate": "Conference hall, delegates in final session",
        "drones": "Night sky over Kyiv, drone swarm incoming",
        "explosion": "Bahrain coast, smoke rising from base",
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
        # Conference hall: rows of seats, podium, LARGE globe projection filling width
        draw.rectangle([x, y, x+w, y+h], fill=(0xF0,0xF4,0xF8))
        # MORE delegate rows - fill the hall
        for row in range(6):
            ry = y + h - 20 - row * 16
            for seat in range(7):
                sx = x + 15 + seat * (w - 30) // 6
                draw.rounded_rectangle([sx-5, ry-7, sx+5, ry], radius=1, fill=(0xD0,0xDC,0xE8), outline=(0xA0,0xB8,0xD0))
                # Delegate head
                draw.ellipse([sx-4, ry-14, sx+4, ry-6], fill=(0xC0,0xA0,0x80))
        # Podium
        draw.rectangle([cx-30, y+h-40, cx+30, y+h-20], fill=(0x70,0x80,0x90))
        # LARGER Globe on wall - fills most of illustration width
        globe_r = min(w, h) // 2 - 5
        draw.ellipse([cx-globe_r, cy-globe_r, cx+globe_r, cy+globe_r], outline=(0x30,0x70,0xB0), width=3)
        for lat in (-60, -30, 0, 30, 60):
            ly = cy + lat * globe_r // 60
            draw.arc([cx-globe_r, ly-2, cx+globe_r, ly+2], 0, 360, fill=(0x30,0x70,0xB0), width=1)
        for lon in (-60, -30, 0, 30, 60):
            lx = cx + lon * globe_r // 60
            draw.arc([lx-1, cy-globe_r, lx+1, cy+globe_r], 0, 360, fill=(0x30,0x70,0xB0), width=1)
        # Continents suggestion - green blobs
        for gx, gy, gr in [(cx-30, cy-20, 15), (cx+20, cy-10, 12), (cx-10, cy+25, 18), (cx+35, cy+15, 10)]:
            draw.ellipse([gx-gr, gy-gr, gx+gr, gy+gr], fill=(0x20,0x80,0x30))
        # COP31 banner at top
        draw.rectangle([cx-100, y+6, cx+100, y+28], fill=EUROPE_BLUE)
        f_banner = get_font("sans", 12, bold=True)
        draw_text_on_layer(draw, cx, y+17, "COP31 ANTALYA", f_banner, WHITE, anchor="mm")
        # Side banners
        for bx in [x+10, x+w-110]:
            draw.rectangle([bx, y+35, bx+100, y+55], fill=(0x1E,0x3A,0x8A))
            f_side = get_font("sans", 8, bold=True)
            draw_text_on_layer(draw, bx+50, y+45, "UNFCCC", f_side, WHITE, anchor="mm")

    elif type_ == "drones":
        # Night sky over Kyiv
        draw.rectangle([x, y, x+w, y+h], fill=(0x0A,0x12,0x25))
        # Moon
        draw.ellipse([x+w-60, y+10, x+w-15, y+55], fill=(0xE8,0xE8,0xC8))
        # City silhouette - simple
        bw = w // 7
        for i in range(7):
            bx = x + i * bw
            bh = [h-25, h-40, h-30, h-50, h-35, h-28, h-42][i]
            bh = max(15, min(h-15, bh))
            draw.rectangle([bx, y+h-bh, bx+bw-2, y+h], fill=(0x04,0x08,0x12))
            # Windows
            for wy in range(y+h-bh+6, y+h-6, 12):
                for wx in range(bx+3, bx+bw-3, 10):
                    if (wx + wy) % 4 == 0:
                        draw.rectangle([wx, wy, wx+3, wy+5], fill=(0xFF,0xD8,0x70))
        # Drone swarm - REDUCED count, kept away from center caption area
        for i in range(12):
            dx = x + 15 + (i % 4) * (w-30)//3
            dy = y + 15 + (i // 4) * (h-70)//2
            draw.polygon([(dx, dy), (dx-3, dy+6), (dx+3, dy+6)], fill=(0xFF,0x30,0x30))
            draw.line([dx, dy+6, dx, dy+10], fill=(0xFF,0x50,0x50), width=1)
        # LIGHT smoke trails - smaller, not covering skyline or caption
        for i in range(4):
            sx = x + 20 + i * (w-40)//3
            sy = y + h - 30 - (i%2)*8
            draw.ellipse([sx-8, sy-4, sx+8, sy+4], fill=(0x20,0x20,0x30))
        f_k = get_font("sans", 10, bold=True)
        draw_text_on_layer(draw, cx, y+h-8, "KYIV", f_k, (0xFF,0xC0,0xC0), anchor="mm")
        
    elif type_ == "explosion":
        # Bahrain coast - FULL panel filled with burning base/coastline scene
        # Sky - fill with dramatic smoke and fire glow, not empty
        draw.rectangle([x, y, x+w, y+h], fill=(0x15,0x25,0x45))
        # Fire glow in sky - radiating from explosion center
        ex = x + w//2
        ey = y + h//3  # explosion higher up
        for r, color in [(120, (0x30,0x10,0x05)), (90, (0x50,0x15,0x05)), (60, (0x80,0x20,0x05)), (30, (0xB0,0x30,0x10))]:
            draw.ellipse([ex-r, ey-r, ex+r, ey+r], fill=color)
        # Heavy smoke plumes across the sky
        for i in range(12):
            sx = x + 20 + i * (w-40)//11
            sy = y + 15 + (i%3)*15
            sr = 20 + (i%4)*8
            draw.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=(0x10,0x10,0x15))
        # Water - animated waves (moved up, more prominent)
        cy = y + h * 0.55  # water line higher - more coastline visible
        for wx in range(0, w, 20):
            draw.arc([x+wx, cy-10, x+wx+20, cy+10], 0, 180, fill=(0x10,0x30,0x55), width=1)
        draw.line([x, cy, x+w, cy], fill=(0x7B,0x60,0x40), width=2)
        # Tanks/storage facilities along coast - more detail
        tank_x = x + 20
        for tx in [tank_x, tank_x+85, tank_x+170, tank_x+255]:
            draw.rectangle([tx, cy-80, tx+55, cy], fill=(0x40,0x40,0x45), outline=(0x25,0x25,0x25))
            draw.ellipse([tx, cy-90, tx+55, cy-70], fill=(0x50,0x50,0x55), outline=(0x25,0x25,0x25))
            # Tank details
            draw.rectangle([tx+10, cy-85, tx+45, cy-75], fill=(0x60,0x60,0x65))
            # Pipes
            draw.line([tx+27, cy-90, tx+27, cy-110], fill=(0x30,0x30,0x30), width=3)
            draw.line([tx+27, cy-110, tx+27-15, cy-115], fill=(0x30,0x30,0x30), width=2)
        # Main explosion at center tank
        ex = x + w//2
        ey = cy - 80
        # Water reflection of fire
        for i in range(7):
            rx = ex + (i-3)*20
            draw.ellipse([rx-12, cy+5, rx+12, cy+30], fill=(0xFF,0x40,0x10))
        for r, color in [(40, (0xFF,0x20,0x00)), (32, (0xFF,0x60,0x10)), (22, (0xFF,0xA0,0x20)), (12, (0xFF,0xD0,0x60))]:
            draw.ellipse([ex-r, ey-r, ex+r, ey+r], fill=color)
        # Fire column rising
        draw.polygon([(ex-25, ey), (ex-12, y+5), (ex+12, y+5), (ex+25, ey)], fill=(0xFF,0x50,0x10))
        # Smoke plume - rising
        for i in range(10):
            sx = ex + (i%3-1)*12
            sy = ey - 30 - i*12
            sr = 15 + i*4
            draw.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=(0x15,0x15,0x18))
        # Debris/sparks
        for i in range(20):
            dx = ex + (i%5-2)*18
            dy = ey - 10 - (i//5)*15
            draw.ellipse([dx-2, dy-2, dx+2, dy+2], fill=(0xFF,0xA0,0x30))
        # Foreground: shoreline detail
        for sx in range(x, x+w, 8):
            draw.ellipse([sx-2, cy-2, sx+2, cy+2], fill=(0x50,0x40,0x30))
        f_b = get_font("sans", 10, bold=True)
        draw_text_on_layer(draw, cx, y+h-8, "BAHRAIN", f_b, (0xFF,0xC0,0xC0), anchor="mm")

for i, story in enumerate(lead_stories):
    draw_lead_panel(story, [y_lead1, y_lead2, y_lead3][i])

# ═══════════════════════════════════════════════════════════════
# 8. TEN MID CARDS - 2 rows of 5
# ═══════════════════════════════════════════════════════════════
mid_stories = [
    {"num": 4, "place": "GULF OF FINLAND", "tag": "WAR", "tag_color": MIDEAST_RED, "tag_bg": TAG_RED,
     "headline": "Russian cargo ship burns after drone strike",
     "deck": "Finland says Ukraine was likely behind it.", "source": "(BBC)", "illustration": "ship_fire"},
    {"num": 5, "place": "PERU ANDES", "tag": "QUAKE", "tag_color": AMERICAS_GREEN, "tag_bg": TAG_GREEN,
     "headline": "Magnitude 6.8 quake shakes Peru's Andes",
     "deck": "No casualties reported yet.", "source": "(AP, USGS)", "illustration": "quake"},
    {"num": 6, "place": "OMAN", "tag": "TANKERS", "tag_color": MIDEAST_RED, "tag_bg": TAG_RED,
     "headline": "Tankers hit off Oman",
     "deck": "Two tankers struck east of Oman; crews safe.", "source": "(UKMTO)", "illustration": "tanker"},
    {"num": 7, "place": "MYANMAR", "tag": "UN", "tag_color": ASIA_ORANGE, "tag_bg": TAG_ORANGE,
     "headline": "France seeks UN action on Myanmar",
     "deck": "Paris asks Security Council to act.", "source": "(AP)", "illustration": "un"},
    {"num": 8, "place": "GAZA", "tag": "AID", "tag_color": MIDEAST_RED, "tag_bg": TAG_RED,
     "headline": "Strike hits food aid vehicle",
     "deck": "Three Palestinians die in air attack.", "source": "(Al Jazeera, Reuters)", "illustration": "aid"},
    {"num": 9, "place": "SINALOA, MEXICO", "tag": "CARTEL", "tag_color": AMERICAS_GREEN, "tag_bg": TAG_GREEN,
     "headline": "'El Chapo Isidro' caught; violence follows",
     "deck": "FBI top-ten fugitive held after shoot-out.", "source": "(Sky News, BBC)", "illustration": "arrest"},
    {"num": 10, "place": "TEHRAN, IRAN", "tag": "POWER", "tag_color": MIDEAST_RED, "tag_bg": TAG_RED,
     "headline": "Iran to ration electricity",
     "deck": "War damage hits the energy network.", "source": "(Straits Times)", "illustration": "power"},
    {"num": 11, "place": "WASHINGTON", "tag": "TECH", "tag_color": AMERICAS_GREEN, "tag_bg": TAG_GREEN,
     "headline": "Nvidia faces US accounting probe",
     "deck": "SEC inquiry at an early stage.", "source": "(Straits Times)", "illustration": "probe"},
    {"num": 12, "place": "BRASILIA, BRAZIL", "tag": "HEALTH", "tag_color": AMERICAS_GREEN, "tag_bg": TAG_GREEN,
     "headline": "Bolsonaro in intensive care",
     "deck": "Ex-president stable, breathing on his own.", "source": "(Al Jazeera, Reuters)", "illustration": "hospital"},
    {"num": 13, "place": "CANBERRA", "tag": "DEFENCE", "tag_color": ASIA_ORANGE, "tag_bg": TAG_ORANGE,
     "headline": "Marles rejects US report on AUKUS subs",
     "deck": "He says the budget office is wrong.", "source": "(ABC, Reuters)", "illustration": "sub"},
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

    # Text column starts after number circle, full remaining width
    text_x = num_cx + 12
    text_w = x + card_w - 6 - text_x

    f_mplace = get_font("sans", 8, bold=True)
    draw_text(text_x, y+3, story["place"], f_mplace, BLACK)

    # Headline: 9pt for most, 8pt for cards 5 and 13 to fit full text
    if story["num"] in (5, 13):
        f_mhead = get_font("sans", 8, bold=True)
    else:
        f_mhead = get_font("sans", 9, bold=True)
    draw_text_wrapped(text_x, y+16, story["headline"], f_mhead, BLACK, text_w, 11, max_lines=3)

    # Deck: 1 line, complete clause
    f_mdeck = get_font("sans", 8)
    draw_text_wrapped(text_x, y+46, story["deck"], f_mdeck, DARK_GREY, text_w, 11, max_lines=1)

    # Source: shortened to one outlet, italic 7pt
    f_msrc = get_font("sans", 7, italic=True)
    # Shorten source to first outlet only
    src = story["source"]
    if "," in src:
        src = src.split(",")[0] + ")"
    draw_text(text_x, y+58, src, f_msrc, MED_GREY)

def draw_mid_illustration(type_, x, y, w, h):
    cx, cy = x + w//2, y + h//2
    if type_ == "ship_fire":
        D.rectangle([x, cy, x+w, y+h], fill=(0x15,0x30,0x50))
        D.polygon([(x+4, cy+6), (x+w-4, cy+6), (x+w-12, y+h-4), (x+12, y+h-4)], fill=(0x30,0x30,0x30))
        D.rectangle([cx-8, cy-12, cx+8, cy+6], fill=(0x40,0x40,0x40))
        for i in range(4):
            fx = cx + (i-1.5)*4
            fy = cy - 12 - i*1.5
            D.polygon([(fx, fy), (fx-3, fy+6), (fx+3, fy+6)], fill=(0xFF,0x30,0x10))
    elif type_ == "quake":
        D.rectangle([x, y, x+w, y+h], fill=(0xF8,0xF0,0xE8))
        D.line([x, cy, x+w, cy], fill=(0x70,0x50,0x30), width=2)
        points = []
        for i in range(16):
            px = x + i * w // 15
            if i < 4: py = cy
            elif i < 10:
                amp = (i-4) * 2.5
                py = cy - amp if i % 2 == 0 else cy + amp
            else: py = cy
            points.append((px, py))
        if len(points) > 1: D.line(points, fill=RED, width=2)
        f_mag = get_font("sans", 9, bold=True)
        draw_text(cx, y+h-6, "M 6.8", f_mag, RED, anchor="mm")
    elif type_ == "tanker":
        D.rectangle([x, cy, x+w, y+h], fill=(0x15,0x30,0x50))
        D.polygon([(x+4, cy+4), (x+w-4, cy+4), (x+w-8, y+h-4), (x+8, y+h-4)], fill=(0x28,0x28,0x28))
        D.rectangle([cx-15, cy-8, cx+15, cy+4], fill=(0x48,0x48,0x48))
        D.polygon([(x+w-12, cy-12), (x+w-4, cy-7), (x+w-12, cy-2)], fill=RED)
    elif type_ == "un":
        D.rectangle([x, y, x+w, y+h], fill=(0xE8,0xF0,0xF8))
        D.rectangle([cx-2, y+4, cx+2, cy-2], fill=(0x7B,0x5B,0x30))
        D.rectangle([cx-10, y+4, cx+10, y+10], fill=(0x38,0x38,0x38))
        D.rectangle([cx-12, cy, cx+12, cy+10], fill=(0x58,0x38,0x18))
        D.ellipse([cx-12, cy+14, cx+12, cy+38], outline=EUROPE_BLUE, width=1)
        D.line([cx, cy+14, cx, cy+38], fill=EUROPE_BLUE, width=1)
        for lat in (-15, 0, 15):
            ly = cy + 26 + lat * 12 // 15
            D.arc([cx-12, ly-2, cx+12, ly+2], 0, 360, fill=EUROPE_BLUE, width=1)
    elif type_ == "aid":
        D.rectangle([x, y, x+w, y+h], fill=(0xF0,0xE8,0xE8))
        D.rectangle([x+4, cy, x+w-4, y+h-4], fill=(0xD8,0xD8,0xD8))
        D.rectangle([cx-6, cy+4, cx+6, cy+16], fill=(0xD8,0xD8,0xD8))
        D.rectangle([cx-2, cy+4, cx+2, cy+16], fill=RED)
        D.rectangle([cx-6, cy+8, cx+6, cy+12], fill=RED)
        for i in range(2):
            dx = cx - 6 + i*12
            D.line([dx, cy+18, dx+2, cy+22], fill=(0x80,0x20,0x20), width=1)
    elif type_ == "arrest":
        D.rectangle([x, y, x+w, y+h], fill=(0xF0,0xF0,0xF0))
        for cx_off in (-12, 12):
            D.ellipse([cx+cx_off-8, cy-8, cx+cx_off+8, cy+8], outline=(0x28,0x28,0x28), width=2)
        D.ellipse([cx-2, cy-2, cx+2, cy+2], outline=(0x28,0x28,0x28), width=1)
    elif type_ == "power":
        D.rectangle([x, y, x+w, y+h], fill=(0xF8,0xF8,0xE8))
        D.polygon([(cx-15, y+h-4), (cx-8, cy), (cx+8, cy), (cx+15, y+h-4)], outline=(0x50,0x50,0x50), width=1)
        D.line([cx-8, cy, cx+8, cy], fill=(0x50,0x50,0x50), width=1)
        pts = [(cx, cy-4), (cx-4, cy+6), (cx+1, cy+6), (cx-2, cy+16)]
        D.polygon(pts, fill=(0xFF,0xB0,0x10), outline=(0xB0,0x70,0x10))
    elif type_ == "probe":
        D.rectangle([x, y, x+w, y+h], fill=(0xF0,0xF0,0xF8))
        D.rectangle([x+4, cy-8, x+w-4, y+h-4], fill=WHITE, outline=(0xB8,0xB8,0xB8))
        for ly in range(cy-4, y+h-8, 8):
            D.line([x+8, ly, x+w-12, ly], fill=(0xC8,0xC8,0xC8), width=1)
        mgx, mgy = cx+12, cy-12
        D.ellipse([mgx-10, mgy-10, mgx+10, mgy+10], outline=(0x30,0x70,0xB0), width=1)
        D.line([mgx+7, mgy+7, mgx+14, mgy+14], fill=(0x30,0x70,0xB0), width=1)
    elif type_ == "hospital":
        D.rectangle([x, y, x+w, y+h], fill=(0xE8,0xF8,0xE8))
        D.rectangle([cx-15, cy-12, cx+15, y+h-4], fill=(0xD8,0xD8,0xD8), outline=(0xB8,0xB8,0xB8))
        D.rectangle([cx-2, cy-8, cx+2, cy+8], fill=RED)
        D.rectangle([cx-8, cy-2, cx+8, cy+2], fill=RED)
        D.rectangle([x+4, y+h-12, x+20, y+h-4], fill=WHITE, outline=(0xB8,0xB8,0xB8))
        D.rectangle([x+6, y+h-12, x+8, y+h-4], fill=RED)
    elif type_ == "sub":
        D.rectangle([x, cy, x+w, y+h], fill=(0x15,0x30,0x50))
        D.ellipse([x+8, cy+4, x+w-8, cy+28], fill=(0x28,0x28,0x38), outline=(0x48,0x48,0x58))
        D.polygon([(cx-6, cy+4), (cx+6, cy+4), (cx+4, cy-6), (cx-4, cy-6)], fill=(0x28,0x28,0x38))
        D.rectangle([cx-1, cy-10, cx+1, cy-2], fill=(0x38,0x38,0x48))
        f_au = get_font("sans", 6, bold=True)
        draw_text(cx, y+h-4, "AUKUS", f_au, (0x70,0x90,0xB0), anchor="mm")

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
bottom_h = 140
map_w = 400
stories_x = PAD_X + map_w + 12
stories_w = W - PAD_X - stories_x

D.rectangle([PAD_X, bottom_y, PAD_X+map_w, bottom_y+bottom_h], fill=(0xF5,0xF5,0xF0), outline=(0xDD,0xDD,0xDD), width=1)
f_map_title = get_font("sans", 9, bold=True)
draw_text(PAD_X + map_w//2, bottom_y + 10, "WHERE IT HAPPENED - pins match story numbers", f_map_title, BLACK, anchor="mt")

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

story_pins = [
    (1, 36.9, 30.7), (2, 50.4, 30.5), (3, 26.2, 50.6), (4, 60.2, 26.0),
    (5, -12.0, -75.0), (6, 20.0, 58.0), (7, 21.0, 96.0), (8, 31.5, 34.5),
    (9, 25.0, -107.0), (10, 35.7, 51.4), (11, 38.9, -77.0), (12, -15.8, -47.9), (13, -35.3, 149.1),
]

def latlon_to_map(lat, lon):
    nx = lon / 180.0
    ny = -lat / 90.0
    return map_cx + nx * map_rx, map_cy + ny * map_ry

# Compute pin positions with collision avoidance
pin_positions = []
for num, lat, lon in story_pins:
    px, py = latlon_to_map(lat, lon)
    pin_positions.append([num, px, py])

# Simple collision avoidance: nudge overlapping pins
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
            # Nudge apart
            nx, ny = dx/dist, dy/dist
            push = (min_dist - dist) / 2
            pin_positions[i][1] -= nx * push
            pin_positions[i][2] -= ny * push
            pin_positions[j][1] += nx * push
            pin_positions[j][2] += ny * push

f_pin_num = get_font("sans", 7, bold=True)
for num, px, py in pin_positions:
    # Clamp to map bounds
    px = max(PAD_X + pin_radius, min(PAD_X + map_w - pin_radius, px))
    py = max(bottom_y + 20 + pin_radius, min(bottom_y + bottom_h - pin_radius, py))
    D.ellipse([px-pin_radius, py-pin_radius, px+pin_radius, py+pin_radius], fill=RED, outline=WHITE, width=1)
    draw_text(px, py, str(num), f_pin_num, WHITE, anchor="mm")

more_stories = [
    "14 Bayelsa, Nigeria: Boat carrying mourners capsizes (DW, Sky News)",
    "15 Jerusalem: Eisenkot invites Likud to coalition talks (Straits Times)",
    "16 US: FBI looks into apparent hack of its crime database (BBC)",
    "17 US: Teen gamer and his mother help FBI rescue a girl (BBC)",
    "18 US: Midterm loss corners Vance as 2028 field widens (ST)",
    "19 Saudi Arabia: Air defences down a missile (Investing.com)",
    "20 Lebanon: Aoun demands Israel withdrawal (Al Jazeera)",
    "21 Iran: President warns of a 'silent economic war' (Al Jazeera)",
    "22 Hormuz: Lewis Pugh swims strait as tanker is struck (BBC)",
    "23 Moldova: Reports a Russian airspace breach (Kyiv Ind.)",
    "24 Belgium: Air traffic to halt in 23 Nov national strike (ST)",
    "25 Germany: IG Metall widens car and shipyard strikes (Reuters)",
    "26 Portugal: Thousands march in Lisbon on living costs (Reuters)",
    "27 Denmark: Expels Russian attache over rapper plot (Guardian)",
    "28 Bangladesh: 30 Awami League homes set on fire (TOI)",
    "29 Australia: Fred Nile, ex-NSW MP, dies aged 92 (ABC)",
    "30 Australia: Bystanders pull driver from burning car (ABC)",
    "31 Melbourne: 70 years since the 1956 Olympics opened (ABC)",
    "32 Trade: EU and Indonesia sign deal after 10 years (DW)",
    "33 Rugby: France beat Argentina to reach the final (Reuters)",
    "34 Football: Arsenal 2-2 Newcastle; Leeds 4-1 Chelsea (BBC)",
    "35 Football: Liverpool host Manchester United today (Al Jazeera)",
]

f_section = get_font("sans", 9, bold=True)
draw_text(stories_x, bottom_y + 10, "ALSO ON SUNDAY 22 NOVEMBER - 22 MORE STORIES", f_section, BLACK)

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
dc_text = "Wires read up to 00:50 UTC, Sunday 22 November 2026; every story here was reported or still developing on 22 November 2026 in at least one time zone. Left out as other days' news: Russian missiles landing in Poland (19 Nov), the Kerch Bridge strikes (earlier this week) and the Shenzhen summit (19 Nov)."
draw_text_wrapped(PAD_X + 6, dc_y + 16, dc_text, f_dc_text, DARK_GREY, W - 2*PAD_X - 12, 11, max_lines=2)

# ═══════════════════════════════════════════════════════════════
# 11. SOURCES LINE
# ═══════════════════════════════════════════════════════════════
f_src = get_font("sans", 7)
src_text = "Sources: Reuters, BBC, Al Jazeera, DW, The Straits Times, Sky News, CNA, ABC Australia, Times of India, The Guardian, Kyiv Independent. Every story names its outlet. Pictures and map: original, drawn in code."
draw_text(PAD_X, y_sources + 9, src_text, f_src, MED_GREY, anchor="lm")

# ═══════════════════════════════════════════════════════════════
# 12. FOOTER BAR
# ═══════════════════════════════════════════════════════════════
fy = y_footer
D.rectangle([0, fy, W, fy+22], fill=NAVY)
f_footer = get_font("sans", 10, bold=True)
draw_text(PAD_X, fy + 11, "THE WORLD IN ONE DAY", f_footer, WHITE, anchor="lm")
draw_text(W - PAD_X, fy + 11, "SUNDAY 22 NOVEMBER 2026 - ONE PAGE", f_footer, WHITE, anchor="rm")

# ═══════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════
os.makedirs("out", exist_ok=True)
IMG.save("out/entry.png", optimize=True)
print(f"Saved to out/entry.png")
print(f"Size: {os.path.getsize('out/entry.png')} bytes")

import hashlib
with open("out/entry.png", "rb") as f:
    md5 = hashlib.md5(f.read()).hexdigest()
print(f"MD5: {md5}")