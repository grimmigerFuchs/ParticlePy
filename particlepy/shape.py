# shape.py
# -*- coding: utf-8 -*-

from typing import Tuple
from abc import ABC
import contextlib

with contextlib.redirect_stdout(None):
    import pygame

# TODO: (AA shapes)
# TODO: angle as arg
# TODO: decrease_size -> decrease_radius
# TODO: attr!


class BaseShape(object):
    """The basic shape class. Is used as :attr:`shape` argument in :class:`particlepy.particle.Particle`.
        Is subclassed to create other shapes, e.g. :class:`particlepy.shape.Circle` or :class:`particlepy.shape.Rect`

    Args:
        radius (float): Radius of shape
        color (Tuple[int]): Color of shape
        alpha (int, optional): Transparency of shape `(0 - 255)`, defaults to `255`

    Attributes:
        radius (float): Radius of shape
        _start_radius (float): Radius of shape when being instanced. Property function is :func:`BaseShape.start_radius`
        angle (int): Degrees of rotation of shape
        color (List[int]): Color of shape
        _start_color (List[int]): Color of shape when being instanced. Property function is :func:`BaseShape.start_color`
        alpha (int): Transparency of shape, ranges from `0` to `255`
        _start_alpha (int): Transparency of shape when being instanced. Property function is :func:`BaseShape.start_alpha`
        surface (:class:`pygame.Surface`): Pygame surface of shape
    """
    def __init__(self, radius: float, color: Tuple[int], alpha: int = 255):
        self.radius = radius
        self._start_radius = self.radius

        self.angle = 0

        self.color = list(color)
        self._start_color = tuple(self.color)
        self.alpha = alpha
        self._start_alpha = self.alpha

        self.surface = self.make_surface()

    @property
    def start_radius(self):
        """Returns :attr:`_start_radius`

        Returns:
            float: :attr:`_start_radius`
        """
        return self._start_radius

    @property
    def start_color(self):
        """Returns :attr:`_start_color`

        Returns:
            Tuple[int]: :attr:`_start_color`
        """
        return self._start_color

    @property
    def start_alpha(self):
        """Returns :attr:`_start_alpha`

        Returns:
            int: :attr:`_start_alpha`
        """
        return self._start_alpha

    def decrease_size(self, delta_size: float):
        """Decreases radius of shape by :attr:`delta_size`

        Args:
            delta_size (float): Radius decrease value
        """
        self.radius -= delta_size
        if self.radius < 0:
            self.radius = 0

    def rotate(self, angle: float):
        """Rotates shape by :attr:`angle`

        Args:
            angle (float): Rotation angle
        """
        if self.radius >= 1:
            self.angle += angle
            self.surface = pygame.transform.rotate(self.surface, self.angle)

    def make_surface(self) -> pygame.Surface:
        """Creates shape surface by creating transparent surface and making shape by calling :func:`particlepy.shape.BaseShape.make_shape`

        Returns:
            :class:`pygame.Surface`: Currently created shape surface (:attr:`surface`)
        """
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.surface.set_alpha(self.alpha)
        self.make_shape()
        return self.surface

    def make_shape(self):
        """Creates shape for shape surface. Can be modified to make different shapes and effects.
        """
        raise NotImplementedError("particlepy.shape.BaseShape.make_shape() creates no shape."
                                  "Own functions have to be written for custom shapes.")


class Circle(BaseShape, ABC):
    """Circle shape class. Is subclass of :class:`particlepy.shape.BaseShape` and inherits all attributes and methods
    """
    def make_shape(self):
        """Makes a circle
        """
        pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)


class Rect(BaseShape, ABC):
    """Rectangle shape class. Is subclass of :class:`particlepy.shape.BaseShape` and inherits all attributes and methods
    """
    def make_shape(self):
        """Makes a rectangle
        """
        self.surface.fill(self.color)
