import sqlite3

from base import Base

from data_schema.metadata import Metadata
from data_schema.stops import Stops
from data_schema.stop_times import StopTimes
from data_schema.matching_trips import MatchingTrips

class Dataloader(Base):

    def __init__(self, config):
        super().__init__(config)
        self.db_file = config.get("working_dir") + r"\transit_data.db"

    def full_refresh(self):
        conn = sqlite3.connect(self.db_file)

        # setup each table. the order here is important.
        setup_list = [Metadata, Stops, StopTimes, MatchingTrips]
        for table in setup_list:
            self.logger.info(f"Dataloader - setting up table {table}")
            table(self.config, conn).setup()

        conn.commit()
        conn.close()

    def get_trip_id_list(self):
        conn = sqlite3.connect(self.db_file)

        get_trip_id_list = MatchingTrips(self.config, conn).get_trip_id_list()
        
        conn.close()

        return get_trip_id_list