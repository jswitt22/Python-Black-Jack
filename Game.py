#  Game class

import pygwidgets
from Deck import *
from Player import *
from Card import *
from Constants import *

class Game():
    BETTING = 'Betting'
    DEALING = 'Dealing'
    PLAYING = 'Playing'
    REVEALING = 'Revealing'
    ROUND_OVER = 'Round Over'

    def __init__(self, window, numberOfPlayers=1):
        self.window = window

        # Game objects
        self.oShoe = BlackJackShoe(window)
        self.oPlayerList = []
        for playerIndex in range(numberOfPlayers):
            oPlayer = Player(window, PLAYER_LIST[playerIndex])
            self.oPlayerList.append(oPlayer)
        oDealer = Player(window, DEALER)
        self.oPlayerList.append(oDealer)

        # Game variables
        self.currentPlayerIndex = 0
        self.gameState = Game.BETTING
        self.numberOfPlayers = numberOfPlayers
        self.dealerRevealed = False

        # Game text/images
        self.oPlayerIndicator = pygwidgets.DisplayText(self.window, value='^', textColor=BLACK, fontSize=SCORE_FONT_SIZE)
        self.updateIndicator()
        self.oGameStateText = pygwidgets.DisplayText(self.window, loc=(500, 300),value=self.gameState, textColor=BLACK, fontSize=SCORE_FONT_SIZE)

        self.printGameState()

    def reset(self):  # this method is called when a new shoe starts
        pass

    def startRound(self):
        self.setGameState(Game.DEALING)

    def dealOneCard(self):
        cardToDeal = self.oShoe.getCard()
        self.oPlayerList[self.currentPlayerIndex].dealCard(cardToDeal)
        if self.gameState == Game.DEALING:
            self.nextPlayer()
        else:
            currentPlayerScore = self.oPlayerList[self.currentPlayerIndex].getScore()
            if currentPlayerScore >= 21:
                self.nextPlayer()

    def nextPlayer(self):
        if self.gameState == Game.DEALING:
            if self.currentPlayerIndex == len(self.oPlayerList)-1:
                self.currentPlayerIndex = 0
                if self.oPlayerList[self.currentPlayerIndex].getNumberOfCards() == 2:
                    self.setGameState(Game.PLAYING)
            else:
                self.currentPlayerIndex += 1
        else:
            if self.currentPlayerIndex == len(self.oPlayerList)-1:
                self.currentPlayerIndex = 0
                self.setGameState(Game.ROUND_OVER)
            else:
                self.currentPlayerIndex += 1
                if self.currentPlayerIndex == len(self.oPlayerList)-1:
                    self.setGameState(Game.REVEALING)
            self.updateIndicator()

    def revealDealer(self):
        DealerScore = self.oPlayerList[self.numberOfPlayers].getScore()
        if not self.dealerRevealed:
            self.oPlayerList[self.numberOfPlayers].revealCards()
            self.dealerRevealed = True
        else:
            if DealerScore < 17:
                self.dealOneCard()
                DealerScore = self.oPlayerList[self.numberOfPlayers].getScore()

        if DealerScore >= 17:
            self.nextPlayer()

    def nextRound(self):
        for oPlayer in self.oPlayerList:
            oPlayer.deleteCards()
        self.setGameState(Game.BETTING)
        self.dealerRevealed = False

    def setGameState(self, gameState):
        self.gameState = gameState
        self.oGameStateText.setText(gameState)

    def getGameState(self):
        return self.gameState

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
        if self.gameState == Game.PLAYING:
            self.oPlayerIndicator.draw()
        self.oGameStateText.draw()

    def printGameState(self):
        # Debug
        for oPlayer in self.oPlayerList:
            print(oPlayer)
        print(self.oShoe)