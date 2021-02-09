# shape.py
# -*- coding: utf-8 -*-

from typing import Tuple
from abc import ABC
import copy
import numpy
import contextlib

with contextlib.redirect_stdout(None):
    import pygame


# TODO: AA shapes
# todo: remove rotate_shape()
# todo: change _start_... to _orig_...


class Shape(object):
    def __init__(self, alpha: float = 255, angle: float = 0):
        self._start_alpha = alpha
        self.alpha = self._start_alpha
        self.angle = angle
        self._start_angle = self.angle

        self.surface: pygame.Surface = None
        self.rect: pygame.Rect = None

    @property
    def start_alpha(self):
        return self._start_alpha

    @property
    def start_angle(self):
        return self._start_angle

    def check_size_above_zero(self) -> bool:
        raise NotImplementedError

    def get_progress(self) -> Tuple[float, float]:
        raise NotImplementedError

    def decrease(self, delta: float):
        raise NotImplementedError

    def make_surface(self) -> pygame.Surface:
        self.make_shape()
        raise NotImplementedError

    def make_shape(self):
        raise NotImplementedError


class BaseForm(Shape, ABC):
    """The basic form class. Is used as :attr:`shape` argument in :class:`particlepy.particle.Particle`.
        Is subclassed to create other shapes, e.g. :class:`Circle` or :class:`Rect`

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
        rect (:class:`pygame.Rect`): Pygame Rect of :attr:`surface`. Position does not affect anything
    """

    def __init__(self, radius: float, color: Tuple[int, int, int], alpha: int = 255, angle: float = 0):
        super(BaseForm, self).__init__(alpha=alpha, angle=angle)

        self.radius = radius
        self._start_radius = self.radius

        self.color = list(color)
        self._start_color = tuple(self.color)

        self.rect = None
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

    def check_size_above_zero(self):
        if self.radius > 0:
            return True
        else:
            return False

    def get_progress(self) -> Tuple[float, float]:
        """Returns tuple of two floats: `progress` and `inverted_progress`

        Returns:
            Tuple[float, float]: `progress` and `inverted_progress`
        """
        progress = self.radius / self._start_radius
        return progress, 1 - progress

    def decrease(self, delta: float):
        """Decreases radius of shape by :attr:`delta_radius`

        Args:
            delta (float): Radius decrease value
        """
        self.radius -= delta
        if self.radius < 0:
            self.radius = 0

    def make_surface(self) -> pygame.Surface:
        """Creates shape surface and rect by calling :func:`BaseShape.make_shape()` and :func:`BaseShape.rotate()`

        Returns:
            :class:`pygame.Surface`: Currently created shape surface (:attr:`surface`)
        """
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.surface.set_alpha(self.alpha)
        self.make_shape()
        self.rotate_shape()
        self.rect = self.surface.get_rect()
        return self.surface

    def make_shape(self):
        """Creates shape for shape surface. Can be modified to make different shapes and effects.
        """
        raise NotImplementedError("BaseShape.make_shape() creates no shape."
                                  "Own functions have to be written for custom shapes.")

    def rotate_shape(self):
        """Rotates shape. Only called by :func:`BaseShape.make_shape()`
        """
        if self.radius > 1:  # pygame issue: https://github.com/pygame/pygame/issues/2464
            self.surface = pygame.transform.rotate(self.surface, self.angle)


class Circle(BaseForm, ABC):
    """Circle shape class. Is subclass of :class:`BaseShape` and inherits all attributes and methods

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
        super(Circle, self).__init__(radius, color, alpha, angle)

    def make_shape(self):
        """Makes a circle
        """
        pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)


class Rect(BaseForm, ABC):
    """Rectangle shape class. Is subclass of :class:`BaseShape` and inherits all attributes and methods

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
        super(Rect, self).__init__(radius, color, alpha, angle)

    def make_shape(self):
        """Makes a rectangle
        """
        self.surface.fill(self.color)


class Image(Shape, ABC):
    # todo: copy
    def __init__(self, surface: pygame.Surface, size: Tuple[int, int], alpha: int = 255, angle: float = 0):
        super(Image, self).__init__(alpha=alpha, angle=angle)
        self._start_size = tuple(size)
        self.size = list(self._start_size)

        self._start_surface = surface.copy()
        self.surface = None
        self.rect = None

        self.make_surface()

    @property
    def start_size(self):
        return self._start_size

    @property
    def start_surface(self):
        return self._start_surface

    def check_size_above_zero(self) -> bool:
        if (self.size[0] > 0) and (self.size[1] > 0):
            return True
        else:
            return False

    def get_progress(self) -> Tuple[float, float]:
        progress = (self.size[0] - numpy.diff(self.size) / 2) / (self._start_size[0] - numpy.diff(self._start_size) / 2)
        return progress, 1 - progress

    def decrease(self, delta: float):
        for i in range(2):
            self.size[i] -= delta
            if self.size[i] <= 0:
                self.size[i] = 0

    def make_surface(self) -> pygame.Surface:
        self.make_shape()
        if self.alpha < 255:
            self.surface.set_alpha(self.alpha)
        return self.surface

    def make_shape(self):
        if self.size != self._start_size:
            self.surface = pygame.transform.scale(self._start_surface, (int(self.size[0]), int(self.size[1])))
        if self.angle != 0 and (self.size[0] > 1 and self.size[1] > 1):
            self.surface = pygame.transform.rotate(self.surface, self.angle)
        self.rect = self.surface.get_rect()
