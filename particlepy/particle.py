# particle.py

from typing import *
import contextlib

with contextlib.redirect_stdout(None):
    import pygame
    from pygame import gfxdraw

from particlepy.visuals import *


class ParticleSystem:
    """
    This is the particle system class. It is used to create particles in it and manage them in a group.

    :param remove_particles_batched: If True removes particles together after all particles are dead in the system,
                                     defaults to False
    :type remove_particles_batched: bool, optional
    """

    def __init__(self, remove_particles_batched=False):
        """Constructor method
        """
        self.remove_particles_batched = remove_particles_batched
        self.particles = []  # list to instantiate particles into
        self.alive = True

    def create(self, particle):
        """
        Takes a particle class in and creates it in the particle system

        :param particle: Particle to create
        :type particle: particlepy.BaseParticle
        """
        self.particles.append(particle)

    def kill(self):
        """Kills all particles in particle system instantly
        """
        self.particles.clear()
        self.alive = False

    def update(self, delta_time=1, gravity=0):
        """
        Updates position, velocity, size, progress and twisted_progress according to delta_time and gravity in whole particle system at once:
        gravity lets particles fall down and delta_time smooths out the movement

        :param delta_time: Delta time, defaults to 1
        :type delta_time: float, optional
        :param gravity: Gravity for letting particles fall down, defaults to 0
        :type gravity: float, optional
        """
        if len(self.particles) > 0: self.alive = True

        removes = []
        if self.remove_particles_batched: alive = True

        for particle in self.particles:
            particle.update(start_size=particle.start_size, size=particle.size, delta_time=delta_time, gravity=gravity)
            if not self.remove_particles_batched:
                if not particle.alive:
                    removes.append(particle)

        if not self.remove_particles_batched:
            for i in range(len(removes)):
                self.particles.remove(removes[i])
        else:
            self.alive = True
            for particle in self.particles:
                if not particle.alive:
                    self.alive = False
                else:
                    self.alive = True
                    break
            if not self.alive:
                self.particles.clear()
                self.alive = False

    def draw(self, surface):
        """
        Draws the particle of the whole particle system on the given surface with,
        if activated, other particle settings like transparency or antialiasing

        :param surface: Surface to draw particle on
        :type surface: pygame.Surface
        """
        for particle in self.particles:
            particle.draw(surface)


# PARTICLES
class BaseParticle:
    """
    This is the base particle class. It has no size and is only being used to create subclasses.

    :param position: Position (center) to create particle
    :type position: list of float
    :param velocity: The velocity with which particles are being moved by and affected by gravity
    :type velocity: list of float
    :param color: RGB color of particle
    :type color: list of int
    :param alpha: Transparency (0 - 255), defaults to 255
    :type alpha: float, optional
    :param lighting_color: RGB color of lighting, the more black the more transparent,
                           uses lighting color only if not None, defaults to None
    :type lighting_color: list of int
    :ivar position: Position (center) of particle
    :vartype position: list of float
    :ivar velocity: Velocity of particle
    :vartype velocity: list of float
    :ivar progress: A variable from 0 to 1 to measure how much the particle has progressed to its disappearing
    :vartype progress: float
    :ivar inverted_progress: A variable from 1 to 0 to measure how much the particle has progressed to its disappearing, inversion of progress
    :vartype twisted_progress: float
    :ivar alive: Shows if a particle is alive
    :vartype alive: bool
    :ivar color: RGB color of particle
    :vartype color: list of int
    :ivar start_color: RGB color at time point of instantiation
    :vartype start_color: list of int
    :ivar alpha: Transparency (0 to 255)
    :vartype alpha: float
    :ivar start_alpha: Transparency at time point of instantiation
    :vartype start_alpha: float
    :ivar lighting_color:
    :vartype lighting_color:
    """

    def __init__(self, position, velocity, color, alpha=255, lighting_color=None):
        """Constructor method
        """
        if color is None:
            color = [255, 255, 255]
        self.position = list(position)
        self.velocity = list(velocity)
        self.progress = 0
        self.inverted_progress = 1 - self.progress
        self.alive = True
        self.color = list(color)
        self.start_color = self.color
        self.alpha = alpha
        self.start_alpha = self.alpha
        self.lighting_color = lighting_color

    def kill(self):
        """Kills the particle instantly
        """
        self.alive = False

    @staticmethod
    def get_progress(start_size, size) -> float:
        """
        Gets progress of particle, only used in particle classes (staticmethod)

        :param start_size: Start size of particle
        :type start_size: float
        :param size: Size of particle
        :type size: float
        :return: Progress of particle
        :rtype: float
        """
        return size / start_size

    def update(self, start_size, size, delta_time=1, gravity=0):
        """
        Updates position, velocity, progress and inverted_progress according to delta_time and gravity:
        gravity lets particles fall down and delta_time smooths out the movement

        :param start_size: Start size of particle
        :type start_size: float
        :param size: Size of particle
        :type size: float
        :param delta_time: Delta time, defaults to 1
        :type delta_time: float, optional
        :param gravity: Gravity for letting particles fall down, defaults to 0
        :type gravity: float, optional
        """
        # manipulate positions
        self.position[0] += self.velocity[0] * delta_time
        self.position[1] += self.velocity[1] * delta_time
        self.velocity[1] += gravity

        # get progress of particle to death
        self.progress = self.get_progress(start_size, size)
        self.inverted_progress = 1 - self.progress

    def fade_color(self, color):
        """
        Fade the color of a particle over the time frame of its lifespan to a different color

        :param color: Color to fade to
        :type color: list of int
        """
        self.color = [self.start_color[0] + (color[0] - self.start_color[0]) * self.inverted_progress,
                      self.start_color[1] + (color[1] - self.start_color[1]) * self.inverted_progress,
                      self.start_color[2] + (color[2] - self.start_color[2]) * self.inverted_progress]

    def fade_alpha(self, alpha):
        """
        Fade the alpha of a particle over the time frame of its lifespan to a different alpha value

        :param alpha: Alpha value to fade to
        :type alpha: float
        """
        self.alpha = self.start_alpha + (alpha - self.start_alpha) * self.inverted_progress


