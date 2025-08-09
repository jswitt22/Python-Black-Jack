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
readyButton = pygwidgets.TextButton(window, (20, 530),
                            'Ready', width=100, height=45)
hitButton = pygwidgets.TextButton(window, (340, 520),
                            'Hit', width=120, height=55)
standButton = pygwidgets.TextButton(window, (540, 520),
                            'Stand', width=120, height=55)
quitButton = pygwidgets.TextButton(window, (880, 530),
                            'Quit', width=100, height=45)
resetButton = pygwidgets.TextButton(window, (20, 20),
                                    'Clear Cards', width=120, height=55)
revealButton = pygwidgets.TextButton(window, (860, 20),
                                     'Reveal', width=120, height=55)

# 5 - Initialize variables
oGame = Game(window, numberOfPlayers=2)
lastFrameGameState = ''

# 6 - Loop forever
while True:

    # 7 - Check for and handle events
    for event in pygame.event.get():
        if ((event.type == QUIT) or
            ((event.type == KEYDOWN) and (event.key == K_ESCAPE)) or
            (quitButton.handleEvent(event))):
            pygame.quit()
            sys.exit()

        if readyButton.handleEvent(event):
            print('clicked Ready')
            standButton.enable()
            hitButton.enable()
            readyButton.disable()
            oGame.startRound()

        if hitButton.handleEvent(event):
            print('clicked Hit')
            oGame.dealOneCard()

        if standButton.handleEvent(event):
            print('clicked Stand')
            oGame.nextPlayer()

        if resetButton.handleEvent(event):
            print('clicked Reset')
            oGame.nextRound()

        if revealButton.handleEvent(event):
            print('clicked Reveal')
            oGame.revealDealer()

    # 8 - Do any "per frame" actions
    thisFrameGameState = oGame.getGameState()
    if thisFrameGameState != lastFrameGameState:
        if thisFrameGameState == Game.BETTING:
            standButton.disable()
            hitButton.disable()
            readyButton.enable()
            resetButton.disable()
            revealButton.disable()
        if thisFrameGameState == Game.DEALING:
            standButton.disable()
            hitButton.disable()
            readyButton.disable()
            resetButton.disable()
            revealButton.disable()
        if thisFrameGameState == Game.PLAYING:
            standButton.enable()
            hitButton.enable()
            readyButton.disable()
            resetButton.disable()
            revealButton.disable()
        if thisFrameGameState == Game.ROUND_OVER:
            standButton.disable()
            hitButton.disable()
            readyButton.disable()
            resetButton.enable()
            revealButton.disable()
        if thisFrameGameState == Game.REVEALING:
            standButton.disable()
            hitButton.disable()
            readyButton.disable()
            resetButton.enable()
            revealButton.enable()
    lastFrameGameState = oGame.getGameState()

    # 9 - Clear the window before drawing it again
    background.draw()

    # 10 - Draw the window elements
    # Tell the game to draw itself
    oGame.draw()
    # Draw remaining user interface components
    readyButton.draw()
    hitButton.draw()
    standButton.draw()
    quitButton.draw()
    resetButton.draw()
    revealButton.draw()

    # 11 - Update the window
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)