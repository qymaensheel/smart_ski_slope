import random

import pygame
from config import Config
from visual_simulation import draw_grid
from skier import Skier
from pygame.locals import (
    K_RIGHT,
    KEYDOWN,
    QUIT,
    K_ESCAPE
)

config = Config.get_instance()

if __name__ == '__main__':
    print("hello")
    pygame.init()

    w_width = config.SCREEN_WIDTH
    w_height = config.SCREEN_HEIGHT
    screen = pygame.display.set_mode([w_width, w_height + 100])
    screen.fill((128, 128, 128))
    running = True

    pygame.Surface.convert_alpha(config.IMAGES['SKIER'])
    pygame.Surface.convert_alpha(config.IMAGES['SNOW_GROOMER'])

    time_delay = config.AUTORUN_TIME_DELAY
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, time_delay)

    skiers = []
    step = -1

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN or event.type == timer_event and config.AUTORUN:
                step += 1
                if random.random() <= config.PROB_NEW_SKIER:
                    skier_x, skier_y = config.START_POSITION[random.randint(0, config.NUMBER_OF_ROUTES-1)]
                    skier_x += random.randrange(-20, 20)
                    skiers.append(Skier(skier_x, skier_y))

                skiers_skiing = []
                for skier in skiers:
                    skier.move()
                    if skier.y < config.SKIER_MAX_Y:
                        skiers_skiing.append(skier)
                skiers = skiers_skiing.copy()
                draw_grid(screen, w_width, w_height, step, skiers)

    pygame.quit()
