#!/usr/bin/env python3
# example.py

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

    # get mouse position
    mouse_pos = pygame.mouse.get_pos()

    for _ in range(5):
        particle_system.emit(
            particlepy.particle.Particle(shape=particlepy.shape.Rect(radius=16,
                                                                     angle=random.randint(0, 360),
                                                                     color=(3, 80, 111),
                                                                     alpha=255),
                                         position=mouse_pos,
                                         velocity=(random.uniform(-150, 150), random.uniform(-150, 150)),
                                         delta_radius=0.2))

    # update particle properties
    particle_system.update(delta_time=delta_time)

    # color manipulation
    for particle in particle_system.particles:
        particle.shape.color = particlepy.math.fade_color(particle=particle,
                                                          color=(83, 150, 181),
                                                          progress=particle.inverted_progress)

    # render shapes
    particle_system.make_shape()

    # post shape creation manipulation
    for particle in particle_system.particles:
        particle.shape.angle += 5

    # render particles
    particle_system.render(surface=screen)

    # update display
    pygame.display.update()
    screen.fill((13, 17, 23))
    clock.tick(FPS)
