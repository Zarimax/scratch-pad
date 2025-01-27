# protobuf==3.19.6 w/ backported builder.py from latest version
#  installed to C:\ProgramData\Anaconda3\Lib\site-packages\google\protobuf\internal
# gtfs_realtime_pb2.py generated with protoc-22.0-win64
# http://gtfs.ovapi.nl/nl/

import sqlite3
import requests
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf import message
import io

# from http://gtfs.ovapi.nl/README:
# 1) Identify in the User-Agent header who you are, this helps us to contact you. This 
# ultimately allows us to offer this service without registration and contact you in 
# case of wrong doing.
# 2) Implement HTTP Headers such as If-Modified-Since and/or If-None-Match if your 
# implementation thinks we offer updates more frequently than once a minute, and you 
# want to implement the Niquist-frequency.
# 3) We rarely update our schedules more than daily and our new operational day starts 
# at 03AM UTC. We take special measurements to maximize the stability of trip_ids 
# between schedules to assure a grace period.

# METADATA PROCESSING
# Once per day at some random interval between 2am and 4am:
# get metadata from http://gtfs.ovapi.nl/nl/gtfs-nl.zip (if modified since last run)
# unzip and load into sqllite

# - Take these parameters:
#    begin_stop_name: "Haarlem, Emmaplein"
#    end_stop_name: "Haarlem, Centrum/Houtplein"
# - translate stop names into stop_id lists with [stops.txt]
# - get all trip_id from [stop_times.txt] where a begin.stop_id is followed by an end.stop_id (handle none)

# REAL-TIME PROCESSING
# Once per minute during wake hours
# get metadata from http://gtfs.ovapi.nl/nl/vehiclePositions.pb (if modified since last run)
# - extract data for the target trip_id (handle none)
# - filter to where current_stop_sequence <= stop_sequence containing begin.stop_id
# - estimate bus arrival time = 
#     begin.stop_id.arrival_time - 
#     timestamp +
#     difference between timestamp and current time +
#     off_schedule_minutes

# TODO - algorithm for calculating off_schedule_minutes, (both early and late)
#   if current_stop_sequence.arrival_time >= timestamp >= previous_stop_sequence.departure_time
#      off_schedule_minutes = 0  # bus is ontime
#   else
#      find the most recent departure time in the past where timestamp > departure time
#      calculate the difference between current_stop_sequence.arrival_time 

# stops.txt
# stop_id,stop_code,stop_name,stop_lat,stop_lon,location_type,parent_station,stop_timezone,wheelchair_boarding,platform_code,zone_id
# 2749450,55002150,"Haarlem, Emmaplein",52.3751,4.621665,0,stoparea:456026,,1,,CXX:ScheduledStopPoint:55002150
# 2749453,55002200,"Haarlem, Emmaplein",52.375011,4.621784,0,stoparea:456026,,1,,CXX:ScheduledStopPoint:55002200
# 2905198,55000120,"Haarlem, Centrum/Houtplein",52.374971,4.631007,0,,,1,,
# 2905199,55000151,"Haarlem, Centrum/Houtplein",52.373662,4.630046,0,,,1,,
# 2745604,55000120,"Haarlem, Centrum/Houtplein",52.374916,4.630788,0,stoparea:454980,,1,,CXX:ScheduledStopPoint:55000120
# 2745605,55000150,"Haarlem, Centrum/Houtplein",52.374723,4.630248,0,stoparea:454980,,1,,CXX:ScheduledStopPoint:55000150
# 2745606,55000151,"Haarlem, Centrum/Houtplein",52.373932,4.630085,0,stoparea:454980,,1,,CXX:ScheduledStopPoint:55000151

# stop_times.txt
# trip_id,stop_sequence,stop_id,stop_headsign,arrival_time,departure_time,pickup_type,drop_off_type,timepoint,shape_dist_traveled,fare_units_traveled
# 273844192,12,2749452,,08:09:00,08:09:00,0,0,0,7418,7415
# 273844192,13,2749453,,08:10:00,08:10:00,0,0,0,7818,7815
# 273844192,14,2745605,,08:11:00,08:11:00,0,0,0,8550,8547
# 273844194,12,2749452,,08:43:00,08:43:00,0,0,0,7418,7415
# 273844194,13,2749453,,08:44:00,08:44:00,0,0,0,7818,7815
# 273844194,14,2745605,,08:46:00,08:46:00,0,0,0,8550,8547

# DISPLAY
# Simulator for: Medium 16x32 RGB LED matrix panel - 6mm Pitch ???
# color turns to red if not enough time?
# ping LED when refreshing real-time data.
# ping multiple LEDs when refreshing metadata.
# make a sad face for errors + error code

"""
id: "2025-01-05:CXX:N080:7509"      
vehicle {
  trip {
    trip_id: "273844194"
    start_time: "08:27:00"
    start_date: "20250105"
    schedule_relationship: SCHEDULED
    route_id: "107775"
    direction_id: 0
  }
  position {
    latitude: 52.36516189575195
    longitude: 4.551567077636719
  }
  current_stop_sequence: 4
  current_status: IN_TRANSIT_TO
  timestamp: 1736062289
  stop_id: "2749734"
  vehicle {
    label: "3215"
  }
}
"""

db_file = r"C:\Users\Black Beast\Desktop\bus-tracker\transit_data.db"

# Create or connect to the SQLite database on disk
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute("SELECT DISTINCT trip_id FROM matching_trips")
matching_records = cursor.fetchall()
trip_id_list = [record[0] for record in matching_records]

# URL of the GTFS .pb file
url = "http://gtfs.ovapi.nl/nl/vehiclePositions.pb"

# Fetch the .pb file
response = requests.get(url)
data = response.content

# Parse the protobuf data
# Assuming FeedMessage is the message class generated from the gtfs-realtime.proto schema
# This schema must be available and compiled beforehand for the code to work
from gtfs_realtime_pb2 import FeedMessage

# Decode the protobuf data using the FeedMessage format
feed = FeedMessage()
feed.ParseFromString(data)

# Search for records containing the matching trip_id
matching_records = []

for entity in feed.entity:
    if hasattr(entity, 'vehicle') and entity.vehicle.trip.trip_id in trip_id_list:
        matching_records.append(entity)

# Print the matching records
for record in matching_records:
    print(record)