import datetime
from pathlib import Path

import pygame


class Config:
    instance = None

    def __init__(self):
        self.SCREEN_WIDTH = 1600
        self.SCREEN_HEIGHT = 800
        self.STARTING_BUDGET = 0  # PLN
        self.NUMBER_OF_ROUTES = 4
        self.GROOMER_POSITIONS = [(1500, 800), (1400, 800)]
        self.GROOMERS_COST = [750, 750]
        self.ROUTE_COST_PER_HOUR = 100
        self.TICKET = 70
        self.GROOMER_V = 10
        self.SKIER_V = 40
        self.SKIER_MAX_Y = 700
        self.PROB_NEW_SKIER = 0.9
        self.AUTORUN = True
        self.AUTORUN_TIME_DELAY = 50  # ms
        self.QUALITY_STEP = 1
        self.START_POSITIONS = [(190, 136), (560, 136), (880, 136), (1265, 136)]
        self.OPENING_HOURS = {'open': datetime.time(8), 'close': datetime.time(20)}
        self.PLOT = True
        self.PLOT_PATH = Path("outputs")
        self.SIMULATION_END_DATE = datetime.datetime(2023, 1, 7, 23, 0, 0)
        self.IMAGES = {
            "SKIER": pygame.transform.scale(pygame.image.load('imgs/skier.png'), (30, 30)),
            "SNOW_GROOMER": pygame.transform.scale(pygame.image.load('imgs/snow_groomer.png'), (100, 80)),
            "SKI_SLOPE": pygame.transform.scale(pygame.image.load('imgs/ski_slope.png'),
                                                (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        }

    def __str__(self):
        return_str = ""
        for k, v in self.__dict__.items():
            if k != 'IMAGES':
                return_str += f'{k}: {v}\n'

        return return_str

    @classmethod
    def get_instance(cls):
        if not Config.instance:
            Config.instance = Config()
        return Config.instance
