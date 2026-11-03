# Grid in Motion: Car Moving on a Road (Python / pygame)

A 2D computer graphics animation in the **Swiss (International Typographic) Style**.
Same design as the original C++/OpenGL plan, ported to **Python + pygame**.
Every transformation is computed with our own 3x3 homogeneous matrices (`src/mat3.py`).
pygame is used only to open the window, fill polygons and draw text.

Course: Computer Graphics and Multimedia, 0613-404 | Instructor: Bipasha Majumder | Dhaka International University
Team: Fardin Kamal, Maheer, Shoaib

## Run

```bash
pip install -r requirements.txt
python src/main.py
```

## Controls

| Key | Action |
|---|---|
| Up | Accelerate |
| Down | Brake |
| G | Toggle 12-column grid overlay |
| D | Debug mode (pivot and axes) |
| N | Day / night |
| B | Blueprint explode / reassemble |
| E | Outro (press again to close) |
| Enter | Skip intro |
| Space | Pause |
| Esc | Quit |

## Structure

```
src/
  mat3.py    3x3 matrix math (T, R, S, pivot rotation)
  gfx.py     matrix stack, primitives, palette, text
  state.py   shared state and constants
  car.py     car, wheels, blueprint parts, debug      (Fardin)
  world.py   road, parallax, signs, camera            (Maheer)
  ui.py      grid, HUD, speedometer, intro/outro      (Shoaib)
  main.py    game loop, input, integration
docs/        screenshots
```

## Where each transformation is used

| Transformation | Where |
|---|---|
| Translation | car position, bounce, scrolling road, parallax, poster slide |
| Rotation | wheel spin, body tilt (pivot at rear axle), needle and ticks |
| Scaling | squash and stretch, parallax depth, camera zoom, approaching signs |
| Reflection | oncoming car, scale x by -1 |
| Combination | `M = C . T . R(pivot) . S`, wheels as children via matrix stack |

Testing without a window: `python src/main.py --shot out.png --frames 200 --hold up --grid --debug`
