import pygame
from pygame import gfxdraw


def circle_lighting_surf(particle):
    size = particle.size
    surf = pygame.Surface((size * 4, size * 4))
    pygame.draw.circle(surf, particle.lighting_color, (size * 2, size * 2), size * 2)
    surf.set_colorkey((0, 0, 0))
    return surf


def rect_lighting_surf(particle):
    size = int(particle.size)
    surf = pygame.Surface((size * 4, size * 4))
    pygame.draw.rect(surf, particle.lighting_color, (size, size, size * 2, size * 2))
    surf.set_colorkey((0, 0, 0))
    return surf
