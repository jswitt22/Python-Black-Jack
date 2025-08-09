# Player class

from pygwidgets import *
from Card import *
from Constants import *

class Player:
    DEALER_CARDS_TOP = 50
    CARDS_TOP = 350

    def __init__(self, window, player, money=500):
        self.window = window
        self.player = player


        if self.player == DEALER:
            top = Player.DEALER_CARDS_TOP
        else:
            top = Player.CARDS_TOP
        left = PLAYER_LEFT_LIST[PLAYER_LIST.index(self.player)]
        self.loc = (left, top)

        self.score = 0
        self.money = money

        self.oScoreText = pygwidgets.DisplayText(self.window, (self.loc[0]+40, self.loc[1]+120), str(self.score), textColor=BLACK, justified='center')

        self.cards = []

    def __str__(self):
        cardStringList = []
        for card in self.cards:
            cardStringList.append(str(card))
        cardString = ', '.join(cardStringList)

        string = f"""{self.player} info:
 Location: {str(self.loc)}
 Cards: {cardString}
 Score: {str(self.score)} 
 Money: ${str(self.money)}
"""
        return string

    def dealCard(self, oCard):
        numberOfCards = len(self.cards)
        if self.player != DEALER:
            oCard.reveal()
            cardLocation = (self.loc[0] + CARD_OFFSET_X*numberOfCards, self.loc[1] + CARD_OFFSET_Y*numberOfCards)
        else:
            if numberOfCards > 0:
                oCard.reveal()
            cardLocation = (self.loc[0] + CARD_OFFSET_X * numberOfCards, self.loc[1])
        oCard.setLoc(cardLocation)
        self.cards.append(oCard)
        self.score += oCard.getValue()
        self.oScoreText.setText(str(self.score))

    def draw(self):
        for card in self.cards:
            card.draw()
        self.oScoreText.draw()

if __name__ == '__main__':
    # Main code to test the Player class

    import pygame

    # Constants
    WINDOW_WIDTH = 100
    WINDOW_HEIGHT = 100

    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    oPlayerList = []
    for player in PLAYER_LIST:
        oPlayer = Player(window, player)
        oPlayerList.append(oPlayer)

    for oPlayer in oPlayerList:
        print(oPlayer)