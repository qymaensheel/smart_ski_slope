import pygame
from config import Config

config = Config.get_instance()


class Skier:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.v = config.SKIER_V

    def blit(self, screen: pygame.display) -> None:
        screen.blit(config.IMAGES["SKIER"], (self.x, self.y))

    def move(self) -> None:
        self.y += self.v
