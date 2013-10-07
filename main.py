import pygame
import random
import sys
from pygame.locals import *

import objects

eColi = objects.eColi
print 'Before:'
eColi.print_channels()
env = objects.Environment('Lab', 1, objects.ENVR, 37, True)
comm = objects.Ecosystem([eColi], env)
comm.equalize()
print '\nAfter:'
eColi.print_channels()