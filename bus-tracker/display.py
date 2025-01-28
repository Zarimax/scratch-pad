from base import Base

class Display(Base):

    def __init__(self, config):
        super().__init__(config)

    def turn_on(self):
        self.logger.info("Display - turn_on")

    def turn_off(self):
        self.logger.info("Display - turn_off")

    def show_arrival_times(self, arrival_times):
        self.logger.info(f"Display - show arrival times {arrival_times}")