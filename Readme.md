NNV Python Wrapper
===

authors: Yogesh B., Harmon N., Diego M.

Usage:
--
To run the NNV Python Wrapper:

```bash
python  NNVEntry.py [-h] --json JSON --inputdir INPUTDIR [--config CONFIG]
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

