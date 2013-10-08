import pygame
import random
import sys
from pygame.locals import *

import objects

eColi = objects.eColi
print 'Before:\nE. coli'
eColi.print_channels()
env = objects.Environment('Lab', 1, objects.ENVR)
print '\nEnv'
env.print_res()
comm = objects.Ecosystem([eColi], env)
comm.equalize()
print '\nAfter:\nE.coli'
eColi.print_channels()
print '\nEnv'
comm.env.print_res()
print comm.tracker