class Circle(BaseParticle):
    """
    This is the circular particle class. It is a subclass of the
    :class:`particlepy.BaseParticle` class

    :param position: Position (center) to create particle
    :type position: list of float
    :param velocity: The velocity with which particles are being moved by and affected by gravity
    :type velocity: list of float
    :param size: Size / Radius of particle
    :type size: float
    :param delta_size: Value of which the particle size / radius is being shortened at every update
    :type delta_size: float
    :param color: RGB color of particle
    :type color: list of int
    :param alpha: Transparency (0 - 255), defaults to 255
    :type alpha: float, optional
    :param antialiasing: Antialiasing, depending on display size in pygame antialiasing should not be used with transparency,
                         defaults to False
    :type antialiasing: bool, optional
    :param lighting_color: RGB color of lighting, the more black the more transparent,
                           uses lighting color only if not None, defaults to None
    :type lighting_color: list of int
    :ivar position: Position (center) of particle
    :vartype position: list of float
    :ivar velocity: Velocity of particle
    :vartype velocity: list of float
    :ivar progress: A variable from 0 to 1 to measure how much the particle has progressed to its disappearing
    :vartype progress: float
    :ivar inverted_progress: A variable from 1 to 0 to measure how much the particle has progressed to its disappearing, inversion of progress
    :vartype inverted_progress: float
    :ivar alive: Shows if a particle is alive
    :vartype alive: bool
    :ivar color: RGB color of particle
    :vartype color: list of int
    :ivar start_color: RGB color at time point of instantiation
    :vartype start_color: list of int
    :ivar alpha: Transparency (0 to 255)
    :vartype alpha: float
    :ivar start_alpha: Transparency at time point of instantiation
    :vartype start_alpha: float
    :ivar lighting_color:
    :vartype lighting_color:
    """

    def __init__(self, position, velocity, size, delta_size, color, alpha=255, antialiasing=False, lighting_color=None):
        """Constructor method
        """
        super().__init__(position, velocity, color, alpha, lighting_color)

        self.size = size
        self.start_size = self.size
        self.delta_radius = delta_size
        self.antialiasing = antialiasing

    def update(self, start_size, size, delta_time=1, gravity=0):
        """
        Updates position, velocity, size, progress and inverted_progress according to delta_time and gravity:
        gravity lets particles fall down and delta_time smooths out the movement

        :param start_size: Start size of particle
        :type start_size: float
        :param size: Size of particle
        :type size: float
        :param delta_time: Delta time, defaults to 1
        :type delta_time: float, optional
        :param gravity: Gravity for letting particles fall down, defaults to 0
        :type gravity: float, optional
        """
        super().update(start_size, size, delta_time, gravity)

        if self.alive: self.size -= self.delta_radius  # decrease radius
        if self.size <= 0: self.alive = False  # check if alive

    def draw(self, surface):
        """
        Draws the particle on the given surface with, if activated, antialiasing or transparency

        :param surface: Surface to draw particle on
        :type surface: pygame.Surface
        """
        if self.alive:
            if self.antialiasing:
                gfxdraw.aacircle(surface, int(self.position[0]), int(self.position[1]), int(self.size),
                                 (int(self.color[0]), int(self.color[1]), int(self.color[2]), int(self.alpha)))
            gfxdraw.filled_circle(surface, int(self.position[0]), int(self.position[1]), int(self.size),
                                  (int(self.color[0]), int(self.color[1]), int(self.color[2]), int(self.alpha)))
            if self.lighting_color is not None:
                surface.blit(Lighting.circle_lighting_surf(self),
                             (self.position[0] - self.size * 2, self.position[1] - self.size * 2),
                             special_flags=pygame.BLEND_RGB_ADD)


