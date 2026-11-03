"""Car, wheels and effects  (Fardin's part).

Local car space: origin = centre of the car on the ground, +x = forward,
y is screen-down, so the car body lives at negative y.
"""
import math

from mat3 import translation as T, rotation as R, scaling as S, rotation_about
from gfx import RED, SMALL
from state import CAR_X, GROUND_Y, WHEEL_R

REAR_AXLE = (-100.0, -30.0)
FRONT_AXLE = (100.0, -30.0)

# Car palette: fixed so the car reads the same in day and night mode.
TIRE = (26, 26, 28)
RIM = (200, 199, 192)
RIM_DARK = (62, 63, 66)
TRIM = (28, 28, 30)
GLASS = (174, 196, 203)
LENS = (250, 246, 226)

# Blueprint layout: how far each part flies from its assembled place.
OFFS = {
    "body": (-270, -280),
    "cabin": (40, -285),
    "window": (300, -285),
    "lamp": (180, -200),
    "tail": (220, -160),
    "wheel_r": (-250, -190),
    "wheel_f": (-340, -190),
}

# Silhouettes are polygons instead of stacked rectangles.
BODY = [
    (-168, -42), (-171, -72), (-164, -94), (-146, -104),
    (-108, -110), (92, -110), (140, -104), (160, -96),
    (170, -80), (172, -56), (168, -42),
]
CABIN = [(-96, -108), (-70, -148), (16, -152), (60, -112), (60, -108)]
WINDOW = [(-88, -112), (-65, -142), (10, -145), (52, -113)]


def car_matrix(st):
    """M = T(pos) . R_pivot(tilt, rear axle) . S(squash, stretch)"""
    return (T(CAR_X, GROUND_Y)
            @ rotation_about(st.tilt, *REAR_AXLE)
            @ S(st.sx, st.sy))


def _fly(g, name, e):
    dx, dy = OFFS[name]
    g.translate(dx * e, dy * e)


def _wheel(g, name, centre, ang, e):
    g.push()
    _fly(g, name, e)
    g.translate(*centre)          # child of the body: parent matrix x local
    g.rotate(ang)                 # spin

    g.circle(0, 0, WHEEL_R, TIRE)
    g.circle(0, 0, 20, RIM)
    g.circle(0, 0, 16, RIM_DARK)
    for i in range(5):            # alloy spokes
        a = 2 * math.pi * i / 5
        g.line(0, 0, 17 * math.cos(a), 17 * math.sin(a), 4, RIM)
    g.circle(0, 0, 6, RED)        # centre cap
    g.circle(0, 0, 2.5, LENS)
    g.pop()


def _part(g, name, e, pts, color, label=None):
    g.push()
    _fly(g, name, e)
    g.poly(pts, color)
    if label and e > 0.96:
        x = min(p[0] for p in pts)
        y = min(p[1] for p in pts)
        g.text(label, x, y - 17, SMALL, g.ink)
    g.pop()


def draw_car(g, wheel_ang, e=0.0, braking=False, debug=False):
    """Draw the car in its local space (caller has already set the matrix)."""
    # Wheels first: the body then covers their top edge, forming a wheel arch.
    _wheel(g, "wheel_r", REAR_AXLE, wheel_ang, e)
    _wheel(g, "wheel_f", FRONT_AXLE, wheel_ang, e)

    # Lower body and details.
    g.push()
    _fly(g, "body", e)
    g.poly(BODY, RED)
    g.rect(-158, -50, 316, 8, TRIM)                  # rocker panel
    g.line(-26, -108, -34, -50, 2, (140, 26, 24))    # door seam
    g.rect(-10, -92, 22, 4, TRIM)                    # door handle
    g.poly([(48, -112), (60, -122), (68, -118), (58, -108)], TRIM)  # mirror
    g.rect(160, -84, 11, 22, TRIM)                   # grille
    if e > 0.96:
        g.text("01 BODY", min(p[0] for p in BODY), min(p[1] for p in BODY) - 17, SMALL, g.ink)
    g.pop()

    # Greenhouse and glass.
    _part(g, "cabin", e, CABIN, TRIM, "02 CABIN")
    _part(g, "window", e, WINDOW, GLASS, "03 WINDOW")
    g.push()                                          # B-pillar
    _fly(g, "window", e)
    g.rect(-20, -145, 6, 34, TRIM)
    g.pop()

    # Lights.
    g.push()
    _fly(g, "lamp", e)
    g.poly([(143, -101), (160, -97), (166, -88), (149, -92)], LENS)
    g.poly([(149, -99), (159, -96), (161, -92), (151, -94)], (255, 252, 240))
    if e > 0.96:
        g.text("04 HEADLIGHT", 142, -115, SMALL, g.ink)
    g.pop()

    g.push()
    _fly(g, "tail", e)
    g.rect(-169, -88, 8, 14, RED if braking else (176, 30, 24))
    if braking:
        g.rect(-174, -86, 5, 10, (255, 120, 90))
    if e > 0.96:
        g.text("05 TAILLIGHT", -170, -111, SMALL, g.ink)
    g.pop()

    # Blueprint labels for the wheels.
    if e > 0.96:
        for nm, c, lab in (("wheel_r", REAR_AXLE, "06 WHEEL R"),
                           ("wheel_f", FRONT_AXLE, "07 WHEEL F")):
            g.push()
            _fly(g, nm, e)
            g.text(lab, c[0] - 30, c[1] - 52, SMALL, g.ink)
            g.pop()

    if debug:
        ink = g.ink
        g.line(0, 0, 120, 0, 2, ink)
        g.line(0, 0, 0, -120, 2, ink)
        g.text("x", 124, -8, SMALL, ink)
        g.text("y", 6, -134, SMALL, ink)
        g.circle(0, 0, 4, ink)
        g.circle(REAR_AXLE[0], REAR_AXLE[1], 6, RED)       # tilt pivot
        g.text("pivot", REAR_AXLE[0] - 16, REAR_AXLE[1] + 8, SMALL, RED)
        g.circle(FRONT_AXLE[0], FRONT_AXLE[1], 3, RED)
