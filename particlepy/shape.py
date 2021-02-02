# shape.py

from typing import Tuple
from abc import ABC
import contextlib

with contextlib.redirect_stdout(None):
    import pygame


# TODO: AA shapes


class BaseShape(object):
    def __init__(self, radius: float, color: Tuple[int, int, int], alpha: int = 255):
        self.radius = radius
        self._start_radius = self.radius

        self.angle = 0

        try:
            self.color = list(color)
        except TypeError:
            self.color = None
        try:
            self._start_color = tuple(self.color)
        except TypeError:
            self._start_color = self.color
        self.alpha = alpha
        self._start_alpha = self.alpha

        self.surface = self.make_surface()

    @property
    def start_radius(self):
        return self._start_radius

    @property
    def start_color(self):
        return self._start_color

    @property
    def start_alpha(self):
        return self._start_alpha

    def decrease_size(self, delta_size: float):
        self.radius -= delta_size
        if self.radius < 0:
            self.radius = 0

    def rotate(self, angle: float):
        if self.radius >= 1:
            self.angle += angle
            self.surface = pygame.transform.rotate(self.surface, self.angle)

    def make_surface(self) -> pygame.Surface:
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.surface.set_alpha(self.alpha)
        self.make_shape()
        return self.surface

    def make_shape(self):
        raise NotImplementedError


class Circle(BaseShape, ABC):
    def make_shape(self):
        pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)


class Rect(BaseShape, ABC):
    def make_shape(self):
        self.surface.fill(self.color)
