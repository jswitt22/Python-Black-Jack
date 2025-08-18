# CardWidgets.py
# contains classes of widgets useful for card games
import pygwidgets

# GameButton Class
class GameButton(pygwidgets.TextButton):
    def __init__(self, window, loc, text, hiddenGameStates, revealedGameStates, buttonType='bet', width=None, height=40, textColor=(0, 0, 0), upColor=(170, 170, 170),
                 overColor=(210, 210, 210), downColor=(140, 140, 140), fontName=None, fontSize=20, soundOnClick=None,
                 enterToActivate=False, callBack=None, nickname=None, activationKeysList=None):
        self.hiddenGameStates = hiddenGameStates
        self.revealedGameStates = revealedGameStates
        self.buttonType = buttonType
        self.clickedCounter = 0

        super().__init__(window, loc, text, width, height, textColor, upColor, overColor, downColor, fontName, fontSize,
                         soundOnClick, enterToActivate, callBack, nickname, activationKeysList)

    def hideOrShow(self, gameState):
        if gameState in self.hiddenGameStates:
            self.disable()
            self.hide()
        if gameState in self.revealedGameStates:
            self.enable()
            self.show()

# End GameButton Class