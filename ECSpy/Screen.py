import pygame
from .Rescource import Rescource



class Screen(Rescource):
    def __init__(self,size : tuple):
        super().__init__("Screen")
        self.screen = pygame.display.set_mode(size)