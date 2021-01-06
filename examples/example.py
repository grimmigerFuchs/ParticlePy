#!/usr/bin/env python3

import contextlib
import sys
import time
import random
import pyticles as pt

with contextlib.redirect_stdout(None):  # mute pygame import message
    import pygame

# pygame config
pygame.init()
SIZE = 800, 800
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Pyticles example program")
pygame.mouse.set_visible(False)  # cursor will be replaced with dot
clock = pygame.time.Clock()
FPS = 60

# delta time
old_time = time.time()

# instances
particles = pt.particle.ParticleSystem(remove_particle_if_not_alive=True)  # particle system; argument: no batched removals

# how much particles get spawned at creation
SPAWN_TIMES = 1
GRAVITY = 0.009

# main loop
while True:
    # quit window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # delta time
    delta_time = time.time() - old_time
    delta_time *= FPS
    old_time = time.time()

    # instantiate particles
    if pygame.mouse.get_pressed(3)[0]:  # instantiate when left mouse button is pressed
        for i in range(SPAWN_TIMES):
            # circle
            particles.create(pt.particle.Circle(position=pygame.mouse.get_pos(),                                # get mouse pos
                                                velocity=(random.uniform(0, 1) * random.choice((-1, 1)), -3),   # x and y velocity
                                                radius=random.randint(2, 25),                                   # size of particles
                                                delta_radius=random.uniform(0.035, 0.050),                      # decreases size every frame
                                                color=random.randint(210, 255),                                 # rgb or greyscale color
                                                alpha=255,                                                      # transparency optional; should not be used with aa
                                                antialiasing=True))                                             # aa normally turned off
            """
            # rectangle
            particles.create(pt.particle.Rect(position=pygame.mouse.get_pos(),
                                              velocity=(random.uniform(0, 1) * random.choice((-1, 1)), -3),
                                              size=random.randint(2, 25),                                       # int or tuple
                                              delta_size=random.uniform(0.035, 0.050),                          # int or tuple
                                              color=random.randint(210, 255),
                                              alpha=255))
            """

    # draw green point at mouse position
    pygame.draw.circle(screen, (25, 225, 25), pygame.mouse.get_pos(), 5)

    # update position and size
    particles.update(delta_time=delta_time, gravity=GRAVITY)  # delta time is optional; gravity pulls particles down

    # draw particles
    particles.draw(surface=screen)  # draw particles on given surface

    print(f"Particles in system : {len(particles.particles)}")  # how much particles in particle system

    # refresh window
    pygame.display.update()
    screen.fill((25, 25, 25))
    clock.tick(FPS)
