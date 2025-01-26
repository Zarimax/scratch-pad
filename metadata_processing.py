import sqlite3
import csv
import os

# File paths
stops_file = r"C:\Users\Black Beast\Desktop\gtfs-nl\stops.txt"
stop_times_file = r"C:\Users\Black Beast\Desktop\gtfs-nl\stop_times.txt"
db_file = r"C:\Users\Black Beast\Desktop\transit_data.db"

# Create or connect to the SQLite database on disk
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute("""
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
""")

cursor.execute("""
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
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS metadata (
    table_name TEXT PRIMARY KEY,
    last_updated INTEGER
)
""")

# Function to check if a table needs to be updated
def needs_update(table_name, file_path):
    cursor.execute("SELECT last_updated FROM metadata WHERE table_name = ?", (table_name,))
    row = cursor.fetchone()
    if row is None:
        return True  # Table has never been updated
    last_updated = row[0]
    file_mtime = int(os.path.getmtime(file_path))
    return file_mtime > last_updated

# Function to update a table and set its last_updated metadata
def update_table(table_name, file_path, insert_query):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        cursor.execute(f"DELETE FROM {table_name}")
        cursor.executemany(insert_query, reader)
    file_mtime = int(os.path.getmtime(file_path))
    cursor.execute("""
    INSERT OR REPLACE INTO metadata (table_name, last_updated)
    VALUES (?, ?)
    """, (table_name, file_mtime))

# Load stops table if necessary
if needs_update("stops", stops_file):
    update_table("stops", stops_file, """
    INSERT INTO stops (
        stop_id, stop_code, stop_name, stop_lat, stop_lon, location_type,
        parent_station, stop_timezone, wheelchair_boarding, platform_code, zone_id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """)

# Load stop_times table if necessary
if needs_update("stop_times", stop_times_file):
    update_table("stop_times", stop_times_file, """
    INSERT INTO stop_times (
        trip_id, stop_sequence, stop_id, stop_headsign, arrival_time, departure_time,
        pickup_type, drop_off_type, timepoint, shape_dist_traveled, fare_units_traveled
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """)

# Define stop names
begin_stop_name = "Haarlem, Emmaplein"
end_stop_name = "Haarlem, Centrum/Houtplein"

# Delete old matching trips data if it exists
cursor.execute("DROP TABLE IF EXISTS matching_trips")

# Create the persistent matching_trips table
cursor.execute("""
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
""")

# TODO - only load matching tables if it doesn't exist
# TODO - save result of 'SELECT stop_id FROM stops WHERE stop_name = ?'

# Populate the persistent matching_trips table
cursor.execute("""
INSERT INTO matching_trips
SELECT st3.*
FROM stop_times st3
WHERE st3.trip_id IN (
    SELECT DISTINCT st1.trip_id
    FROM stop_times st1
    JOIN stop_times st2
    ON st1.trip_id = st2.trip_id
    WHERE st1.stop_id IN (
        SELECT stop_id FROM stops WHERE stop_name = ?
    )
    AND st2.stop_id IN (
        SELECT stop_id FROM stops WHERE stop_name = ?
    )
    AND st1.stop_sequence < st2.stop_sequence
)
""", (begin_stop_name, end_stop_name))

# Check and print the contents of the persistent matching_trips table
cursor.execute("SELECT * FROM matching_trips")
matching_records = cursor.fetchall()
for record in matching_records:
    print(record)

# Commit changes and close the connection
conn.commit()
conn.close()

