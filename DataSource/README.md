# Data Source (C) and Data Sender (Python)

data_source runs cyclictest at high priority to aggrigate latency timeseries, formats the data and then sends it to the Flask RestFul API server using data_sender.py
It also has a seperation mechanism between the RT-task(cyclictest) and the NRT-task(data_sender) to make sure they don't collidate during work.

## Local running

simply call the following
1. `git clone https://github.com/amrohendawi/rt-performance-monitoring`
2. `cd Data Source`
then make sure all project dependencies are available by calling:
3. `chmod +x install_prerequisites.sh && ./install_prerequisites.sh`
4. finally run the data_source by executing:
    `chmod +x RUNME.sh && ./RUNME.sh`

In case of failure probably some dependencies aren't automatically installed.
In this case Please open install_prerequisites.sh and install the listed packages manually.

## Running on docker

simply call the following

```
git clone https://github.com/amrohendawi/rt-performance-monitoring
cd Data Source
sudo Docker build .
docker run -p 8080:8080 "docker-ID"
```

## cyclictest

cyclictest is an open-source rt-tests program that measures latency of a certain task.
it offers many options to customize the latency test such as setting number of CPU cores, test duration, scheduling priority, output shape etc.
it has been modified and merged with newly implemented part to match the project's goals.

The cyclictest version in this project is still independent from the rest of the project parts.
That means you can call cyclictest for various types of tests other that the default routine called by data_source.c

## data_sender

this is a pretty straightforward http client, that sends latency timeseries packed in json format specified by the Flask RestFul API to the data forwarding module.
