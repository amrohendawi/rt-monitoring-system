from .db_connection import DB_Conn
from .database_operations import DB_Operations
from traceback import print_exc

class DB_Ops_Read(DB_Operations):

    def __init__(self):
        self.client = DB_Conn.get_client()

    def read_data(self, db_name, measurement):
        # TODO: Prevent the usage of this endpoint as it is not performant
        # query_all_table = 'SELECT * FROM ' + measurement
        query_all_table = 'SELECT * FROM ' + measurement + ' LIMIT 100' # TODO: Delete this line later, and uncomment the above one
        if(not self.exists_db(db_name)):
            return "Such a database does not exist!"

        try:
            data = self.client.query(query_all_table, database=db_name)
        except Exception:
            print_exc()
        data = list(data.get_points())

        return data
