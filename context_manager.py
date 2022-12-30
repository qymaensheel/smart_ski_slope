import datetime

from groomer import Groomer
from config import Config
from route import Route

config = Config.get_instance()


class ContextManager:
    instance = None

    def __init__(self):
        self.date = datetime.datetime(2022, 1, 1, 8, 0, 0)
        self.probability_new_skier = config.PROB_NEW_SKIER

        self.routes = [Route(x) for x in config.START_POSITION]
        self.groomers_available = [Groomer(x) for x in config.GROOMERS]

    def get_routes_availability(self) -> list[bool]:
        return [x.available for x in self.routes]

    def get_routes_quality(self) -> list[int]:
        return [x.quality for x in self.routes]

    def get_skiers_count(self) -> list[int]:
        return [len(x.skiers) for x in self.routes]

    # def get_probability_table(self): -> list
    #     quality_lst = self.get_routes_quality()
    #     probability_of_quitting = 100 * config.NUMBER_OF_ROUTES - sum(quality_lst)
    #     quality_lst.append(probability_of_quitting)
    #     quality_lst = [x / (100 * config.NUMBER_OF_ROUTES) for x in quality_lst]
    #     return quality_lst

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

    def print_status(self) -> None:
        print('\nRoutes availability:')
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
