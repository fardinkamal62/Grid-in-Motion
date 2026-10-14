# Grid in Motion: Car Moving on a Road
**Computer Graphics Project** 

**Team:** Fardin, Maheer, Shoaib

**Language:** C++ (OpenGL / FreeGLUT)

**Style:** Swiss (International Typographic Style)

---

## 1. What We Are Building

A 2D side-view animation of a car driving down an endless road. The camera is
sideways, like a 2D racing game. The car stays at a fixed spot on screen and the
world scrolls past it.

**The twist:** the Swiss grid IS the world. A visible 12-column grid controls the
road dashes, the buildings, the typography and the UI. Nothing is placed randomly.

**What it must prove (the rubric):**

| Transformation | Where we show it |
|---|---|
| Translation | Car movement, suspension bounce, scrolling road, parallax layers |
| Rotation | Wheel spin, body tilt, speedometer needle |
| Scaling | Depth cues, camera zoom, squash/stretch, approaching signs |
| Combination | Pivot rotation, wheels attached to the car body, camera + object together |

**Our differentiator:** a live HUD showing the 3x3 matrix being applied to the car
in real time. It proves we understand the math, not just the function calls.

---

## 2. Design Style: Swiss Rules (everyone follows these)

1. **Palette:** off-white (paper), near-black (ink), ONE accent: Swiss red.
   Nothing else. Grays are allowed only as mixes of ink and paper.
2. **Flat only:** no gradients, shadows, outlines or textures.
3. **Shapes:** rectangles, circles and straight lines only.
4. **One typeface family**, in 2-3 sizes: big numerals for impact, small labels for information.
5. **Grid:** 12 columns, each 100 px wide (screen 1200 x 800). Every object's
   position snaps to a grid unit. When the grid overlay is on, things must visibly line up.
6. **Asymmetry and whitespace:** do not center everything. The car sits at about
   one third of the screen width, text aligns left, and empty space is intentional.
7. **Red is rare:** use it only for things that matter (wheels, needle, key numerals,
   stripe). If everything is red, nothing is.
8. **Day/night mode** just swaps ink and paper. The red stays the same.

---

## 3. Shared Agreements (do these together first, Day 1-2)

Do not skip this. It prevents integration problems later.

- [ ] One Git repo. Each member works on their own branch (`fardin`, `maheer`, `shoaib`) and merges to `main` only when it builds.
- [ ] Everyone confirms they can compile and run an empty window on their own laptop. Agree on one build command and write it in the README.
- [ ] **Coordinate system:** origin at bottom-left, x to the right, y upward, screen 1200 x 800.
- [ ] **Ground line:** agree on the y-value where the road surface is.
- [ ] **Car anchor:** the car's screen x is fixed at one third of the screen width (grid column 4).
- [ ] **Shared state:** agree on the list of values everyone can read (speed, max speed, distance travelled, time, zoom, toggles for grid/debug/night/pause). Only add a new one after telling the group.
- [ ] **Color names:** `ink`, `paper`, `red`, and a gray helper. Nobody hardcodes other colors.
- [ ] **File layout:** one file per area, plus a main file. Decide the names now and stick to them.
- [ ] **Key map:** Up = accelerate, Down = brake, G = grid, D = debug, N = day/night, Space = pause, B = blueprint explode, E = outro, Esc = quit.

**Rule:** every transformation must be built with our own 3x3 matrices. Do not use
OpenGL's built-in translate/rotate/scale for scene geometry. This is what the math
marks are for.

---

## 4. FARDIN: Core Math, Car, Integration

**You own:** the matrix library, the matrix stack, the car, the main loop, and the final merge.

**Why you have more:** everything else depends on your math core, and you are the integrator.

### Step 1: Matrix core (Day 1-2, finish FIRST, others are waiting)
1. Define a 3x3 matrix type with an identity default.
2. Add builders: translation, rotation (degrees), scaling.
3. Add matrix multiplication and "apply to a point."
4. Add pivot rotation and pivot scaling (move pivot to origin, transform, move back).
5. **Test with pencil and paper first:** rotate (1,0) by 90 degrees and check you get (0,1). Then test a pivot case.
6. Share this with Maheer and Shoaib as soon as it works.

### Step 2: Matrix stack and drawing primitives (Day 2-3)
1. Build a stack with push, pop, "apply a transform," and reset.
2. Build primitives (filled rectangle, filled circle, line) where every vertex goes through the current matrix.
3. Build the palette helpers (ink, paper, red, gray).
4. Test: draw a rectangle, push, translate, draw another, pop, draw a third. Confirm the third is unaffected.

