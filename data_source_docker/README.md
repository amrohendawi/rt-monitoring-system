# Data Source (C) and Data Sender (Python)

data_source runs cyclictest at high priority to aggrigate latency timeseries, format the data and then send it to the Flask RestFul API server using data_sender.py

### Installation

simply call the following
1. `git clone https://gitlab.fokus.fraunhofer.de/iiot/tub-projects/ws1920_sourcing_aggregation/tree/data_source`
2. `sudo Docker build .`
3. `docker run -p 8080:8080 "docker-ID"`
