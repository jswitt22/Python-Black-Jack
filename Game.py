#  Game class

import pygwidgets
from Deck import *
from Player import *
from Card import *
from Constants import *

class Game():
    BETTING = 'Betting'
    DEALING = 'Dealing'
    IS_ANYONE_HOME = 'Insurance?' # TODO - Implement special gameState phase if the dealer has an Ace or Face Card
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
        self.gameState = ''
        self.numberOfPlayers = numberOfPlayers
        self.dealerIndex = len(self.oPlayerList) - 1
        self.dealerRevealed = False

        # Game text/images
        self.oPlayerIndicator = pygwidgets.DisplayText(self.window, value='^', textColor=BLACK, fontSize=SCORE_FONT_SIZE)
        self.updateIndicator()
        self.oGameStateText = pygwidgets.DisplayText(self.window,value=self.gameState, textColor=BLACK, fontSize=SCORE_FONT_SIZE)

        self.setGameState(Game.BETTING)

        self.printGameState()

    def reset(self):  # this method is called when a new shoe starts
        pass

    def startRound(self):
        self.setGameState(Game.DEALING)

    def dealOneCard(self):
        cardToDeal = self.oShoe.getCard()
        oCurrentPlayer = self.oPlayerList[self.currentPlayerIndex]
        oCurrentPlayer.dealCard(cardToDeal)
        currentPlayerScore = oCurrentPlayer.getScore()
        dealer = oCurrentPlayer.player == DEALER
        if self.gameState == Game.DEALING:
            if not dealer and currentPlayerScore == 21:
                oCurrentPlayer.giveBlackJack()
            self.nextPlayer()
        else:
            if not dealer and currentPlayerScore >= 21:
                self.nextPlayer()

    def nextPlayer(self):
        oCurrentPlayer = self.oPlayerList[self.currentPlayerIndex]
        if self.gameState == Game.DEALING:
            if self.currentPlayerIndex == self.dealerIndex:
                self.currentPlayerIndex = 0
                if oCurrentPlayer.getNumberOfCards() == 2:
                    self.setGameState(Game.PLAYING)
            else:
                self.currentPlayerIndex += 1
        else:
            if self.currentPlayerIndex == self.dealerIndex:
                self.currentPlayerIndex = 0
                self.setGameState(Game.ROUND_OVER)
            else:
                self.currentPlayerIndex += 1
                if self.currentPlayerIndex == self.dealerIndex:
                    self.setGameState(Game.REVEALING)
            self.updateIndicator()

    def revealDealer(self):
        oDealer = self.oPlayerList[self.numberOfPlayers]
        DealerScore = oDealer.getScore()
        if not self.dealerRevealed:
            oDealer.revealCards()
            self.dealerRevealed = True
        else:
            if DealerScore < 17:
                self.dealOneCard()
                DealerScore = oDealer.getScore()

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
        textX, textY, textWidth, textHeight = self.oGameStateText.getRect()
        centeredLoc = (WINDOW_CENTER_X - textWidth/2, textHeight/2)
        self.oGameStateText.setLoc(centeredLoc)

    def getGameState(self):
        return self.gameState

    def updateIndicator(self):
        oCurrentPlayer = self.oPlayerList[self.currentPlayerIndex]
        indicatorX = oCurrentPlayer.loc[0] + CARD_WIDTH/2 #TODO - card width constant should be gotten from the actual width of the card image
        indicatorY = oCurrentPlayer.loc[1] + CARD_HEIGHT + SCORE_FONT_SIZE/1.5 #TODO - card height constant should be gotten from the actual height of the card image
        self.oPlayerIndicator.setLoc((indicatorX, indicatorY))

    def checkBlackJack(self):
        oCurrentPlayer = self.oPlayerList[self.currentPlayerIndex]
        if oCurrentPlayer.blackJack and self.gameState == Game.PLAYING:
            self.nextPlayer()

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