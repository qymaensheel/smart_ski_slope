import datetime


class ContextConfig:
    instance = None

    def __init__(self):
        self.ROUTES_QUALITY_THRESHOLD = 50
        self.ROUTES_QUALITY_CLOSURE_THRESHOLD = 30
        self.TIME_TO_CLOSE = datetime.time(hour=16, minute=0)
        self.CRITICAL_TEMPERATURE_THRESHOLD = 8

    @classmethod
    def get_instance(cls):
        if not ContextConfig.instance:
            ContextConfig.instance = ContextConfig()
        return ContextConfig.instance
