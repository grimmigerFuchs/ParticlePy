# __init__.py

__author__ = "grimmigerFuchs"
__credits__ = [__author__, "DaFluffyPotato"]
__version__ = "0.1.2"


from contextlib import redirect_stdout
import math
with redirect_stdout(None):
    import pygame

# particlepy
import particlepy.particle
import particlepy.math