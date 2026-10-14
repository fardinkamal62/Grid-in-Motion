# Grid in Motion: Car Moving on a Road

A 2D computer graphics animation in **C++ / OpenGL (FreeGLUT)**, designed in the **Swiss (International Typographic) Style**.

A car drives through an endless world built on a visible 12-column grid. The road dashes, buildings, typography and UI all snap to it. Every transformation is computed with our own 3×3 homogeneous matrices, not OpenGL's built-in translate/rotate/scale.

| | |
|---|---|
| **Course** | Computer Graphics and Multimedia, 0613-404 |
| **Instructor** | Bipasha Majumder |
| **University** | Dhaka International University |
| **Team** | Fardin Kamal [fardinkamal62@gmail.com](mailto:fardinkamal62@gmail.com) · Maheer [maheer.mahibi@gmail.com](mailto:maheer.mahibi@gmail.com) · Shoaib [mdsiamulislamsoaib@gmail.com](mailto:mdsiamulislamsoaib@gmail.com) |

---

## Table of Contents
1. [Concept](#concept)
2. [Swiss Style Rules](#swiss-style-rules)
3. [2D Transformations Used](#2d-transformations-used)
4. [Matrix Math](#matrix-math)
5. [Features](#features)
6. [Controls](#controls)
7. [Project Structure](#project-structure)
8. [Build and Run](#build-and-run)
9. [Team Contributions](#team-contributions)
10. [Git Workflow](#git-workflow)
11. [Screenshots and Demo](#screenshots-and-demo)
12. [References](#references)

---

## Concept

The camera is a **side view**, like a 2D racing game. The car stays at a fixed point on the screen (about one third from the left, grid column 4) and the world scrolls past it. The grid is not decoration: it is the structure of the world.

A live **matrix HUD** shows the 3×3 matrix applied to the car in real time, so the math is visible while the animation runs.

## Swiss Style Rules

1. **Palette:** paper (off-white), ink (near-black), and one accent, Swiss red. Grays are only mixes of ink and paper.
2. **Flat only:** no gradients, shadows, outlines or textures.
3. **Primitives only:** rectangles, circles and straight lines.
4. **One typeface family**, 2-3 sizes: big numerals for impact, small labels for information.
5. **Grid:** 12 columns × 100 px on a 1200 × 800 screen. Objects snap to grid units.
6. **Asymmetry and whitespace:** left-aligned text, off-center composition, intentional empty space.
7. **Red is rare:** wheels, speedometer needle, key numerals and the car stripe.
8. **Day/night mode** swaps ink and paper. Red stays the same.

## 2D Transformations Used

| Transformation | Where it appears |
|---|---|
| **Translation** | Car position, suspension bounce, scrolling road dashes, parallax layers |
| **Rotation** | Wheel spin, body tilt on acceleration/braking, speedometer needle and ticks |
| **Scaling** | Squash and stretch, parallax depth, camera zoom, approaching signs |
| **Reflection** | Mirrored oncoming car (scale x by -1) |
| **Combination** | Pivot rotation, wheels as children of the body (matrix stack), camera × object transforms |

## Matrix Math

Points are column vectors `[x y 1]ᵀ`. All transforms are 3×3 homogeneous matrices.

```
Translation T(tx, ty)      Rotation R(θ)              Scaling S(sx, sy)
| 1  0  tx |               | cosθ  -sinθ  0 |         | sx  0   0 |
| 0  1  ty |               | sinθ   cosθ  0 |         | 0   sy  0 |
| 0  0  1  |               |  0      0    1 |         | 0   0   1 |
```

**Rotation about a pivot (px, py):**

```
M = T(px, py) · R(θ) · T(-px, -py)
```

**Wheel rotation angle** (rolling without slipping):

```
angle = distance travelled / wheel radius
```

**Hierarchy:** child transform = parent matrix × local matrix, handled with a push/pop matrix stack. Moving the body automatically moves the wheels.

## Features

**Car**
- Body, cabin, window and stripe built from rectangles
- Wheels as children of the body, spinning with physically correct speed
- Suspension bounce, body tilt (pivot at rear axle), squash and stretch
- Mirrored oncoming car
- Blueprint explode mode (parts fly to a grid layout and reassemble)
- Brake lights and idle vibration

**World**
- Infinite looping road with grid-aligned lane dashes and curbs
- Three parallax layers (far, mid, near) with different speeds and scales
- Milepost numerals and approaching signs as typographic scenery
- Smooth camera zoom (out at high speed, in when slow)

**UI and Design**
- Toggleable 12-column grid overlay
- Speedometer with rotating needle and tick marks
- Live transformation HUD (3×3 matrix and readable values)
- Debug mode showing pivots and coordinate axes
- Poster-style intro and closing outro
- Day/night mode

## Controls

| Key | Action |
|---|---|
| `↑` | Accelerate |
| `↓` | Brake |
| `G` | Toggle grid overlay |
| `D` | Toggle debug mode (pivots and axes) |
| `N` | Toggle day/night |
| `B` | Blueprint explode / reassemble |
| `E` | Show outro |
| `Space` | Pause |
| `Esc` | Quit |

## Project Structure

```
.
├── README.md
├── docs/                  report, style sheet, screenshots
├── src/
│   ├── mat3.h             3×3 matrix math
│   ├── gfx.h              matrix stack, primitives, palette
│   ├── state.h            shared global state
│   ├── car.h              car, wheels, effects        (Fardin)
│   ├── world.h            road, parallax, camera      (Maheer)
│   ├── ui.h               grid, HUD, speedometer      (Shoaib)
│   └── main.cpp           game loop, input, integration
└── .gitignore
```

## Build and Run

**Requirements:** a C++17 compiler, OpenGL, and FreeGLUT.

```bash
# Linux
g++ -std=c++17 main.cpp -o bin/car -lGL -lGLU -lglut

# Windows (MinGW + freeglut)
g++ -std=c++17 main.cpp -o bin\car -lfreeglut -lopengl32 -lglu32

# macOS
g++ -std=c++17 main.cpp -o bin/car -framework OpenGL -framework GLUT
```

Run:

```bash
./bin/car
```
