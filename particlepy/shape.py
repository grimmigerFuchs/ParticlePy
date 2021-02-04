# shape.py
# -*- coding: utf-8 -*-

from typing import Tuple
from abc import ABC
import contextlib

with contextlib.redirect_stdout(None):
    import pygame

# TODO: AA shapes


class BaseShape(object):
    """The basic shape class. Is used as :attr:`shape` argument in :class:`particlepy.particle.Particle`.
        Is subclassed to create other shapes, e.g. :class:`particlepy.shape.Circle` or :class:`particlepy.shape.Rect`

    Args:
        radius (float): Radius of shape
        color (Tuple[int, int, int]): Color of shape
        alpha (int, optional): Transparency of shape `(0 - 255)`, defaults to `255`
        angle (float, optional): Degrees of rotation of shape, defaults to `0`

    Attributes:
        radius (float): Radius of shape
        _start_radius (float): Radius of shape when being instanced. Property is :func:`BaseShape.start_radius`
        angle (int): Degrees of rotation of shape
        color (List[int, int, int]): Color of shape
        _start_color (Tuple[int, int, int]): Color of shape when being instanced. Property is :func:`BaseShape.start_color`
        alpha (int): Transparency of shape, ranges from `0` to `255`
        _start_alpha (int): Transparency of shape when being instanced. Property is :func:`BaseShape.start_alpha`
        surface (:class:`pygame.Surface`): Pygame surface of shape
    """
    def __init__(self, radius: float, color: Tuple[int, int, int], alpha: int = 255, angle: float = 0):
        self.radius = radius
        self._start_radius = self.radius

        self.angle = angle

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

    def decrease_radius(self, delta_radius: float):
        """Decreases radius of shape by :attr:`delta_radius`

        Args:
            delta_radius (float): Radius decrease value
        """
        self.radius -= delta_radius
        if self.radius < 0:
            self.radius = 0

    def make_surface(self) -> pygame.Surface:
        """Creates shape surface by creating transparent surface and making shape by calling :func:`particlepy.shape.BaseShape.make_shape()`

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

    def rotate_shape(self):
        """Rotates shape. Only called by :func:`particlepy.BaseShape.make_shape()`
        """
        if self.radius > 1:  # pygame issue: https://github.com/pygame/pygame/issues/2464
            self.surface = pygame.transform.rotate(self.surface, self.angle)


class Circle(BaseShape, ABC):
    """Circle shape class. Is subclass of :class:`particlepy.shape.BaseShape` and inherits all attributes and methods

    Args:
        radius (float): Radius of shape
        color (Tuple[int, int, int]): Color of shape
        alpha (int, optional): Transparency of shape `(0 - 255)`, defaults to `255`
        angle (float, optional): Degrees of rotation of shape, defaults to `0`

    Attributes:
        radius (float): Radius of shape
        _start_radius (float): Radius of shape when being instanced. Property is :func:`BaseShape.start_radius`
        angle (int): Degrees of rotation of shape
        color (List[int, int, int]): Color of shape
        _start_color (Tuple[int, int, int]): Color of shape when being instanced. Property is :func:`BaseShape.start_color`
        alpha (int): Transparency of shape, ranges from `0` to `255`
        _start_alpha (int): Transparency of shape when being instanced. Property is :func:`BaseShape.start_alpha`
        surface (:class:`pygame.Surface`): Pygame surface of shape
    """

    def __init__(self, radius: float, color: Tuple[int, int, int], alpha: int = 255, angle: float = 0):
        """Constructor method
        """
        super(Circle, self).__init__(radius=radius, color=color, alpha=alpha, angle=angle)

    def make_shape(self):
        """Makes a circle and rotates it according to :attr:`angle`
        """
        pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)
        self.rotate_shape()


class Rect(BaseShape, ABC):
    """Rectangle shape class. Is subclass of :class:`particlepy.shape.BaseShape` and inherits all attributes and methods

    Args:
        radius (float): Radius of shape
        color (Tuple[int, int, int]): Color of shape
        alpha (int, optional): Transparency of shape `(0 - 255)`, defaults to `255`
        angle (float, optional): Degrees of rotation of shape, defaults to `0`

    Attributes:
        radius (float): Radius of shape
        _start_radius (float): Radius of shape when being instanced. Property is :func:`BaseShape.start_radius`
        angle (int): Degrees of rotation of shape
        color (List[int, int, int]): Color of shape
        _start_color (Tuple[int, int, int]): Color of shape when being instanced. Property is :func:`BaseShape.start_color`
        alpha (int): Transparency of shape, ranges from `0` to `255`
        _start_alpha (int): Transparency of shape when being instanced. Property  is :func:`BaseShape.start_alpha`
        surface (:class:`pygame.Surface`): Pygame surface of shape
    """

    def __init__(self, radius: float, color: Tuple[int, int, int], alpha: int = 255, angle: float = 0):
        """Constructor method
        """
        super(Rect, self).__init__(radius=radius, color=color, alpha=alpha, angle=angle)

    def make_shape(self):
        """Makes a rectangle and rotates it according to :attr:`angle`
        """
        self.surface.fill(self.color)
        self.rotate_shape()
