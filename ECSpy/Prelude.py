
from .App import App
from .Screen import Screen
from .Rescource import Rescource
from .Events import eventHandlerPlugin
from .Clock import Clock
import pygame

class GameData(Rescource):
    def __init__(self, screenSize : tuple, caption : str):
        super().__init__("GameData")
        self.screenSize = screenSize
        self.Caption = caption


def preludePlugin(app : App):
    pygame.init()
    app.addRescource(Screen(app.getRescource("GameData").screenSize))
    app.addRescource(Clock())
    pygame.display.set_caption(app.getRescource("GameData").Caption)
    app.addPlugin(eventHandlerPlugin)
