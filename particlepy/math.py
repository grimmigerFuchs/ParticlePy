# math.py
# -*- coding: utf-8 -*-

from typing import Tuple

import particlepy.particle


def fade_color(particle: particlepy.particle.Particle, color: Tuple[int, int, int], progress: float) -> list:
    """Fades color of :attr:`particle` over life span (:attr:`progress`) to new color (:attr:`color`)

    Args:
        particle (:class:`particlepy.particle.Particle`): Particle to fade color with
        color (Tuple[int, int, int]): Color to fade to
        progress (float): Life span identifier:
            :attr:`particlepy.particle.Particle.progress` or :attr:`particlepy.particle.Particle.inverted_progress`

    Returns:
        List[float]: New color of particle

    Raises:
        AssertionError: If :attr:`particle.shape` not :class:`particlepy.shape.BaseForm`
    """
    assert isinstance(particle.shape, particlepy.shape.BaseForm)
    return [particle.shape.orig_color[i] + (color[i] - particle.shape.orig_color[i]) * progress for i in range(3)]


def fade_alpha(particle: particlepy.particle.Particle, alpha: int, progress: float) -> float:
    """Fades :attr:`alpha` (transparency) of argument :attr:`particle` over life span (:attr:`progress`) to new color (:attr:`color`)

    Args:
        particle (:class:`particlepy.particle.Particle`): Particle to alpha color with
        alpha (int): Transparency to fade to
        progress (float): Life span identifier:
            :attr:`particlepy.particle.Particle.progress` or :attr:`particlepy.particle.Particle.inverted_progress`

    Returns:
        float: New alpha of particle
    """
    return particle.shape.orig_alpha + (alpha - particle.shape.orig_alpha) * progress
