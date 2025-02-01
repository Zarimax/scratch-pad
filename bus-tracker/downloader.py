import requests

from base import Base

# FeedMessage is the message class generated from the gtfs-realtime.proto schema
# This schema must be available and compiled beforehand for the code to work
from gtfs_realtime_pb2 import FeedMessage
from datetime import datetime, timedelta, timezone
import time


class Downloader(Base):

    def __init__(self, config):
        super().__init__(config)
        self.data = None
        self.last_request = None
        self.rate_limit = 60 # seconds
        self.previous_etag = None
        self.previous_last_modified = None


    def do_request(self, url, headers):
        if self.last_request:
            wait_time = self.rate_limit - (datetime.now(timezone.utc) - self.last_request).total_seconds()
            if wait_time > 0:
                self.logger.info(f"Downloader - rate limit hit. waiting {wait_time} seconds")
                time.sleep(wait_time)
        
        response = requests.get(url, headers=headers)
        self.last_request = datetime.now(timezone.utc)
        return response

    def get_full_data(self):
        pass

    def get_realtime_data(self):
        # URL of the GTFS .pb file
        url = "http://gtfs.ovapi.nl/nl/vehiclePositions.pb"
        headers = {
            "User-Agent": "MyGTFSClient/1.0 (rick.suter@gmail.com)",
        }

        if self.previous_etag:
            headers["If-None-Match"] = self.previous_etag
        if self.previous_last_modified:
            headers["If-Modified-Since"] = self.previous_last_modified

        # Fetch the .pb file
        response = self.do_request(url, headers=headers)

        # TODO - need more error handling for more failure states?
        if response.status_code == 304:
            self.logger.info("Downloader - Data has not changed since last fetch")
        else:
            self.data = response.content
            self.logger.info("Downloader - Data downloaded successfully")
            
            # Save ETag and Last-Modified headers for future requests
            if "ETag" in response.headers:
                self.previous_etag = response.headers["ETag"]
            if "Last-Modified" in response.headers:
                self.previous_last_modified = response.headers["Last-Modified"]

            self.logger.info(f"Downloader - etag: {self.previous_etag} last_modified: {self.previous_last_modified}")

        return self.parse_data_to_feed(self.data)

    def parse_data_to_feed(self, data):
        # Decode the protobuf data using the FeedMessage format
        feed = FeedMessage()
        feed.ParseFromString(data)
        
        return feed