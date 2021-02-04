# math.py
# -*- coding: utf-8 -*-

from typing import Tuple

import particlepy.particle


def fade_color(particle: particlepy.particle.Particle, color: Tuple[int, int, int], progress: float):
    """Fades color of :attr:`particle` over life span (:attr:`progress`) to new color (:attr:`color`)

    Args:
        particle (:class:`particlepy.particle.Particle`): Particle to fade color with
        color (Tuple[int, int, int]): Color to fade to
        progress (float): Life span identifier:
            :attr:`particlepy.particle.Particle.progress` or :attr:`particlepy.particle.Particle.inverted_progress`

    Returns:
        List[float]: New color of particle
    """
    return [particle.shape.start_color[0] + (color[0] - particle.shape.start_color[0]) * progress,
            particle.shape.start_color[1] + (color[1] - particle.shape.start_color[1]) * progress,
            particle.shape.start_color[2] + (color[2] - particle.shape.start_color[2]) * progress]


def fade_alpha(particle: particlepy.particle.Particle, alpha: int, progress: float):
    """Fades :attr:`alpha` (transparency) of argument :attr:`particle` over life span (:attr:`progress`) to new color (:attr:`color`)

    Args:
        particle (:class:`particlepy.particle.Particle`): Particle to alpha color with
        alpha (int): Transparency to fade to
        progress (float): Life span identifier:
            :attr:`particlepy.particle.Particle.progress` or :attr:`particlepy.particle.Particle.inverted_progress`

    Returns:
        float: New alpha of particle
    """
    return particle.shape.start_alpha + (alpha - particle.shape.start_alpha) * progress
