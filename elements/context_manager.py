import datetime

from config import Config
from elements.groomer import Groomer
from elements.route import Route
from elements.weather import Weather

config = Config.get_instance()


class ContextManager:
    instance = None

    def __init__(self):
        self.date = datetime.datetime(2023, 1, 1, 8, 0, 0)
        self.probability_new_skier = config.PROB_NEW_SKIER
        self.weather = Weather()
        self.routes = [Route(x) for x in config.START_POSITIONS]
        self.groomers = [Groomer(*position, config.GROOMERS_COST[i]) for i, position in
                         enumerate(config.GROOMER_POSITIONS)]

        self.wallet = config.STARTING_BUDGET
        self.daily_skiers = 0
        self.budget_plot_values = []
        self.route_qualities_plot_values = [[] for _ in self.routes]
        self.daily_skiers_plot_values = []

    def get_routes_availability(self) -> list[bool]:
        return [x.available for x in self.routes]

    def get_routes_quality(self) -> list[int]:
        return [x.quality for x in self.routes]

    def get_skiers_count(self) -> list[int]:
        return [len(x.skiers) for x in self.routes]

    def is_slope_open(self):
        return config.OPENING_HOURS['open'] < self.date.time() < config.OPENING_HOURS['close']

    def get_probability_table(self) -> list[float]:
        quality_list = []
        for route in self.routes:
            if route.available:
                quality_list.append(route.quality)
            else:
                quality_list.append(0)
        if sum(quality_list) > 0:
            quality_list = [x / sum(quality_list) for x in quality_list]
        return quality_list

    def update_probability(self) -> None:
        qualities = self.get_routes_quality()
        fraction = sum(qualities) / (config.NUMBER_OF_ROUTES * 100)
        self.probability_new_skier = fraction * config.PROB_NEW_SKIER

    def pay_for_route(self) -> None:
        if self.date.minute == 0 and self.date.second == 0:
            for route in self.routes:
                if route.available:
                    self.wallet -= config.ROUTE_COST_PER_HOUR

    def close_routes_for_night(self) -> None:
        for route in self.routes:
            route.available = False

    def open_routes_for_day(self) -> None:
        for route in self.routes:
            route.available = True
        for groomer in self.groomers:
            if groomer.route_grooming is not None:
                groomer.route_grooming.available = False

    def add_hourly(self) -> None:
        if self.date.minute == 0:
            self.budget_plot_values.append(self.wallet)
            qualities = self.get_routes_quality()
            for idx, quality in enumerate(qualities):
                self.route_qualities_plot_values[idx].append(quality)

    def add_daily(self) -> None:
        if self.date.hour == 0 and self.date.minute == 0:
            self.daily_skiers_plot_values.append(self.daily_skiers)
            self.daily_skiers = 0

    def adjust_route_qualities(self):
        for route in self.routes:
            if 0 <= route.quality + self.weather.hourly_change_rate <= 100:
                route.quality += self.weather.hourly_change_rate

    def print_status(self) -> None:
        print('\nDate')
        print(self.date.time())
        print('Temperature')
        print(self.weather.current_temp)
        print('Routes availability:')
        print(self.get_routes_availability())
        print('Routes quality:')
        print(self.get_routes_quality())
        print('Skiers count:')
        print(self.get_skiers_count())
        print('Probability of new skier:')
        print(self.probability_new_skier)

    @classmethod
    def get_instance(cls):
        if not ContextManager.instance:
            ContextManager.instance = ContextManager()
        return ContextManager.instance
