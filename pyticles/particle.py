import pygame
import pygame.gfxdraw


# PARTICLES
class BaseParticle:
    def __init__(self, position: tuple or list, velocity: tuple or list, color: int or tuple or list, alpha: int):
        self.position = list(position)
        self.velocity = list(velocity)

        self.alive = True

        # color
        if isinstance(color, int):
            self.color = color, color, color, alpha
        elif isinstance(color, tuple) or isinstance(color, list):
            self.color = color[0], color[1], color[2], alpha

    def update(self, delta_time: float = 1, gravity: float = 0):
        # manipulate positions
        self.position[0] += self.velocity[0] * delta_time
        self.position[1] += self.velocity[1] * delta_time
        self.velocity[1] += gravity


class Circle(BaseParticle):
    def __init__(self, position, velocity, radius: float, delta_radius: float, color, alpha: int = 255, antialiasing: bool = False):
        super().__init__(position, velocity, color, alpha)

        # radius
        self.radius = radius
        self.delta_radius = delta_radius

        # antialiasing
        self.antialiasing = antialiasing

    def update(self, delta_time: float = 1, gravity: float = 0):
        super().update(delta_time, gravity)

        if self.alive: self.radius -= self.delta_radius  # decrease radius
        if self.radius <= 0: self.alive = False  # check if alive

    def draw(self, surface):
        if self.alive:
            if self.antialiasing:
                pygame.gfxdraw.aacircle(surface, int(self.position[0]), int(self.position[1]), int(self.radius), self.color)
            pygame.gfxdraw.filled_circle(surface, int(self.position[0]), int(self.position[1]), int(self.radius), self.color)


class Rect(BaseParticle):
    def __init__(self, position, velocity, size: float or tuple or list, delta_size: float or tuple or list, color, alpha):
        super().__init__(position, velocity, color, alpha)

        # size
        if isinstance(size, float) or isinstance(size, int):
            self.size = [size, size]
        elif isinstance(size, tuple) or isinstance(size, list):
            self.size = list(size)
        self.delta_size = delta_size

    def update(self, delta_time: float = 1, gravity: float = 0):
        super().update(delta_time, gravity)

        # decrease size
        if self.alive:
            if isinstance(self.delta_size, float):
                self.size[0] -= self.delta_size
                self.size[1] -= self.delta_size
            elif isinstance(self.delta_size, tuple) or isinstance(self.delta_size, list):
                self.size[0] -= self.delta_size[0]
                self.size[1] -= self.delta_size[1]

        if self.size[0] <= 0 or self.size[1] <= 0:
            self.alive = False

    def draw(self, surface):
        if self.alive:
            pygame.gfxdraw.box(surface, (self.position[0] - self.size[0] / 2, self.position[1] - self.size[1] / 2,
                                         self.size[0], self.size[1]), self.color)


# PARTICLE SYSTEM
class ParticleSystem:
    def __init__(self, remove_particle_if_not_alive: bool = False):
        # options
        self.remove_particle_if_not_alive = remove_particle_if_not_alive

        # particles
        self.particles = []

        self.alive = True

    def create(self, particle: BaseParticle):
        self.particles.append(particle)
        if not isinstance(particle, BaseParticle): print("not!")

    def update(self, delta_time: float = 1, gravity: float = 0):
        if len(self.particles) > 0: self.alive = True

        removes = []
        if not self.remove_particle_if_not_alive: alive = True

        for particle in self.particles:
            particle.update(delta_time, gravity)
            if self.remove_particle_if_not_alive:
                if not particle.alive:
                    removes.append(particle)

        if self.remove_particle_if_not_alive:
            for i in range(len(removes)):
                self.particles.remove(removes[i])
        else:
            for particle in self.particles:
                if not particle.alive:
                    alive = False
                else:
                    alive = True
                    break
            if not alive:
                self.particles.clear()
                self.alive = False

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)
