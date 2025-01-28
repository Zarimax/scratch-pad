from base import Base

class Tracker(Base):

    def __init__(self, config):
        super().__init__(config)

    def get_arrival_times(self, feed, trip_id_list):
        arrival_times = []
        matching_records = []

        for entity in feed.entity:
            if hasattr(entity, 'vehicle') and entity.vehicle.trip.trip_id in trip_id_list:
                matching_records.append(entity)

        # TODO - remove debug Print the matching records
        for record in matching_records:
            print(record)

        # TODO - calculate arrival times

        return arrival_times