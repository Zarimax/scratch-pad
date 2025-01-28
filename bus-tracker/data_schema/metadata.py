from data_schema.database import Database

class Metadata(Database):

    def __init__(self, config, conn):
        self.table_name = "metadata"

        self.create_sql = """
        CREATE TABLE IF NOT EXISTS metadata (
            table_name TEXT PRIMARY KEY,
            last_updated INTEGER
        )
        """

        self.insert_sql = None  # specified in load_table

        super().__init__(config, conn)

    def setup(self):
        self.create()