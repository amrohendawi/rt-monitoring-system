from flask import request
from flask_restful import Resource, reqparse
from utils.param_check import check_params
from traceback import print_exc
from database.db_ops_write import DB_Ops_Write
from database.db_ops_read import DB_Ops_Read

class WriteReadData(Resource):

    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('db_name', type=str, help='Name of the database')
        self.reqparser.add_argument('measurement', type=str, help='Name of the measurement')
        self.reqparser.add_argument('data', type=str, location='json')

        self.db_write = DB_Ops_Write()
        self.db_read = DB_Ops_Read()

        super(WriteReadData, self).__init__()

    def post(self):
        args = self.reqparser.parse_args()

        params_check_result = check_params(['db_name'], args)
        if params_check_result[0] is False:
            return params_check_result[1]

        db_name = args['db_name']
        json_data = request.get_json()
        result = False

        try:
            result = self.db_write.write_data(json_data, db_name)
        except:
            print_exc()

        if result is not True:
            return str(result)

        return True

    def get(self):

        args = self.reqparser.parse_args()
        db_name = args['db_name']
        measurement = args['measurement']

        params_check_result = check_params(['db_name', 'measurement'], args)
        if params_check_result[0] is False:
            return params_check_result[1]


        try:
            result = self.db_read.read_data(db_name, measurement)
        except Exception:
            print_exc()
            raise Exception

        return result
