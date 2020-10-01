NNV Python Wrapper
===

authors: Yogesh B., Harmon N., Diego M.

Usage:
--
To run the NNV Python Wrapper:

```bash
python  NNVEntry.py [-h] --json JSON --inputdir INPUTDIR [--config CONFIG]
```

Example:

```bash
(venv) ubuntu@localhost:~/yogesh/python-tut$ python NNVEntry.py --json /home/ubuntu/yogesh/python-tut/example_inputs/CNN/template_parameters.json  --inputdir /home/ubuntu/yogesh/python-tut/example_inputs/CNN
/home/ubuntu/yogesh/python-tut/example_inputs/CNN/template_parameters.json
None
/home/ubuntu/yogesh/python-tut/example_inputs/CNN
config file /home/ubuntu/yogesh/python-tut/config.ini
/home/ubuntu/yogesh/python-tut/input/CNN
/home/ubuntu/yogesh/python-tut/input/FFNN
/home/ubuntu/yogesh/python-tut/input/DiscreteNonLinearNNCS
/home/ubuntu/yogesh/python-tut/input/DiscreteLinearNNCS
/home/ubuntu/yogesh/python-tut/input/ContinuousLinearNNCS
/home/ubuntu/yogesh/python-tut/input/ContinuousNonLinearNNCS
The current strategy is: CNN
parsing file: /home/ubuntu/yogesh/python-tut/example_inputs/CNN/template_parameters.json
image40.png
vgg16nnv.mat

net = 

  struct with fields:

    nn: [1x1 CNN]


std =

    0.2023    0.1994    0.2010


mean =

    0.4914    0.4822    0.4465


=============================================Starting parallel pool (parpool) using the 'local' profile ...
Connected to the parallel pool (number of workers: 16).

=============================================
The robustness of the network is UNCERTAIN due to the conservativeness of approximate analysis
Label index: 0
Possible classified index: 6 
Please try to verify the robustness with exact-star (exact analysis) option 
Robusteness analysis total time = 64.0123
Robust = 2
2.0

```

Parameter **JSON** file: 

```json
{
    "dim": 6,
    "nI" : 1,
    "dynamic_func":"test_dynamics",
    "outputMat":"[0 0 0 0 1 0;1 0 0 -1 0 0; 0 1 0 0 -1 0];",
    "Ts" : 0.2,
    "reachable-steps":5,
    "nnfile": "controller_test.mat",
    "feedbackMap": "[0]",
    "lb" : "[90;29;0;30;30;0]",
    "ub" : "[92;30;0;31;30.2;0]",

    "reach-method": "approx-star",
    "cores": 1,
    "steps": 5,
    "lb-refInput": "[30;1.4]",
    "ub-refInput": "[30;1.4]",
    "HalfSpace-matrix": "[1 0 0 -1 -1.4 0];",
    "HalfSpace-vector": "10",
    "verify":1,
    "reach":1
}
```

**INPUTDIR**: Points to the input directory where the input files(controller.mat files,
test images, etc.) are located.

**config** : Optional `config.ini` file which specifies the
configuration PATH to the NNV toolchain and the MATLAB functions
used by the wrapper.

```ini
[JOB_INPUT]
PARAMETER_JSON =/home/ubuntu/yogesh/nnv_data/inputs/1599927464/template_parameters.json
INPUT_DIRECTORY = /home/ubuntu/yogesh/nnv_data/inputs/1599927464/

[MATLAB]
NNV_PATH =/home/ubuntu/yogesh/aatools/diego-nnv/nnv/code/nnv
FUNCTION_PATHS =/home/ubuntu/yogesh/python-tut/input/CNN
                /home/ubuntu/yogesh/python-tut/input/FFNN
                /home/ubuntu/yogesh/python-tut/input/DiscreteNonLinearNNCS
                /home/ubuntu/yogesh/python-tut/input/DiscreteLinearNNCS
                /home/ubuntu/yogesh/python-tut/input/ContinuousLinearNNCS
                /home/ubuntu/yogesh/python-tut/input/ContinuousNonLinearNNCS

```

Misc.
--
* Install the python dependencies in a virtualenv from the `requirements.txt`
example:
```bash
python3.7 -m virtualenv venv
```
To install the matlab python package:

``` bash
cd "matlabroot\extern\engines\python"

python setup.py build --build-base=$(mktemp -d) install --prefix pynnv/venv/
```


Creating a docker container for this:
For the current dockerfile, we have used MATLAB2020a as the host machine version of the MATLAB.

We can set the path of the matlab host installation as :
`MATLAB_PATH=/usr/local/MATLAB/R2020a/
`
Next, create the docker container(the process is going to take a long time(~30min..)) depending on the internet connection.
It first downloads the verivital/nnv from the git repo., create the matlab container,
installs the matlab python and finally installs the PyNNV and the file path setup.
 
To build run:
``
sh run_setup.sh
``

To execute the pynnv container:
Important point here is that we need to have the `network=host` to be able to ran the matlab from the container.

```
MATLAB_PATH=/usr/local/MATLAB/R2020a/; docker run --rm  -it --network=host -v $MATLAB_PATH:$MATLAB_PATH:ro pynnv:0.1.0 /bin/bash
```


