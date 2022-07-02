from flask import Flask
from flask_restful import Api

from endpoints.NewDB import NewDb
from endpoints.GetDBs import GetDBs
from endpoints.DeleteDB import DeleteDB
from endpoints.GetMeasurements import GetMeasurements
from endpoints.WriteReadData import WriteReadData
from endpoints.ReadLastEntries import ReadLastEntries
from endpoints.Criteria import Criteria
from endpoints.Query import Query

app = Flask(__name__)
api = Api(app)

api.add_resource(NewDb, '/newdb')
api.add_resource(GetDBs, '/getdbs')
api.add_resource(DeleteDB, '/deletedb')
api.add_resource(GetMeasurements, '/getmeasurements')
api.add_resource(WriteReadData, '/writereaddata')
api.add_resource(ReadLastEntries, '/readlastentries')
api.add_resource(Criteria, '/criteria')
api.add_resource(Query, '/query')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4545)