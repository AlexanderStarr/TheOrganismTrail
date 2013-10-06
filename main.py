import pygame
import random
import sys
from pygame.locals import *

import objects

eColi = objects.eColi

print str(eColi)
print "Count\tVolume"
while eColi.conc['atp'] > 10:
    print str(eColi.count) + "\t" + str(eColi.volume())
    eColi.count = eColi.count * 2
    eColi.conc['atp'] = eColi.conc['atp']/2