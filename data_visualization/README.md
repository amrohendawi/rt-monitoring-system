# Data Storage Rest API with Influx

You can store your data with the help of this RestFul API into InfluxDB.


### Installation

That is the hardest part of all. That's gonna take a very long fight with you and your terminal, so better let's get started immediately.

1. `git clone https://gitlab.fokus.fraunhofer.de/iiot/tub-projects/ws1920_sourcing_aggregation/tree/data_forw`
2. `cd Data-Storage-with-Influx/`
3. `docker-compose up`

and that's it!! 

## How to use this RestFul API:

There are 4 endpoints that the api offers. These are:
1. /newdb
2. /getdbs
3. /deletedb
4. /writereaddata

## 1. New DB
You can create a new database with this. A sample request looks like this:

* URL: `http://localhost:4545/newdb?db_name=mynewdb`
* Method: Post
* Params: db_name
* Response:

If there is not any db with the same name
```
"A new db with the name mynewdb created"
```
else there is already a db with exact same name
```
"DB already exists!"
```
  
## 2. Get DBs
You get the list of existing databases. A sample might look like following:

* URL: `http://localhost:4545/getdbs`
* Method: Get
* Params: None

Example: http://localhost:4545/getdbs`
```
{
    "Existing Databases": [
        "_internal",
        "example",
        "mynewdb"
    ]
}
```


## 3. Delete DB

You can delete an unnecessary database. 

* URL: `http://localhost:4545/deletedb`
* Method: Post
* Params: db_name

Example: http://localhost:4545/deletedb?db_name=mydb3

If successful
```
"Database deleted successfully" 
```
else:
```
`"DB does not exist!"`
```

## 4. Writing and Reading Data

You can write data to or read from the database. 

### 4.1 Writing Data
To write some data, use the following scheme.

* Method: Post
* Url: http://localhost:4545/writereaddata
* Params: db_name, measurement
* Response: 

Example: http://localhost:4545/writereaddata?db_name=mydb2&measurement=machine_1
If successful:
```
true
```
else:
```
"Something went wrong during the write process!"
```
Content-Type: `application/json`

Body:
```
{
	"data": [
		{
			"measurement": "lat",
			"tags": {
				"cpu": "2",
				"priority": "80",
				"interval": "1000"
			},
			"fields": {
				"values": [
					11,
					22,
					33,
					44,
					55
				]
			}
		}
	]
}
```


### 4.2 Reading Data
To read all the data in the database, use the following scheme.

URL: `http://localhost:4545/writereaddata?db_name=mydb&measurement=lat_vals`

* Method: Get
* Url: http://localhost:4545/writereaddata
* Params: db_name, measurement

Response: 

If successful
```
[
{
    "time": "2020-02-05T18:05:17.7848789Z",
    "cpu": "6",
    "interval": "1000",
    "priority": "86",
    "slot": 0,
    "value": 6
},
{
    "time": "2020-02-05T18:05:17.7849786Z",
    "cpu": "6",
    "interval": "1000",
    "priority": "86",
    "slot": 1,
    "value": 18
}
]
```
else if no result is found:
```
[]
```

### 5. Measurement List
To get the list of measurements in a database

URl: `http://localhost:4545/getmeasurements?db_name=mydb`

* Method: Get
* Url: http://localhost:4545/getmeasurements
* Params: db_name

If successful:
```
[
    "lat",
    "lat_vals"
]
```
else if there is no result found:
```
[]
```

### 6. Getting Criteria
To get the list of the criteria

URL: `http://localhost:4545/criteria?db_name=mydb&measurement=lat_vals`

* Method: Get
* Url: http://localhost:4545/criteria
* Params: db_name, measurement

 If successful:
```
{
    "cpu": [
        "2",
        "4"
    ],
    "priority": [
        "80",
        "81",
        "82",
        "83",
    ],
    "interval": [
        "1000",
        "800"
    ]
} 
```
else:
```    
{
    "cpu": [],
    "priority": [],
    "interval": []
}
```

### 7. Sending Custom Query
To send your custom query, this endpoint can be used.


* Method: Get
* Url: http://localhost:4545/query
* Params: db_name, measurement, query

URL: http://localhost:4545/query?db_name=mydb&measurement=lat_vals&query=SELECT * FROM lat_vals WHERE cpu='4'

If successful:
```
[
    {
        "time": "2020-02-05T18:05:22.9378349Z",
        "cpu": "4",
        "interval": "800",
        "priority": "84",
        "slot": 0,
        "value": 93
    },
    {
        "time": "2020-02-05T18:05:22.9378997Z",
        "cpu": "4",
        "interval": "800",
        "priority": "84",
        "slot": 1,
        "value": 100
    }
]
```
else if not found any result:
```
[]
```