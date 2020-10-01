#!/usr/bin/env bash
MATLAB_PATH=/usr/local/MATLAB/R2020a/
# Build the dockerfile first....
TAG_LABEL=0.1.0
docker build --target nnv_base -t nnv_base:$TAG_LABEL .
docker build --target matlab_base_R2020a -t matlab-base:$TAG_LABEL .
docker build --target pynnv_base -t pynnv_base:$TAG_LABEL .

docker rm nnv
docker run --name nnv  -it --network=host -v $MATLAB_PATH:$MATLAB_PATH:ro pynnv_base:$TAG_LABEL /bin/bash matlab-requirements.sh
docker commit nnv pynnv:$TAG_LABEL
docker rm nnv

# to use the final container run...
# MATLAB_PATH=/usr/local/MATLAB/R2020a/; docker run --rm  -it --network=host -v $MATLAB_PATH:$MATLAB_PATH:ro pynnv:0.1.0 /bin/bash