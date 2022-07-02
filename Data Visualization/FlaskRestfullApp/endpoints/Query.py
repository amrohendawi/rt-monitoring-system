from flask_restful import Resource, reqparse
from utils.param_check import check_params
from traceback import print_exc
# from database.db import query
from database.db_ops_query import DB_Ops_Query

class Query(Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('db_name', type=str, help='Name of the database')
        self.reqparser.add_argument('measurement', type=str, help='Name of the measurement')
        self.reqparser.add_argument('query', type=str)
        self.db_query = DB_Ops_Query()
        super(Query, self).__init__()

    def get(self):
        args = self.reqparser.parse_args()
        db_name = args['db_name']
        measurement = args['measurement']
        query_str = args['query']

        params_check_result = check_params(['db_name', 'measurement', 'query'], args)
        if params_check_result[0] is False:
            return params_check_result[1]

        try:
            r = self.db_query.query(db_name, measurement, query_str)
        except Exception:
            print_exc()
            raise Exception
        return r
