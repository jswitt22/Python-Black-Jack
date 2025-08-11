from pygwidgets import *
from Card import *
from Constants import *

# Player class
class Player:
    DEALER_CARDS_TOP = 100
    CARDS_TOP = WINDOW_HEIGHT - CARD_HEIGHT*3

    def __init__(self, window, player, money=500):
        self.window = window
        self.player = player

        if self.player == DEALER:
            top = Player.DEALER_CARDS_TOP
            self.revealed = False
        else:
            top = Player.CARDS_TOP
            self.revealed = True
        left = PLAYER_LEFT_LIST[PLAYER_LIST.index(self.player)]
        self.loc = (left, top)

        self.score = 0
        self.money = money
        self.bet = 0
        self.blackJack = False

        self.textCenterX = self.loc[0] + CARD_WIDTH/2
        self.scoreTextY = self.loc[1] + CARD_HEIGHT + 10
        self.oScoreText = pygwidgets.DisplayText(self.window, (self.textCenterX, self.scoreTextY), str(self.score), textColor=TEXT_COLOR, fontSize=SCORE_FONT_SIZE)
        scoreTextHeight = self.oScoreText.getRect()[3]
        self.moneyTextY = self.scoreTextY + (scoreTextHeight*1.5)*2
        self.oMoneyText = pygwidgets.DisplayText(self.window, (self.textCenterX, self.moneyTextY), f'Money: {self.money}', textColor=TEXT_COLOR, fontSize=SCORE_FONT_SIZE)
        self.betTextY = WINDOW_CENTER_Y - scoreTextHeight/2
        self.oBetText = pygwidgets.DisplayText(self.window, (self.textCenterX, self.betTextY), f'Bet: {self.bet}', textColor=TEXT_COLOR, fontSize=SCORE_FONT_SIZE)

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

    def increaseBet(self, amount):
        validBet = self.money >= amount and self.bet >= -1*amount
        if not validBet:
            return
        self.bet += amount
        self.oBetText.setText(f'Bet: {self.bet}')
        self.money -= amount
        self.oMoneyText.setText(f'Money: {self.money}')

    def dealCard(self, oCard):
        numberOfCards = len(self.cards)
        if self.player != DEALER:
            oCard.reveal()
            cardLocation = (self.loc[0] + PLAYER_CARD_OFFSET_X*numberOfCards, self.loc[1] + CARD_OFFSET_Y*numberOfCards)
        else:
            if numberOfCards > 0:
                oCard.reveal()
            cardLocation = (self.loc[0] + CARD_OFFSET_X*numberOfCards, self.loc[1])
        oCard.setLoc(cardLocation)
        self.cards.append(oCard)
        self._setScore()

    def revealCards(self):
        for oCard in self.cards:
            oCard.reveal()
        self.revealed = True
        self._setScore()

    def getNumberOfCards(self):
        return len(self.cards)

    def getScore(self):
        return self.score

    def _setScore(self):
        # Calculate score based on current cards
        scoreCount = 0
        aceCount = 0
        for oCard in self.cards:
            if oCard.getRank() == 'Ace': # Ignore Aces values for now
                thisCardValue = 0
                aceCount += 1
            else:
                thisCardValue = oCard.getValue()
            scoreCount += thisCardValue
        for ace in range(aceCount): # Count the aces as 1 or 11 depending on which is best
            if scoreCount+11 > 21:
                thisCardValue = 1
            else:
                thisCardValue = 11
            scoreCount += thisCardValue
        self.score = scoreCount

        # Update displayed score (Different if cards aren't revealed)
        if self.revealed:
            self.oScoreText.setText(str(self.score))
        elif len(self.cards) >= 2:
            hiddenScore = self.cards[1].getValue()
            if hiddenScore == 1:
                hiddenScore = 11
            self.oScoreText.setText(str(hiddenScore))

    def giveBlackJack(self):
        self.blackJack = True
        self.oScoreText.setText('Black Jack!')

    def deleteCards(self):
        self.cards = []
        self._setScore()
        if self.player == DEALER:
            self.revealed = False
        self.blackJack = False

    def centerText(self, oDisplayText):
        textX, textY, textWidth, textHeight = oDisplayText.getRect()
        oDisplayText.setLoc((self.textCenterX - textWidth/2, textY))

    def draw(self):
        for card in self.cards:
            card.draw()
        self.centerText(self.oScoreText)
        self.oScoreText.draw()
        self.centerText(self.oMoneyText)
        self.centerText(self.oBetText)
        if self.player != DEALER:
            self.oMoneyText.draw()
            self.oBetText.draw()
# End Player class

# Cheater class (subclass of Player)
class Cheater(Player):

    def dealCard(self, oCard):
        numberOfCards = len(self.cards)
        card1 = CHEATER_CARD_1
        card2 = CHEATER_CARD_2
        if numberOfCards == 0:
            cardToDeal = Card(self.window, card1['Rank'], card1['Suit'], card1['Value'])
        else:
            cardToDeal = Card(self.window, card2['Rank'], card2['Suit'], card2['Value'])
        super().dealCard(cardToDeal)
# End Cheater class

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

    oCheater = Cheater(window, PLAYER1)
    oPlayerList.append(oCheater)

    for oPlayer in oPlayerList:
        print(oPlayer)