import pygame, random, sys, os
from pygame.locals import *
from defs.defaults import *

# Initialize
pygame.init()
pygame.display.set_caption('The Organism Trail')
screen = pygame.display.set_mode((800,600))
FPS = 30
clock = pygame.time.Clock()
IMG_DIR = os.path.join('data', 'img')

# Prepare the splash and background images for Pygame.
splash = pygame.image.load(os.path.join(IMG_DIR, 'splash.png'))
splash = splash.convert()
background = pygame.image.load(os.path.join(IMG_DIR, 'background.png'))
background = background.convert()

# The main code is something of a mess currently.  This file handles all of
# the game's GUI, menu logic, etc.  All the cellular simulation occurs in
# the files in the folder 'defs'.

# Essentially, there is a Game class to keep track of where in the game you are.
# The Menu and MenuItem classes are simply used to display text and
# filter out mouse clicks to pass along to the Game class for processing.

class Game():
    def __init__(self):
        self.toDraw = []
        self.playerOps = []
        self.org = Organism('', {}, {})
        self.eco = None
        self.time = 0
        self.play = False

    # If a menu has a button clicked, then it passes that information here.
    # From here we can redraw stuff, pause simulation, etc.
    def handleButton(self, menu, button):
        # If the button is in the genes menu, then add the gene to playerOps
        # and update the player genes menue to be drawn.
        if menu.name == 'Genes':
            self.playerOps.append(operons[button.text])
            self.toDraw[1] = Menu("PGenes", [op.name for op in self.playerOps], center=(background.get_width()/4, None), fontSize=20, fontSpace=1)
        
        # If in the main menu, either quit or load the next menu.
        elif menu.name == 'Main':
            if button.text == 'Quit':
                sys.exit()
            elif button.text == 'Start':
                menu.deactivate()
                self.toDraw = [addGenesMenu, playerGenesMenu, goButtonMenu, addGenesTitle]
        
        # Clicking on a button in the player genes menu removes the operon
        # from the list, and updates that list for when it is redrawn.
        elif menu.name == 'PGenes':
            self.playerOps.remove(operons[button.text])
            self.toDraw[1] = Menu("PGenes", [op.name for op in self.playerOps], center=(background.get_width()/4, None), fontSize=20, fontSpace=1)
        
        # If the player clicks Go, then we need to create their organism,
        # initialize an environment and ecosystem, then load the menus for
        # the growth screen.
        elif menu.name == 'Go':
            self.playerOps = hiddenGenes + self.playerOps
            genome = Genome(self.playerOps)
            self.org = Organism('Player Organism', genome, copy.deepcopy(CELLR))
            env = Environment('Game Environment', 1, ENVR)
            self.eco = Ecosystem([self.org], env)
            self.toDraw = [playButtonMenu, pauseButtonMenu, timeMenu, countMenu, quitButtonMenu]
        
        # These should be self explanatory.
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

# Initialize a game.
game = Game()

# Draw the splash screen and title text.  Then wait 3 seconds and move on.
screen.blit(splash, (0,0))
splashMenu = Menu("Splash", ("The Organism Trail",), fontSize=80)
splashMenu.draw(screen)
pygame.display.flip()
pygame.time.wait(3000)
screen.blit(background, (0,0))

# Define all of the menus and items we will need to use.
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

# Queue the main menu to be drawn.
game.toDraw = [mainMenu]

# This is the main game loop.
while True:
    # Limits the FPS of the game.
    clock.tick(FPS)

    # Load a blank background.
    screen.blit(background, (0,0))

    # Draw everything in the game's drawing queue.
    for i in game.toDraw:
        i.draw(screen)

    # Update the display.
    pygame.display.flip()

    # game.play determines whether or not to execute the cellular simulation logic.
    if game.play:
        # Run an ecosystem cycle, then update the time and count.
        game.eco.cycle()
        game.time = game.time + 1
        game.count = int(game.eco.orgs[0].count)

        # If it hasn't grown at all since 10 minutes, then stop.
        if len(game.eco.tracker[game.eco.orgs[0]]) > 10 and game.eco.tracker[game.eco.orgs[0]][-10] == game.eco.tracker[game.eco.orgs[0]][-1]:
            limitedBy = game.eco.orgs[0].limitedBy()
            game.play = False

            # If we know why they stopped growing, then tell the player.
            if limitedBy:
                gameOverMenu = Menu("GameOver", ("Game Over", "Your organism stopped growing due to:", limitedBy))
            else:
                gameOverMenu = Menu("GameOver", ('Game Over', "Your organism stopped growing"))
            game.toDraw.append(gameOverMenu)
            pygame.display.flip()

        # Also stop after 3 game hours.
        if game.time >= 180:
            game.play = False
            gameOverMenu = Menu("GameOver", ("Time's Up!", ))
            game.toDraw.append(gameOverMenu)
            pygame.display.flip()

        # Update the drawing queue with the new time and cell count.
        game.toDraw[2] = Menu('Time', ('Time (minutes):', str(game.time)), center=(background.get_width()*1/4, background.get_height()*8/10))
        game.toDraw[3] = Menu('Cells', ('Number of Cells:', str(game.count)), center=(background.get_width()*3/4, background.get_height()*8/10))

        # Limits the rate at which the ecosystem cycles.  Can decrease or remove this to run faster.
        pygame.time.wait(125)

    # Handle all the Pygame events.
    for event in pygame.event.get():
        # Exit the program if the window is closed or escape is hit.
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

        # If they click the mouse, then pass the event to every menu
        # currently being drawn so they can process it if necessary.
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #print event  # Used for debugging.
            for m in game.toDraw:
                if m.handleEvent:
                    m.handleEvent(event, game)
