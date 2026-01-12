from .App import App
from .ECSglobals import mainApplication as app
import pygame


def eventHandlerPlugin(app : App):
    app.addSystem("Update",handleEvents)

def handleEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    app.getRescource("Clock").Clock.tick(60)