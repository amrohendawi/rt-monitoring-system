# get debial image
FROM debian:latest

#execute all commands as root
USER root

#install ssh, give user "root" a password
RUN apt-get -y --force-yes update \
    && apt-get install -y openssh-server \
    && echo 'root:root' | chpasswd \
    && sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd \
    && mkdir /var/run/sshd 

#get, compile and install RT tests
RUN apt-get install -y --no-install-recommends apt-utils build-essential sudo
RUN apt-get -y install rt-tests
ENV MYP /repo
WORKDIR ${MYP}
COPY . ${MYP}
RUN apt-get install -y python3 python3-pip
RUN pip3 install requests numpy 
RUN apt-get install gcc
CMD gcc data_source.c -o data_source && ./data_source 95 5
