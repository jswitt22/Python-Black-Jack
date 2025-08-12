# Black Jack - Python Version
# Main Program

# 1 - Import packages
import pygame
from pygame.locals import *
import sys
import pygwidgets
from Game import *
from Constants import *

def disableButtons(buttonList):
    for TextButton in buttonList:
        TextButton.disable()

def enableButtons(buttonList):
    for TextButton in buttonList:
        TextButton.enable()

def drawList(list):
    for object in list:
        object.draw()

def main():
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
    # Images
    background = pygwidgets.Image(window, (0, 0),
                                'images/background.png') # TODO - replace this image with a custom blackjack table background
    # Buttons
    buttonList = []
    readyButton = pygwidgets.TextButton(window, (MARGIN, BOTTOM_BUTTON_Y),
                                'Ready', width=STANDARD_BUTTON_WIDTH, height=STANDARD_BUTTON_HEIGHT)
    buttonList.append(readyButton)
    hitButtonLeft = WINDOW_CENTER_X - HIT_BUTTON_WIDTH - MARGIN/2
    hitButton = pygwidgets.TextButton(window, (hitButtonLeft, BOTTOM_BUTTON_Y),
                                'Hit', width=STANDARD_BUTTON_WIDTH, height=STANDARD_BUTTON_HEIGHT)
    buttonList.append(hitButton)
    standButtonLeft = WINDOW_CENTER_X + MARGIN/2
    standButton = pygwidgets.TextButton(window, (standButtonLeft, BOTTOM_BUTTON_Y),
                                'Stand', width=STANDARD_BUTTON_WIDTH, height=STANDARD_BUTTON_HEIGHT)
    buttonList.append(standButton)
    quitButton = pygwidgets.TextButton(window, (RIGHT_BUTTON_X, BOTTOM_BUTTON_Y),
                                'Quit', width=STANDARD_BUTTON_WIDTH, height=STANDARD_BUTTON_HEIGHT)
    buttonList.append(quitButton)
    resetButton = pygwidgets.TextButton(window, (LEFT_BUTTON_X, TOP_BUTTON_Y),
                                        'Clear Cards', width=STANDARD_BUTTON_WIDTH, height=STANDARD_BUTTON_HEIGHT)
    buttonList.append(resetButton)
    revealButton = pygwidgets.TextButton(window, (RIGHT_BUTTON_X, TOP_BUTTON_Y),
                                         'Reveal', width=STANDARD_BUTTON_WIDTH, height=STANDARD_BUTTON_HEIGHT)
    buttonList.append(revealButton)
    revealButtonLeft, revealButtonTop, revealButtonWidth, revealButtonHeight = revealButton.getRect()
    dealButtonLeft = revealButtonLeft - DEAL_BUTTON_WIDTH - MARGIN
    dealButton = pygwidgets.TextButton(window, (dealButtonLeft, TOP_BUTTON_Y),
                                         'Deal', width=STANDARD_BUTTON_WIDTH, height=STANDARD_BUTTON_HEIGHT)
    buttonList.append(dealButton)
    checkDealerButton = pygwidgets.TextButton(window, (WINDOW_CENTER_X - STANDARD_BUTTON_WIDTH/2, TOP_BUTTON_Y),
                                         'Is Anyone Home?', width=STANDARD_BUTTON_WIDTH, height=STANDARD_BUTTON_HEIGHT) # TODO - put this button in a better place
    checkDealerButton.disable()
    checkDealerButton.hide()
    buttonList.append(checkDealerButton)

    # 5 - Initialize variables
    oGame = Game(window, numberOfPlayers=5)
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

            if event.type == MOUSEBUTTONDOWN or MOUSEMOTION:
                oGame.handleEvent(event)

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

            if checkDealerButton.handleEvent(event):
                print('clicked CheckDealer')
                oGame.checkDealer()
                checkDealerButton.disable()
                checkDealerButton.hide()

        # 8 - Do any "per frame" actions
        thisFrameGameState = oGame.getGameState()
        if thisFrameGameState != lastFrameGameState:
            if thisFrameGameState == Game.BETTING:
                disableButtons([standButton, hitButton, resetButton, revealButton, dealButton])
                enableButtons([readyButton])
            if thisFrameGameState == Game.DEALING:
                disableButtons([standButton, hitButton, readyButton, resetButton, revealButton])
                enableButtons([dealButton])
            if thisFrameGameState == Game.IS_ANYONE_HOME:
                disableButtons([standButton, hitButton, readyButton, resetButton, revealButton, dealButton])
                enableButtons([checkDealerButton])
                checkDealerButton.show()
            if thisFrameGameState == Game.PLAYING:
                disableButtons([readyButton, resetButton, revealButton, dealButton])
                enableButtons([standButton, hitButton])
            if thisFrameGameState == Game.REVEALING:
                disableButtons([standButton, hitButton, readyButton, resetButton, dealButton])
                enableButtons([revealButton])
            if thisFrameGameState == Game.ROUND_OVER:
                disableButtons([standButton, hitButton, readyButton, revealButton, dealButton])
                enableButtons([resetButton, hitButton])
        lastFrameGameState = oGame.getGameState()

        oGame.checkForSkipPlayer()

        # 9 - Clear the window before drawing it again
        window.fill(BLACK) # TODO - replace this with background.draw() when we have a new image for the background

        # 10 - Draw the window elements
        # Tell the game to draw itself
        oGame.draw()
        # Draw remaining user interface components
        drawList(buttonList)

        # 11 - Update the window
        pygame.display.update()

        # 12 - Slow things down a bit
        clock.tick(FRAMES_PER_SECOND)

if __name__ == '__main__':
    main()