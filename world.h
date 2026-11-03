#pragma once
#include "gfx.h"
#include "state.h"
#include <cmath>
#include <string>

struct World
{
    void drawWorld()
    {
        // Camera zoom transformation applied around screen center (600, 400)
        gPush();
        gApply(Mat3::pivotScale(S.zoom, S.zoom, S.W / 2.0f, S.H / 2.0f));

        // --- LAYER 1: FAR PARALLAX (Speed factor 0.2, scale 0.6, y = 320) ---
        {
            gPush();
            float farDist = fmodf(S.dist * 0.2f, 1200.0f);
            gApply(Mat3::T(-farDist, 320.0f));
            gApply(Mat3::S(1.0f, 0.6f));

            // Distant minimalist buildings (Swiss rectangular blocks)
            Col farCol = GREY(0.7f); // lighter gray
            for (int i = -1; i <= 3; i++)
            {
                float bx = i * 400.0f;
                float bw = 120.0f;
                float bh = 220.0f + (i * 37) % 90; // repeatable pseudo-random height
                fillRect(bx, 0.0f, bw, bh, farCol);
            }
            gPop();
        }

        // --- LAYER 2: MID PARALLAX (Speed factor 0.5, scale 0.8, y = 210) ---
        {
            gPush();
            float midDist = fmodf(S.dist * 0.5f, 1200.0f);
            gApply(Mat3::T(-midDist, 210.0f));
            gApply(Mat3::S(1.0f, 0.8f));

            Col midCol = GREY(0.4f);
            for (int i = -1; i <= 3; i++)
            {
                float bx = i * 500.0f + 100.0f;
                float bw = 150.0f;
                float bh = 180.0f + (i * 53) % 110;
                fillRect(bx, 0.0f, bw, bh, midCol);

                // Typographic scenery: Milepost numerals on mid layer buildings
                if (i >= 0 && i < 10)
                {
                    std::string mileStr = "KM " + std::to_string(i + (int)(S.dist / 1200.0f) * 5 + 1);
                    drawNumeral(mileStr, bx + 20.0f, bh + 20.0f, 32.0f, RED());
                }
            }
            gPop();
        }

        // --- MAIN ROAD SURFACE ---
        // Ground road from y = 0 to y = 210 across screen width
        fillRect(0.0f, 0.0f, S.W, 210.0f, INK());

        // Road curbs (alternating black/white blocks)
        float dashOffset = fmodf(S.dist, 80.0f);
        for (float x = -80.0f; x <= S.W + 80.0f; x += 80.0f)
        {
            float curX = x - dashOffset;
            fillRect(curX, 200.0f, 40.0f, 10.0f, PAPER());
            fillRect(curX, 0.0f, 40.0f, 10.0f, PAPER());
        }

        // Lane dashes (infinite looping road dashes spaced 100px apart)
        float laneOffset = fmodf(S.dist, 100.0f);
        for (float x = -100.0f; x <= S.W + 100.0f; x += 100.0f)
        {
            float dashX = x - laneOffset;
            fillRect(dashX, 100.0f, 50.0f, 10.0f, PAPER());
        }

        // --- LAYER 3: NEAR PARALLAX (Speed factor 0.9, scale 1.0, y = 150) ---
        {
            gPush();
            float nearDist = fmodf(S.dist * 0.9f, 1200.0f);
            gApply(Mat3::T(-nearDist, 150.0f));

            // Approaching signs and poles
            for (int i = 0; i <= 4; i++)
            {
                float sx = i * 350.0f + 200.0f;
                // Pole
                fillRect(sx, 0.0f, 8.0f, 90.0f, GREY(0.5f));
                // Sign board
                fillRect(sx - 25.0f, 70.0f, 58.0f, 35.0f, PAPER());
                // Red accent on sign
                fillRect(sx - 25.0f, 95.0f, 58.0f, 10.0f, RED());
            }
            gPop();
        }

        gPop(); // restore camera zoom
    }
};
