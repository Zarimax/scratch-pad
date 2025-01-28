from data_schema.database import Database

class StopTimes(Database):

    def __init__(self, config, conn):
        self.table_name = "stop_times"

        self.create_sql = """
        CREATE TABLE IF NOT EXISTS stop_times (
            trip_id TEXT,
            stop_sequence INTEGER,
            stop_id TEXT,
            stop_headsign TEXT,
            arrival_time TEXT,
            departure_time TEXT,
            pickup_type INTEGER,
            drop_off_type INTEGER,
            timepoint INTEGER,
            shape_dist_traveled REAL,
            fare_units_traveled REAL
        )
        """

        self.insert_sql = """
        INSERT INTO stop_times (
            trip_id,
            stop_sequence,
            stop_id,
            stop_headsign,
            arrival_time,
            departure_time,
            pickup_type,
            drop_off_type,
            timepoint,
            shape_dist_traveled,
            fare_units_traveled
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        super().__init__(config, conn)

    def setup(self):
        self.create_and_load_if_newer()