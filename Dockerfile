# Base image
FROM ubuntu

# Do image configuration
RUN /bin/bash -c 'echo This would generally be apt-get or other system config'

# Install python 3.7
RUN apt update
RUN apt install software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3.7