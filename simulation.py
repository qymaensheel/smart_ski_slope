import datetime
import random

import numpy as np
import pygame
from pygame.locals import (
    KEYDOWN,
    QUIT,
)

from config import Config
from elements.context_app.context_app import ContextApp
from elements.context_manager import ContextManager
from elements.skier import Skier
from plots import plot_data
from visual_simulation import draw_grid

config = Config.get_instance()
context_app = ContextApp()


def groom_lowest_route():
    if context_manager.date.time() == datetime.time(hour=6) or \
            context_manager.date.time() == datetime.time(hour=20):

        index_min = np.argmin(context_manager.get_routes_quality())
        selected_route = context_manager.routes[index_min]
        chosen_groomer = None
        for g in context_manager.groomers:
            if g.available:
                chosen_groomer = g
                break
        if chosen_groomer is not None:
            chosen_groomer.groom(selected_route)
            context_manager.wallet -= chosen_groomer.cost


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
                context_app.notify()
                step += 1

                # open and close routes
                if context_manager.date.time() == config.OPENING_HOURS['open']:
                    context_manager.open_routes_for_day()
                if context_manager.date.time() == config.OPENING_HOURS['close']:
                    context_manager.close_routes_for_night()

                # start grooming
                # groom_lowest_route()

                for groomer in context_manager.groomers:
                    if not groomer.available:
                        groomer.move(context_manager.is_slope_open())

                # create skiers
                if context_manager.is_slope_open() and context_app.slope_open:
                    if random.random() <= context_manager.probability_new_skier:
                        probabilities_new_skier = context_manager.get_probability_table()
                        if sum(probabilities_new_skier) == 1:
                            total_number_of_skiers += 1
                            context_manager.daily_skiers += 1
                            skier_choice = np.random.choice(list(range(config.NUMBER_OF_ROUTES)), size=1,
                                                            p=probabilities_new_skier)
                            skier_choice = int(skier_choice)
                            skier_route_choice = context_manager.routes[skier_choice]
                            skier_x, skier_y = skier_route_choice.start_position
                            skier_x += random.randrange(-20, 20)
                            skier_y += random.randrange(-10, 10)
                            new_skier = Skier(skier_x, skier_y)
                            skier_route_choice.skiers.append(new_skier)
                            context_manager.wallet += config.TICKET

                context_manager.add_hourly()
                context_manager.add_daily()
                context_manager.pay_for_route()
                for route in context_manager.routes:
                    route.move_skiers()

                if context_manager.date.minute == 0:
                    context_manager.weather.update_current_temp()
                    context_manager.weather.calc_change_rate()
                    context_manager.adjust_route_qualities()

                context_manager.print_status()
                draw_grid(screen, w_width, w_height)
                context_manager.update_probability()
                context_manager.date += datetime.timedelta(minutes=5)

                plot_data()

                if context_manager.date >= config.SIMULATION_END_DATE:
                    quit(0)
    pygame.quit()
