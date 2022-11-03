from .database_operations import DB_Operations
from .db_connection import DB_Conn
from time import time_ns
from copy import deepcopy
from traceback import print_exc

class DB_Ops_Write(DB_Operations):
    def __init__(self):
        self.client = DB_Conn.get_client()

    def write_data(self, data_points, db_name):
        data = data_points['data']
        data = self._seperate_values(data)
        try:
            result = self.client.write_points(data, batch_size=10000, protocol=u'json', database=db_name)
        except Exception:
            print_exc()

        return result

    def _seperate_values(self, data):
        objects = []
        measurement = data[0]['measurement']
        tags = data[0]['tags']
        values = data[0]['fields']['values']
        for val in range(len(values)):
            data_point = {
                "measurement": measurement,
                "tags": tags,
                "time": time_ns(),
                "fields": {
                    "slot": val,
                    "value": values[val],
                }
            }
            objects.append(deepcopy(data_point))
        return objects
