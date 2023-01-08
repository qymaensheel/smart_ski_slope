import pygame

from config import Config

config = Config.get_instance()


class Groomer:
    def __init__(self, x: int, y: int, cost=200):
        self.available = True
        self.starting_position = (x, y)
        self.x = x
        self.y = y
        self.v = config.GROOMER_V
        self.cost = cost
        self.route_grooming = None

    def blit(self, screen: pygame.display) -> None:
        screen.blit(config.IMAGES["SNOW_GROOMER"], (self.x, self.y))

    def move(self) -> None:
        # if self.route_grooming is not None:
        self.y += self.v
        if self.y > config.SKIER_MAX_Y:
            self.available = True
            self.x, self.y = self.starting_position
            self.route_grooming.available = True
            self.route_grooming.quality = 100
            self.route_grooming = None
