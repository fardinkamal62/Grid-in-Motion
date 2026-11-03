"""Shared global state + tuning constants."""

W, H = 1200, 800
COL = 100                 # one grid unit / column width
MAX_SPEED = 900.0         # world px / second
ACCEL = 330.0
BRAKE = 800.0
KMH = 0.2                 # px/s -> km/h for the HUD
WHEEL_R = 30.0
CAR_X, GROUND_Y = 400.0, 680.0


class State:
    def __init__(self):
        self.t = 0.0              # simulation time (stops when paused)
        self.real_t = 0.0         # wall time (never stops)
        self.speed = 350.0
        self.dist = 0.0           # total distance travelled (px)
        self.accel = 0.0
        self.tilt = 0.0
        self.sx = 1.0
        self.sy = 1.0
        self.zoom = 1.0
        self.wheel_angle = 0.0
        self.braking = False
        # toggles
        self.grid = False
        self.debug = False
        self.night = False
        self.paused = False
        self.bp = 0.0             # blueprint progress 0..1
        self.bp_target = 0.0
        # poster overlay (intro / outro)
        self.overlay_mode = "intro"
        self.overlay_y = 0.0
        self.overlay_target = 0.0
        self.intro_done = False
