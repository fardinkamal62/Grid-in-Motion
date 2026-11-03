"""Grid overlay, HUD, speedometer, poster overlay  (Shoaib's part)."""
import math
from gfx import RED, SMALL, MEDIUM, BIG
from state import W, H, COL, KMH


def draw_grid(g):
    """Alignment grid used while composing the scene."""
    line = g.mix(0.16)
    for i in range(13):
        g.rect(i * COL - (1 if i == 12 else 0), 0, 1, H, line)
    for i in range(1, 8):
        g.rect(0, i * COL, W, 1, g.mix(0.08))


def draw_hud(g, st, M_car):
    px, py, pw, ph = 60, 24, 520, 154
    g.panel(px, py, pw, ph, g.paper, 190)
    g.rect(px, py, pw, 3, g.ink)
    ink = g.ink
    g.text("TRANSFORM HUD", px + 20, py + 14, SMALL, ink)
    g.text("CONTROLS", px + 220, py + 14, SMALL, ink)
    g.rect(px + 200, py + 36, 1, 102, g.mix(0.12))

    m = M_car.m
    rows = [
        ("POS", "%7.1f %7.1f" % (m[2], m[5])),
        ("ROT", "%7.2f deg" % math.degrees(st.tilt)),
        ("SCALE", "%5.3f %5.3f" % (st.sx, st.sy)),
        ("WHEEL", "%7.1f deg" % (math.degrees(st.wheel_angle) % 360)),
        ("ZOOM", "%5.3f" % st.zoom),
    ]
    for i, (k, v) in enumerate(rows):
        y = py + 50 + i * 18
        g.text(k, px + 20, y, SMALL, g.mix(0.55))
        g.text(v, px + 100, y, SMALL, ink)

    left = [("UP", "accelerate"), ("DOWN", "brake"),
            ("SPACE", "pause"), ("ESC", "quit")]
    right = [("G", "grid"), ("D", "debug"), ("N", "night"),
             ("B", "blueprint"), ("E", "outro")]
    for col, items in enumerate((left, right)):
        for row, (key, action) in enumerate(items):
            kx = px + 250 + col * 175
            ax = px + 262 + col * 175
            y = py + 50 + row * 18
            g.text(key, kx, y, SMALL, ink, anchor="r", bold=True)
            g.text(action, ax, y, SMALL, g.mix(0.6))


START, SWEEP = math.radians(135), math.radians(270)


def _needle_angle(kmh):
    return START + SWEEP * min(kmh, 180) / 180


def draw_speedometer(g, st):
    x, y, w, h = 880, 24, 240, 262
    cx, cy, r = x + w / 2, y + 130, 74

    g.panel(x, y, w, h, g.paper, 190)
    g.rect(x, y, w, 3, g.ink)
    g.text("SPEED", x + 20, y + 12, SMALL, g.mix(0.55))
    g.rect(x + 20, y + 31, w - 40, 1, g.mix(0.12))

    # Bezel and dial face.
    g.circle(cx, cy, r + 3, g.ink)
    g.circle(cx, cy, r, g.paper)
    g.circle(cx, cy, r - 1, g.mix(0.04))

    kmh = min(st.speed * KMH, 180)
    for i in range(19):                                   # ticks, rotated by matrix
        major = i % 3 == 0
        a = START + SWEEP * i / 18
        g.push()
        g.translate(cx, cy)
        g.rotate(a)
        if major:
            g.rect(r - 17, -1.6, 12, 3.2, g.ink)
        else:
            g.rect(r - 9, -0.7, 5, 1.4, g.mix(0.55))
        g.pop()
        if major:
            lr = r - 27
            g.text(str(i * 10), cx + math.cos(a) * lr, cy + math.sin(a) * lr,
                   SMALL, g.ink, anchor="c", vmid=True)

    g.push()                                              # tapered needle
    g.translate(cx, cy)
    g.rotate(_needle_angle(kmh))
    g.poly([(-13, -4.5), (r - 20, -2.2), (r - 12, 0),
            (r - 20, 2.2), (-13, 4.5)], RED)
    g.pop()
    g.circle(cx, cy, 9, g.ink)
    g.circle(cx, cy, 6, g.paper)
    g.circle(cx, cy, 3, RED)

    g.text("%03d" % round(kmh), cx - 4, 248, 34, RED, anchor="r", bold=True, vmid=True)
    g.text("KM/H", cx + 3, 256, SMALL, g.ink, vmid=True)


def draw_overlay(g, st):
    """Poster-style intro / outro. Slides in/out with a translation matrix."""
    if st.overlay_y <= -H + 1:
        return
    g.push()
    g.translate(0, st.overlay_y)
    g.rect(0, 0, W, H, g.paper)
    for i in range(13):
        g.rect(i * COL, 0, 1, H, g.mix(0.07))
    ink = g.ink
    if st.overlay_mode == "intro":
        g.text("COMPUTER GRAPHICS AND MULTIMEDIA  /  0613-404", 100, 60, SMALL, ink)
        g.text("GRID IN", 100, 130, BIG, ink, bold=True)
        g.text("MOTION", 100, 250, BIG, ink, bold=True)
        g.rect(100, 400, 200, 12, RED)
        g.text("Car moving on a road", 100, 440, MEDIUM, ink)
        g.text("01", 1100, 330, BIG, RED, anchor="r", bold=True)
        g.text("ENDLESS ROAD", 1100, 460, SMALL, ink, anchor="r")
        g.text("Dhaka International University", 100, 640, SMALL, ink)
        g.text("Instructor  Bipasha Majumder", 100, 662, SMALL, ink)
        g.text("Fardin Kamal  /  Maheer  /  Shoaib", 100, 684, SMALL, ink)
        g.text("PRESS ENTER TO START", 100, 740, SMALL, g.mix(0.55))
    else:
        g.text("COMPUTER GRAPHICS AND MULTIMEDIA  /  0613-404", 100, 60, SMALL, ink)
        g.text("THANK", 100, 130, BIG, ink, bold=True)
        g.text("YOU.", 100, 250, BIG, ink, bold=True)
        g.rect(100, 400, 200, 12, RED)
        g.text("%.1f" % (st.dist / 1200.0), 1100, 330, BIG, RED, anchor="r", bold=True)
        g.text("KM TRAVELLED", 1100, 460, SMALL, ink, anchor="r")
        g.text("CAR + EFFECTS    Fardin Kamal", 100, 620, SMALL, ink)
        g.text("WORLD + CAMERA   Maheer", 100, 642, SMALL, ink)
        g.text("GRID + HUD + UI  Shoaib", 100, 664, SMALL, ink)
        g.text("Instructor  Bipasha Majumder", 100, 706, SMALL, ink)
        g.text("PRESS E TO CLOSE", 100, 740, SMALL, g.mix(0.55))
    g.pop()
