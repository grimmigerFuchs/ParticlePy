#!/usr/bin/env python3

from contextlib import redirect_stdout
import particlepy
import sys
import time
import random
with redirect_stdout(None):
    import pygame


# pygame config
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ParticlePy example program 3")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

FPS = 60
old_time = time.time()

particles = particlepy.ParticleSystem(remove_particles_batched=False)
SPAWN_TIMES = 2
GRAVITY = 0

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
                                           delta_size=0.28,
                                           color=(240, 84, 84),
                                           alpha=255,
                                           antialiasing=True,
                                           lighting_color=(2, 1, 0)))

    particles.update(delta_time=delta_time, gravity=GRAVITY)
    for particle in particles.particles:
        particle.fade_color((58, 81, 104))
        particle.fade_alpha(125)
    particles.draw(surface=screen)

    pygame.display.update()
    screen.fill((34, 40, 49))
    clock.tick(FPS)
