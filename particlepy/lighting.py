import pygame


def circle_lighting_surf(particle):
    """
    This function takes in one particle and returns a transparent circular pygame surface used for lighting,
    this function is only used by particle classes

    :param particle: Takes in a particle
    :type particle: particle class with size
    :return: Returns a pygame surface
    :rtype: pygame.Surface
    """
    size = particle.size
    surf = pygame.Surface((size * 4, size * 4))
    pygame.draw.circle(surf, particle.lighting_color, (size * 2, size * 2), size * 2)
    surf.set_colorkey((0, 0, 0))
    return surf


def rect_lighting_surf(particle):
    """
    This function takes in one particle and returns a transparent rectangular pygame surface used for lighting,
    this function is only used by particle classes

    :param particle: Takes in a particle instance
    :type particle: particle instance with size
    :return: Returns a pygame surface
    :rtype: pygame.Surface
    """
    size = int(particle.size)
    surf = pygame.Surface((size * 4, size * 4))
    pygame.draw.rect(surf, particle.lighting_color, (size, size, size * 2, size * 2))
    surf.set_colorkey((0, 0, 0))
    return surf
