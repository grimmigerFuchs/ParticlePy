#!/usr/bin/env python3

import contextlib
import sys
import time
import random
import particlepy as par

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
particles = par.particle.ParticleSystem(remove_particles_batched=False)  # particle system; argument: no batched removals

# how much particles get spawned at creation
SPAWN_TIMES = 1
GRAVITY = 0.04

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
            particles.create(par.particle.Circle(position=pygame.mouse.get_pos(),                                   # get mouse pos
                                                 velocity=(random.uniform(0, 1) * random.choice((-1, 1)), -4.5),    # x and y velocity
                                                 size=random.randint(6, 14),                                        # size of particles
                                                 delta_size=random.uniform(0.05, 0.1),                              # decreases size every frame
                                                 color=(255, 255, 255),                                             # rgb
                                                 alpha=255,
                                                 antialiasing=True))                                                # aa normally turned off

            """
            # rectangle
            particles.create(par.particle.Rect(position=pygame.mouse.get_pos(),
                                               velocity=(random.uniform(0, 1) * random.choice((-1, 1)), -4.5),
                                               size=random.randint(6, 14),
                                               delta_size=random.uniform(0.035, 0.050),
                                               color=(255, 255, 255),
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
