from data_schema.database import Database

class MatchingTrips(Database):

    def __init__(self, config, conn):
        self.table_name = "matching_trips"

        self.create_sql = """
        CREATE TABLE IF NOT EXISTS matching_trips (
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
        INSERT INTO matching_trips
        SELECT st3.*
        FROM stop_times st3
        WHERE st3.trip_id IN (
            SELECT DISTINCT st1.trip_id
            FROM stop_times st1
            JOIN stop_times st2
            ON st1.trip_id = st2.trip_id
            WHERE st1.stop_id IN (
                SELECT stop_id FROM stops WHERE stop_name = "%s"
            )
            AND st2.stop_id IN (
                SELECT stop_id FROM stops WHERE stop_name = "%s"
            )
            AND st1.stop_sequence < st2.stop_sequence
        )
        """ % (
            config.get("begin_stop_name"),
            config.get("end_stop_name")
        )

        super().__init__(config, conn)

    def setup(self):
        self.drop_and_insert()

    def get_trip_id_list(self):
        self.cursor.execute("SELECT DISTINCT trip_id FROM matching_trips")
        matching_records = self.cursor.fetchall()
        return [record[0] for record in matching_records]