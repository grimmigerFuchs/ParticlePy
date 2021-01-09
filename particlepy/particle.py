# particle.py

from contextlib import redirect_stdout
import particlepy.lighting
import random

with redirect_stdout(None):
    import pygame
    from pygame import gfxdraw


# CLASSES
# PARTICLES
class BaseParticle:
    def __init__(self, position: tuple or list, velocity: tuple or list, color: tuple or list, alpha: float = 255, lighting_color=None):
        self.position = list(position)
        self.velocity = list(velocity)

        self.progress = 0
        self.twisted_progress = 1 - self.progress

        self.alive = True

        # COLOR
        self.color = list(color)
        self.start_color = self.color
        self.alpha = alpha
        self.start_alpha = self.alpha
        self.lighting_color = None
        if lighting_color is not None and (isinstance(lighting_color, tuple) or isinstance(lighting_color, list)):
            self.lighting_color = lighting_color

    def kill(self):
        self.alive = False

    @staticmethod
    def get_progress(start_size: float or tuple or list, size: float or tuple or list):
        return size / start_size

    def update(self, start_size: float, size: float, delta_time: float = 1, gravity: float = 0):
        # manipulate positions
        self.position[0] += self.velocity[0] * delta_time
        self.position[1] += self.velocity[1] * delta_time
        self.velocity[1] += gravity

        # get progress of particle
        self.progress = self.get_progress(start_size, size)
        self.twisted_progress = 1 - self.progress

    # fading
    def fade_color(self, color):
        self.color = [self.start_color[0] + (color[0] - self.start_color[0]) * self.twisted_progress,
                      self.start_color[1] + (color[1] - self.start_color[1]) * self.twisted_progress,
                      self.start_color[2] + (color[2] - self.start_color[2]) * self.twisted_progress]

    def fade_alpha(self, alpha):
        self.alpha = self.start_alpha + (alpha - self.start_alpha) * self.twisted_progress


class Circle(BaseParticle):
    def __init__(self, position, velocity, size: float, delta_size: float, color: tuple or list, alpha: float = 255, antialiasing: bool = False, lighting_color=None):
        super().__init__(position, velocity, color, alpha, lighting_color)

        # radius
        self.size = size
        self.start_size = self.size
        self.delta_radius = delta_size

        # antialiasing
        self.antialiasing = antialiasing

    def update(self, start_size: float, size: float, delta_time: float = 1, gravity: float = 0):
        super().update(start_size=start_size, size=size, delta_time=delta_time, gravity=gravity)

        if self.alive: self.size -= self.delta_radius  # decrease radius
        if self.size <= 0: self.alive = False  # check if alive

    def draw(self, surface):
        if self.alive:
            if self.antialiasing:
                gfxdraw.aacircle(surface, int(self.position[0]), int(self.position[1]), int(self.size),
                                 (int(self.color[0]), int(self.color[1]), int(self.color[2]), int(self.alpha)))
            gfxdraw.filled_circle(surface, int(self.position[0]), int(self.position[1]), int(self.size),
                                  (int(self.color[0]), int(self.color[1]), int(self.color[2]), int(self.alpha)))
            if self.lighting_color is not None:
                surface.blit(particlepy.lighting.circle_lighting_surf(self),
                             (self.position[0] - self.size * 2, self.position[1] - self.size * 2),
                             special_flags=pygame.BLEND_RGB_ADD)


class Rect(BaseParticle):
    def __init__(self, position, velocity, size: float, delta_size: float, color: tuple or list, alpha: float = 255, lighting_color=None):
        super().__init__(position, velocity, color, alpha, lighting_color)

        # size
        if isinstance(size, float) or isinstance(size, int):
            self.size = size
        self.start_size = self.size
        self.delta_size = delta_size

    def update(self, start_size: float, size: float, delta_time: float = 1, gravity: float = 0):
        super().update(start_size=start_size, size=size, delta_time=delta_time, gravity=gravity)

        # decrease size
        if self.alive: self.size -= self.delta_size

        # check if alive
        if self.size <= 0: self.alive = False

    def draw(self, surface):
        if self.alive:
            gfxdraw.box(surface, (self.position[0] - self.size / 2, self.position[1] - self.size / 2, self.size, self.size),
                        (int(self.color[0]), int(self.color[1]), int(self.color[2]), int(self.alpha)))
            if self.lighting_color is not None:
                surface.blit(particlepy.lighting.rect_lighting_surf(self),
                             (self.position[0] - self.size * 2, self.position[1] - self.size * 2),
                             special_flags=pygame.BLEND_RGB_ADD)


# PARTICLE SYSTEM
class ParticleSystem:
    def __init__(self, remove_particles_batched: bool = False):
        # options
        self.remove_particles_batched = remove_particles_batched

        # particles
        self.particles = []

        self.alive = True

    def create(self, particle: BaseParticle):
        self.particles.append(particle)

    def kill(self):
        self.particles.clear()
        self.alive = False

    def update(self, delta_time: float = 1, gravity: float = 0):
        random.seed()

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
        for particle in self.particles:
            particle.draw(surface)
