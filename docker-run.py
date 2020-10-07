import binascii
from pathlib import Path

import docker

NNV_Docker = 'pynnv_base:0.1.1'
MATLAB_PATH= '/usr/local/MATLAB/R2020a/'



def run(job_params,folder_path):
    args = ['python',
            'NNVEntry.py',
            '--json',
            str(job_params),
            '--inputdir',
            str(folder_path),
            '--config',
            '/home/ubuntu/yogesh/python-tut/config.ini']

    cmd =  ' '.join([str(elem) for elem in args])
    print(cmd)
    import subprocess
    result = subprocess.run(args=args)
    # # cmd= 'sleep 100000'
    # result = str(result, 'utf-8')
    print(result)
    # return result

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
    # cmd= 'sleep 100000'
    result =client.containers.run(NNV_Docker, cmd,network_mode='host',volumes={folder_path: {'bind': folder_path, 'mode': 'rw'},MATLAB_PATH:{'bind':MATLAB_PATH, 'mode':'ro'}})
    result = str(result, 'utf-8')
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
    # folder = "ContinuousLinearNNCS"
    # file = "template_parameters.json"

    # DiscreteNonLinearNNCS
    folder = "DiscreteNonLinearNNCS"
    file = "template_parameters.json"

    folder_path = str(Path(Path(__file__).absolute().parent, "example_inputs",folder))
    file_path = str(Path(Path(__file__).absolute().parent, "example_inputs",folder,file))

    # test = b'Error using Conv2DLayer/reach_star_single_input (line 716)\nInvalid MEX-file \'/verivital/code/nnv/engine/matconvnet/vl_nnconv.mexa64\': libjpeg.so.8: cannot open shared object file: No such file or directory\n\nError in Conv2DLayer/reach_star_multipleInputs (line 758)\n                parfor i=1:n\n\nError in Conv2DLayer/reach (line 852)\n                images = obj.reach_star_multipleInputs(in_images, option);\n\nError in CNN/reach (line 217)\n                rs_new = obj.Layers{i-1}.reach(rs, obj.reachMethod, obj.reachOption, obj.relaxFactor, obj.dis_opt, obj.lp_solver);\n\nError in CNN/classify (line 284)\n                obj.reach(in_image, method, numOfCores);\n\nError in CNN/verifyRobustness (line 338)\n            label_id = obj.classify(in_image, method, numOfCores);      \n\nError in randomnoise_attack (line 95)\n    r_nn = net.verifyRobustness(inputSetStar, im_target, reach_method, numCores);\n\nTraceback (most recent call last):\n  File "NNVEntry.py", line 23, in <module>\n    NNVExec(template_param_json,input_dir,config_file=config_file)\n  File "/PyNNV/NNV.py", line 73, in __init__\n    print(context.compute())\n  File "/PyNNV/CNN.py", line 115, in compute\n    return self.invokeattack()    \n  File "/PyNNV/CNN.py", line 112, in invokeattack\n    return self.eng.randomnoise_attack(self.getnnfile(), self.getimage(),self.im_target,self.threshold, self.delta,self.mean, self.std,self.method,self.pixels)\n  File "/usr/local/lib/python3.7/site-packages/matlab/engine/matlabengine.py", line 71, in __call__\n    _stderr, feval=True).result()\n  File "/usr/local/lib/python3.7/site-packages/matlab/engine/futureresult.py", line 67, in result\n    return self.__future.result(timeout)\n  File "/usr/local/lib/python3.7/site-packages/matlab/engine/fevalfuture.py", line 82, in result\n    self._result = pythonengine.getFEvalResult(self._future,self._nargout, None, out=self._out, err=self._err)\nmatlab.engine.MatlabExecutionError: \n  File /verivital/code/nnv/engine/nn/layers/Conv2DLayer.m, line 758, in Conv2DLayer.reach_star_multipleInputs\n\n  File /verivital/code/nnv/engine/nn/layers/Conv2DLayer.m, line 852, in Conv2DLayer.reach\n\n  File /verivital/code/nnv/engine/nn/cnn/CNN.m, line 217, in CNN.reach\n\n  File /verivital/code/nnv/engine/nn/cnn/CNN.m, line 284, in CNN.classify\n\n  File /verivital/code/nnv/engine/nn/cnn/CNN.m, line 338, in CNN.verifyRobustness\n\n  File /PyNNV/input/CNN/randomnoise_attack.m, line 95, in randomnoise_attack\nInvalid MEX-file \'/verivital/code/nnv/engine/matconvnet/vl_nnconv.mexa64\': libjpeg.so.8: cannot open shared object file: No such file or directory\n\n'
    # test =str(test, 'utf-8')
    # teststr = test
    # print(teststr)
    dockerInit(file_path,folder_path)
    # run(file_path,folder_path)