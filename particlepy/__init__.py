# __init__.py

__author__ = "grimmigerFuchs"
__credits__ = [__author__, "DaFluffyPotato"]
__version__ = "1.0.1"


from contextlib import redirect_stdout
with redirect_stdout(None):
    import pygame

# particlepy
from particlepy.particle import *
