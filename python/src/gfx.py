"""Matrix stack, primitives (rect / circle / line / text) and the palette.

Primitives are transformed by OUR matrix stack and then rasterised with
pygame.draw.polygon. pygame never sees a rotation or scale.
"""
import math
import pygame
from mat3 import Mat3, translation, rotation, scaling

RED = (218, 41, 28)               # Swiss red - never changes
INK_DAY, PAPER_DAY = (17, 17, 17), (240, 238, 232)

SMALL, MEDIUM, BIG = 14, 28, 120  # the only three type sizes
_FONT_NAMES = "helveticaneue,helvetica,arial,liberationsans,nimbussans,dejavusans"


class Gfx:
    def __init__(self, surface):
        self.s = surface
        self.stack = [Mat3()]
        self.night = False
        self._fonts = {}
        self._texts = {}

    # ---- palette -------------------------------------------------
    @property
    def ink(self):
        return PAPER_DAY if self.night else INK_DAY

    @property
    def paper(self):
        return INK_DAY if self.night else PAPER_DAY

    def mix(self, t):
        """Gray = t of ink + (1-t) of paper. The only way to get grays."""
        a, b = self.ink, self.paper
        return tuple(int(a[i]*t + b[i]*(1-t)) for i in range(3))

    # ---- matrix stack --------------------------------------------
    @property
    def top(self):
        return self.stack[-1]

    def load(self, m):
        self.stack = [m]

    def push(self):
        self.stack.append(self.stack[-1])

    def pop(self):
        self.stack.pop()

    def mul(self, m):
        self.stack[-1] = self.stack[-1] @ m

    def translate(self, x, y):
        self.mul(translation(x, y))

    def rotate(self, th):
        self.mul(rotation(th))

    def scale(self, sx, sy=None):
        self.mul(scaling(sx, sy))

    # ---- primitives ----------------------------------------------
    def _poly(self, pts, color):
        t = self.top
        pygame.draw.polygon(self.s, color, [t.apply(x, y) for x, y in pts])

    def rect(self, x, y, w, h, color):
        self._poly(((x, y), (x + w, y), (x + w, y + h), (x, y + h)), color)

    def circle(self, cx, cy, r, color):
        n = 36 if r * self.top.scale_factor() > 12 else 18
        self._poly([(cx + r*math.cos(2*math.pi*i/n), cy + r*math.sin(2*math.pi*i/n))
                    for i in range(n)], color)

    def line(self, x1, y1, x2, y2, width, color):
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / d * width / 2, dx / d * width / 2
        self._poly(((x1+nx, y1+ny), (x2+nx, y2+ny), (x2-nx, y2-ny), (x1-nx, y1-ny)), color)

    def _font(self, size, bold):
        k = (size, bold)
        if k not in self._fonts:
            self._fonts[k] = pygame.font.SysFont(_FONT_NAMES, size, bold=bold)
        return self._fonts[k]

    def text(self, s, x, y, size, color, anchor="l", bold=False, vmid=False):
        """Text is positioned and sized by the matrix, but never rotated."""
        px, py = self.top.apply(x, y)
        sz = int(round(size * self.top.scale_factor()))
        if sz < 5:
            return
        sz = min(sz, 400)
        key = (s, sz, bold, color)
        surf = self._texts.get(key)
        if surf is None:
            if len(self._texts) > 400:
                self._texts.clear()
            surf = self._font(sz, bold).render(s, True, color)
            self._texts[key] = surf
        w, h = surf.get_size()
        if anchor == "r":
            px -= w
        elif anchor == "c":
            px -= w / 2
        if vmid:
            py -= h / 2
        self.s.blit(surf, (px, py))
