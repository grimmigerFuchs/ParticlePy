from typing import Tuple

import particlepy.particle


def fade_color(particle: particlepy.particle.Particle, color: Tuple[int, int, int], progress: float):
    particle.shape.color = [particle.shape.start_color[0] + (color[0] - particle.shape.start_color[0]) * progress,
                            particle.shape.start_color[1] + (color[1] - particle.shape.start_color[1]) * progress,
                            particle.shape.start_color[2] + (color[2] - particle.shape.start_color[2]) * progress]


def fade_alpha(particle: particlepy.particle.Particle, alpha: int, progress: float):
    particle.shape.alpha = particle.shape.start_alpha + (alpha - particle.shape.start_alpha) * progress
