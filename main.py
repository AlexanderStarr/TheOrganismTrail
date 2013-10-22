import pygame
import random
import sys
from pygame.locals import *

from defs.defaults import *

env = Environment('Lab', 1, ENVR)
eco = Ecosystem([eColi], env)
for i in range(1440):
    eco.cycle()

print ""