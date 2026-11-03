"""Car, wheels and effects  (Fardin's part).

Local car space: origin = centre of the car on the ground, +x = forward,
y is screen-down, so the car body lives at negative y.
"""
from mat3 import translation as T, rotation as R, scaling as S, rotation_about
from gfx import RED, SMALL
from state import CAR_X, GROUND_Y, WHEEL_R

REAR_AXLE = (-90.0, -30.0)
FRONT_AXLE = (90.0, -30.0)

# blueprint layout: how far each part flies from its assembled place
OFFS = {
    "body": (-250, -290), "stripe": (-250, -360), "cabin": (200, -260),
    "window": (330, -210), "lamp": (300, -150), "tail": (200, -150),
    "wheel_r": (-240, -190), "wheel_f": (-320, -190),
}


def car_matrix(st):
    """M = T(pos) . R_pivot(tilt, rear axle) . S(squash, stretch)"""
    return (T(CAR_X, GROUND_Y + st.bounce)
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
    g.circle(0, 0, WHEEL_R, RED)
    g.circle(0, 0, 20, g.paper)
    g.line(-20, 0, 20, 0, 4, g.ink)
    g.line(0, -20, 0, 20, 4, g.ink)
    g.circle(0, 0, 5, g.ink)
    g.pop()


def _part(g, name, e, x, y, w, h, color, label=None):
    g.push()
    _fly(g, name, e)
    g.rect(x, y, w, h, color)
    if label and e > 0.96:
        g.text(label, x, y - 17, SMALL, g.ink)
    g.pop()


def draw_car(g, wheel_ang, e=0.0, braking=False, debug=False):
    """Draw the car in its local space (caller has already set the matrix)."""
    ink, paper = g.ink, g.paper
    _part(g, "body", e, -150, -100, 300, 60, ink, "01 BODY")
    _part(g, "cabin", e, -80, -160, 140, 60, ink, "02 CABIN")
    _part(g, "window", e, -65, -150, 110, 40, paper, "03 WINDOW")
    _part(g, "stripe", e, -150, -75, 300, 10, RED, "04 STRIPE")
    _part(g, "lamp", e, 140, -90, 10, 10, paper, "05 LAMP")
    _part(g, "tail", e, -150, -90, 8, 10, RED if braking else g.mix(0.5), "06 TAIL")
    _wheel(g, "wheel_r", REAR_AXLE, wheel_ang, e)
    _wheel(g, "wheel_f", FRONT_AXLE, wheel_ang, e)
    if e > 0.96:
        for nm, c, lab in (("wheel_r", REAR_AXLE, "07 WHEEL R"), ("wheel_f", FRONT_AXLE, "08 WHEEL F")):
            g.push(); _fly(g, nm, e)
            g.text(lab, c[0] - 30, c[1] - 52, SMALL, g.ink)
            g.pop()
    if debug:
        g.line(0, 0, 120, 0, 2, ink)
        g.line(0, 0, 0, -120, 2, ink)
        g.text("x", 124, -8, SMALL, ink)
        g.text("y", 6, -134, SMALL, ink)
        g.circle(0, 0, 4, ink)
        g.circle(REAR_AXLE[0], REAR_AXLE[1], 6, RED)       # tilt pivot
        g.text("pivot", REAR_AXLE[0] - 16, REAR_AXLE[1] + 8, SMALL, RED)
        g.circle(FRONT_AXLE[0], FRONT_AXLE[1], 3, RED)
