# shape.py
# -*- coding: utf-8 -*-

from typing import Tuple
from abc import ABC
import numpy
import contextlib

with contextlib.redirect_stdout(None):
    import pygame


# TODO: AA shapes


def rotate(surface: pygame.Surface, angle: float):
    """Rotates shape by angle

    Notes:
        Only exists because of `pygame issue 2464 <https://github.com/pygame/pygame/issues/2464>`__.
    """
    if bool(sum((True if size > 1 else False for size in surface.get_size()))) and angle != 0:
        return pygame.transform.rotate(surface, angle)
    else:
        return surface


class Shape(object):
    """This is the shape class. It is only used to subclass and use as a base for shapes.

    Args:
        alpha (int, optional): Transparency of shape `(0 - 255 → RGBA)`, defaults to `255`
        angle (float, optional): Degrees of rotation, defaults to `0`

    Attributes:
        alpha (int): Transparency of shape, ranges from `0` to `255`
        _orig_alpha (int): Transparency of shape when being instanced. Property is :func:`Shape.orig_alpha()`
        angle (float): Degrees of rotation
        _orig_angle (float): Angle of shape when being instanced. Property is :func:`Shape.orig_angle()`
    """

    def __init__(self, alpha: int = 255, angle: float = 0):
        """Constructor method
        """
        self._orig_alpha = alpha
        self.alpha = self._orig_alpha
        self.angle = angle
        self._orig_angle = self.angle

        self.surface: pygame.Surface = None
        self.rect: pygame.Rect = None

    @property
    def orig_alpha(self):
        """Returns original alpha

        Returns:
            int: :attr:`_orig_alpha`
        """
        return self._orig_alpha

    @property
    def orig_angle(self):
        """Returns original angle

        Returns:
            float: :attr:`_orig_angle`
        """
        return self._orig_angle

    def check_size_above_zero(self) -> bool:
        """Checks if surface size is above `null`

        Returns:
            bool: `True` if surface size above `null`, `False` if otherwise
        """
        raise NotImplementedError

    def get_progress(self) -> Tuple[float, float]:
        """Returns :attr:`progress` and :attr:`inverted_progress` of shape

        Returns:
            Tuple[float, float]: :attr:`progress`, :attr:`inverted_progress`
        """
        raise NotImplementedError

    def decrease(self, delta: float):
        """Decreases size by :attr:`attr`
        """
        raise NotImplementedError

    def make_surface(self) -> pygame.Surface:
        """Makes the surface by also calling :func:`Shape.make_shape()`

        Returns:
            :class:`pygame.Surface`: Surface of shape
        """
        self.make_shape()

    def make_shape(self):
        """Is being called by :func:`Shape.make_surface()` and used to make the visual representation of the shape
        """
        raise NotImplementedError


