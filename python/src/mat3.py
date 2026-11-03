"""3x3 homogeneous matrices (column-vector convention: [x y 1]^T).

No OpenGL / pygame transform helpers are used anywhere in this project:
every translation, rotation, scale and reflection goes through this file.
"""
import math


class Mat3:
    __slots__ = ("m",)

    def __init__(self, m=(1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0)):
        self.m = tuple(m)

    def __matmul__(self, o):
        a, b = self.m, o.m
        return Mat3((
            a[0]*b[0] + a[1]*b[3] + a[2]*b[6], a[0]*b[1] + a[1]*b[4] + a[2]*b[7], a[0]*b[2] + a[1]*b[5] + a[2]*b[8],
            a[3]*b[0] + a[4]*b[3] + a[5]*b[6], a[3]*b[1] + a[4]*b[4] + a[5]*b[7], a[3]*b[2] + a[4]*b[5] + a[5]*b[8],
            a[6]*b[0] + a[7]*b[3] + a[8]*b[6], a[6]*b[1] + a[7]*b[4] + a[8]*b[7], a[6]*b[2] + a[7]*b[5] + a[8]*b[8],
        ))

    def apply(self, x, y):
        """Transform the point (x, y) -> (x', y')."""
        m = self.m
        return (m[0]*x + m[1]*y + m[2], m[3]*x + m[4]*y + m[5])

    def scale_factor(self):
        """Uniform-equivalent scale (sqrt of |det| of the 2x2 part)."""
        m = self.m
        return math.sqrt(abs(m[0]*m[4] - m[1]*m[3]))

    def rows(self):
        m = self.m
        return [m[0:3], m[3:6], m[6:9]]


def identity():
    return Mat3()


def translation(tx, ty):
    return Mat3((1, 0, tx, 0, 1, ty, 0, 0, 1))


def rotation(theta):
    c, s = math.cos(theta), math.sin(theta)
    return Mat3((c, -s, 0, s, c, 0, 0, 0, 1))


def scaling(sx, sy=None):
    if sy is None:
        sy = sx
    return Mat3((sx, 0, 0, 0, sy, 0, 0, 0, 1))


def rotation_about(theta, px, py):
    """M = T(px,py) . R(theta) . T(-px,-py)"""
    return translation(px, py) @ rotation(theta) @ translation(-px, -py)
