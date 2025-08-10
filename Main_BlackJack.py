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
STANDARD_BUTTON_WIDTH = 120
STANDARD_BUTTON_HEIGHT = 60
DEAL_BUTTON_WIDTH = STANDARD_BUTTON_WIDTH
HIT_BUTTON_WIDTH = STANDARD_BUTTON_WIDTH
BOTTOM_BUTTON_Y = WINDOW_HEIGHT - STANDARD_BUTTON_HEIGHT - MARGIN
TOP_BUTTON_Y = MARGIN
RIGHT_BUTTON_X = WINDOW_WIDTH - STANDARD_BUTTON_WIDTH - MARGIN
LEFT_BUTTON_X = MARGIN
FRAMES_PER_SECOND = 30

# 3 - Initialize the world
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 4 - Load assets: image(s), sounds,  etc.
background = pygwidgets.Image(window, (0, 0),
                            'images/background.png') # TODO - replace this image with a custom blackjack table background
readyButton = pygwidgets.TextButton(window, (MARGIN, BOTTOM_BUTTON_Y),
                            'Ready', width=STANDARD_BUTTON_WIDTH, height=STANDARD_BUTTON_HEIGHT)
hitButtonLeft = WINDOW_CENTER_X - HIT_BUTTON_WIDTH - MARGIN/2
hitButton = pygwidgets.TextButton(window, (hitButtonLeft, BOTTOM_BUTTON_Y),
                            'Hit', width=STANDARD_BUTTON_WIDTH, height=STANDARD_BUTTON_HEIGHT)
standButtonLeft = WINDOW_CENTER_X + MARGIN/2
standButton = pygwidgets.TextButton(window, (standButtonLeft, BOTTOM_BUTTON_Y),
                            'Stand', width=STANDARD_BUTTON_WIDTH, height=STANDARD_BUTTON_HEIGHT)
quitButton = pygwidgets.TextButton(window, (RIGHT_BUTTON_X, BOTTOM_BUTTON_Y),
                            'Quit', width=STANDARD_BUTTON_WIDTH, height=STANDARD_BUTTON_HEIGHT)
resetButton = pygwidgets.TextButton(window, (LEFT_BUTTON_X, TOP_BUTTON_Y),
                                    'Clear Cards', width=STANDARD_BUTTON_WIDTH, height=STANDARD_BUTTON_HEIGHT)
revealButton = pygwidgets.TextButton(window, (RIGHT_BUTTON_X, TOP_BUTTON_Y),
                                     'Reveal', width=STANDARD_BUTTON_WIDTH, height=STANDARD_BUTTON_HEIGHT)
revealButtonLeft, revealButtonTop, revealButtonWidth, revealButtonHeight = revealButton.getRect()
dealButtonLeft = revealButtonLeft - DEAL_BUTTON_WIDTH - MARGIN
dealButton = pygwidgets.TextButton(window, (dealButtonLeft, TOP_BUTTON_Y),
                                     'Deal', width=STANDARD_BUTTON_WIDTH, height=STANDARD_BUTTON_HEIGHT)

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

        if dealButton.handleEvent(event):
            print('clicked Deal')
            oGame.dealOneCard()

    # 8 - Do any "per frame" actions
    thisFrameGameState = oGame.getGameState()
    if thisFrameGameState != lastFrameGameState:
        if thisFrameGameState == Game.BETTING:
            standButton.disable()
            hitButton.disable()
            readyButton.enable()
            resetButton.disable()
            revealButton.disable()
            dealButton.disable()
        if thisFrameGameState == Game.DEALING:
            standButton.disable()
            hitButton.disable()
            readyButton.disable()
            resetButton.disable()
            revealButton.disable()
            dealButton.enable()
        if thisFrameGameState == Game.PLAYING:
            standButton.enable()
            hitButton.enable()
            readyButton.disable()
            resetButton.disable()
            revealButton.disable()
            dealButton.disable()
        if thisFrameGameState == Game.REVEALING:
            standButton.disable()
            hitButton.disable()
            readyButton.disable()
            resetButton.enable()
            revealButton.enable()
            dealButton.disable()
        if thisFrameGameState == Game.ROUND_OVER:
            standButton.disable()
            hitButton.disable()
            readyButton.disable()
            resetButton.enable()
            revealButton.disable()
            dealButton.disable()
    lastFrameGameState = oGame.getGameState()

    oGame.checkBlackJack()

    # 9 - Clear the window before drawing it again
    window.fill(BLACK) # TODO - replace this with background.draw() when we have a new image for the background

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
    dealButton.draw()

    # 11 - Update the window
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)