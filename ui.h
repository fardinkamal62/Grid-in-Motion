#pragma once
#include "gfx.h"
#include "state.h"
#include <cmath>
#include <cstdio>
#include <string>

struct UI
{
    void drawGridOverlay()
    {
        if (!S.grid) return;

        // 12 columns across 1200 px (100 px per column)
        Col gridCol = GREY(0.85f);
        for (int i = 0; i <= 12; i++)
        {
            float x = i * 100.0f;
            line(x, 0.0f, x, S.H, 1.0f, gridCol);
            char colNum[8];
            snprintf(colNum, sizeof(colNum), "%d", i);
            drawLabel(colNum, x + 4.0f, S.H - 20.0f, gridCol);
        }

        // Horizontal grid lines (every 100 px)
        for (float y = 0.0f; y <= S.H; y += 100.0f)
        {
            line(0.0f, y, S.W, y, 0.5f, gridCol);
        }
    }

    void drawSpeedometer()
    {
        float cx = 1050.0f;
        float cy = 680.0f;
        float r = 70.0f;

        // Dial background circle
        fillCircle(cx, cy, r, PAPER());
        // Dial outer ring (ink)
        // Draw tick marks (0 to maxSpeed mapped to angles from -210 deg to 30 deg)
        for (int i = 0; i <= 10; i++)
        {
            float deg = -210.0f + i * 24.0f;
            float rad = deg * 3.14159265f / 180.0f;
            float x1 = cx + (r - 8.0f) * cosf(rad);
            float y1 = cy + (r - 8.0f) * sinf(rad);
            float x2 = cx + r * cosf(rad);
            float y2 = cy + r * sinf(rad);
            line(x1, y1, x2, y2, 2.0f, INK());
        }

        // Rotating needle
        float speedRatio = S.speed / S.maxSpeed;
        float needleDeg = -210.0f + speedRatio * 240.0f;
        float needleRad = needleDeg * 3.14159265f / 180.0f;
        float nx = cx + (r - 12.0f) * cosf(needleRad);
        float ny = cy + (r - 12.0f) * sinf(needleRad);
        line(cx, cy, nx, ny, 3.0f, RED());
        fillCircle(cx, cy, 6.0f, INK());

        // Speedometer labels & speed readout
        drawLabel("SPEED (PX/S)", cx - 45.0f, cy - 30.0f, GREY(0.4f));
        char spdStr[32];
        snprintf(spdStr, sizeof(spdStr), "%.0f", S.speed);
        drawNumeral(spdStr, cx - 35.0f, cy - 70.0f, 36.0f, INK());
    }

    void drawMatrixHUD()
    {
        // Live Matrix HUD panel (top-left, col 1-4)
        float px = 30.0f;
        float py = 760.0f;

        drawLabel("--- LIVE MATRIX HUD (3x3 HOMOGENEOUS) ---", px, py, RED());
        
        char lineBuf[128];
        const Mat3 &M = S.carMatrix;

        snprintf(lineBuf, sizeof(lineBuf), "[ %.2f   %.2f   %.2f ]", M.m[0][0], M.m[0][1], M.m[0][2]);
        drawLabel(lineBuf, px, py - 20.0f, INK());
        snprintf(lineBuf, sizeof(lineBuf), "[ %.2f   %.2f   %.2f ]", M.m[1][0], M.m[1][1], M.m[1][2]);
        drawLabel(lineBuf, px, py - 38.0f, INK());
        snprintf(lineBuf, sizeof(lineBuf), "[ %.2f   %.2f   %.2f ]", M.m[2][0], M.m[2][1], M.m[2][2]);
        drawLabel(lineBuf, px, py - 56.0f, INK());

        // Readable values underneath
        snprintf(lineBuf, sizeof(lineBuf), "Trans X: %.1f | Trans Y: %.1f", M.m[0][2], M.m[1][2]);
        drawLabel(lineBuf, px, py - 80.0f, GREY(0.3f));
        snprintf(lineBuf, sizeof(lineBuf), "Tilt: %.1f deg | Zoom: %.2f | Dist: %.0f", S.tilt, S.zoom, S.dist);
        drawLabel(lineBuf, px, py - 98.0f, GREY(0.3f));

        // Controls reminder
        drawLabel("[^/v] Accel/Brake | [G] Grid | [D] Debug | [N] Day/Night | [B] Blueprint | [E] Outro | [Esc] Quit", 30.0f, 25.0f, GREY(0.4f));
    }

    void drawIntroScreen()
    {
        if (S.time > 2.5f) return; // intro lasts 2.5 seconds

        // Poster-style intro overlay
        fillRect(0.0f, 0.0f, S.W, S.H, PAPER());
        
        // Large Swiss typographic title block
        drawNumeral("GRID IN MOTION", 100.0f, 500.0f, 64.0f, INK());
        drawNumeral("CAR MOVING ON A ROAD - SWISS STYLE", 100.0f, 430.0f, 28.0f, RED());

        drawLabel("Computer Graphics & Multimedia (0613-404)", 100.0f, 350.0f, INK());
        drawLabel("Team: Fardin | Maheer | Shoaib", 100.0f, 320.0f, GREY(0.3f));
        drawLabel("Loading 12-column grid and matrix stack...", 100.0f, 200.0f, RED());
    }

    void drawOutroScreen()
    {
        if (!S.outro) return;

        // Outro poster screen
        fillRect(100.0f, 100.0f, S.W - 200.0f, S.H - 200.0f, PAPER());
        // Border frame
        line(100.0f, 100.0f, S.W - 100.0f, 100.0f, 4.0f, INK());
        line(S.W - 100.0f, 100.0f, S.W - 100.0f, S.H - 100.0f, 4.0f, INK());
        line(S.W - 100.0f, S.H - 100.0f, 100.0f, S.H - 100.0f, 4.0f, INK());
        line(100.0f, S.H - 100.0f, 100.0f, 100.0f, 4.0f, INK());

        drawNumeral("PROJECT COMPLETE", 150.0f, 600.0f, 48.0f, INK());
        drawNumeral("THANK YOU", 150.0f, 520.0f, 36.0f, RED());

        char statBuf[128];
        snprintf(statBuf, sizeof(statBuf), "Total Distance Travelled: %.0f px", S.dist);
        drawLabel(statBuf, 150.0f, 440.0f, INK());
        drawLabel("Press Esc to Exit or E to Resume", 150.0f, 380.0f, GREY(0.3f));
    }
};
