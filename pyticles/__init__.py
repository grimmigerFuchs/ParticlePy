# pyticles.py

__author__ = "grimmigerFuchs"
__credits__ = [__author__, "DaFluffyPotato"]
__version__ = "0.1.2"


from contextlib import redirect_stdout
with redirect_stdout(None):
    import pygame

shapes = ["circle", "rect"]


class Shape:
    def __init__(self):
        self.circle = shapes[0]
        self.rect = shapes[1]


class Particle:
    def __init__(self, position: tuple or list, velocity: tuple or list, gravity: float, radius: float,
                 delta_radius: float, color: tuple or list or int, shape: str):
        self.position = list(position)
        self.velocity = list(velocity)
        self.radius = radius
        self.delta_radius = delta_radius
        self.gravity = gravity

        # color can be rgb or greyscale
        if isinstance(color, tuple) or isinstance(color, list):
            self.color = color
        elif isinstance(color, int):
            self.color = color, color, color
        else:
            self.color = (255, 255, 255)

        # shapes
        self.shape = shape.lower()

    def update(self, delta_time: float = 1):
        # manipulate positions
        self.position[0] += self.velocity[0] * delta_time
        self.position[1] += self.velocity[1] * delta_time
        self.velocity[1] += self.gravity

        # decrease radius
        self.radius -= self.delta_radius

    def to_remove(self):  # check if particle is to be removed
        if self.radius <= 0: return True  # if no longer visible return remove signal
        else: return False

    def draw(self, surface):
        if self.shape == "circle":
            pygame.draw.circle(surface, self.color, self.position, self.radius)  # draw particle as circle
        elif self.shape == "rect":
            pygame.draw.rect(surface, self.color,
                             (self.position[0] - self.radius / 2, self.position[1] - self.radius / 2,
                              int(self.radius * 2), int(self.radius * 2)))