class BaseForm(Shape, ABC):
    """The basic form class. Is used as :attr:`shape` argument in :class:`particlepy.particle.Particle`.
        Is subclassed to create other shapes, e.g. :class:`Circle` or :class:`Rect`

    Args:
        radius (float): Radius of shape
        color (Tuple[int, int, int]): Color of shape
        alpha (int, optional): Transparency of shape `(0 - 255 → RGBA)`, defaults to `255`
        angle (float, optional): Degrees of rotation, defaults to `0`

    Attributes:
        radius (float): Radius of shape
        _orig_radius (float): Radius of shape when being instanced. Property is :func:`BaseForm.orig_radius()`
        color (List[int, int, int]): Color of shape
        _orig_color (Tuple[int, int, int]): Color of shape when being instanced. Property is :func:`BaseForm.orig_color()`
        alpha (int): Transparency of shape, ranges from `0` to `255`
        _orig_alpha (int): Transparency of shape when being instanced. Property is :func:`BaseForm.orig_alpha()`
        angle (int): Degrees of rotation of shape
        _orig_angle (float): Angle of shape when being instanced. Property is :func:`BaseForm.orig_angle()`
        surface (:class:`pygame.Surface`): Pygame surface of shape
        rect (:class:`pygame.Rect`): Pygame Rect of :attr:`surface`. Position does not affect anything
    """

    def __init__(self, radius: float, color: Tuple[int, int, int], alpha: int = 255, angle: float = 0):
        """Constructor method
        """
        super(BaseForm, self).__init__(alpha=alpha, angle=angle)

        self.radius = radius
        self._orig_radius = self.radius

        self.color = list(color)
        self._orig_color = tuple(self.color)

        self.make_surface()

    @property
    def orig_radius(self):
        """Returns :attr:`_orig_radius`

        Returns:
            float: :attr:`_orig_radius`
        """
        return self._orig_radius

    @property
    def orig_color(self):
        """Returns :attr:`_orig_color`

        Returns:
            Tuple[int]: :attr:`_orig_color`
        """
        return self._orig_color

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
        progress = self.radius / self._orig_radius
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
        """Makes the surface by also calling :func:`Shape.make_shape()`

        Returns:
            :class:`pygame.Surface`: Surface of shape
        """
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.surface.set_alpha(self.alpha)
        self.make_shape()
        self.surface = rotate(surface=self.surface, angle=self.angle)
        self.rect = self.surface.get_rect()
        return self.surface

    def make_shape(self):
        """Creates shape for shape surface. Can be modified to make different shapes and effects.
        """
        raise NotImplementedError(
            "BaseForm.make_shape() creates no shape. Own functions have to be written for custom shapes.")


class Circle(BaseForm, ABC):
    """Circle shape class. Is subclass of :class:`BaseForm` and inherits all attributes and methods

    Args:
        radius (float): Radius of shape
        color (Tuple[int, int, int]): Color of shape
        alpha (int, optional): Transparency of shape `(0 - 255 → RGBA)`, defaults to `255`
        angle (float, optional): Degrees of rotation, defaults to `0`

    Attributes:
        radius (float): Radius of shape
        _orig_radius (float): Radius of shape when being instanced. Property is :func:`Circle.orig_radius()`
        color (List[int, int, int]): Color of shape
        _orig_color (Tuple[int, int, int]): Color of shape when being instanced. Property is :func:`Circle.orig_color()`
        alpha (int): Transparency of shape, ranges from `0` to `255`
        _orig_alpha (int): Transparency of shape when being instanced. Property is :func:`Circle.orig_alpha()`
        angle (int): Degrees of rotation of shape
        _orig_angle (float): Angle of shape when being instanced. Property is :func:`Circle.orig_angle()`
        surface (:class:`pygame.Surface`): Pygame surface of shape
        rect (:class:`pygame.Rect`): Pygame Rect of :attr:`surface`. Position does not affect anything
    """

    def __init__(self, radius: float, color: Tuple[int, int, int], alpha: int = 255, angle: float = 0):
        """Constructor method
        """
        super(Circle, self).__init__(radius, color, alpha, angle)

    def make_shape(self):
        """Makes a circle
        """
        pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)


class Rect(BaseForm, ABC):
    """Rectangle shape class. Is subclass of :class:`BaseForm` and inherits all attributes and methods

    Args:
        radius (float): Radius of shape
        color (Tuple[int, int, int]): Color of shape
        alpha (int, optional): Transparency of shape `(0 - 255 → RGBA)`, defaults to `255`
        angle (float, optional): Degrees of rotation, defaults to `0`

    Attributes:
        radius (float): Radius of shape
        _orig_radius (float): Radius of shape when being instanced. Property is :func:`Rect.orig_radius()`
        color (List[int, int, int]): Color of shape
        _orig_color (Tuple[int, int, int]): Color of shape when being instanced. Property is :func:`Rect.orig_color()`
        alpha (int): Transparency of shape, ranges from `0` to `255`
        _orig_alpha (int): Transparency of shape when being instanced. Property is :func:`Rect.orig_alpha()`
        angle (int): Degrees of rotation of shape
        _orig_angle (float): Angle of shape when being instanced. Property is :func:`Rect.orig_angle()`
        surface (:class:`pygame.Surface`): Pygame surface of shape
        rect (:class:`pygame.Rect`): Pygame Rect of :attr:`surface`. Position does not affect anything
    """

    def __init__(self, radius: float, color: Tuple[int, int, int], alpha: int = 255, angle: float = 0):
        """Constructor method
        """
        super(Rect, self).__init__(radius, color, alpha, angle)

    def make_shape(self):
        """Makes a rectangle
        """
        self.surface.fill(self.color)