### Step 3: The car (Day 3-6)
1. **Body:** low rectangle plus a cabin rectangle on top, a window, and a red stripe. Abstract and Bauhaus-like.
2. **Wheels as children:** each wheel's position is relative to the body. Moving the body moves the wheels for free.
3. **Wheel spin:** each wheel rotates around its own center. The angle comes from the physics: **angle = distance travelled / wheel radius**. Add a spoke or hub dot so the rotation is visible.
4. **Suspension bounce:** a small up-and-down sine movement whose strength grows with speed.
5. **Body tilt (combination):** when accelerating the nose lifts, when braking it dips. Rotate about a pivot at the rear axle.
6. **Squash and stretch:** a slight scale change on acceleration and braking, applied about the car's base.
7. Save the car's final matrix somewhere Shoaib's HUD can read it.

### Step 4: Extra car features (Day 6-7)
1. **Mirrored oncoming car:** a smaller car in the opposite lane drawn by reflecting (scale x by -1) and shrinking. This adds the reflection transformation.
2. **Blueprint explode (B key):** every car part flies out to a grid-aligned layout with rotation, holds, then eases back. Each part has its own matrix.
3. **Brake lights** on braking and **idle vibration** at standstill.

### Step 5: Main loop and physics (Day 3, refine later)
1. Window, 60 fps timer, keyboard handling (including key release for Up/Down).
2. Update speed with acceleration, braking and friction. Clamp to 0..max.
3. Update distance, wheel angle, tilt, stretch and zoom each frame, with smooth easing.
4. Use real elapsed time, not a fixed step, if the animation speed differs between laptops.

### Step 6: Integration (Day 7-8)
1. Merge Maheer's and Shoaib's branches one at a time. Build and test after each merge.
2. Draw order: world (back to front) -> car -> UI.
3. Make sure the camera transform wraps the world and the car, but NOT the UI.
4. Fix state conflicts and test all keys.

### Fardin's deliverables
- Working matrix library with a short written explanation of the math
- Complete car with all transformations
- Stable merged build on `main`
- Notes for the report: matrix order, why pivot rotation works, the wheel angle formula

---

## 5. SHOAIB: The World and Camera

**You own:** the road, parallax scenery, looping, and the camera.

**Needs from Fardin:** the matrix library and primitives (until then, sketch on paper and plan numbers).

### Step 1: Road (Day 3)
1. A black road rectangle across the full width at the agreed ground position.
2. Lane dashes: white rectangles spaced exactly one grid unit apart.
3. Scroll the dashes in the opposite direction to the car by the distance travelled.
4. **Infinite loop:** use the remainder of distance divided by the dash spacing so dashes wrap and never run out. Draw a few extra off-screen so there is no pop-in.
5. Add edge lines and a curb of alternating black and white blocks.

### Step 2: Parallax layers (Day 3-5)
1. Make three layers: **far, mid, near**.
2. Each layer scrolls at a different fraction of the car's distance (far slowest, near fastest).
3. Each layer is scaled to fake depth (far = small, near = large), scaled about a sensible pivot.
4. Buildings are plain rectangles whose positions are on the grid and whose heights vary by a repeatable pseudo-random rule based on their index (same index always gives the same height, so looping looks consistent).
5. Use lighter grays for far layers and darker for near, so depth reads without gradients.
6. Write down your chosen scroll fractions and scale values, and the reason for each.

### Step 3: Typography as scenery (Day 5)
1. Mileposts: big numerals on the mid layer, spaced every N grid units.
2. Near-layer signs and poles whose **scale grows** as they pass the car (the approach effect).
3. Keep all numerals in the shared typeface style and red only where needed.

### Step 4: Camera (Day 5-6)
1. The camera is a scale transform around the screen center, applied to the world and car together.
2. Zoom out when the car is fast, zoom in when it slows or stops.
3. Use smooth easing (ease in/out) so the zoom never snaps. Compare a simple exponential ease against a smoothstep curve and pick the better feel.
4. Check that the car stays at its grid anchor after zooming.

### Step 5: Polish and checks (Day 7)
1. Confirm every color goes through the shared palette so day/night works everywhere.
2. Turn on the grid overlay and verify dashes, buildings and signs all align.
3. Test at speed 0, mid and max for flicker or gaps.
4. **Optional bonus (only if time remains):** a V key for a pseudo-3D rear view where road edges converge to a vanishing point and dashes scale up as they come toward the viewer, with an eased transition.

