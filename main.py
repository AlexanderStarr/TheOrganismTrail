import pygame
import random
import sys
from pygame.locals import *

import objects

eColi = objects.eColi
print 'Before:\nE. coli'
eColi.printChannels()
env = objects.Environment('Lab', 1, objects.ENVR)
#print '\nEnv'
#env.printRes()
comm = objects.Ecosystem([eColi], env)
comm.equalize()
eColi.exchangeRes(env.partition(comm)[0])
print '\nAfter:\nE.coli'
eColi.printChannels()
#print '\nEnv'
#comm.env.printRes()
print comm.tracker