#!/usr/bin/env python3

import contextlib
import sys
import time
import random
import pyticles

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
particles = []  # particle list
shape = pyticles.Shape()  # instance of possible shapes

spawn_times = 1  # how much particles get spawned at creation

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
        for i in range(spawn_times):
            particles.append(pyticles.Particle(position=pygame.mouse.get_pos(),         # get mouse pos
                                               velocity=(random.uniform(-1, 1), -3),    # choose random x-velocity
                                               gravity=0.009,                           # lets particles fall down
                                               radius=random.randint(2, 25),            # random radius
                                               delta_radius=0.048,                      # value to decrease radius every frame
                                               color=random.randint(210, 255),          # rgb or greyscale
                                               shape=shape.circle))                     # using instanced shape class as guide for shapes

    # draw green point at mouse position
    pygame.draw.circle(screen, (25, 225, 25), pygame.mouse.get_pos(), 5)

    removes = []  # list of particles to remove because of to small radius
    for particle in particles:
        particle.update(delta_time=delta_time)  # update particle positions and radii
        if particle.to_remove(): removes.append(particle)  # check if radius size is invalid -> remove particle if not

    # remove invalid particles
    for i in range(len(removes)):
        particles.remove(removes[i])

    # draw particles
    for particle in particles:
        particle.draw(screen)  # draw particles on given surface

    print(f"Particles : {len(particles)}")  # how much particles on screen

    # refresh window
    pygame.display.update()
    screen.fill((25, 25, 25))
    clock.tick(FPS)
