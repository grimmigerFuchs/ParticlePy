# particle.py

from typing import Tuple
from copy import copy
import contextlib

with contextlib.redirect_stdout(None):
    import pygame

import particlepy.shape

# TODO: remove instance copy arg


class Particle(object):
    """This is the particle class. It simulates the physics of a particle.

    :param shape: The shape which is used to represent the particle visually. Is instance of
        :class:`particlepy.shape.BaseShape`
    :type shape: :class:`particlepy.shape.BaseShape`
    :param position: The center position of the particle
    :type position: tuple or list
    :param velocity: The velocity the particle has
    :type velocity: tuple or list
    :param delta_size: The value the radius is decreasing at
    :type delta_size: float
    :param is_prefab: `True` if given shape was a instance, defaults to `False`
    :type is_prefab: bool, optional
    :param particle_dict: A dictionary for extra information which can be used later on, defaults to None
    :type particle_dict: dict, optional
    :param alive: `True` if particle should be alive, and `False` if otherwise., defaults to `True`
    :type alive: bool, optional
    :ivar shape: The shape which is used to represent the particle visually. Is instance of
        :class:`particlepy.shape.BaseShape`
    :type shape: :class:`particlepy.shape.BaseShape`
    :ivar position: The center position of the particle
    :type position: tuple or list
    :param velocity: The velocity the particle has
    :type velocity: tuple or list
    :param delta_size: The value the radius is decreasing at
    :type delta_size: float
    :ivar progress: A variable counting from 0 to 1 to represent the lifespan
    :type progress: float
    :ivar inverted_progress: A variable counting from 1 to 0 to represent the lifespan
    :type inverted_progress: float
    :ivar dict: A dictionary for extra information which can be used later on
    :type dict: dict
    :ivar alive: `True` if particle is alive, and `False` if otherwise.
    :type alive: bool
    """

    def __init__(self, shape: particlepy.shape.BaseShape, position: tuple or list, velocity: tuple or list,
                 delta_size: float, is_prefab: bool = False, particle_dict: dict = None, alive: bool = True):
        """Constructor method
        """
        if is_prefab:
            self.shape = copy(shape)
        else:
            self.shape = shape

        self.position = list(position)
        self.velocity = list(velocity)

        self.delta_size = delta_size
        self.progress, self.inverted_progress = 0, 1
        self.get_progress()

        if particle_dict:
            self.dict = particle_dict
        else:
            self.dict = {}

        self.alive = alive

    def kill(self):
        """Sets :ivar:`alive` `False`
        """
        self.alive = False

    def revive(self):
        """Sets :ivar:`alive` `True`
        """
        self.alive = True

    def get_progress(self) -> Tuple[float, float]:
        """Returns a tuple of two floats: :ivar:`progress` and :ivar:`inverted_progress`

        :return: A tuple of two floats: :ivar:`progress` and :ivar:`inverted_progress`
        :rtype: tuple
        """
        progress = self.shape.radius / self.shape.start_radius
        self.progress, self.inverted_progress = progress, 1 - progress
        return self.progress, self.inverted_progress

    def update(self, gravity: tuple or list = (0, 0), delta_time: float = 1):
        """Updates position and velocity of particle and kills it, if :ivar:`radius` < 0

        :param gravity: Affects the velocity and 'pulls' it in a direction, defaults to (0, 0)
        :type gravity: tuple or list, optional
        :param delta_time: A value to let the particle move according to frame time, defaults to 1
        :type delta_time: float, optional
        """
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
        """Renders the particle on given surface

        :param surface: The surface on which the particle is being rendered on
        :type surface: :class:`pygame.Surface`
        """
        if self.alive:
            surface.blit(self.shape.surface, (self.position[0] - self.shape.surface.get_width() / 2,
                                              self.position[1] - self.shape.surface.get_height() / 2))


class ParticleSystem(object):
    """The particle system class. It is used to manage particles in a group

    :param particle_system_dict: A dictionary for extra information which can be used later on
    :type particle_system_dict: dict
    :param alive: `True` if particle system should be alive, and `False` if otherwise., defaults to `True`
    :type alive: bool, optional
    :ivar particles: A list in which all particles of the particles are stores
    :type particles: list
    :ivar dict: A dictionary for extra information which can be used later on
    :type dict: dict
    :ivar alive: `True` if particle is alive, and `False` if otherwise.
    :type alive: bool
    """
    def __init__(self, particle_system_dict: dict = None, alive: bool = True):
        """Constructor method
        """
        self.particles: list = []
        if particle_system_dict:
            self.dict = particle_system_dict
        else:
            self.dict = {}
        self.alive = alive

    def new(self, particle: Particle):
        """Creates a new particle

        :param particle: Particle which is being created
        :type particle: :class:`particlepy.Particle`
        """
        if self.alive:
            self.particles.append(copy(particle))
        else:
            raise Exception("Particle system is not alive, not able to add particles")

    def clear(self):
        """Clears the particle list
        """
        self.particles.clear()

    def kill(self):
        """Sets :ivar:`alive` `False`
        """
        self.alive = False

    def revive(self):
        """Sets :ivar:`alive` `True`
        """
        self.alive = True

    def update(self, gravity: tuple or list = (0, 0), delta_time: float = 1):
        """Calls `particlepy.Particle.update()` for every particle in system

        :param gravity: Affects the velocity and 'pulls' particles in a direction, defaults to (0, 0)
        :type gravity: tuple or list, optional
        :param delta_time: A value to let the particles move according to frame time, defaults to 1
        :type delta_time: float, optional
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
        """Renders made surface of all particles on given surface

        :param surface: Surface on which the particles are being rendered
        :type surface: :class:`pygame.Surface`
        """
        if self.alive:
            for particle in self.particles:
                particle.render(surface=surface)
