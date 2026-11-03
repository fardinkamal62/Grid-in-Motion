#pragma once
#include "mat3.h"

struct State
{
    float W = 1200, H = 800;
    float speed = 0, maxSpeed = 600; // px/s
    float dist = 0;                  // total distance travelled
    float wheelDeg = 0;              // wheel rotation
    float tilt = 0, stretch = 1;     // body pitch (deg), squash/stretch
    float zoom = 1;                  // camera scale
    float time = 0;
    bool grid = true, paused = false, debug = false, night = false;
    bool up = false, down = false;
    bool blueprint = false, outro = false;
    Mat3 carMatrix;                  // stored for HUD display
};
inline State S;
