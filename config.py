import pygame


class Config:
    instance = None

    def __init__(self):
        self.SCREEN_WIDTH = 1600
        self.SCREEN_HEIGHT = 800

        self.NUMBER_OF_ROUTES = 4
        self.GROOMERS = [100, 200]
        self.SKIER_V = 40
        self.SKIER_MAX_Y = 700
        self.PROB_NEW_SKIER = 0.9
        self.AUTORUN = True
        self.AUTORUN_TIME_DELAY = 50  # ms
        self.QUALITY_STEP = 1
        self.START_POSITION = [(190, 136), (560, 136), (880, 136), (1265, 136)]
        self.IMAGES = {
            "SKIER": pygame.transform.scale(pygame.image.load('imgs/skier.png'), (30, 30)),
            "SNOW_GROOMER": pygame.transform.scale(pygame.image.load('imgs/snow_groomer.png'), (80, 60)),
            "SKI_SLOPE": pygame.transform.scale(pygame.image.load('imgs/ski_slope.png'),
                                                (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        }

    @classmethod
    def get_instance(cls):
        if not Config.instance:
            Config.instance = Config()
        return Config.instance
