from .database_operations import DB_Operations
from .db_connection import DB_Conn
from traceback import print_exc

class DB_Ops_Query(DB_Operations):

    def __init__(self):
        self.client = DB_Conn.get_client()


    def query(self, db_name, measurement, query):
        if(not self.exists_db(db_name)):
            return 'The given database doesn\'t exist!'
        try:
            r = self.client.query(query, database=db_name)
        except:
            print_exc()
            raise Exception

        return list(r.get_points())