class Image(Shape, ABC):
    """Image shape class. Is subclass of :class:`Shape` and inherits all attributes and methods and adds to it

    Args:
        surface (:class:`pygame.Surface`): Surface of shape
        size (Tuple[int, int]): Scaled size of surface
        alpha (int, optional): Transparency of shape `(0 - 255 → RGBA)`, defaults to `255`
        angle (float, optional): Degrees of rotation, defaults to `0`

    Attributes:
        alpha (int): Transparency of shape, ranges from `0` to `255`
        _orig_alpha (int): Transparency of shape when being instanced. Property is :func:`Image.orig_alpha()`
        angle (int): Degrees of rotation of shape
        _orig_angle (float): Angle of shape when being instanced. Property is :func:`Image.orig_angle()`
        size (List[int, int]): Scaled size of surface
        _orig_size (Tuple[int, int]): Scaled size of surface shape when being instanced. Property is :func:`Image.orig_size()`
        surface (:class:`pygame.Surface`): Pygame surface of shape
        _orig_surface (:class:`pygame.Surface`): Surface of shape when being instanced. Property is :func:`Image.orig_surface()`
        rect (:class:`pygame.Rect`): Pygame Rect of :attr:`surface`. Position does not affect anything
    """

    def __init__(self, surface: pygame.Surface, size: Tuple[int, int], alpha: int = 255, angle: float = 0):
        """Constructor method
        """
        super(Image, self).__init__(alpha=alpha, angle=angle)
        self._orig_size = tuple(size)
        self.size = list(self._orig_size)

        self._orig_surface = surface.copy()
        self.make_surface()

    @property
    def orig_size(self):
        """Returns :attr:`_orig_size`

        Returns:
            Tuple[int, int]: :attr:`_orig_size`
        """
        return self._orig_size

    @property
    def orig_surface(self):
        """Returns :attr:`_orig_surface`

        Returns:
            Tuple[int, int]: :attr:`_orig_surface`
        """
        return self._orig_surface

    def check_size_above_zero(self) -> bool:
        """Checks if surface size is above `null`

        Returns:
            bool: `True` if surface size above `null`, `False` if otherwise
        """
        if (self.size[0] > 0) and (self.size[1] > 0):
            return True
        else:
            return False

    def get_progress(self) -> Tuple[float, float]:
        """Returns :attr:`progress` and :attr:`inverted_progress` of shape

        Returns:
            Tuple[float, float]: :attr:`progress`, :attr:`inverted_progress`
        """
        progress = (self.size[0] - numpy.diff(self.size) / 2) / (self._orig_size[0] - numpy.diff(self._orig_size) / 2)
        return progress, 1 - progress

    def decrease(self, delta: float):
        """Decreases size by :attr:`attr`
        """
        for i in range(2):
            self.size[i] -= delta
            if self.size[i] <= 0:
                self.size[i] = 0

    def make_surface(self) -> pygame.Surface:
        """Makes the surface by also calling :func:`Image.make_shape()`

        Returns:
            :class:`pygame.Surface`: Surface of shape
        """
        self.make_shape()
        if self.alpha < 255:
            self.surface.set_alpha(self.alpha)
        return self.surface

    def make_shape(self):
        """Is being called by :func:`Image.make_surface()` and used to make the visual representation of the shape
        """
        if self.size != self._orig_size:
            self.surface = pygame.transform.scale(self._orig_surface, (int(self.size[0]), int(self.size[1])))
        self.surface = rotate(surface=self.surface, angle=self.angle)
        self.rect = self.surface.get_rect()
