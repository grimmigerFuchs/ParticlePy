#!/usr/bin/env python3
# example_02.py

import pygame
import particlepy
import sys
import time
import random


def palette_swap(surface: pygame.Surface, old_color, new_color):
    surf_copy = surface.copy()
    img_copy = pygame.Surface(surf_copy.get_size())
    img_copy.fill(new_color)
    surf_copy.set_colorkey(old_color)
    img_copy.blit(surf_copy, (0, 0))
    img_copy.set_colorkey((0, 0, 0))
    return img_copy


pygame.init()

# pygame config
SIZE = 800, 800
SCALE_RATIO = 4
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("ParticlePy example program")
pygame.mouse.set_visible(False)

# surfaces
display = pygame.Surface(tuple(item // SCALE_RATIO for item in SIZE))
display.set_colorkey((0, 0, 0))

# timing
clock = pygame.time.Clock()
FPS = 60

# delta time
old_time = time.time()
delta_time = 0

# particle system to manage particles
particle_system = particlepy.particle.ParticleSystem()

# load image
image = pygame.image.load("data/image.png").convert_alpha()

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
    particle_system.update(delta_time=delta_time, gravity=(0, -3))

    # get mouse position
    mouse_pos = tuple(pos // SCALE_RATIO for pos in pygame.mouse.get_pos())

    for _ in range(6):
        particle_system.emit(
            particlepy.particle.Particle(shape=particlepy.shape.Image(surface=image, size=(25, 25), alpha=255),
                                         position=mouse_pos,
                                         velocity=(random.uniform(-80, 80), random.uniform(-80, 80)),
                                         delta_radius=0.5))

    # render shapes
    particle_system.make_shape()

    # render particles
    particle_system.render(surface=display)

    # update display
    screen.blit(pygame.transform.scale(palette_swap(display, (255, 255, 255), (90, 90, 90)), SIZE), (-20, 15))
    screen.blit(pygame.transform.scale(display, SIZE), (0, 0))
    pygame.display.update()

    screen.fill((22, 27, 34))
    display.fill((0, 0, 0))

    clock.tick(60)
