import pygame

from config import Config
from elements.context_manager import ContextManager

config = Config.get_instance()
context_manager = ContextManager.get_instance()


def draw_grid(screen, w_width, w_height):
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    red = (255, 0, 0)
    screen.fill(white)

    # blit background
    screen.blit(config.IMAGES["SKI_SLOPE"], (0, 0))

    # blit groomers
    for groomer in context_manager.groomers:
        groomer.blit(screen)

    # blit skiers
    for route in context_manager.routes:
        for skier in route.skiers:
            skier.blit(screen)
    # Display texts
    font = pygame.font.Font('freesansbold.ttf', 32)

    # time
    text = font.render(f'{context_manager.date.strftime("%d/%m/%Y %H:%M")}', True, black, white)
    textRect = text.get_rect()
    textRect.center = (w_width // 2, w_height + 40)
    screen.blit(text, textRect)

    # routes data
    for route in context_manager.routes:
        if route.quality == 0:
            route.available = False
        route_x, route_y = route.start_position
        # quality
        text = font.render(f'{int(route.quality)}%', True, black, white)
        textRect = text.get_rect()
        textRect.center = (route_x, route_y - 100)
        screen.blit(text, textRect)

        # availability
        if route.available:
            text = font.render('O', True, green, white)
        else:
            text = font.render('X', True, red, white)
        textRect = text.get_rect()
        textRect.center = (route_x + 70, route_y - 100)
        screen.blit(text, textRect)

    pygame.display.flip()
