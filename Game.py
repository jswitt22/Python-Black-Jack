#  Game class

import pygwidgets
from Deck import *
from Player import *
from Card import *
from Constants import *

class Game():
    CARD_OFFSET_X = -30
    CARD_OFFSET_Y = -30

    def __init__(self, window, numberOfPlayers=1):
        self.oShoe = BlackJackShoe(window)

        self.playerList = []
        for playerIndex in range(numberOfPlayers):
            oPlayer = Player(window, PLAYER_LIST[playerIndex])
            self.playerList.append(oPlayer)
        oDealer = Player(window, DEALER)
        self.playerList.append(oDealer)

        self.printGameState()

        self.startRound()
        self.printGameState()

    def reset(self):  # this method is called when a new shoe starts
        pass

    def startRound(self):
        for i in range(2):
            for player in self.playerList:
                oCard = self.oShoe.getCard()
                player.dealCard(oCard)

    def getCardNameAndValue(self, index):
        pass

    def showCard(self, index):
        pass

    def draw(self):
        pass

    def printGameState(self):
        # Debug
        for player in self.playerList:
            print(player)
        print(self.oShoe)