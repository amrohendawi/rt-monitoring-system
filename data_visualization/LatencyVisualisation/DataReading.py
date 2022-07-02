import time
import requests as req
# import prin
from traceback import print_exc

class DataReading(object):
    def __init__(self):
        super()

    def periodic_reading(self, db_name, measurement, period):
        current_time = time.time_ns()
        payload = {'db_name': db_name, 'measurement': measurement,
                'period': period, 'current_time': current_time}
        try:
            # TODO: After finishin filter implementation, use URL for the following request
            latest_entries = req.get(
                'http://rest_api:4545/readlastentries', params=payload)
        except Exception:
            print_exc()
            raise Exception

        return latest_entries
