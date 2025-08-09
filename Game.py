#  Game class

import pygwidgets
from Deck import *
from Player import *
from Card import *
from Constants import *

class Game():

    def __init__(self, window, numberOfPlayers=1):
        self.window = window

        self.oShoe = BlackJackShoe(window)

        self.oPlayerList = []
        for playerIndex in range(numberOfPlayers):
            oPlayer = Player(window, PLAYER_LIST[playerIndex])
            self.oPlayerList.append(oPlayer)
        oDealer = Player(window, DEALER)
        self.oPlayerList.append(oDealer)

        self.currentPlayerIndex = 0

        self.oPlayerIndicator = pygwidgets.DisplayText(self.window, value='^', textColor=BLACK, fontSize=SCORE_FONT_SIZE)
        self.updateIndicator()

        self.printGameState()

    def reset(self):  # this method is called when a new shoe starts
        pass

    def startRound(self):
        for i in range(2):
            for oPlayer in self.oPlayerList:
                oCard = self.oShoe.getCard()
                oPlayer.dealCard(oCard)
        self.printGameState()

    def dealOneCard(self):
        cardToDeal = self.oShoe.getCard()
        self.oPlayerList[self.currentPlayerIndex].dealCard(cardToDeal)

    def nextPlayer(self):
        if self.currentPlayerIndex == len(self.oPlayerList):
            self.currentPlayerIndex = 0
        else:
            self.currentPlayerIndex += 1
        self.updateIndicator()

    def updateIndicator(self):
        indicatorX = self.oPlayerList[self.currentPlayerIndex].loc[0] + CARD_WIDTH/2
        indicatorY = self.oPlayerList[self.currentPlayerIndex].loc[1] + CARD_HEIGHT + SCORE_FONT_SIZE/1.5
        self.oPlayerIndicator.setLoc((indicatorX, indicatorY))

    def getCardNameAndValue(self, index):
        pass

    def showCard(self, index):
        pass

    def draw(self):
        for oPlayer in self.oPlayerList:
            oPlayer.draw()
        self.oPlayerIndicator.draw()

    def printGameState(self):
        # Debug
        for oPlayer in self.oPlayerList:
            print(oPlayer)
        print(self.oShoe)