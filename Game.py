#  Game class

import pygwidgets
from Deck import *
from Card import *
from Constants import *

class Game():
    PLAYER_OFFSET = 110
    CARD_OFFSET_X = -30
    CARD_OFFSET_Y = -30
    DEALER_CARDS_TOP = 100
    CARDS_TOP = 300
    DEALER_LEFT = 460
    PLAYER_LEFT_LIST = [127, 293, 460, 627, 793, DEALER_LEFT]
    PLAYER_LIST = ['Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5', 'Dealer']
    NCARDS = 2
    POINTS_CORRECT = 15
    POINTS_INCORRECT = 10
    WHITE = (255, 255, 255)

    def __init__(self, window, numberOfPlayers=5):
        self.window = window
        self.oDeck = Deck(self.window)
        self.score = 100
        self.playerList = []
        for i in range(numberOfPlayers):
            self.playerList.append(Game.PLAYER_LIST[i])
        self.playerList.append('Dealer')
        self.cardsToDeal = (numberOfPlayers + 1)*Game.NCARDS
        self.scoreText = pygwidgets.DisplayText(window, (450, 164),
                                   'Score: ' + str(self.score),
                                    fontSize=36, textColor=Game.WHITE,
                                    justified='right')

        self.messageText = pygwidgets.DisplayText(window, (50, 460),
                                    '', width=900, justified='center',
                                    fontSize=36, textColor=Game.WHITE)

        self.loserSound = pygame.mixer.Sound("sounds/loser.wav")
        self.winnerSound = pygame.mixer.Sound("sounds/ding.wav")
        self.cardShuffleSound = pygame.mixer.Sound("sounds/cardShuffle.wav")

        self.cardPositionsList = []
        # Calculate the x and y positions of all cards, once
        for cardRound in range(1, Game.NCARDS + 1):
            for player in self.playerList:
                if player == 'Dealer':
                    thisTop = Game.DEALER_CARDS_TOP
                else:
                    thisTop = Game.CARDS_TOP + Game.CARD_OFFSET_Y*(cardRound - 1)
                thisLeft = Game.PLAYER_LEFT_LIST[Game.PLAYER_LIST.index(player)] + Game.CARD_OFFSET_X*(cardRound - 1)
                self.cardPositionsList.append((thisLeft, thisTop))

        self.reset()  # start a round of the game

    def reset(self):  # this method is called when a new round starts
        self.cardShuffleSound.play()
        self.cardList = []
        self.oDeck.shuffle()
        for cardIndex in range(self.cardsToDeal):  # deal out cards
            oCard = self.oDeck.getCard()
            self.cardList.append(oCard)
            thisPosition = self.cardPositionsList[cardIndex]
            oCard.setLoc((thisPosition[0], thisPosition[1]))

        for cardIndex in range(self.cardsToDeal):
            self.showCard(cardIndex)
        self.cardNumber = 0
        self.currentCardName, self.currentCardValue = \
                                         self.getCardNameAndValue(self.cardNumber)

        self.messageText.setValue('Starting card is ' + self.currentCardName +
                                                '. Will the next card be higher or lower?')

    def getCardNameAndValue(self, index):
        oCard = self.cardList[index]
        theName = oCard.getName()
        theValue = oCard.getValue()
        return theName, theValue

    def showCard(self, index):
        oCard = self.cardList[index]
        oCard.reveal()

    def hitHigherOrLower(self, higherOrLower):
        self.cardNumber = self.cardNumber + 1
        self.showCard(self.cardNumber)
        nextCardName, nextCardValue = self.getCardNameAndValue(self.cardNumber)

        if higherOrLower == HIGHER:
            if nextCardValue > self.currentCardValue:
                self.score = self.score + Game.POINTS_CORRECT
                self.messageText.setValue('Yes, the ' + nextCardName + ' was higher')
                self.winnerSound.play()
            else:
                self.score = self.score - Game.POINTS_INCORRECT
                self.messageText.setValue('No, the ' + nextCardName + ' was not higher')
                self.loserSound.play()

        else:  # user hit the Lower button
            if nextCardValue < self.currentCardValue:
                self.score = self.score + Game.POINTS_CORRECT
                self.messageText.setValue('Yes, the ' + nextCardName + ' was lower')
                self.winnerSound.play()
            else:
                self.score = self.score - Game.POINTS_INCORRECT
                self.messageText.setValue('No, the ' + nextCardName + ' was not lower')
                self.loserSound.play()

        self.scoreText.setValue('Score: ' + str(self.score))

        self.currentCardValue = nextCardValue  # set up for the next card 

        done = (self.cardNumber == (self.cardsToDeal - 1))  # did we reach the last card?
        return done

    def draw(self):
        # Tell each card to draw itself
        for oCard in self.cardList:
            oCard.draw()

        self.scoreText.draw()
        self.messageText.draw()