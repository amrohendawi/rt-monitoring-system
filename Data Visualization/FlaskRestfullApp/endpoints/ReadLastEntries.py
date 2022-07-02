from flask import jsonify
from flask_restful import Resource, reqparse
from utils.param_check import check_params
from traceback import print_exc
from database.db_ops_read_last import DB_Read_Last_Entries

class ReadLastEntries(Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('db_name', type=str, help='Name of the database')
        self.reqparser.add_argument('measurement', type=str, help='Name of the measurement')
        self.db_query = DB_Read_Last_Entries()
        super(ReadLastEntries, self).__init__()

    def get(self):
        args = self.reqparser.parse_args()
        db_name = args['db_name']
        measurement = args['measurement']

        params_check_result = check_params(['db_name', 'measurement'], args)
        if params_check_result[0] is False:
            return params_check_result[1]

        try:
            last_entries = self.db_query.read_last_entries(db_name, measurement)
        except:
            print_exc()
            raise Exception
        return jsonify(last_entries)
