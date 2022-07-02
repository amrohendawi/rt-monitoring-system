from .database_operations import DB_Operations
from .db_connection import DB_Conn
from traceback import print_exc

class DB_Read_Last_Entries(DB_Operations):

    def __init__(self):
        self.client = DB_Conn.get_client()

    def read_last_entries(self, db_name, measurement):
        latest_entries_query = "SELECT * FROM {} ORDER BY time DESC LIMIT {}".format(measurement, 1000)
        try:
            latest_entries = self.query(db_name, measurement, latest_entries_query)
        except Exception:
            print_exc()
            raise Exception

        return latest_entries        


    def query(self, db_name, measurement, query):
        if(not self.exists_db(db_name)):
            return 'The given database doesn\'t exist!'
        try:
            r = self.client.query(query, database=db_name)
        except:
            print_exc()
            raise Exception

        return list(r.get_points())