import pygame

# Constants

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TEXT_COLOR = WHITE

PLAYER1 = 'Player 1'
PLAYER2 = 'Player 2'
PLAYER3 = 'Player 3'
PLAYER4 = 'Player 4'
PLAYER5 = 'Player 5'
DEALER = 'Dealer'

# Window
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
WINDOW_CENTER_X = WINDOW_WIDTH / 2
WINDOW_CENTER_Y = WINDOW_HEIGHT / 2
MARGIN = 20

# Card spacing
BACK_OF_CARD_IMAGE = pygame.image.load('images/BackOfCard.png')
CARD_WIDTH = BACK_OF_CARD_IMAGE.get_width()
CARD_HEIGHT = BACK_OF_CARD_IMAGE.get_height()
PLAYER_CARD_OFFSET_X = 15
CARD_OFFSET_X = 30
CARD_OFFSET_Y = -30

# Button spacing
BET_BUTTON_WIDTH = 30

# Player locations
DEALER_LEFT = WINDOW_CENTER_X - CARD_WIDTH/2
PLAYER_LEFT_LIST = [1*WINDOW_WIDTH/6 - CARD_WIDTH/2,
                    2*WINDOW_WIDTH/6 - CARD_WIDTH/2,
                    3*WINDOW_WIDTH/6 - CARD_WIDTH/2,
                    4*WINDOW_WIDTH/6 - CARD_WIDTH/2,
                    5*WINDOW_WIDTH/6 - CARD_WIDTH/2,
                    DEALER_LEFT]
PLAYER_LIST = [PLAYER1, PLAYER2, PLAYER3, PLAYER4, PLAYER5, DEALER]

# Cheater Cards (for debugging)
PLAYER_CHEATS = {PLAYER1: False, PLAYER2: False, PLAYER3: False, PLAYER4: False, PLAYER5: False, DEALER: False}
CHEATER_CARD_1 = {'Rank': 'Jack', 'Suit': 'Spades', 'Value': 10}
CHEATER_CARD_2 = {'Rank': 'Ace', 'Suit': 'Spades', 'Value': 1}

# Fonts
SCORE_FONT_SIZE = 30