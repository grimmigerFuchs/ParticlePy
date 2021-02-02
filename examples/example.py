#!/usr/bin/env python3
# example.py

import pygame
import particlepy
import sys
import time
import random

# pygame config
pygame.init()
SIZE = 800, 800
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("ParticlePy example program")
clock = pygame.time.Clock()
FPS = 60

# delta time
old_time = time.time()
delta_time = 0

particles = particlepy.ParticleSystem()
prefab_shape = particlepy.shape.Rect(radius=16, color=(3, 80, 111), alpha=255)

# main loop
while True:
    # quit window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    # delta time
    now = time.time()
    delta_time = now - old_time
    old_time = now

    mouse_pos = pygame.mouse.get_pos()

    for _ in range(3):
        particles.new(particlepy.Particle(shape=prefab_shape,
                                          position=mouse_pos,
                                          velocity=(random.uniform(-150, 150), random.uniform(-150, 150)),
                                          delta_size=0.23,
                                          is_prefab=True))

    particles.update(delta_time=delta_time)

    # color manipulation
    for particle in particles.particles:
        particle.shape.color = particlepy.math.fade_color(particle=particle,
                                                          color=(83, 150, 181),
                                                          progress=particle.inverted_progress)

    particles.make_shape()

    # post surface creation manipulation
    for particle in particles.particles:
        particle.shape.rotate(angle=4)

    particles.render(surface=screen)

    pygame.display.update()
    screen.fill((13, 17, 23))
    clock.tick(FPS)
