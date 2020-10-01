#!/usr/bin/env bash

echo $MATLAB_PATH
export PATH=$MATLAB_PATH/bin:$PATH
matlab_setup_dir="$MATLAB_PATH/extern/engines/python"
if [ -d "${matlab_setup_dir}" ]; then
  pushd $MATLAB_PATH/extern/engines/python
  python setup.py build --build-base=$(mktemp -d) install
  echo "We are in the folder of MATLAB"
  popd
else
  echo "WARNING: Required MATLAB directory (${matlab_setup_dir}) does not exist within Jupyter-Matlab docker image. Continuing without MATLAB."
fi

matlab -nodisplay -nosplash -nodesktop -r "run('/verivital/setup_verivital.m');quit;"