#  Game class

import pygwidgets
from Deck import *
from Card import *
from Constants import *

class Game():
    CARD_OFFSET_X = -30
    CARD_OFFSET_Y = -30
    DEALER_CARDS_TOP = 100
    CARDS_TOP = 300
    DEALER_LEFT = 460
    PLAYER_LEFT_LIST = [127, 293, 460, 627, 793, DEALER_LEFT]
    PLAYER_LIST = ['Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5', 'Dealer']

    def __init__(self, window, numberOfPlayers=1):
        pass

    def reset(self):  # this method is called when a new round starts
        pass

    def getCardNameAndValue(self, index):
        pass

    def showCard(self, index):
        pass

    def draw(self):
        pass