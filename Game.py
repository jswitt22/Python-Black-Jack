#  Game class

import pygwidgets
from Deck import *
from Player import *
from Card import *
from Constants import *
import pygame

class Game(): # TODO - implement method for adding/subtracting player bets
    # Game States
    BETTING = 'Betting'
    DEALING = 'Dealing'
    IS_ANYONE_HOME = 'Insurance?'
    PLAYING = 'Playing'
    REVEALING = 'Revealing'
    ROUND_OVER = 'Round Over'
    # Game Sounds
    pygame.init()
    DEAL_SOUND = pygame.mixer.Sound('sounds/cardFlip.wav')
    SHUFFLE_SOUND = pygame.mixer.Sound('sounds/cardShuffle.wav')
    WIN_SOUND = pygame.mixer.Sound('sounds/ding.wav')

    def __init__(self, window, numberOfPlayers=1):
        self.window = window

        # Game objects
        # Cards and Players
        self.oShoe = BlackJackShoe(window)
        self.oPlayerList = []
        for playerIndex in range(numberOfPlayers):
            currentPlayer = PLAYER_LIST[playerIndex]
            if PLAYER_CHEATS[currentPlayer]:
                oPlayer = Cheater(window, currentPlayer)
            else:
                oPlayer = Player(window, currentPlayer)
            self.oPlayerList.append(oPlayer)
        if PLAYER_CHEATS[DEALER]:
            oDealer = Cheater(window, DEALER)
        else:
            oDealer = Player(window, DEALER)
        self.oPlayerList.append(oDealer)
        # Buttons
        self.buttonsDict = {}
        for oPlayer in self.oPlayerList:
            if oPlayer.player == DEALER:
                continue
            betButtonTop = WINDOW_HEIGHT - BET_BUTTON_WIDTH * 4
            betButtonLeft = oPlayer.textCenterX
            betIncreaseButton = pygwidgets.TextButton(window, (betButtonLeft, betButtonTop),
                                                      '+10', width=BET_BUTTON_WIDTH, height=BET_BUTTON_WIDTH)
            betDecreaseButton = pygwidgets.TextButton(window, (betButtonLeft - BET_BUTTON_WIDTH, betButtonTop),
                                                      '-10', width=BET_BUTTON_WIDTH, height=BET_BUTTON_WIDTH)
            playerButtonList = [betIncreaseButton, betDecreaseButton]
            self.buttonsDict[oPlayer.player] = playerButtonList

        # Game variables
        self.currentPlayerIndex = 0
        self.gameState = ''
        self.numberOfPlayers = numberOfPlayers
        self.dealerIndex = len(self.oPlayerList) - 1
        self.dealerRevealed = False

        # Game text/images
        self.oPlayerIndicator = pygwidgets.DisplayText(self.window, value='^', textColor=TEXT_COLOR, fontSize=SCORE_FONT_SIZE)
        x, y, self.indicatorWidth, self.indicatorHeight = self.oPlayerIndicator.getRect()
        self.updateIndicator()
        self.oGameStateText = pygwidgets.DisplayText(self.window,value=self.gameState, textColor=TEXT_COLOR, fontSize=SCORE_FONT_SIZE)

        Game.SHUFFLE_SOUND.play()
        self.setGameState(Game.BETTING)

        self.printGameState()

    def reset(self):  # this method is called when a new shoe starts
        pass # TODO - implement shoe reshuffle

    def startRound(self):
        self.setGameState(Game.DEALING)

    def dealOneCard(self):
        Game.DEAL_SOUND.play()
        cardToDeal = self.oShoe.getCard()
        oCurrentPlayer = self.oPlayerList[self.currentPlayerIndex]
        oCurrentPlayer.dealCard(cardToDeal)
        currentPlayerScore = oCurrentPlayer.getScore()
        cardDealt = oCurrentPlayer.cards[oCurrentPlayer.getNumberOfCards()-1]
        dealer = oCurrentPlayer.player == DEALER
        if self.gameState == Game.DEALING:
            if not dealer and currentPlayerScore == 21:
                oCurrentPlayer.giveBlackJack()
                Game.WIN_SOUND.play()
            elif dealer and oCurrentPlayer.getNumberOfCards() == 2:
                if cardDealt.getValue() == 1 or cardDealt.getValue() == 10:
                    self.setGameState(Game.IS_ANYONE_HOME)
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
                if self.gameState != Game.IS_ANYONE_HOME:
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
            Game.DEAL_SOUND.play()
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
        textCenterX = oCurrentPlayer.loc[0] + CARD_WIDTH/2
        indicatorX = textCenterX - self.indicatorWidth/2
        indicatorY = oCurrentPlayer.loc[1] + CARD_HEIGHT + self.indicatorHeight*1.5
        self.oPlayerIndicator.setLoc((indicatorX, indicatorY))

    def checkBlackJack(self):
        oCurrentPlayer = self.oPlayerList[self.currentPlayerIndex]
        if oCurrentPlayer.blackJack and self.gameState == Game.PLAYING:
            self.nextPlayer()

    def checkDealer(self):
        oDealer = self.oPlayerList[self.numberOfPlayers]
        DealerScore = oDealer.getScore()
        if DealerScore == 21:
            oDealer.revealCards()
            self.setGameState(Game.ROUND_OVER)
        else:
            self.setGameState(Game.PLAYING)
            # TODO - display text that says "Nobody's home"

    def handleEvent(self, event):
        if self.gameState != Game.BETTING:
            return
        for player, oButtonList in self.buttonsDict.items():
            for oButton in oButtonList:
                if oButton.handleEvent(event):
                    print(f'{player} clicked {oButton.getNickname()}')
                    playerIndex = PLAYER_LIST.index(player)
                    if oButton.getNickname() == '-10':
                        amount = -10
                    if oButton.getNickname() == '+10':
                        amount = 10
                    self.oPlayerList[playerIndex].increaseBet(amount)

    def draw(self):
        for oPlayer in self.oPlayerList:
            oPlayer.draw()
        if self.gameState == Game.PLAYING:
            self.oPlayerIndicator.draw()
        self.oGameStateText.draw()
        for oButtonList in self.buttonsDict.values():
            for oButton in oButtonList:
                oButton.draw()

    def printGameState(self):
        # Debug
        for oPlayer in self.oPlayerList:
            print(oPlayer)
        print(self.oShoe)