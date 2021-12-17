FROM ubuntu:latest
ENV MYP /repo
WORKDIR ${MYP}
COPY . ${MYP}
RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils build-essential sudo
RUN apt-get -y install rt-tests
RUN apt-get install -y python3 python3-pip
RUN pip3 install requests numpy 
RUN apt-get install gcc
CMD gcc data_source.c -o data_source && ./data_source 95 5
