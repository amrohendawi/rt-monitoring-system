from flask_restful import Resource
from database.database_operations import DB_Operations

class GetDBs(Resource):

    def __init__(self):
        self.db_ops = DB_Operations()
        super(GetDBs, self).__init__()

    def get(self):
        dbs = self.db_ops.get_dbs()
        return {"Existing Databases": dbs}
