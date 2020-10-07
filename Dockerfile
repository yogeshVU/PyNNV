FROM python:3.7.9-slim-buster as matlab_base_R2020a
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    libpng-dev libfreetype6-dev \
    libblas-dev liblapack-dev gfortran build-essential xorg protobuf-compiler cmake libjpeg-dev && apt-get clean \
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/*
ARG MATLAB_PATH=/usr/local/MATLAB/R2020a
ENV MATLAB_PATH=$MATLAB_PATH
WORKDIR $MATLAB_PATH
ENV PATH="/usr/bin:${MATLAB_PATH}/bin:${PATH}"

FROM matlab_base_R2020a as nnv_base
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /
#RUN apt install software-properties-common -y
#RUN add-apt-repository ppa:deadsnakes/ppa -y
#RUN apt install python3.7 -y
RUN apt update && apt install git-core wget  -y \
 && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /verivital
WORKDIR /verivital

ARG NNV_REPO=https://github.com/dieman95/nnv
ARG BRANCH=cora2020
ARG COMMIT_HASH=6497e82694ef52741bfd1396330367bbe3870808
RUN echo $NNV_REPO $BRANCH $COMMIT_HASH
RUN git clone --branch ${BRANCH} $NNV_REPO . \
&& git checkout ${COMMIT_HASH} \
&& git reset --hard
#RUN git clone --branch cora2020 https://github.com/dieman95/nnv . \
#&& git checkout 6497e82694ef52741bfd1396330367bbe3870808 \
#&& git reset --hard


#RUN cd /verivital && git clone https://github.com/verivital/nnv .
#RUN cd /verivital && git clone --recursive https://github.com/verivital/nnv.git
#RUN cd /verivital && git clone https://github.com/verivital/nnv .
RUN cd /verivital && git submodule init && git submodule sync && git submodule update
RUN echo "cd /verivital/code/nnv \n try \n   install \n catch \n   disp('Exception caught!') \n end \n cd /verivital/code/nnv \n startup_nnv \n cd /verivital \n savepath('/verivital/pathdef.m')" > /verivital/setup_verivital.m
RUN cd /verivital && wget https://raw.githubusercontent.com/yogeshVU/PyNNV/master/matlab-requirements.sh && chmod +x matlab-requirements.sh


FROM nnv_base:0.1.1 as pynnv_base
# This creates a setup_verivital.m
RUN mkdir -p /PyNNV
#RUN pip install -r requirements.txt
RUN pip install -r https://raw.githubusercontent.com/yogeshVU/PyNNV/master/requirements.txt
RUN wget -q http://mirrors.kernel.org/ubuntu/pool/main/libj/libjpeg-turbo/libjpeg-turbo8_2.0.3-0ubuntu1_amd64.deb \
&& apt-get -qy --allow-downgrades install ./libjpeg-turbo8_2.0.3-0ubuntu1_amd64.deb \
&& rm libjpeg-turbo8_2.0.3-0ubuntu1_amd64.deb

WORKDIR /PyNNV
COPY . /PyNNV
#RUN chmod +x matlab-requirements.sh


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


