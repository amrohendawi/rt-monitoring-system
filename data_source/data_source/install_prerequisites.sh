sudo apt-get update
# install python3 and necessary libraries for running flank data_sender
sudo apt-get install python3
sudo apt-get install python3-pip
sudo pip3 install numpy requests
# libnuma-dev necessary for data_source
sudo apt install libnuma-dev
# curl necessary for creating first DB before sending any data
sudo apt-get install curl
