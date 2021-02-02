# particle.py

from typing import Tuple, List
from copy import copy
import contextlib

with contextlib.redirect_stdout(None):
    import pygame

import particlepy.shape


class Particle(object):
    def __init__(self, shape: particlepy.shape.BaseShape, position: tuple or list, velocity: tuple or list,
                 delta_size: float, is_prefab: bool = False, particle_dict: dict = None, alive: bool = True):
        if particle_dict is None:
            particle_dict = {}
        if is_prefab:
            self.shape = copy(shape)
        else:
            self.shape = shape
        self.progress, self.inverted_progress = 0, 1
        self.get_progress()
        self.delta_size = delta_size

        self.position = list(position)
        self.velocity = list(velocity)

        self.alive = alive

        if particle_dict:
            self.dict = particle_dict
        else:
            self.dict = {}

    def kill(self):
        self.alive = False

    def revive(self):
        self.alive = True

    def get_progress(self) -> Tuple[float, float]:
        progress = self.shape.radius / self.shape.start_radius
        self.progress, self.inverted_progress = progress, 1 - progress
        return self.progress, self.inverted_progress

    def update(self, gravity: tuple or list = (0, 0), delta_time: float = 1):
        self.shape.decrease_size(self.delta_size)
        if self.shape.radius > 0:
            if self.alive:
                self.position[0] += self.velocity[0] * delta_time
                self.position[1] += self.velocity[1] * delta_time
                self.velocity[0] += gravity[0]
                self.velocity[1] += gravity[1]

                self.get_progress()
        else:
            self.kill()

    def render(self, surface: pygame.Surface):
        if self.alive:
            surface.blit(self.shape.surface, (self.position[0] - self.shape.surface.get_width() / 2,
                                              self.position[1] - self.shape.surface.get_height() / 2))


class ParticleSystem(object):
    def __init__(self, alive: bool = True):
        self.particles: List[Particle, ...] = []
        self.alive = alive

        self.dict = {}

    def new(self, particle: Particle):
        if self.alive:
            self.particles.append(particle)
        else:
            raise Exception("Particle system is not alive, not able to add particles")

    def clear(self):
        self.particles.clear()

    def kill(self):
        self.alive = False

    def revive(self):
        self.alive = True

    def update(self, gravity: tuple or list = (0, 0), delta_time: float = 1):
        if self.alive:
            for particle in self.particles:
                particle.update(gravity=gravity, delta_time=delta_time)
                if not particle.alive:
                    self.particles.remove(particle)

    def make_shape(self):
        if self.alive:
            for particle in self.particles:
                particle.shape.make_surface()

    def render(self, surface: pygame.Surface):
        if self.alive:
            for particle in self.particles:
                particle.render(surface=surface)
