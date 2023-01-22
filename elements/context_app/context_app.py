import copy
import datetime

import numpy as np

from elements.context_app.context_config import ContextConfig
from elements.context_manager import ContextManager


class ContextApp:

    def __init__(self):
        self.enable = True  # enable Context App
        self.slope_open = True
        self.ctx_config = ContextConfig.get_instance()
        self.context_manager = ContextManager.get_instance()
        self.reopen_date = None

    def notify(self):
        if self.enable:
            self.__manage_slope_availability()

        return

    def __manage_slope_availability(self):

        current_date = self.context_manager.date
        routes_quality_avg = np.mean(self.context_manager.get_routes_quality())

        if routes_quality_avg < self.ctx_config.ROUTES_QUALITY_CLOSURE_THRESHOLD:
            if self.reopen_date is None:
                if current_date.time() >= self.ctx_config.TIME_TO_CLOSE:
                    for route in self.context_manager.routes:
                        route.available = False
                    # GROOMING
                    tomorrow = current_date + datetime.timedelta(days=1)
                    self.reopen_date = datetime.datetime(year=tomorrow.year, month=tomorrow.month,
                                                         day=tomorrow.day, hour=5, minute=00, second=0)
            elif self.reopen_date is not None and current_date >= self.reopen_date:
                for route in self.context_manager.routes:
                    route.available = True
                self.reopen_date = None

        if routes_quality_avg < self.ctx_config.ROUTES_QUALITY_THRESHOLD:
            if self.context_manager.is_slope_open():
                chosen_groomer = None
                for groomer in self.context_manager.groomers:
                    if groomer.available:
                        chosen_groomer = groomer
                        break
                if chosen_groomer is not None:
                    routes = self.context_manager.routes.copy()

                    routes.sort(key=lambda route: route.quality)
                    selected_route = routes[0]
                    if selected_route.is_groomed:
                        selected_route = routes[1]
                    chosen_groomer.groom(selected_route)


