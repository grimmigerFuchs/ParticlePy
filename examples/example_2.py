#!/usr/bin/env python3

import particlepy
import sys
import time
import random
import pygame


# pygame config
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ParticlePy example program 2")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

FPS = 60
old_time = time.time()

# particle system
particles = particlepy.ParticleSystem(remove_particles_batched=False)
SPAWN_TIMES = 2
GRAVITY = 0

# main loop
while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    delta_time = time.time() - old_time
    delta_time *= FPS
    old_time = time.time()

    for _ in range(SPAWN_TIMES):
        particles.create(particlepy.Circle(position=pygame.mouse.get_pos(),
                                           velocity=(random.uniform(0, 2.4) * random.choice((-1, 1)), random.uniform(0, 2.4) * random.choice((-1, 1))),
                                           size=9 + random.uniform(0, 1.35),
                                           delta_size=0.41,
                                           color=(212, 118, 12),
                                           antialiasing=True,
                                           lighting_color=(5, 1, 0)))

    particles.update(delta_time=delta_time, gravity=GRAVITY)
    for particle in particles.particles:
        particle.fade_color((255, 80, 46))
        particle.fade_alpha(200)
    particles.draw(surface=screen)

    pygame.display.update()
    screen.fill((13, 17, 23))
    clock.tick(FPS)
