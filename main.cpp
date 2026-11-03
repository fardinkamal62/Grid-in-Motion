#include "gfx.h"
#include "state.h"
#include "car.h"
#include "world.h"
#include "ui.h"
#include <algorithm>

static Car car;
static World world;
static UI ui;

static float clampf(float v, float a, float b) { return std::max(a, std::min(b, v)); }

void update(float dt)
{
    float prev = S.speed;
    if (S.up)
        S.speed += 400 * dt;
    else if (S.down)
        S.speed -= 700 * dt;
    else
        S.speed -= 150 * dt; // friction
    S.speed = clampf(S.speed, 0, S.maxSpeed);

    float accel = (S.speed - prev) / dt;
    float a = clampf(accel / 400.f, -1, 1);
    S.tilt += (-a * 4.f - S.tilt) * std::min(1.f, dt * 8); // pitch on accel/brake
    S.stretch += ((1 + 0.06f * a) - S.stretch) * std::min(1.f, dt * 8);

    S.dist += S.speed * dt;
    S.wheelDeg = (S.dist / 22.f) * 180.f / 3.14159265f; // angle = distance / radius

    float target = 1.0f - 0.25f * (S.speed / S.maxSpeed); // zoom out when fast
    S.zoom += (target - S.zoom) * std::min(1.f, dt * 3);  // exponential ease

    car.update(dt);
}

void display()
{
    Col p = PAPER();
    glClearColor(p.r, p.g, p.b, 1);
    glClear(GL_COLOR_BUFFER_BIT);
    gReset();

    // 1. Draw World (road, parallax layers, camera zoom)
    world.drawWorld();

    // 2. Draw Car (body, cabin, wheels, brake lights, mirror car, debug overlay)
    car.drawMirroredOncomingCar();
    car.drawMainCar();
    car.drawDebugOverlay();

    // 3. Draw UI (grid overlay, speedometer, live HUD, intro/outro screens - NOT affected by camera zoom)
    ui.drawGridOverlay();
    ui.drawSpeedometer();
    ui.drawMatrixHUD();
    ui.drawIntroScreen();
    ui.drawOutroScreen();

    glutSwapBuffers();
}

void timer(int)
{
    if (!S.paused && !S.outro && S.time > 2.5f)
    {
        S.time += 0.016f;
        update(0.016f);
    }
    else if (S.time <= 2.5f)
    {
        S.time += 0.016f; // allow intro time to progress
    }
    glutPostRedisplay();
    glutTimerFunc(16, timer, 0);
}

void specialDown(int k, int, int)
{
    if (k == GLUT_KEY_UP)
        S.up = true;
    if (k == GLUT_KEY_DOWN)
        S.down = true;
}
void specialUp(int k, int, int)
{
    if (k == GLUT_KEY_UP)
        S.up = false;
    if (k == GLUT_KEY_DOWN)
        S.down = false;
}
void keyboard(unsigned char k, int, int)
{
    if (k == 'g' || k == 'G')
        S.grid = !S.grid;
    if (k == 'd' || k == 'D')
        S.debug = !S.debug;
    if (k == 'n' || k == 'N')
        S.night = !S.night;
    if (k == 'b' || k == 'B')
        S.blueprint = !S.blueprint;
    if (k == 'e' || k == 'E')
        S.outro = !S.outro;
    if (k == ' ')
        S.paused = !S.paused;
    if (k == 27)
        exit(0);
}

int main(int argc, char **argv)
{
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize((int)S.W, (int)S.H);
    glutCreateWindow("Car Moving on a Road - Swiss Style");
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0, S.W, 0, S.H, -1, 1);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glEnable(GL_LINE_SMOOTH);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glutDisplayFunc(display);
    glutKeyboardFunc(keyboard);
    glutSpecialFunc(specialDown);
    glutSpecialUpFunc(specialUp);
    glutTimerFunc(16, timer, 0);
    glutMainLoop();
}
