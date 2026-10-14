#pragma once
#include <GL/glut.h>
#include <vector>
#include <string>
#include "mat3.h"
#include "state.h"

struct Col
{
    float r, g, b;
};
// Swiss palette: ink, paper, one accent. "night" just swaps ink and paper.
inline Col INK() { return S.night ? Col{0.97f, 0.97f, 0.95f} : Col{0.05f, 0.05f, 0.05f}; }
inline Col PAPER() { return S.night ? Col{0.05f, 0.05f, 0.05f} : Col{0.97f, 0.97f, 0.95f}; }
inline Col RED() { return Col{0.88f, 0.10f, 0.10f}; }
inline Col GREY(float t)
{
    Col a = PAPER(), b = INK();
    return {a.r + (b.r - a.r) * t, a.g + (b.g - a.g) * t, a.b + (b.b - a.b) * t};
}

// ---- matrix stack (push/pop hierarchy) ----
inline std::vector<Mat3> g_stack{Mat3()};
inline Mat3 &gCur() { return g_stack.back(); }
inline void gReset() { g_stack.assign(1, Mat3()); }
inline void gPush() { g_stack.push_back(g_stack.back()); }
inline void gPop()
{
    if (g_stack.size() > 1)
        g_stack.pop_back();
}
inline void gApply(const Mat3 &M) { gCur() = gCur() * M; } // post-multiply: child space

// ---- primitives: every vertex goes through OUR matrix ----
inline void gVertex(float x, float y)
{
    Vec2 p = gCur().apply(x, y);
    glVertex2f(p.x, p.y);
}
inline void setCol(Col c) { glColor3f(c.r, c.g, c.b); }

inline void fillRect(float x, float y, float w, float h, Col c)
{
    setCol(c);
    glBegin(GL_QUADS);
    gVertex(x, y);
    gVertex(x + w, y);
    gVertex(x + w, y + h);
    gVertex(x, y + h);
    glEnd();
}
inline void fillCircle(float cx, float cy, float r, Col c, int seg = 48)
{
    setCol(c);
    glBegin(GL_TRIANGLE_FAN);
    gVertex(cx, cy);
    for (int i = 0; i <= seg; i++)
    {
        float a = 6.2831853f * i / seg;
        gVertex(cx + r * cosf(a), cy + r * sinf(a));
    }
    glEnd();
}
inline void line(float x1, float y1, float x2, float y2, float w, Col c)
{
    setCol(c);
    glLineWidth(w);
    glBegin(GL_LINES);
    gVertex(x1, y1);
    gVertex(x2, y2);
    glEnd();
}

// Big stroke-font numerals: position and scale come from our matrix.
inline void drawNumeral(const std::string &s, float x, float y, float height, Col c)
{
    Vec2 p = gCur().apply(x, y);
    float k = height / 119.05f * gCur().m[0][0];
    setCol(c);
    glLineWidth(2);
    glPushMatrix();
    glTranslatef(p.x, p.y, 0);
    glScalef(k, k, 1);
    for (char ch : s)
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ch);
    glPopMatrix();
}
// Small bitmap labels in screen space (for HUD).
inline void drawLabel(const std::string &s, float x, float y, Col c)
{
    setCol(c);
    glRasterPos2f(x, y);
    for (char ch : s)
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ch);
}