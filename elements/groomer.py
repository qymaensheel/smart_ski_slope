import datetime

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

    def move(self, daytime=True) -> None:
        # if self.route_grooming is not None:
        self.y += self.v
        if self.y > config.SKIER_MAX_Y:
            self.available = True
            self.x, self.y = self.starting_position
            if daytime:
                self.route_grooming.available = True

            self.route_grooming.is_groomed = False
            self.route_grooming = None

    def groom(self, selected_route):
        self.route_grooming = selected_route
        new_quality = self.route_grooming.quality + config.GROOMER_REPAIR_FACTOR
        if new_quality > 100:
            new_quality = 100
        self.route_grooming.quality = new_quality
        selected_route.available = False
        self.available = False
        selected_route.is_groomed = True
        self.x, self.y = selected_route.start_position
