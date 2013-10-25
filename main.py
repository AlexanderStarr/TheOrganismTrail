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

class Game():
    def __init__(self):
        self.toDraw = []
        self.playerOps = []
        self.org = Organism('', {}, {})
        self.eco = None
        self.time = 0
        self.play = False

    def handleButton(self, menu, button):
        if menu.name == 'Genes':
            self.playerOps.append(operons[button.text])
            self.toDraw[1] = Menu("PGenes", [op.name for op in self.playerOps], center=(background.get_width()/4, None), fontSize=20, fontSpace=1)
        elif menu.name == 'Main':
            if button.text == 'Quit':
                sys.exit()
            elif button.text == 'Start':
                menu.deactivate()
                self.toDraw = [addGenesMenu, playerGenesMenu, goButtonMenu, addGenesTitle]
        elif menu.name == 'PGenes':
            self.playerOps.remove(operons[button.text])
            self.toDraw[1] = Menu("PGenes", [op.name for op in self.playerOps], center=(background.get_width()/4, None), fontSize=20, fontSpace=1)
        elif menu.name == 'Go':
            self.playerOps = hiddenGenes + self.playerOps
            genome = Genome(self.playerOps)
            self.org = Organism('Player Organism', genome, copy.deepcopy(CELLR))
            env = Environment('Game Environment', 1, ENVR)
            self.eco = Ecosystem([self.org], env)
            self.toDraw = [playButtonMenu, pauseButtonMenu, timeMenu, countMenu, quitButtonMenu]
        elif menu.name == 'Play':
            self.play = True
        elif menu.name == 'Pause':
            self.play = False
        elif menu.name == 'Quit':
            sys.exit()


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

    def draw(self, screen):
        screen.blit(self.get_surface(), self.get_pos())

    def handleEvent(self, event, game):
        self.text = self.text

class Menu():
    def __init__(self, name, items, center=(None, None), fontSize=36, fontSpace=4):
        self.name = name
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.background = background
        self.active=False
        font = pygame.font.Font(None, fontSize)
        menuHeight = (fontSize+fontSpace)*len(items)
        if center[0]:
            centerX = center[0]
        else:
            centerX = self.background.get_width()/2
        if center[1]:
            startY = center[1]
        else:
            startY = self.background.get_height()/2 - menuHeight/2
            
        self.items = list()
        for item in items:
            centerY = startY + fontSize + fontSpace
            newItem = MenuItem(item, (centerX, centerY), fontSize=fontSize)
            self.items.append(newItem)
            startY = startY + fontSize + fontSpace

    def draw(self, screen):
        self.active = True
        for item in self.items:
            item.draw(screen)

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
            
game = Game()
mainMenu = Menu("Main", ("Start", "Quit"))
addGenesList = [op.name for op in displayedGenes]
addGenesMenu = Menu("Genes", addGenesList, center=(background.get_width()*3/4, None), fontSize=20, fontSpace=1)
playerGenesMenu = Menu("PGenes", [op.name for op in game.playerOps], center=(background.get_width()/4, None), fontSize=20, fontSpace=1)
goButtonMenu = Menu("Go", ('Go!',), center=(background.get_width()/2, background.get_height()*8/10))
addGenesTitle = MenuItem("Click operons on right to add, click operons on left to remove", (background.get_width()/2, background.get_height()/10))
playButtonMenu = Menu("Play", ('Play',), center=(background.get_width()/2, background.get_height()/16))
pauseButtonMenu = Menu("Pause", ('Pause',), center=(background.get_width()*1/4, background.get_height()/16))
quitButtonMenu= Menu("Quit", ('Quit',), center=(background.get_width()*3/4, background.get_height()/16))
timeMenu = Menu('Time', ('Time (minutes):', str(game.time)), center=(background.get_width()*1/4, background.get_height()*8/10))
countMenu = Menu('Cells', ('Number of Cells:', str(game.org.count)), center=(background.get_width()*3/4, background.get_height()*8/10))
game.toDraw = [mainMenu]

while True:
    clock.tick(FPS)
    screen.blit(background, (0,0))
    for i in game.toDraw:
        i.draw(screen)
    pygame.display.flip()
    if game.play:
        game.eco.cycle()
        game.time = game.time + 1
        game.count = int(game.eco.orgs[0].count)
        # If it hasn't grown for 5 minutes, then stop
        if len(game.eco.tracker[game.eco.orgs[0]]) > 10 and game.eco.tracker[game.eco.orgs[0]][-10] == game.eco.tracker[game.eco.orgs[0]][-1]:
            limitedBy = game.eco.orgs[0].limitedBy()
            game.play = False
            if limitedBy:
                gameOverMenu = Menu("GameOver", ("Game Over", "Your organism stopped growing due to", limitedBy))
            else:
                gameOverMenu = Menu("GameOver", ('Game Over', "Your organism stopped growing"))
            game.toDraw.append(gameOverMenu)
            pygame.display.flip()
        if game.time > 180:
            game.play = False
            gameOverMenu = Menu("GameOver", ("Time's Up!", ))
        game.toDraw[2] = Menu('Time', ('Time (minutes):', str(game.time)), center=(background.get_width()*1/4, background.get_height()*8/10))
        game.toDraw[3] = Menu('Cells', ('Number of Cells:', str(game.count)), center=(background.get_width()*3/4, background.get_height()*8/10))
        pygame.time.wait(125)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print event
            for m in game.toDraw:
                if m.handleEvent:
                    m.handleEvent(event, game)
