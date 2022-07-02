from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import threading
import time
from flask import Flask, request
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from traceback import print_exc
import requests as req
import json
import sys

from DataReading import DataReading
from DataPreparation import DataPreparation
from RequestPreparation import RequestPreparation

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
DB_NAME = 'mydb'
MEASUREMENT = 'lat_vals'
PERIOD = 5 # 1 sec
URL = 'http://rest_api:4545'

server = Flask(__name__)

# TODO: Put a label while loading data to indicate whether data is coming or no data found

data_reading = DataReading()
data_preparation = DataPreparation()
request_preparation = RequestPreparation(DB_NAME, MEASUREMENT)

app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dash/',
    external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([      
        dcc.Graph(
            id='real-time'
        ),
        dcc.Interval(
            id='interval-component',
            interval=1000*PERIOD,
            n_intervals=0
        )
    ]),
    html.Div([
        dcc.Graph(id="filtered"),
        html.Div([
            dcc.Dropdown(
                id='cpu-tbd',
                placeholder="Cpu"
            )]),
        html.Div([
            dcc.Dropdown(
                id='priority-tbd',
                placeholder="Priority"
            )]),
        html.Div([
            dcc.Dropdown(
                id='interval-tbd',
                placeholder="Interval"
            )])
        ,
        html.Button(id='update-button', children='Submit', n_clicks=0),
        ])
    ])

#This updates the data of the real time graph
@app.callback(Output(component_id='real-time', component_property='figure'),
              [Input('interval-component', 'n_intervals')])
def update_data(n_clicks):
    try:
        data = data_reading.periodic_reading(DB_NAME, MEASUREMENT, PERIOD)  # data as string
        data = json.loads(data.text)  # data as json
        data_as_graph = data_preparation.transform_data_into_graph(data)
    except Exception:
        print_exc()
    return data_as_graph

def isFilterEmpty(f_cpu, f_priority, f_interval):
    if f_cpu is None and f_interval is None and f_priority is None:
        return True
    else:
        return False

# this function displays the data set based on the filter results that are entered by the user
@app.callback(Output(component_id='filtered', component_property='figure'),
              [Input(component_id='update-button', component_property='n_clicks')],
              [State(component_id='cpu-tbd', component_property='value'),
              State(component_id='priority-tbd', component_property='value'),
              State(component_id='interval-tbd', component_property='value')])
def display_filtered_data(btn_clicks, f_cpu, f_priority, f_interval):
    if isFilterEmpty(f_cpu, f_priority, f_interval):
        return data_preparation.transform_empty_data_into_graph([[], []])

    filters = [ { 'cpu': f_cpu }, 
                { 'priority': f_priority }, 
                {'interval' : f_interval }
            ]
    params = request_preparation.prepare_request(filters)
    try:
        data = req.get(URL+'/query', params=params) # Receive the response and then convert it to JSON
        data = json.loads(data.text)
    except Exception:
        print_exc()
        raise Exception

    data_as_graph = data_preparation.transform_data_into_graph(data)
    return data_as_graph

# Update the content of the filters
@app.callback([Output(component_id='cpu-tbd', component_property='options'),
              Output(component_id='priority-tbd', component_property='options'),
              Output(component_id='interval-tbd', component_property='options')],
                [Input(component_id='interval-component', component_property='n_intervals')])
def loadFilterContent(n):
    try:
        criteria = req.get(URL+'/criteria', params={'db_name': DB_NAME, 'measurement': MEASUREMENT})
        criteria = criteria.json()
    except Exception:
        print_exc()
 
    cpu = [{'label': i, 'value': i} for i in criteria['cpu']]
    priority = [{'label': i, 'value': i} for i in criteria['priority']]
    interval = [{'label': i, 'value': i} for i in criteria['interval']]

    return cpu, priority, interval

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8050)
