from .database_operations import DB_Operations
from traceback import print_exc
from .db_connection import DB_Conn

class DB_Ops_Create(DB_Operations):

    def __init__(self):
        self.client = DB_Conn.get_client()

    def create_db(self, db_name):
        if self.exists_db(db_name):
            return "DB already exists!"
        try:
            self.client.create_database(db_name)
        except Exception:
            print_exc()

        return "A new db with the name " + db_name + " created"


