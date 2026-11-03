"""Road, parallax and camera  (Maheer's part)."""
import random
from mat3 import translation as T, scaling as S
from gfx import BIG

ROAD_Y = 600
PERIOD = 24                      # building tile length in grid units

# far / mid / near : scroll factor, depth scale, gray (amount of ink), max height
LAYERS = [
    dict(speed=0.15, scale=0.50, gray=0.07, hmax=6, seed=3, windows=False),
    dict(speed=0.35, scale=0.75, gray=0.14, hmax=5, seed=8, windows=False),
    dict(speed=0.65, scale=1.00, gray=0.24, hmax=4, seed=21, windows=True),
]


def _build(seed, hmax):
    rng, out, x = random.Random(seed), [], 0
    while x < PERIOD:
        w = min(rng.choice([1, 2, 2, 3]), PERIOD - x)
        out.append((x * 100, w * 100, rng.randint(2, hmax) * 100))
        x += w + (rng.choice([0, 0, 1]) if PERIOD - x - w > 1 else 0)
    return out


for _l in LAYERS:
    _l["b"] = _build(_l["seed"], _l["hmax"])


def camera(zoom):
    """C = T(c) . S(zoom) . T(-c): zoom about the car so it stays put."""
    return T(400, 680) @ S(zoom, zoom) @ T(-400, -680)


def _buildings(g, st):
    for L in LAYERS:
        s, tile = L["scale"], PERIOD * 100 * L["scale"]
        off = (st.dist * L["speed"]) % tile
        x0 = -off - tile
        col = g.mix(L["gray"])
        while x0 < 1900:
            for bx, bw, bh in L["b"]:
                sx0 = x0 + bx * s
                if sx0 > 1900 or sx0 + bw * s < -500:
                    continue
                g.push()
                g.translate(x0, ROAD_Y)
                g.scale(s)                       # parallax depth
                g.rect(bx, -bh, bw, bh, col)
                if L["windows"]:
                    cols = max(1, int(bw / 50))
                    cw = bw / cols
                    for r in range(int((bh - 40) / 60)):
                        for c in range(cols):
                            g.rect(bx + c * cw + (cw - 20) / 2, -bh + 30 + r * 60, 20, 28, g.paper)
                g.pop()
            x0 += tile


def _sky_numerals(g, st):
    off = st.dist * 0.08
    k0 = int(off // 1200) - 1
    for k in range(k0, k0 + 4):
        x = k * 1200 - off + 150
        g.text("%02d" % (k % 100), x, 300, BIG, g.mix(0.07), bold=True)


def _road(g, st):
    d = st.dist
    g.rect(-900, ROAD_Y, 3400, 800, g.mix(0.10))
    j0 = int((d - 900) // 100)                           # curb blocks
    for j in range(j0, j0 + 32):
        g.rect(j * 100 - d, ROAD_Y, 100, 20, g.ink if j % 2 == 0 else g.paper)
    j0 = int((d - 900) // 200)                           # lane dashes
    for j in range(j0, j0 + 16):
        g.rect(j * 200 - d, 700, 100, 8, g.ink)


def draw_world(g, st):
    _sky_numerals(g, st)
    _buildings(g, st)
    _road(g, st)
