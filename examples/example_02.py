#!/usr/bin/env python3
# example.py

import pygame
import particlepy
import sys
import time
import copy
import random

pygame.init()

# pygame config
SIZE = 800, 800
SCALE_RATIO = 4
screen = pygame.display.set_mode(SIZE)
display = pygame.Surface(tuple(item // SCALE_RATIO for item in SIZE))
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

# load image
image = pygame.image.load("data/image.png")

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
    particle_system.update(delta_time=delta_time, gravity=(0, -4))

    # get mouse position
    mouse_pos = tuple(pos // SCALE_RATIO for pos in pygame.mouse.get_pos())

    for _ in range(6):
        particle_system.emit(
            particlepy.particle.Particle(shape=particlepy.shape.Image(surface=image, size=(20, 20), alpha=255),
                                         position=mouse_pos,
                                         velocity=(random.uniform(-100, 100), random.uniform(-100, 100)),
                                         delta_radius=0.5))

    # render shapes
    particle_system.make_shape()

    # render particles
    particle_system.render(surface=display)

    # update display
    screen.blit(pygame.transform.scale(display, SIZE), (0, 0))
    pygame.display.update()
    display.fill((22, 27, 34))
    clock.tick(FPS)
