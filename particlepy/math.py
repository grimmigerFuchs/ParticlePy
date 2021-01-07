# math.py

import particlepy.particle
import math


def fade_to_color(particle: particlepy.particle.BaseParticle, wanted_color):
    particle.color[0] = particle.start_color[0] + (wanted_color[0] - particle.start_color[0]) * particle.progress
    particle.color[1] = particle.start_color[1] + (wanted_color[1] - particle.start_color[1]) * particle.progress
    particle.color[2] = particle.start_color[2] + (wanted_color[2] - particle.start_color[2]) * particle.progress
