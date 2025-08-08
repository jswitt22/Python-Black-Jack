# Black Jack - Python Version
# Main Program

# 1 - Import packages
import pygame
from pygame.locals import *
import sys
import pygwidgets
from Game import *
from Constants import *

# 2 - Define constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
FRAMES_PER_SECOND = 30

# 3 - Initialize the world
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 4 - Load assets: image(s), sounds,  etc.
background = pygwidgets.Image(window, (0, 0),
                            'images/background.png')
newGameButton = pygwidgets.TextButton(window, (20, 530),
                            'New Game', width=100, height=45)
higherButton = pygwidgets.TextButton(window, (540, 520),
                            'Higher', width=120, height=55)
higherButton.disable()
lowerButton = pygwidgets.TextButton(window, (340, 520),
                            'Lower', width=120, height=55)
lowerButton.disable()
quitButton = pygwidgets.TextButton(window, (880, 530),
                            'Quit', width=100, height=45)

# 5 - Initialize variables
oGame = Game(window, numberOfPlayers=1)

# 6 - Loop forever
while True:

    # 7 - Check for and handle events
    for event in pygame.event.get():
        if ((event.type == QUIT) or
            ((event.type == KEYDOWN) and (event.key == K_ESCAPE)) or
            (quitButton.handleEvent(event))):
            pygame.quit()
            sys.exit()

        if newGameButton.handleEvent(event):
            print('clicked new game')
            lowerButton.enable()
            higherButton.enable()

        if higherButton.handleEvent(event):
            print('clicked higher')

        if lowerButton.handleEvent(event):
            print('clicked lower')

    # 8 - Do any "per frame" actions

    # 9 - Clear the window before drawing it again
    background.draw()

    # 10 - Draw the window elements
    # Tell the game to draw itself
    oGame.draw()
    # Draw remaining user interface components
    newGameButton.draw()
    higherButton.draw()
    lowerButton.draw()
    quitButton.draw()

    # 11 - Update the window
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)