class Rect(BaseParticle):
    """
    This is the rectangular particle class. It is a subclass of the
    :class:`particlepy.BaseParticle` class

    :param position: Position (center) to create particle
    :type position: list of float
    :param velocity: The velocity with which particles are being moved by and affected by gravity
    :type velocity: list of float
    :param size: Size / Radius of particle
    :type size: float
    :param delta_size: Value of which the particle size / radius is being shortened at every update
    :type delta_size: float
    :param color: RGB color of particle
    :type color: list of int
    :param alpha: Transparency (0 - 255), defaults to 255
    :type alpha: float, optional
    :param lighting_color: RGB color of lighting, the more black the more transparent,
                           uses lighting color only if not None, defaults to None
    :type lighting_color: list of int
    :ivar position: Position (center) of particle
    :vartype position: list of float
    :ivar velocity: Velocity of particle
    :vartype velocity: list of float
    :ivar progress: A variable from 0 to 1 to measure how much the particle has progressed to its disappearing
    :vartype progress: float
    :ivar inverted_progress: A variable from 1 to 0 to measure how much the particle has progressed to its disappearing, inversion of progress
    :vartype inverted_progress: float
    :ivar alive: Shows if a particle is alive
    :vartype alive: bool
    :ivar color: RGB color of particle
    :vartype color: list of int
    :ivar start_color: RGB color at time point of instantiation
    :vartype start_color: list of int
    :ivar alpha: Transparency (0 to 255)
    :vartype alpha: float
    :ivar start_alpha: Transparency at time point of instantiation
    :vartype start_alpha: float
    :ivar lighting_color:
    :vartype lighting_color:
    """

    def __init__(self, position, velocity, size, delta_size, color, alpha=255, lighting_color=None):
        """Constructor method
        """
        super().__init__(position, velocity, color, alpha, lighting_color)

        # size
        if isinstance(size, float) or isinstance(size, int):
            self.size = size
        self.start_size = self.size
        self.delta_size = delta_size

    def update(self, start_size, size, delta_time=1, gravity=0):
        """
        Updates position, velocity, size, progress and inverted_progress according to delta_time and gravity:
        gravity lets particles fall down and delta_time smooths out the movement

        :param start_size: Start size of particle
        :type start_size: float
        :param size: Size of particle
        :type size: float
        :param delta_time: Delta time, defaults to 1
        :type delta_time: float, optional
        :param gravity: Gravity for letting particles fall down, defaults to 0
        :type gravity: float, optional
        """
        super().update(start_size, size, delta_time, gravity)

        # decrease size
        if self.alive: self.size -= self.delta_size

        # check if alive
        if self.size <= 0: self.alive = False

        # TODO: Add rectangle rotation

    def draw(self, surface):
        """
        Draws the particle on the given surface with, if activated, transparency

        :param surface: Surface to draw particle on
        :type surface: pygame.Surface
        """
        if self.alive:
            gfxdraw.box(surface,
                        (int(self.position[0]) - int(self.size / 2), int(self.position[1]) - int(self.size / 2),
                         int(self.size), int(self.size)),
                        (int(self.color[0]), int(self.color[1]), int(self.color[2]), int(self.alpha)))
            if self.lighting_color is not None:
                surface.blit(Lighting.rect_lighting_surf(self),
                             (self.position[0] - self.size * 2, self.position[1] - self.size * 2),
                             special_flags=pygame.BLEND_RGB_ADD)
