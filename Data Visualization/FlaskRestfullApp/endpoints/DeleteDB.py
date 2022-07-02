from flask_restful import Resource, reqparse
from utils.param_check import check_params
from database.db_ops_delete import DB_Ops_Delete

class DeleteDB(Resource):

    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('db_name', type=str, help='Name of the database')
        self.db_delete = DB_Ops_Delete()
        super(DeleteDB, self).__init__()

    def post(self):
        args = self.reqparser.parse_args()
        params_check_result = check_params(['db_name'], args)
        if params_check_result[0] is False:
            return params_check_result[1]
        db_name = args['db_name']   
        result = self.db_delete.delete_db(db_name)

        return str(result)
