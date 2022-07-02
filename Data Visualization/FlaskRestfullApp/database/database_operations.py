from traceback import print_exc
from .db_connection import DB_Conn

class DB_Operations(object):

    def __init__(self):
        self.client = DB_Conn.get_client()

    def exists_db(self, db_name):
        dbs = self.get_dbs()    
        if db_name in dbs:
            return True
        else:
            return False

    def get_dbs(self):    
        try:
            databases = self.client.get_list_database()
        except Exception:
            print_exc()
        dbs = [key['name'] for key in databases] 

        return dbs