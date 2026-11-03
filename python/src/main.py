"""Grid in Motion - Car Moving on a Road   (Python / pygame port)

Game loop, input and integration. All geometry goes through mat3.py.
Run:  python src/main.py
"""
import argparse
import math
import os
import random
import sys

import pygame

from mat3 import identity, translation as T, scaling as S
from gfx import Gfx
from state import State, W, H, MAX_SPEED, ACCEL, BRAKE, WHEEL_R
import car
import world
import ui


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def smooth(t):
    return t * t * (3 - 2 * t)


def update(st, dt, keys):
    st.real_t += dt
    # poster overlay (uses real time, keeps animating while paused)
    if st.overlay_mode == "intro" and not st.intro_done and st.real_t > 4.0:
        st.intro_done, st.overlay_target = True, -H - 20
    st.overlay_y += (st.overlay_target - st.overlay_y) * min(1.0, dt * 4)

    if st.paused:
        return
    st.t += dt
    prev = st.speed
    up, down = keys[pygame.K_UP], keys[pygame.K_DOWN]
    if up:
        st.speed += ACCEL * dt
    elif down:
        st.speed -= BRAKE * dt
    else:
        st.speed -= (st.speed * 0.25 + 15) * dt          # coasting drag
    st.speed = clamp(st.speed, 0.0, MAX_SPEED)
    st.braking = bool(down and prev > 1)

    a = (st.speed - prev) / dt if dt > 0 else 0.0
    st.accel += (a - st.accel) * min(1.0, dt * 10)
    k = clamp(st.accel / 600.0, -1.0, 1.0)
    st.tilt += (-k * 0.07 - st.tilt) * min(1.0, dt * 8)  # nose up when accelerating
    st.sx += (1 + 0.05 * k - st.sx) * min(1.0, dt * 10)  # squash and stretch
    st.sy += (1 - 0.05 * k - st.sy) * min(1.0, dt * 10)

    st.dist += st.speed * dt
    st.wheel_angle = (st.dist / WHEEL_R) % (2 * math.pi)  # rolling: angle = distance / radius

    st.bounce = math.sin(st.dist * 0.045) * min(3.0, st.speed / 150.0)   # suspension
    if st.speed < 30:
        st.bounce += math.sin(st.t * 70) * 0.8                          # idle vibration

    st.bp += (st.bp_target - st.bp) * min(1.0, dt * 2.5)
    if abs(st.bp - st.bp_target) < 0.002:
        st.bp = st.bp_target
    base = 1.1 - 0.25 * st.speed / MAX_SPEED
    target_zoom = base + (0.8 - base) * smooth(st.bp)
    st.zoom += (target_zoom - st.zoom) * min(1.0, dt * 3)

    OC_SPEED = 320.0                                      # oncoming car
    st.oc_x -= (st.speed + OC_SPEED) * dt
    st.oc_dist += OC_SPEED * dt
    if st.oc_x < -500:
        st.oc_x = 1700 + random.random() * 1800


def render(g, st):
    g.night = st.night
    g.s.fill(g.paper)
    cam = world.camera(st.zoom)
    M_car = car.car_matrix(st)
    e = smooth(st.bp)

    g.load(cam)                                           # camera x object
    world.draw_world(g, st)

    g.push()                                              # oncoming car = reflection
    g.translate(st.oc_x, 776)
    g.scale(-0.6, 0.6)                                    # scale x by -1 mirrors it
    car.draw_car(g, st.oc_dist / WHEEL_R)
    g.pop()

    g.push()
    g.mul(M_car)
    car.draw_car(g, st.wheel_angle, e, st.braking, st.debug)
    g.pop()

    g.load(identity())                                    # screen-space UI
    if st.grid:
        ui.draw_grid(g)
    ui.draw_hud(g, st, cam @ M_car, M_car)
    ui.draw_speedometer(g, st)
    ui.draw_overlay(g, st)


def on_key(st, key):
    if key == pygame.K_g:
        st.grid = not st.grid
    elif key == pygame.K_d:
        st.debug = not st.debug
    elif key == pygame.K_n:
        st.night = not st.night
    elif key == pygame.K_b:
        st.bp_target = 0.0 if st.bp_target else 1.0
    elif key == pygame.K_SPACE:
        st.paused = not st.paused
    elif key in (pygame.K_RETURN, pygame.K_KP_ENTER):
        if st.overlay_mode == "intro":
            st.intro_done, st.overlay_target = True, -H - 20
    elif key == pygame.K_e:
        if st.overlay_target == 0 and st.overlay_mode == "outro":
            st.overlay_target = -H - 20
        else:
            st.overlay_mode, st.overlay_target, st.intro_done = "outro", 0.0, True


def main():
    ap = argparse.ArgumentParser(description="Grid in Motion")
    ap.add_argument("--shot", help="render N frames, save PNG, exit (testing)")
    ap.add_argument("--frames", type=int, default=120)
    ap.add_argument("--hold", choices=["up", "down", "none"], default="none")
    for f in ("grid", "debug", "night", "blueprint", "outro", "skip-intro"):
        ap.add_argument("--" + f, action="store_true")
    args = ap.parse_args()

    if args.shot:
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    pygame.display.set_caption("Grid in Motion - Car Moving on a Road")
    try:
        screen = pygame.display.set_mode((W, H), pygame.SCALED | pygame.RESIZABLE)
    except pygame.error:
        screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    g, st = Gfx(screen), State()

    st.grid, st.debug, st.night = args.grid, args.debug, args.night
    if args.blueprint:
        st.bp = st.bp_target = 1.0
    if args.skip_intro or args.shot:
        st.intro_done, st.overlay_target, st.overlay_y = True, -H - 20, -H - 20
    if args.outro:
        st.overlay_mode, st.overlay_target, st.overlay_y = "outro", 0.0, 0.0

    if args.shot:
        class K(dict):
            def __missing__(self, k): return False
        keys = K()
        if args.hold == "up": keys[pygame.K_UP] = True
        if args.hold == "down": keys[pygame.K_DOWN] = True
        for _ in range(args.frames):
            update(st, 1 / 60, keys)
        render(g, st)
        pygame.image.save(screen, args.shot)
        return

    running = True
    while running:
        dt = min(clock.tick(60) / 1000.0, 0.05)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                running = False
            elif ev.type == pygame.KEYDOWN:
                on_key(st, ev.key)
        update(st, dt, pygame.key.get_pressed())
        render(g, st)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
