# math.py

import particlepy.particle


def fade_to_color(particle: particlepy.particle.BaseParticle, wanted_color):
    return (particle.start_color[0] + (wanted_color[0] - particle.start_color[0]) * particle.twisted_progress,
            particle.start_color[1] + (wanted_color[1] - particle.start_color[1]) * particle.twisted_progress,
            particle.start_color[2] + (wanted_color[2] - particle.start_color[2]) * particle.twisted_progress)
