from .database_operations import DB_Operations
from .db_connection import DB_Conn
from traceback import print_exc

class DB_Ops_Delete(DB_Operations):

    def __init__(self):
        self.client = DB_Conn.get_client()

    def delete_db(self, db_name):
        if(not self.exists_db(db_name)):
            return "DB does not exist!"
        try:
            self.client.drop_database(db_name)
        except Exception:
            print_exc()

        return "Database deleted successfully"
