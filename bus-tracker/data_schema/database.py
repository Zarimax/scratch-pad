import os
import csv

class Database:

    def __init__(self, config, conn):
        self.config = config
        self.cursor = conn.cursor()
        
        # TODO - use pathlib for paths?
        self.file_path = f"{self.config['working_dir']}\\gtfs-nl\\{self.table_name}.txt"

    def drop(self):
        self.cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")

    def create(self):
        self.cursor.execute(self.create_sql)
        for index_sql in self.index_sql_list:
            self.cursor.execute(index_sql)

    def drop_and_insert(self):
        self.drop()
        self.create()
        self.cursor.execute(self.insert_sql)

    def create_and_load_if_newer(self):
        self.create()
        if self.needs_load():
            self.load_table()

    # Function to check if a table needs to be loaded
    def needs_load(self):
        self.cursor.execute("SELECT last_updated FROM metadata WHERE table_name = ?", (self.table_name,))
        row = self.cursor.fetchone()
        if row is None:
            return True  # Table has never been loaded
        last_updated = row[0]
        file_mtime = int(os.path.getmtime(self.file_path))
        return file_mtime > last_updated
    
    def load_table(self):
        with open(self.file_path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            self.cursor.execute(f"DELETE FROM {self.table_name}")
            self.cursor.executemany(self.insert_sql, reader)
        file_mtime = int(os.path.getmtime(self.file_path))
        self.cursor.execute("""
        INSERT OR REPLACE INTO metadata (table_name, last_updated)
        VALUES (?, ?)
        """, (self.table_name, file_mtime))