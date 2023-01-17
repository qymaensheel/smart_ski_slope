import pandas as pd

from config import Config

config = Config.get_instance()


class Weather:
    def __init__(self, input_csv="elements/weather.csv"):
        self.input_csv = pd.read_csv(input_csv)
        self.temperature = self.input_csv['Temperature'].values.tolist()
        self.temperature = self.temperature[config.WEATHER_OFFSET:800 + config.WEATHER_OFFSET]

        self.temperature_idx = -1
        self.current_temp = -1
        self.hourly_change_rate = 0

    def update_current_temp(self):
        self.temperature_idx += 1
        self.current_temp = self.temperature[self.temperature_idx]

    def calc_change_rate(self):
        if self.current_temp > 10:
            self.hourly_change_rate = -(4 * config.WEATHER_CHANGE_RATE)
        elif 5 < self.current_temp < 10:
            self.hourly_change_rate = -(2 * config.WEATHER_CHANGE_RATE)
        elif 0 < self.current_temp < 5:
            self.hourly_change_rate = -config.WEATHER_CHANGE_RATE
        elif -5 < self.current_temp < 0:
            self.hourly_change_rate = config.WEATHER_CHANGE_RATE
        elif -10 < self.current_temp < -5:
            self.hourly_change_rate = 1 * config.WEATHER_CHANGE_RATE
        elif self.current_temp < -10:
            self.hourly_change_rate = 2 * config.WEATHER_CHANGE_RATE
