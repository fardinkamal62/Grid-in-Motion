#pragma once
#include <cmath>
struct Vec2
{
    float x, y;
};

struct Mat3
{
    float m[3][3];
    Mat3()
    {
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++)
                m[i][j] = (i == j);
    }

    static Mat3 T(float tx, float ty)
    {
        Mat3 r;
        r.m[0][2] = tx;
        r.m[1][2] = ty;
        return r;
    }
    static Mat3 S(float sx, float sy)
    {
        Mat3 r;
        r.m[0][0] = sx;
        r.m[1][1] = sy;
        return r;
    }
    static Mat3 R(float deg)
    {
        float a = deg * 3.14159265f / 180.f, c = cosf(a), s = sinf(a);
        Mat3 r;
        r.m[0][0] = c;
        r.m[0][1] = -s;
        r.m[1][0] = s;
        r.m[1][1] = c;
        return r;
    }
    // COMBINATION: translate to origin -> transform -> translate back
    static Mat3 pivotRotate(float deg, float px, float py) { return T(px, py) * R(deg) * T(-px, -py); }
    static Mat3 pivotScale(float sx, float sy, float px, float py) { return T(px, py) * S(sx, sy) * T(-px, -py); }

    Mat3 operator*(const Mat3 &o) const
    {
        Mat3 r;
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++)
            {
                r.m[i][j] = 0;
                for (int k = 0; k < 3; k++)
                    r.m[i][j] += m[i][k] * o.m[k][j];
            }
        return r;
    }
    Vec2 apply(float x, float y) const
    {
        return {m[0][0] * x + m[0][1] * y + m[0][2], m[1][0] * x + m[1][1] * y + m[1][2]};
    }
};