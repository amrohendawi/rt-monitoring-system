from flask_restful import Resource, reqparse
from utils.param_check import check_params
from traceback import print_exc
from database.db_ops_read_crit import DB_Ops_Read_Criteria

class Criteria(Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('db_name', type=str, help='Name of the database')
        self.reqparser.add_argument('measurement', type=str, help='Name of the measurement')
        self.read_crit = DB_Ops_Read_Criteria()
        super(Criteria, self).__init__()

    def get(self):
        args = self.reqparser.parse_args()
        db_name = args['db_name']
        measurement = args['measurement']

        params_check_result = check_params(['db_name', 'measurement'], args)
        if params_check_result[0] is False:
            return params_check_result[1]

        try:
            criteria = self.read_crit.read_criteria(db_name, measurement)
        except Exception:
            print_exc()
            raise Exception
        return criteria
