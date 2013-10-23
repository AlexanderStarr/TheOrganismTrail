import pygame, random, sys, os
from pygame.locals import *
from defs.defaults import *

# Initialize
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('The Organism Trail')
FPS = 30
clock = pygame.time.Clock()

IMG_DIR = os.path.join('data', 'img')
background = pygame.image.load(os.path.join(IMG_DIR, 'background.png'))
background = background.convert()
screen.blit(background, (0,0))

'''env = environments['Lab']
eco = Ecosystem([eColi], env)
env.printRes()
for i in range(180):
    eco.cycle()
eco.orgs[0].printRes()
env.printRes()

'''
class Game():
    def __init__(self):
        self.menu = None
        self.playerOps = []

    def handleButton(self, menu, button):
        if menu.name == 'Genes':
            self.playerOps.append(operons[button.text])
        if menu.name == 'Main':
            if button.text == 'Quit':
                sys.exit()
            elif button.text == 'Start':
                menu.deactivate()
                self.menu = addGenesMenu

class MenuItem(pygame.font.Font):
    def __init__(self, text, position, fontSize=36, antialias=1, color=(255,255,255), background=None):
        pygame.font.Font.__init__(self, None, fontSize)
        self.text = text
        if background == None:
            self.textSurface = self.render(self.text, antialias, color)
        else:
            self.textSurface = self.render(self.text, antialias, color, background)
        self.position = self.textSurface.get_rect(centerx=position[0], centery=position[1])
    
    def get_pos(self):
        return self.position
    
    def get_text(self):
        return self.text
        
    def get_surface(self):
        return self.textSurface

class Menu():
    def __init__(self, name, items, center=None, fontSize=36, fontSpace=4):
        self.name = name
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.background = background
        self.active=False
        font = pygame.font.Font(None, fontSize)
        menuHeight = (fontSize+fontSpace)*len(items)
        startY = self.background.get_height()/2 - menuHeight/2
        self.items = list()
        for item in items:
            centerX = self.background.get_width()/2
            centerY = startY + fontSize + fontSpace
            newItem = MenuItem(item, (centerX, centerY), color=(0,0,0), fontSize=fontSize)
            self.items.append(newItem)
            startY = startY + fontSize + fontSpace

    def drawMenu(self):
        self.active = True
        screen = pygame.display.get_surface()
        for item in self.items:
            screen.blit(item.get_surface(), item.get_pos())

    def isActive(self):
        return self.active

    def activate(self,):
        self.active = True

    def deactivate(self):
        self.active = False

    def handleEvent(self, event, game):
        if event.type == MOUSEBUTTONDOWN and self.isActive():
            currentItem = 0
            eventX = event.pos[0]
            eventY = event.pos[1]
            for item in self.items:
                textPos = item.get_pos()
                if eventX > textPos.left and eventX < textPos.right and eventY > textPos.top and eventY < textPos.bottom:
                    game.handleButton(self, item)
            

mainMenu = Menu("Main", ("Start", "Quit"))
addGenesMenu = Menu("Genes", operons.keys(), fontSize=16, fontSpace=2)
game = Game()
game.menu = mainMenu

while True:
    screen.blit(background, (0,0))
    game.menu.drawMenu()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print event
            game.menu.handleEvent(event, game)
            print game.playerOps
