#pragma once
#include "gfx.h"
#include "state.h"
#include <cmath>

struct Car
{
    // Blueprint explode progress (0 = normal, 1 = fully exploded)
    float explodeFactor = 0.0f;

    void update(float dt)
    {
        if (S.blueprint)
        {
            explodeFactor += (1.0f - explodeFactor) * std::min(1.0f, dt * 4.0f);
        }
        else
        {
            explodeFactor += (0.0f - explodeFactor) * std::min(1.0f, dt * 4.0f);
        }
    }

    void drawMainCar()
    {
        // Base screen position for car (Column 4 -> x = 400, ground y = 210)
        float baseX = 400.0f;
        float baseY = 210.0f;

        // Suspension bounce
        float bounce = sinf(S.time * 18.0f) * (S.speed / (S.maxSpeed > 0 ? S.maxSpeed : 1.0f)) * 3.5f;
        if (S.speed < 5.0f) bounce = sinf(S.time * 3.0f) * 1.0f; // idle vibration

        // Car transformation hierarchy
        gPush();
        // 1. World translation to car anchor + suspension bounce
        gApply(Mat3::T(baseX, baseY + bounce));

        // 2. Body tilt about rear axle pivot (-50, 0)
        gApply(Mat3::pivotRotate(S.tilt, -50.0f, 0.0f));

        // 3. Squash and stretch about base center
        gApply(Mat3::pivotScale(S.stretch, 2.0f - S.stretch, 0.0f, 25.0f));

        // If blueprint mode is active, apply exploded parts transformation
        float exp = explodeFactor;

        // --- CAR BODY ---
        gPush();
        gApply(Mat3::T(0, exp * 40.0f)); // body flies up in blueprint mode
        // Main chassis rectangle (-70 to +70, height 50)
        fillRect(-70.0f, 0.0f, 140.0f, 50.0f, INK());
        // Swiss Red Stripe
        fillRect(-70.0f, 22.0f, 140.0f, 8.0f, RED());
        gPop();

        // --- CABIN ---
        gPush();
        gApply(Mat3::T(0, exp * 90.0f)); // cabin flies higher
        // Cabin rectangle (-30 to +50, y 50 to 90)
        fillRect(-30.0f, 50.0f, 80.0f, 40.0f, INK());
        // Window (-20 to +40, y 55 to 85)
        fillRect(-20.0f, 55.0f, 60.0f, 30.0f, PAPER());
        gPop();

        // --- BRAKE LIGHTS ---
        if (S.down || S.speed < 10.0f)
        {
            gPush();
            gApply(Mat3::T(0, exp * 40.0f));
            fillRect(-72.0f, 12.0f, 4.0f, 14.0f, RED());
            gPop();
        }

        // --- WHEELS (Children of the body) ---
        // Rear Wheel (-50, 0)
        gPush();
        gApply(Mat3::T(-50.0f, -exp * 40.0f)); // wheels drop down in blueprint mode
        gApply(Mat3::R(-S.wheelDeg));          // wheel rotation without slipping
        fillCircle(0.0f, 0.0f, 22.0f, RED());   // Red wheel per Swiss rules
        fillCircle(0.0f, 0.0f, 8.0f, PAPER());   // Hub
        // Spoke 1
        line(0.0f, 0.0f, 0.0f, 22.0f, 3.0f, INK());
        line(0.0f, 0.0f, 22.0f, 0.0f, 3.0f, INK());
        gPop();

        // Front Wheel (50, 0)
        gPush();
        gApply(Mat3::T(50.0f, -exp * 40.0f));
        gApply(Mat3::R(-S.wheelDeg));
        fillCircle(0.0f, 0.0f, 22.0f, RED());
        fillCircle(0.0f, 0.0f, 8.0f, PAPER());
        line(0.0f, 0.0f, 0.0f, 22.0f, 3.0f, INK());
        line(0.0f, 0.0f, -22.0f, 0.0f, 3.0f, INK());
        gPop();

        // Save current car matrix for HUD display
        S.carMatrix = gCur();

        gPop(); // restore root stack
    }

    void drawMirroredOncomingCar()
    {
        // Oncoming car in the distance / opposite lane (reflection transformation: scale X by -1)
        float animOffset = fmodf(S.time * 250.0f, S.W + 400.0f);
        float x = S.W + 200.0f - animOffset;
        float y = 230.0f;

        gPush();
        gApply(Mat3::T(x, y));
        gApply(Mat3::S(-0.5f, 0.5f)); // Reflection (scale x by -1) and shrink for distance

        // Small oncoming car body
        fillRect(-50.0f, 0.0f, 100.0f, 35.0f, INK());
        fillRect(-20.0f, 35.0f, 50.0f, 25.0f, INK());
        // Wheels
        fillCircle(-35.0f, 0.0f, 14.0f, RED());
        fillCircle(35.0f, 0.0f, 14.0f, RED());

        gPop();
    }

    void drawDebugOverlay()
    {
        if (!S.debug) return;

        float baseX = 400.0f;
        float baseY = 210.0f;

        // Draw coordinate axes and pivot crosses at car body and wheels
        line(baseX - 100, baseY, baseX + 150, baseY, 1.5f, RED());
        line(baseX, baseY - 50, baseX, baseY + 150, 1.5f, RED());

        // Rear axle pivot marker
        fillCircle(baseX - 50, baseY, 5.0f, RED());
        drawLabel("Pivot (Rear Axle)", baseX - 90, baseY - 20, INK());

        // Wheel pivots
        fillCircle(baseX - 50, baseY, 3.0f, PAPER());
        fillCircle(baseX + 50, baseY, 3.0f, PAPER());
    }
};
