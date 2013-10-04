import pygame
import random
import sys
from pygame.locals import *

from organisms import Bacteria

def inbounds(coords):
    if (0 <= coords[0] <= 630) and (0<= coords[1] <= 470):
        return True
    else:
        return False

pygame.init()
fpsClock = pygame.time.Clock()

windowSurface = pygame.display.set_mode((320,240))
pygame.display.set_caption('Bactimulator')

green = pygame.Color(0,255,0)
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)

windowSurface.fill(white)
activeCells = {(0,0): Bacteria((0,0))}
cellExists = {(0, 0): True}

while True:
    newCells = {}
    cellsToDel = []
    for cell in activeCells:
        if not activeCells[cell].canReproduce():
            cellsToDel.append(cell)
        else:
            newCell = activeCells[cell].reproduce()
            if newCell:
                try:
                    cellExists[newCell]
                except KeyError:
                    newCells[newCell] = Bacteria(newCell)
                    cellExists = {newCell: True}

    for cell in newCells:
        pygame.draw.rect(windowSurface, green, newCells[cell].draw())

    for cell in cellsToDel:
        del activeCells[cell]

    activeCells.update(newCells)
                

    pygame.display.update()
    fpsClock.tick(30)
