## Data-source module

data_source runs cyclictest at high priority to aggrigate latency timeseries, formats the data and then sends it to the Flask RestFul API server using data_sender.py
It also has a seperation mechanism between the RT-task(cyclictest) and the NRT-task(data_sender) to make sure they don't collidate during work.

## Installation

simply call the following
1. `git clone https://gitlab.fokus.fraunhofer.de/iiot/tub-projects/ws1920_sourcing_aggregation/tree/data_source`
2. `cd data_source`
then make sure all project dependencies are available by calling:
3. `chmod +x install_prerequisites.sh && ./install_prerequisites.sh`
finally run the data_source by executing:
4. `chmod +x RUNME.sh && ./RUNME.sh`

## cyclictest
cyclictest is an open-source rt-tests program that measures latency(endtime - starttime) of a certain task.
it offers many options to customize the latency test such as setting number of CPU cores, test duration, scheduling priority, output shape etc.
it has been slightly modified for to match the project's goals.

## data_sender
this is a pretty straightforward http client, that sends latency timeseries packed in json format specified by the Flask RestFul API.