### Shoaib's deliverables
- Endless looping road with grid-aligned dashes
- Three-layer parallax with documented values
- Smooth camera zoom
- Report section: parallax logic, looping method, camera transform order

---

## 6. MAHEER: Design System, UI, Interaction, Report

**You own:** the look of the whole project, everything drawn on top of the world, the intro/outro, and the written deliverables.

**Needs from Fardin:** the matrix library, primitives and car matrix.

### Step 1: Design system (Day 1-3)
1. Write a one-page style sheet: exact palette values, the typeface, the 2-3 text sizes, the grid dimensions, and which items may be red.
2. Review teammates' work against it during the project (you are the Swiss style checker).
3. Sketch the screen layout on paper over a 12-column grid first: where the title block, speedometer and HUD sit.

### Step 2: Grid overlay and text (Day 3-4)
1. Draw 12 columns and horizontal grid lines, thin and low contrast, toggled with G.
2. Title block, small label text and credit line, all aligned to grid columns.
3. Keep text left-aligned and asymmetric. Avoid centering.

### Step 3: Speedometer (Day 4-5)
1. A circular dial with tick marks, each tick placed by rotating a short line around the dial center.
2. A needle rotated by an angle mapped from current speed (zero speed to start angle, max speed to end angle).
3. Add tick numbers and a large numeral speed readout.
4. Needle is red, dial is ink.

### Step 4: Live matrix HUD (Day 5-6), our differentiator
1. A corner panel that shows the car's current 3x3 matrix, updating every frame.
2. Show the human-readable values underneath: translation, rotation angle, scale x and y.
3. Later, add the camera matrix and wheel matrix.
4. Highlight the entry that changed most, in red.
5. Make sure you can explain every number in it during the viva.

### Step 5: Debug mode (Day 6)
1. D key shows pivots and coordinate axes: body pivot, each wheel center, with labels.
2. This doubles as a demo tool, because it shows the hierarchy visually.

### Step 6: Intro and outro (Day 6-7)
1. Create a simple three-state flow: **Intro -> Play -> Outro**.
2. **Intro:** a poster-style title that starts large, scales down and slides into its grid position with an ease-out, holds about 2 seconds, then the car is released.
3. **Outro:** a closing frame with project name, course and the three names, scaling or translating in. Triggered by E or after a timer.

### Step 7: Report, slides and video (Day 8-10)
1. **Report:** concept, Swiss style rules, math background, the transformation-to-code mapping table (which function, which file), screenshots, and each member's contribution.
2. **Slides:** designed in Swiss style themselves (grid, one accent, big numerals). The deck should look like the project.
3. **Demo video (60-90 s):** show every key and every transformation type, with the HUD visible.
4. Collect the short documentation notes from Fardin and Maheer and merge them into one report.

### Maheer's deliverables
- Style sheet and consistent look across the project
- Grid, speedometer, HUD, debug mode, intro/outro
- Final report, slide deck and demo video

---

## 7. Timeline

| Days | Fardin | Shoaib | Maheer |
|---|---|---|---|
| 1-2 | Shared agreements, matrix core | Shared agreements, plan layers on paper | Shared agreements, style sheet and layout sketch |
| 3-4 | Stack, primitives, main loop, car body and wheels | Road, dashes, looping | Grid overlay, text, speedometer start |
| 5-6 | Wheel spin, tilt, squash, bounce | Parallax, numerals, camera | Speedometer, matrix HUD, debug mode |
| 7-8 | Extras (mirror car, explode), merging | Polish, grid-alignment checks | Intro/outro, start report |
| 9 | Fix bugs, final merge | Fix bugs, optional bonus | Video, slides, finish report |
| 10 | Rehearse | Rehearse | Rehearse |

**Sync rule:** a 10-minute check-in every day (or a chat message). Say what you finished, what is blocking you and what you need from someone else.

---

## 8. Priorities If Time Runs Short

**Cut first:** rear-view mode -> blueprint explode -> mirrored car -> outro.
**Never cut:** matrix HUD, wheel spin, parallax, pivot tilt, intro, grid overlay.

---

## 9. Final Checklist

- [ ] All four transformation types visible and commented in the code
- [ ] Everything follows the Swiss rules (flat, one accent, grid-aligned)
- [ ] Day/night toggle works on every element
- [ ] All keys work and are documented
- [ ] Report, slides and demo video finished
- [ ] Git history shows commits from all three members
- [ ] **Viva prep:** every member can explain: the matrix stack, why pivot rotation is translate-rotate-translate-back, the wheel angle formula, the parallax idea and the HUD numbers. Questions may be asked to anyone about any part.
