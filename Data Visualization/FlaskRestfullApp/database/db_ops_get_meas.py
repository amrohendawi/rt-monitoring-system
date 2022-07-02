from .database_operations import DB_Operations
from .db_connection import DB_Conn
from traceback import print_exc

class DB_Ops_Get_Measurements(DB_Operations):

    def __init__(self):
        self.client = DB_Conn.get_client()

    def get_measurements(self, db_name):
        measurement_query = 'SHOW MEASUREMENTS'
        try:
            result = self.client.query(measurement_query, database=db_name)
            measurements = list(result.get_points())
        except Exception:
            print_exc()
        measurements = [key['name'] for key in measurements]

        return measurements
    