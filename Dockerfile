# install debian system (linux based system)
FROM debian:latest 

# install curl to download sysbench 
RUN apt-get update && \
        apt-get -y install curl

# install sysbench, git, gcc, unzip
RUN curl -s https://packagecloud.io/install/repositories/akopytov/sysbench/script.deb.sh | bash
RUN apt-get -y install sysbench git make gcc unzip wget lua5.1 lua5.1-dev && \
        apt-get clean
# install helpers
RUN wget https://luarocks.org/releases/luarocks-2.4.3.tar.gz && tar zxpf luarocks-2.4.3.tar.gz && cd luarocks-2.4.3 && ./configure && make bootstrap
COPY ./benchmark.sh ./
CMD ["chmod +x benchmark.sh"]
CMD ["./benchmark.sh"]
