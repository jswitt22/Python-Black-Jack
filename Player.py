# Player class

from Card import *
from Constants import *

class Player:
    DEALER_CARDS_TOP = 100
    CARDS_TOP = 300

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

    def __str__(self):
        string = f"""{self.player} info:
 Location: {str(self.loc)}
 Score: {str(self.score)} 
 Money: ${str(self.money)}
"""
        return string

if __name__ == '__main__':
    # Main code to test the Player class

    import pygame

    # Constants
    WINDOW_WIDTH = 100
    WINDOW_HEIGHT = 100

    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    oPlayerList = []
    for player in Player.PLAYER_LIST:
        oPlayer = Player(window, player)
        oPlayerList.append(oPlayer)

    for oPlayer in oPlayerList:
        print(oPlayer)