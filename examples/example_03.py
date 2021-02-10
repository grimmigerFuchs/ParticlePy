#!/usr/bin/env python3
# example_03.py

import pygame
import particlepy
import sys
import time
import random

pygame.init()

# pygame config
SIZE = 800, 800
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("ParticlePy example program")
pygame.mouse.set_visible(False)

# timing
clock = pygame.time.Clock()
FPS = 60

# delta time
old_time = time.time()
delta_time = 0

# particle system to manage particles
particle_system = particlepy.particle.ParticleSystem()
max_vel = 150

# main loop
while True:
    # quit window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # delta time
    now = time.time()
    delta_time = now - old_time
    old_time = now

    # update particle properties
    particle_system.update(delta_time=delta_time)
    for particle in particle_system.particles:
        particle.shape.color = particlepy.math.fade_color(particle=particle, color=(58, 81, 104), progress=particle.inverted_progress)
        particle.shape.alpha = particlepy.math.fade_alpha(particle=particle, alpha=125, progress=particle.inverted_progress)

    # get mouse position
    mouse_pos = pygame.mouse.get_pos()

    for _ in range(8):
        particle_system.emit(
            particle=particlepy.particle.Particle(
                shape=particlepy.shape.Circle(
                    radius=9 + random.uniform(0, 1.35),
                    color=(240, 84, 84),
                ),
                position=mouse_pos,
                velocity=(random.uniform(-max_vel, max_vel), random.uniform(-max_vel, max_vel)),
                delta_radius=0.28,
            )
        )

    # render shapes
    particle_system.make_shape()

    # render particles
    particle_system.render(surface=screen)

    # update display
    pygame.display.update()

    screen.fill((34, 40, 49))

    clock.tick(60)
