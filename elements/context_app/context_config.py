class ContextConfig:
    instance = None

    def __init__(self):
        self.ROUTES_QUALITY_THRESHOLD = 80

    @classmethod
    def get_instance(cls):
        if not ContextConfig.instance:
            ContextConfig.instance = ContextConfig()
        return ContextConfig.instance
