import binascii
from pathlib import Path

import docker
NNV_Docker = 'pynnv:0.1.0'
MATLAB_PATH= '/usr/local/MATLAB/R2020a/'




def dockerInit(job_params,folder_path):
    client = docker.from_env()
    args = ['python',
            'NNVEntry.py',
            '--json',
            str(job_params),
            '--inputdir',
            str(folder_path),
            '--config',
            '/PyNNV/config_docker.ini']

    cmd =  ' '.join([str(elem) for elem in args])
    print(cmd)
    # cmd= 'sleep 10000'
    result =client.containers.run(NNV_Docker, cmd,network_mode='host',volumes={folder_path: {'bind': folder_path, 'mode': 'rw'},MATLAB_PATH:{'bind':MATLAB_PATH, 'mode':'ro'}})
    print(result)
    return result

    # client.containers.run('pynnv:0.1.0')


if __name__ == '__main__':
    # CNN
    # folder = "CNN"
    # file = "template_parameters.json"

    # continuousNonLinearNNCS
    # folder = "ContinuousNonLinearNNCS"
    # file = "template_parameters.json"

    # DiscreteLinearNNCS
    # folder = "DiscreteLinearNNCS"
    # file = "template_parameters.json"

    #FFNN
    # folder = "FFNN"
    # file = "template_parameters.json"

    #ContinuousLinearNNCS
    folder = "ContinuousLinearNNCS"
    file = "template_parameters.json"

    # DiscreteNonLinearNNCS
    # folder = "DiscreteNonLinearNNCS"
    # file = "template_parameters.json"

    folder_path = str(Path(Path(__file__).absolute().parent, "example_inputs",folder))
    file_path = str(Path(Path(__file__).absolute().parent, "example_inputs",folder,file))

    test = b"Neural network loaded\nNN Controller created\n       init_set: [1x1 Star]\n       numSteps: 1\n    reachMethod: 'approx-star'\n       numCores: 1\n      ref_input: [2x1 double]\n\n\nmethod =\n\n    'exact-star'\n\n\nmethod =\n\n    'exact-star'\n\n\nmethod =\n\n    'exact-star'\n\n\nmethod =\n\n    'exact-star'\n\n\nmethod =\n\n    'exact-star'\n\n\nmethod =\n\n    'exact-star'\n\n    {1x1 Star}\n\n    1.7296\n\nNeural network loaded\nNN Controller created\n\nmethod =\n\n    'exact-star'\n\n\nmethod =\n\n    'exact-star'\n\n\nmethod =\n\n    'exact-star'\n\n\nmethod =\n\n    'exact-star'\n\n\nmethod =\n\n    'exact-star'\n\n\nmethod =\n\n    'exact-star'\n\n\n\nThe neural network control system is safe/home/ubuntu/yogesh/python-tut/example_inputs/ContinuousLinearNNCS/template_parameters.json\n/PyNNV/config_docker.ini\n/home/ubuntu/yogesh/python-tut/example_inputs/ContinuousLinearNNCS\nconfig file /PyNNV/config_docker.ini\n/PyNNV/input/CNN\n/PyNNV/input/FFNN\n/PyNNV/input/DiscreteNonLinearNNCS\n/PyNNV/input/DiscreteLinearNNCS\n/PyNNV/input/ContinuousLinearNNCS\n/PyNNV/input/ContinuousNonLinearNNCS\nThe current strategy is: ContinuousLinearNNCS\nparsing file: /home/ubuntu/yogesh/python-tut/example_inputs/ContinuousLinearNNCS/template_parameters.json\n{'reachability': ([<matlab.object object at 0x7f61b9539df0>], 1.729649), 'verification': ('SAFE', matlab.double([]), 0.159048)}\n"
    test =str(test, 'utf-8')
    teststr = test
    print(teststr)
    # dockerInit(file_path,folder_path)