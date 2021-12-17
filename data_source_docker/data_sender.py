from random import randint, seed, randrange
import sys
import json
from requests import post
from time import sleep
import numpy as np
import os.path

URL = 'http://0.0.0.0:4545/writereaddata'
TIME_TO_SLEEP = 1
DB_NAME = "mydb"
MEASUREMENT = 'lat_vals'

def read_data(matrix,index):
	x = matrix[:,index].tolist()
	cpu = index
	priority = 90
	interval = randrange(800, 1000, 100)
	payload = {
		"data": [
			{ "measurement": "lat_vals", "tags": { "cpu": str(cpu), "priority": str(priority), "interval": str(interval) }, "fields": { "values": x }}
		]
	}
	return payload,np.shape(x)[0]


def send_data():
	try:
		histogram_matrix = np.loadtxt("histogram")histogram_matrix[~np.all(histogram_matrix[:,1:] == 0, axis=1)]
	except Exception:
		print("error at send_data(): please check if the file histogram is available")
	columns = np.shape(histogram_matrix)[1]
	for y in range(1,columns):
		data,data_len = read_data(histogram_matrix,y)
	try:
		r = post(URL, json=data, params={"db_name": DB_NAME, "measurement": MEASUREMENT})
	except Exception:
		print("error at send_data(): error while posting to server")
	sleep(TIME_TO_SLEEP)
	print("Data: ", data)
	print("sent %d datapoints for cpu %d" %(data_len,y))
	print("Response: ", r)
	sleep(TIME_TO_SLEEP)

if __name__ == '__main__':
    send_data()
