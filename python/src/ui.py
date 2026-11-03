"""Grid overlay, matrix HUD, speedometer, poster overlay  (Shoaib's part)."""
import math
from mat3 import translation as T, rotation as R
from gfx import RED, SMALL, MEDIUM, BIG
from state import W, H, COL, MAX_SPEED, KMH


def draw_grid(g):
    line = g.mix(0.22)
    for i in range(13):
        g.rect(i * COL - (1 if i == 12 else 0), 0, 1, H, line)
    for i in range(1, 8):
        g.rect(0, i * COL, W, 1, g.mix(0.1))
    for i in range(12):
        g.text("%02d" % (i + 1), i * COL + 6, 4, SMALL, g.mix(0.6))


def draw_hud(g, st, M_total, M_car):
    px, py, pw, ph = 60, 24, 430, 262
    g.rect(px, py, pw, ph, g.paper)
    g.rect(px, py, pw, 3, g.ink)
    ink = g.ink
    g.text("TRANSFORM HUD   M = C . T . R(pivot) . S", px + 20, py + 14, SMALL, ink)
    # matrix with brackets
    mx, my = px + 40, py + 48
    g.rect(mx - 12, my - 4, 2, 76, ink); g.rect(mx - 12, my - 4, 8, 2, ink); g.rect(mx - 12, my + 70, 8, 2, ink)
    g.rect(mx + 300, my - 4, 2, 76, ink); g.rect(mx + 292, my - 4, 8, 2, ink); g.rect(mx + 292, my + 70, 8, 2, ink)
    for r, row in enumerate(M_total.rows()):
        for c, v in enumerate(row):
            g.text("%9.3f" % v, mx + 90 * c + 88, my + 24 * r, SMALL, ink, anchor="r")
    m = M_car.m
    rows = [
        ("POS", "%7.1f %7.1f" % (m[2], m[5])),
        ("ROT", "%7.2f deg" % math.degrees(st.tilt)),
        ("SCALE", "%5.3f %5.3f" % (st.sx, st.sy)),
        ("WHEEL", "%7.1f deg" % (math.degrees(st.wheel_angle) % 360)),
        ("ZOOM", "%5.3f" % st.zoom),
    ]
    for i, (k, v) in enumerate(rows):
        g.text(k, px + 20, py + 132 + i * 18, SMALL, g.mix(0.55))
        g.text(v, px + 100, py + 132 + i * 18, SMALL, ink)
    g.text("UP accel  DOWN brake  G grid  D debug", px + 240, py + 132, SMALL, g.mix(0.55))
    g.text("N night  B blueprint  E outro", px + 240, py + 150, SMALL, g.mix(0.55))
    g.text("SPACE pause  ESC quit", px + 240, py + 168, SMALL, g.mix(0.55))


def _needle_angle(kmh):
    return math.radians(150 + 240 * min(kmh, 180) / 180)


def draw_speedometer(g, st):
    cx, cy, r = 1000, 175, 85
    g.rect(880, 24, 240, 262, g.paper)
    g.rect(880, 24, 240, 3, g.ink)
    g.circle(cx, cy, r, g.ink)
    g.circle(cx, cy, r - 6, g.paper)
    kmh = st.speed * KMH
    for i in range(19):                                   # tick marks, rotated by matrix
        major = i % 3 == 0
        a = math.radians(150 + 240 * i / 18)
        g.push()
        g.translate(cx, cy)
        g.rotate(a)
        g.line(r - 22 if major else r - 16, 0, r - 8, 0, 3 if major else 1.5, g.ink)
        g.pop()
        if major:
            g.text(str(i * 10), cx + math.cos(a) * (r - 38), cy + math.sin(a) * (r - 38),
                   SMALL, g.ink, anchor="c", vmid=True)
    g.push()                                              # needle
    g.translate(cx, cy)
    g.rotate(_needle_angle(kmh))
    g.line(-12, 0, r - 14, 0, 4, RED)
    g.pop()
    g.circle(cx, cy, 7, g.ink)
    g.text("%03d" % round(kmh), cx, 245, MEDIUM, RED, anchor="c", bold=True, vmid=True)
    g.text("KM/H", cx + 50, 253, SMALL, g.ink, vmid=True)


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
        g.text("12", 1100, 330, BIG, RED, anchor="r", bold=True)
        g.text("COLUMNS", 1100, 460, SMALL, ink, anchor="r")
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
