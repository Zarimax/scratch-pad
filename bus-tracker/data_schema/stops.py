from data_schema.database import Database

class Stops(Database):

    def __init__(self, config, conn):
        self.table_name = "stops"

        self.create_sql = """
        CREATE TABLE IF NOT EXISTS stops (
            stop_id TEXT,
            stop_code TEXT,
            stop_name TEXT,
            stop_lat REAL,
            stop_lon REAL,
            location_type INTEGER,
            parent_station TEXT,
            stop_timezone TEXT,
            wheelchair_boarding INTEGER,
            platform_code TEXT,
            zone_id TEXT
        ) 
        """

        self.index_sql_list = [
            "CREATE INDEX IF NOT EXISTS idx_stops_stop_id ON stops(stop_id)",
            "CREATE INDEX IF NOT EXISTS idx_stops_stop_name ON stops(stop_name)",
        ]

        self.insert_sql = """
        INSERT INTO stops (
            stop_id,
            stop_code,
            stop_name,
            stop_lat,
            stop_lon,
            location_type,
            parent_station,
            stop_timezone,
            wheelchair_boarding,
            platform_code,
            zone_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        super().__init__(config, conn)

    def setup(self):
        self.create_and_load_if_newer()