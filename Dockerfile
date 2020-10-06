FROM python:3.7.9-slim-buster as nnv_base
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /
RUN apt update
#RUN apt install software-properties-common -y
#RUN add-apt-repository ppa:deadsnakes/ppa -y
#RUN apt install python3.7 -y
RUN apt install git-core -y
RUN mkdir -p /verivital
WORKDIR /verivital
RUN cd /verivital && git clone https://github.com/verivital/nnv .
RUN cd /verivital && git clone --recursive https://github.com/verivital/nnv.git

FROM nnv_base as matlab_base_R2020a
ARG MATLAB_PATH=/usr/local/MATLAB/R2020a
ENV MATLAB_PATH=$MATLAB_PATH
WORKDIR $MATLAB_PATH
RUN apt-get update && apt-get install -y \
    libpng-dev libfreetype6-dev \
    libblas-dev liblapack-dev gfortran build-essential xorg && apt-get clean \
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/*
ENV PATH="/usr/bin:${MATLAB_PATH}/bin:${PATH}"

FROM matlab_base_R2020a as pynnv_base
RUN apt update && apt install -y protobuf-compiler cmake
# This creates a setup_verivital.m
RUN echo "cd /verivital/nnv/code/nnv \n try \n   install \n catch \n   disp('Exception caught!') \n end \n cd /verivital/nnv/code/nnv \n startup_nnv \n cd /verivital \n savepath('/verivital/pathdef.m')" > /verivital/setup_verivital.m
RUN mkdir -p /PyNNV
#RUN pip install -r requirements.txt
RUN pip install -r https://raw.githubusercontent.com/yogeshVU/PyNNV/master/requirements.txt
RUN apt-get install libjpeg-dev -y
WORKDIR /PyNNV
COPY . /PyNNV
RUN chmod +x matlab-requirements.sh


#COPY . /PyNNV
#docker run --rm  -it  -v /home/ubuntu/:/usr/local/MATLAB/R2020a:ro matlab-base:0.1.0 /bin/bash
#docker run --rm  -it  -v /home/ubuntu/:/usr/local/MATLAB/R2020a:ro matlab-base:0.1.0 /bin/bash
#  --mount type=bind,source=/host/path/to/job/artifacts,target=/opt/flink/usrlib \
#docker run --mount type=bind,bind-nonrecursive
#docker build --target nnv_base -t nnv_base:0.1.0 .
#docker run --rm  -it --network=host -v /usr/local/MATLAB/R2020a:/usr/local/MATLAB/R2020a:ro matlab-base:0.1.0 /bin/bash
# docker run --rm  -it --network=host -v /usr/local/MATLAB/R2020a:/usr/local/MATLAB/R2020a:ro pynnv:0.1.0 /bin/bash

#RUN python3.7 -m pip install -r requirements.txt
#ENV PATH="/usr/bin:/usr/local/MATLAB/from-host/bin:${PATH}"
#ENV PATH="/usr/bin:/usr/local/MATLAB/from-host/bin:${PATH}"
#COPY setup.sh .
# docker run --rm  -it  -v /home/ubuntu/:/usr/local/MATLAB/R2020a:ro matlab-base:0.1.0 /bin/bash
# docker run -it --rm nnv_base:0.1.0 /bin/bash


