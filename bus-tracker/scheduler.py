from base import Base
from display import Display
from downloader import Downloader
from dataloader import Dataloader
from tracker import Tracker

class Scheduler(Base):
    def __init__(self, config):
        super().__init__(config)

        self.display = Display(config)
        self.downloader = Downloader(config)
        self.dataloader = Dataloader(config)
        self.tracker = Tracker(config)

        self.exception = None
        self.state = self.state_wake

    def _resolve_time_to_timestamp(time_string):
        pass

    def state_sleep(self):
        """
        SLEEP
            --> WAKE
            --> RECOVER
        """
        self.logger.info("Scheduler - entering state SLEEP")
        try:
            self.display.turn_off()
            # TODO - WAIT for wake up time
            self.state = self.state_wake
        except Exception as e:
            self.exception = e
            self.state = self.state_recover

    def state_wake(self):
        """
        WAKE
            --> RUN
            --> RECOVER
        """
        self.logger.info("Scheduler - entering state WAKE")
        try:
            self.display.turn_on()
            self.downloader.get_full_data()
            self.dataloader.full_refresh()
            self.state = self.state_run
        except Exception as e:
            self.exception = e
            self.state = self.state_recover

    def state_run(self):
        """
        RUN
            --> RUN
            --> SLEEP
            --> RECOVER
        """
        self.logger.info("Scheduler - entering state RUN")
        try:
            feed = self.downloader.get_realtime_data()
            trip_id_list = self.dataloader.get_trip_id_list()
            arrival_times = self.tracker.get_arrival_times(feed, trip_id_list)
            self.display.show_arrival_times(arrival_times)

            # if sleep time, enter sleep state
            #self.state = self.state_sleep
            # else, remain in the run state
            # TODO - WAIT
        except Exception as e:
            self.exception = e
            self.state = self.state_recover

    def state_recover(self):
        """
        RECOVER
            Verify network
            Verify disk
            Verify DB
            --> WAKE
        """
        self.logger.info("Scheduler - entering state RECOVER")
        if self.exception:
            self.logger.error(str(self.exception))
        
        # TODO - recovery steps
        # TODO - track recovery loop count
        self.state = self.state_wake