import requests
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf import message
import io

from base import Base

class Downloader(Base):

    def __init__(self, config):
        super().__init__(config)
        # TODO - rate limit

    def get_full_data(self):
        pass

    def get_realtime_data(self):
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
        
        return feed