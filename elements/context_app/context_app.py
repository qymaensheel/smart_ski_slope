import datetime

import numpy as np

from elements.context_app.context_config import ContextConfig
from elements.context_manager import ContextManager


class ContextApp:

    def __init__(self):
        self.slope_open = None
        self.ctx_config = ContextConfig.get_instance()
        self.context_manager = ContextManager.get_instance()
        self.reopen_date = None

    def notify(self):
        self.__manage_slope_availability()

        return

    def __manage_slope_availability(self):

        current_date = self.context_manager.date
        routes_quality_avg = np.mean(self.context_manager.get_routes_quality())

        if self.reopen_date is None:
            if routes_quality_avg < self.ctx_config.ROUTES_QUALITY_THRESHOLD:
                for route in self.context_manager.routes:
                    route.available = False
                    # GROOMING
                    tomorrow = current_date + datetime.timedelta(days=1)
                    self.reopen_date = datetime.datetime(year=tomorrow.year, month=tomorrow.month,
                                                         day=tomorrow.day, hour=5, minute=00, second=0)
        elif current_date >= self.reopen_date:
            if routes_quality_avg < self.ctx_config.ROUTES_QUALITY_THRESHOLD:
                self.reopen_date += datetime.timedelta(days=1)
            else:
                for route in self.context_manager.routes:
                    route.available = True
                self.reopen_date = None
