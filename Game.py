#  Game class

from unittest import case
import pygwidgets
from CardWidgets import *
from Deck import *
from Player import *
from Card import *
from Constants import *
import pygame

class Game():
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
        self.playerNames = []
        for playerIndex in range(numberOfPlayers):
            currentPlayer = PLAYER_LIST[playerIndex]
            if PLAYER_CHEATS[currentPlayer]:
                oPlayer = Cheater(window, currentPlayer)
            else:
                oPlayer = Player(window, currentPlayer)
            self.oPlayerList.append(oPlayer)
            self.playerNames.append(oPlayer.player)
        if PLAYER_CHEATS[DEALER]:
            oDealer = Cheater(window, DEALER)
        else:
            oDealer = Player(window, DEALER)
        self.oPlayerList.append(oDealer)
        self.playerNames.append(oDealer.player)
        # Buttons
        self.buttonsDict = {}
        for oPlayer in self.oPlayerList:
            if oPlayer.player == DEALER:
                continue
            betButtonTop = WINDOW_HEIGHT - BET_BUTTON_WIDTH * 4
            betButtonLeft = oPlayer.textCenterX - BET_BUTTON_WIDTH
            betButtonHideList = [Game.DEALING, Game.IS_ANYONE_HOME, Game.PLAYING, Game.REVEALING, Game.ROUND_OVER]
            betButtonShowList = [Game.BETTING]
            doubleButtonHideList = [Game.BETTING, Game.DEALING, Game.IS_ANYONE_HOME, Game.REVEALING, Game.ROUND_OVER]
            doubleButtonShowList = [Game.PLAYING]
            betIncreaseButton = GameButton(window, (betButtonLeft + BET_BUTTON_WIDTH, betButtonTop), '+10',
                                                        betButtonHideList, betButtonShowList, buttonType='bet', width=BET_BUTTON_WIDTH, height=BET_BUTTON_WIDTH)
            betDecreaseButton = GameButton(window, (betButtonLeft, betButtonTop), '-10',
                                                        betButtonHideList, betButtonShowList, buttonType='bet', width=BET_BUTTON_WIDTH, height=BET_BUTTON_WIDTH)
            doubleButton = GameButton(window, (betButtonLeft, betButtonTop), 'Double',
                                                    doubleButtonHideList, doubleButtonShowList, buttonType='bet', width=BET_BUTTON_WIDTH*2, height=BET_BUTTON_WIDTH)
            playerButtonList = [betIncreaseButton, betDecreaseButton, doubleButton]
            self.buttonsDict[oPlayer.player] = playerButtonList

        # Game variables
        self.currentPlayerIndex = 0
        self.gameState = ''
        self.numberOfPlayers = numberOfPlayers
        self.dealerIndex = len(self.oPlayerList) - 1
        self.dealerRevealed = False
        self.roundsDealt = 0

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

    def nextPlayer(self):
        notPlaying = True
        while notPlaying:
            if self.currentPlayerIndex == len(self.oPlayerList) - 1:
                self.currentPlayerIndex = 0
            else:
                self.currentPlayerIndex += 1
            oNextPlayer = self.oPlayerList[self.currentPlayerIndex]
            notPlaying = oNextPlayer.notPlaying
        self.updateIndicator()
        return oNextPlayer

    def dealOneCard(self):
        Game.DEAL_SOUND.play()
        cardToDeal = self.oShoe.getCard()
        oCurrentPlayer = self.oPlayerList[self.currentPlayerIndex]
        oCurrentPlayer.dealCard(cardToDeal)
        currentPlayerScore = oCurrentPlayer.getScore()
        dealer = oCurrentPlayer.player == DEALER
        return cardToDeal, oCurrentPlayer, currentPlayerScore, dealer

    def readyButtonAction(self):
        activePlayerNames = []
        for oPlayer in self.oPlayerList:
            if oPlayer.player == DEALER:
                continue
            elif oPlayer.bet == 0:
                oPlayer.notPlaying = True
            else:
                activePlayerNames.append(oPlayer.player)
        if activePlayerNames:
            self.currentPlayerIndex = self.playerNames.index(activePlayerNames[0])
            self.setGameState(Game.DEALING)

    def dealButtonAction(self):
        cardDealt, oCurrentPlayer, currentPlayerScore, dealer = self.dealOneCard()
        if not dealer and currentPlayerScore == 21:
            oCurrentPlayer.giveBlackJack()
            Game.WIN_SOUND.play()
        elif dealer and oCurrentPlayer.getNumberOfCards() == 2:
            if cardDealt.getValue() == 1 or cardDealt.getValue() == 10:
                self.setGameState(Game.IS_ANYONE_HOME)
                self.nextPlayer()
                return
            else:
                self.setGameState(Game.PLAYING)
        self.nextPlayer()

    def hitButtonAction(self):
        _, _, currentPlayerScore, dealer = self.dealOneCard()
        if not dealer and currentPlayerScore >= 21:
            oNewCurrentPlayer = self.nextPlayer()
            if oNewCurrentPlayer.player == DEALER:
                self.setGameState(Game.REVEALING)

    def standButtonAction(self):
        oNewCurrentPlayer = self.nextPlayer()
        if oNewCurrentPlayer.player == DEALER:
            self.setGameState(Game.REVEALING)

    def revealButtonAction(self):
        oDealer = self.oPlayerList[self.numberOfPlayers]
        dealerScore = oDealer.getScore()
        if not self.dealerRevealed:
            Game.DEAL_SOUND.play()
            oDealer.revealCards()
            self.dealerRevealed = True
        else:
            if dealerScore < 17:
                self.dealOneCard()
                dealerScore = oDealer.getScore()

        if dealerScore >= 17:
            self.nextPlayer()
            self.setGameState(Game.ROUND_OVER)

    def resetButtonAction(self):
        for oPlayer in self.oPlayerList:
            oPlayer.deleteCards()
            oPlayer.notPlaying = False
        self.setGameState(Game.BETTING)
        self.currentPlayerIndex = 0
        self.dealerRevealed = False

    def checkDealerButtonAction(self):
        oDealer = self.oPlayerList[self.numberOfPlayers]
        DealerScore = oDealer.getScore()
        if DealerScore == 21:
            oDealer.revealCards()
            self.setGameState(Game.ROUND_OVER)
        else:
            self.setGameState(Game.PLAYING)
            # TODO - display text that says "Nobody's home"

    def doubleButtonAction(self, oPlayer):
        oCurrentPlayer = self.oPlayerList[self.currentPlayerIndex]
        if oPlayer.player != oCurrentPlayer.player or oCurrentPlayer.getNumberOfCards() != 2:
            return False
        currentBet = oPlayer.bet
        if not oPlayer.increaseBet(currentBet):
            return False
        self.dealOneCard()
        self.nextPlayer()
        return True

    def setGameState(self, gameState):
        if gameState == Game.ROUND_OVER:
            self.payout()
        self.gameState = gameState
        self.oGameStateText.setText(gameState)
        textX, textY, textWidth, textHeight = self.oGameStateText.getRect()
        centeredLoc = (WINDOW_CENTER_X - textWidth/2, textHeight/2)
        self.oGameStateText.setLoc(centeredLoc)
        self.updatePlayerButtons()

    def getGameState(self):
        return self.gameState

    def updateIndicator(self):
        oCurrentPlayer = self.oPlayerList[self.currentPlayerIndex]
        textCenterX = oCurrentPlayer.loc[0] + CARD_WIDTH/2
        indicatorX = textCenterX - self.indicatorWidth/2
        indicatorY = oCurrentPlayer.loc[1] + CARD_HEIGHT + self.indicatorHeight*1.5
        self.oPlayerIndicator.setLoc((indicatorX, indicatorY))

    def payout(self):
        oDealer = self.oPlayerList[self.numberOfPlayers]
        dealerScore = oDealer.getScore()
        payout = 0
        for oPlayer in self.oPlayerList:
            playerScore = oPlayer.getScore()
            if oPlayer.player == DEALER:
                continue
            if oPlayer.blackJack:
                payout = int((3/2)*oPlayer.bet)
            elif playerScore > 21:
                payout = (-1)*oPlayer.bet
            elif playerScore > dealerScore or dealerScore > 21:
                payout = oPlayer.bet
            elif playerScore == dealerScore:
                payout = 0
            elif playerScore < dealerScore <= 21:
                payout = (-1)*oPlayer.bet
            oPlayer.payout(payout)

    def updatePlayerButtons(self):
        for oButtonList in self.buttonsDict.values():
            for oButton in oButtonList:
                oButton.hideOrShow(self.gameState)

    def handleEvent(self, event):
        oCurrentPlayer = self.oPlayerList[self.currentPlayerIndex]
        for playerName, oButtonList in self.buttonsDict.items():
            playerIndex = PLAYER_LIST.index(playerName)
            oPlayer = self.oPlayerList[playerIndex]
            for oButton in oButtonList:
                if oButton.handleEvent(event):
                    print(f'{playerName} clicked {oButton.getNickname()}')
                    if oButton.buttonType == 'bet':
                        if oButton.getNickname() == 'Double':
                            self.doubleButtonAction(oPlayer)
                        else:
                            oPlayer.increaseBet(int(oButton.getNickname()))

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