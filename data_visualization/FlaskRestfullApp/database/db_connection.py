from influxdb import InfluxDBClient

HOST = 'db'
PORT = 8086
USERNAME = 'root'
PASSWORD = 'root'
DB = 'mydb'
client = InfluxDBClient(host='db', port=PORT, username=USERNAME, password=PASSWORD, database=DB)


class DB_Conn(object):

    __client = None

    @staticmethod
    def get_client():
        if DB_Conn.__client is None:
            DB_Conn()
        return DB_Conn.__client

    def __init__(self):
        if DB_Conn.__client is not None:
            raise Exception('Private Constructor')
        else:
            DB_Conn.__client = InfluxDBClient(host='db', port=PORT, username=USERNAME, password=PASSWORD, database=DB)
