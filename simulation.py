import datetime
import random

import numpy as np
import pygame
from pygame.locals import (
    KEYDOWN,
    QUIT,
)

from config import Config
from context_manager import ContextManager
from skier import Skier
from visual_simulation import draw_grid

config = Config.get_instance()

if __name__ == '__main__':
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

    context_manager = ContextManager.get_instance()
    total_number_of_skiers = 0
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN or event.type == timer_event and config.AUTORUN:
                step += 1

                if random.random() <= context_manager.probability_new_skier:
                    probabilities_new_skier = context_manager.get_probability_table()
                    if sum(probabilities_new_skier) == 1:
                        total_number_of_skiers += 1
                        skier_choice = np.random.choice(list(range(config.NUMBER_OF_ROUTES)), size=1,
                                                        p=probabilities_new_skier)
                        skier_choice = int(skier_choice)
                        skier_route_choice = context_manager.routes[skier_choice]
                        skier_x, skier_y = skier_route_choice.start_position
                        skier_x += random.randrange(-20, 20)
                        skier_y += random.randrange(-10, 10)
                        new_skier = Skier(skier_x, skier_y)
                        skier_route_choice.skiers.append(new_skier)
                context_manager.print_status()
                for route in context_manager.routes:
                    route.move_skiers()

                draw_grid(screen, w_width, w_height)
                context_manager.update_probability()
                context_manager.date += datetime.timedelta(minutes=5)

    pygame.quit()
