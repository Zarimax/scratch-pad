
class Base:
    def __init__(self, config):
        self.config = config
        self.logger = self.config.get("logger")