from influxdb import InfluxDBClient
from traceback import print_exc
from copy import deepcopy
from time import time_ns

HOST = 'db'
PORT = 8086
USERNAME = 'root'
PASSWORD = 'root'
DB = 'mydb'
# client = InfluxDBClient(host='db', port=8086, username='root', password='root', database='example')
client = InfluxDBClient(host='db', port=PORT, username=USERNAME, password=PASSWORD, database=DB)


def create_db(db_name):

    # Just to get the name of the databases, insead of a another data structure
    dbs = get_dbs()
    
    if db_name in dbs:
        return "Already exists"

    try:
        client.create_database(db_name)
    except Exception:
        print_exc()

    return "A new db with the name " + db_name + " created"

def get_dbs():
    try:
        databases = client.get_list_database()
    except Exception:
        print_exc()


    dbs = [key['name'] for key in databases] 
    return dbs

def delete_db(db_name):
    
    # check whether the db already exits
    dbs = get_dbs()
    if db_name not in dbs:
        return "DB does not exist!"
    
    try:
        client.drop_database(db_name)
    except Exception:
        print_exc()
    
    return "Database deleted successfully"

def write_data(data_points, db_name):
    data = data_points['data']
    data = _seperate_values(data)
    try:
        result = client.write_points(data, batch_size=10000, protocol=u'json', database=db_name)
    except Exception:
        print_exc()

    return result

def read_data(db_name, measurement):
    # TODO: Prevent the usage of this endpoint as it is not performant
    # query_all_table = 'SELECT * FROM ' + measurement
    query_all_table = 'SELECT * FROM ' + measurement + ' LIMIT 100' # TODO: Delete this line later, and uncomment the above one

    if db_name not in get_dbs():
        return "Such a database does not exist!"

    try:
        data = client.query(query_all_table, database=db_name)
    except Exception:
        print_exc()

    data = list(data.get_points())

    return data

def get_measurements(db_name):

    measurement_query = 'SHOW MEASUREMENTS'

    try:
        result = client.query(measurement_query, database=db_name)
        measurements = list(result.get_points())
    except Exception:
        print_exc()

    measurements = [key['name'] for key in measurements]

    return measurements

def read_latest_entries(db_name, measurement, period, current_time):

    query_latest_period = 'SELECT * FROM {} WHERE time < {} AND time >= {}'.format(measurement, str(current_time), str(current_time-period))
    if db_name not in get_dbs():
        return "Such a database does not exist!"

    try:
        data = client.query(query_latest_period, database=db_name)
    except:
        print_exc()
    # TODO: Try deleting the below line to see whether it really is necessary or not.
    points = list(data.get_points())
    # print('The format of the previous read request: ', points)
    return points

# Put multiple values into seperate objects to write into db
def _seperate_values(data):
    objects = [] # contains the parsed values
    measurement = data[0]['measurement']
    tags = data[0]['tags']
    values = data[0]['fields']['values']
    # creates a new object for each value in the tag so that it can be sent to db
    for val in range(len(values)):
        # pairing function is used to create a unique index from the two values
        pair = 1/2 * (val + values[val]) * (val + values[val] + 1) + values[val]
        # add the pair to the tags so that they do not overlap in the database
        data_point = {
            "measurement": measurement,
            "tags": tags,
            "time": time_ns(),
            "fields": {
                "slot": val, # slot represents here the index of the value that it resides
                "value": values[val],
                "unique_pair": pair
            }
        }
        objects.append(deepcopy(data_point)) # Append the new object to the list
    return objects

    #  An incoming object sample
    # {
    # 	"data": [
    # 		{
    # 			"measurement": "lat_vals",
    # 			"tags": {
    # 				"cpu": "2",
    # 				"priority": "80",
    # 				"interval": "1000"
    # 			},
    # 			"fields": {
    # 				"values": [
    # 					34,
    # 					12,
    # 					66,
    # 					93
    # 				]
    # 			}
    # 		}
    # 	]
    # }

def read_criteria(db_name, measurement):
    data = {}

    # query_unique_timestamps = 'SELECT "slot", "value", "cpu" FROM ' + measurement
    # query_unique_timestamps = 'SELECT "slot", "value", "cpu" FROM ' + measurement
    query_unique_cpu = "SHOW TAG VALUES FROM " + measurement + " WITH KEY = \"cpu\""
    query_unique_priority = "SHOW TAG VALUES FROM " + measurement + " WITH KEY = \"priority\""
    query_unique_interval = "SHOW TAG VALUES FROM " + measurement + " WITH KEY = \"interval\""


    try:
        # unique_timestamps = client.query(query_unique_timestamps, database=db_name)
        unique_cpus = client.query(query_unique_cpu, database=db_name)
        unique_intervals = client.query(query_unique_interval, database=db_name)
        unique_priorities = client.query(query_unique_priority, database=db_name)
    except Exception:
        print_exc()
        raise Exception

    # time_stamps = list(set([t['time'] for t in list(unique_timestamps.get_points())])) # set is used to delete the duplicates in the list
    cpus = [c['value'] for c in list(unique_cpus.get_points())]
    priorities = [c['value'] for c in list(unique_priorities.get_points())]
    intervals = [c['value'] for c in list(unique_intervals.get_points())]

    # data['time'] = time_stamps
    data['cpu'] = cpus
    data['priority'] = priorities
    data['interval'] = intervals

    return data

def query(db_name, measurement, query):
    try:
        r = client.query(query, database=db_name)
    except:
        print_exc()
        raise Exception

    return list(r.get_points())

def read_last_entries(db_name, measurement):
    latest_entries_query = "SELECT * FROM {} ORDER BY time DESC LIMIT {}".format(measurement, 1000)
    
    try:
        latest_entries = query(db_name, measurement, latest_entries_query)

    except Exception:
        print_exc()
        raise Exception

    return latest_entries