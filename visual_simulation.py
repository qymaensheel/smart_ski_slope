import random
from time import sleep
import numpy as np
import pygame
from config import Config

config = Config.get_instance()


class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = np.zeros((size, size))


def draw_grid(screen, w_width, w_height, t, skiers):
    white = (255, 255, 255)
    black = (0, 0, 0)
    screen.fill(white)
    blue = (0, 0, 128)

    screen.blit(config.IMAGES["SKI_SLOPE"], (0, 0))

    for skier in skiers:
        screen.blit(config.IMAGES["SKIER"], (skier.x, skier.y))

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(f't = {t}', True, black, white)
    textRect = text.get_rect()
    textRect.center = (w_width // 2, w_height + 40)
    screen.blit(text, textRect)

    # tmp snow groomer blitz
    screen.blit(config.IMAGES["SNOW_GROOMER"], (1500, 780))

    pygame.display.flip()
