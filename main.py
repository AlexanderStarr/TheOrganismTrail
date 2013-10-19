import pygame
import random
import sys
from pygame.locals import *

import objects

cDiff = objects.cDiff
eColi = objects.eColi
env = objects.Environment('Lab', 1, objects.ENVR)
eco = objects.Ecosystem([eColi, cDiff], env)
for i in range(10):
    #for org in eco.orgs:
    eco.orgs[0].printSummary()
    #eco.env.printRes()
    eco.cycle()
for org in eco.orgs:
    org.printRes()