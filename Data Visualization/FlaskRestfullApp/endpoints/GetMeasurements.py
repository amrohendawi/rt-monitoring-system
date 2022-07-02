from flask_restful import Resource, reqparse
from utils.param_check import check_params
from database.db_ops_get_meas import DB_Ops_Get_Measurements

class GetMeasurements(Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('db_name', type=str, help='Name of the database')
        self.get_meas = DB_Ops_Get_Measurements()
        super(GetMeasurements, self).__init__()

    def get(self):
        args = self.reqparser.parse_args()
        params_check_result = check_params(['db_name'], args)
        if params_check_result[0] is False:
            return params_check_result[1]

        db_name = args['db_name']
        result = self.get_meas.get_measurements(db_name)

        return result
