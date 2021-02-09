# particle.py
# -*- coding: utf-8 -*-

from typing import Tuple, List
import copy
import contextlib

with contextlib.redirect_stdout(None):
    import pygame

import particlepy.shape


class Particle(object):
    """This is the particle class. It simulates the physics of a particle and can be used in a particle system (:class:`ParticleSystem`)

    Args:
        shape (:class:`particlepy.shape.Shape`): Visual particle shape
        position (Tuple[float, float]): Center position
        velocity (Tuple[float, float]): Velocity
        delta_radius (float): Radius decrease value
        data (dict, optional): A dictionary for extra data, defaults to `None`
        alive (bool, optional): `True` if particle should be alive, and `False` if otherwise, defaults to `True`

    Attributes:
        shape (:class:`particlepy.shape.Shape`): Visual particle shape
        position (List[float, float]): Center position
        velocity (List[float, float]): Velocity (can be modified with gravity)
        delta_radius (float): Radius decrease value
        progress (float): A variable ranging from 0 to 1 to represent the lifespan
        inverted_progress (float): A variable ranging from 1 to 0 to represent the lifespan
        time (float): A simple timer
        data (dict): A dictionary for extra data
        alive (bool): `True` if particle is alive, and `False` if otherwise
    """

    def __init__(self, shape: particlepy.shape.Shape, position: Tuple[float, float], velocity: Tuple[float, float],
                 delta_radius: float, data: dict = None, alive: bool = True):
        """Constructor method
        """
        self.shape = copy.copy(shape)

        self.position = list(position)
        self.velocity = list(velocity)

        self.delta_radius = delta_radius

        self.progress, self.inverted_progress = self.shape.get_progress()

        if data:
            self.data = data
        else:
            self.data = {}

        self.time = 0
        self.alive = alive

    def kill(self):
        """Sets attribute :attr:`alive` `False`
        """
        self.alive = False

    def revive(self):
        """Sets attribute :attr:`alive` `True`
        """
        self.alive = True

    def update(self, delta_time: float, gravity: Tuple[float, float] = None):
        """Updates position, velocity, progress, etc. of particle and kills it, if :code:`radius <= 0`

        Args:
            delta_time (float): A value to let the particle move according to frame time
            gravity (Tuple[float, float], optional): Affects the velocity and 'pulls' it in a direction, defaults to None
        """
        self.shape.decrease(self.delta_radius)
        if self.shape.check_size_above_zero():
            if self.alive:
                self.position[0] += self.velocity[0] * delta_time
                self.position[1] += self.velocity[1] * delta_time
                if gravity:
                    self.velocity[0] += gravity[0]
                    self.velocity[1] += gravity[1]

                self.progress, self.inverted_progress = self.shape.get_progress()
                self.time += delta_time
        else:
            self.kill()

    def render(self, surface: pygame.Surface):
        """Renders the particle on given surface

        Args:
            surface (:class:`pygame.Surface`): The surface on which the particle is being rendered on
        """
        if self.alive:
            surface.blit(self.shape.surface, (self.position[0] - self.shape.surface.get_width() / 2,
                                              self.position[1] - self.shape.surface.get_height() / 2))


class ParticleSystem(object):
    """The particle system class. It is used to manage particles in a group

    Args:
        data (dict, optional): A dictionary for extra data, defaults to None
        alive (bool, optional): `True` if particle system should be alive, and `False` if otherwise, defaults to `True`

    Attributes:
        particles (List[:class:`Particle`])
        data (dict): A dictionary for extra data
        alive (bool): `True` if particle system is alive, and `False` if otherwise
    """

    def __init__(self, data: dict = None, alive: bool = True):
        """Constructor method
        """
        self.particles: List[particlepy.particle.Particle] = []
        if data:
            self.data = data
        else:
            self.data = {}
        self.alive = alive

    def emit(self, particle: Particle):
        """Creates a new particle

        Args:
            particle (:class:`Particle`): Particle which is being created

        Raises:
            Exception: Particle system is not alive, not able to add particles
        """
        if self.alive:
            self.particles.append(copy.copy(particle))
        else:
            raise Exception("Particle system is not alive, not able to add particles")

    def clear(self):
        """Clears the particle list
        """
        self.particles.clear()

    def kill(self):
        """Sets :attr:`alive` `False`
        """
        self.alive = False

    def revive(self):
        """Sets :attr:`alive` `True`
        """
        self.alive = True

    def update(self, delta_time: float, gravity: Tuple[float, float] = None):
        """Calls :func:`Particle.update()` for every particle in system

        Args:
            delta_time (float): A value to let the particles move according to frame time
            gravity (Tuple[float, float], optional): Affects the velocity and 'pulls' particles in a direction, defaults to None
        """
        if self.alive:
            for particle in self.particles:
                particle.update(gravity=gravity, delta_time=delta_time)
                if not particle.alive:
                    self.particles.remove(particle)

    def make_shape(self):
        """Makes the surface of all particles in system
        """
        if self.alive:
            for particle in self.particles:
                particle.shape.make_surface()

    def render(self, surface: pygame.Surface):
        """Renders surface of all particles on given surface

        Args:
            surface (:class:`pygame.Surface`): Surface on which the particles are being rendered
        """
        if self.alive:
            for particle in self.particles:
                particle.render(surface=surface)
