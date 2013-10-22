import pygame, random, sys, os
from pygame.locals import *
from defs.defaults import *

# Initialize
IMG_DIR = os.path.join('data', 'img')
screen = pygame.display.set_mode((800,600))
background = pygame.image.load(os.path.join(IMG_DIR, 'background.png'))
screen.blit(background, (0,0))

'''env = Environment('Lab', 1, ENVR)
eco = Ecosystem([eColi], env)
for i in range(1440):
    eco.cycle()

print'''

class Game():
    def __init__(self):
        self.high_score = 0

pygame.init()
statusFont = pygame.font.Font(None, 17)
black = (0,0,0)
clock = pygame.time.Clock()
pygame.display.set_caption('The Organism Trail')
FPS = 30

while True:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()