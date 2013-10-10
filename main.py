import pygame
import random
import sys
from pygame.locals import *

import objects

eColi = objects.eColi
print 'Before:\nE. coli'
eColi.printRes()
env = objects.Environment('Lab', 1, objects.ENVR)
#print '\nEnv'
#env.printRes()
comm = objects.Ecosystem([eColi], env)
comm.equalize()
eColi.exchange(env.partition(comm)[0])
print '\nAfter:\nE.coli'
eColi.printRes()
#print '\nEnv'
#comm.env.printRes()
print comm.tracker