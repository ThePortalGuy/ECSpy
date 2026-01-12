import pygame
from .Rescource import Rescource

class Clock(Rescource):
    def __init__(self):
        super().__init__("Clock")
        self.Clock = pygame.time.Clock()