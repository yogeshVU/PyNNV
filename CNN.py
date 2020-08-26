
import json
import matlab
import matlab.engine
from pathlib import Path

import numpy as np
def array2str(arr, precision=None):
    s=np.array_str(arr, precision=precision)
    return s.replace('\n', ',')

import re
import ast
import numpy as np
def str2array(s):
    # Remove space after [
    s=re.sub('\[ +', '[', s.strip())
    # Replace commas and spaces
    s=re.sub('[,\s]+', ', ', s)
    return np.array(ast.literal_eval(s)).tolist()





class CNN:
    def __init__(self,eng=None):
        
        self.nnfile = "" #Path of the NN file
        # Following are needed for reachability and Verification
        self.method = []
        self.image = ""
        self.mean = None
        self.std = None
        self.im_target = None
        self.threshold = None
        self.delta = None
        self.pixels = None
        self.eng = eng
        
    def setController(self,nnfile):
        self.nnfile = nnfile #Path of the NN file

    def printDebug(self):
        print(self.lb,self.ub)
        print(self.steps)
        print(self.nnfile)
        # print("RefInput")
        # print(self.refInput)
        

    def parseJson(self,jsonfile):
        print("parsing file:",jsonfile)
        data = None
        with open(jsonfile) as f:
            data = json.load(f)

        newdata ={}
        
        newdata['mean'] =matlab.double(str2array(data['mean']))
        newdata['std'] =matlab.double(str2array(data['std']))
        

        self.mean = newdata['mean']
        self.std = newdata['std']
        self.threshold = data['threshold']
        self.im_target = data['im_target']
        self.pixels = data['pixels']
        self.attack = data['attack']
        self.nnfile = data['nnfile']
        self.image = data['image']
        self.delta = float(data['delta'])
        self.method = data['reach-method']

    def getnnfile(self):
        filePath=  Path(Path(__file__).absolute().parent, "templates","CNN",self.nnfile)
        # mat_file_list = sorted(network_directory_path.glob("*.mat"))
        # print(mat_file_list)
        # if len(mat_file_list) == 0:
        #     raise RuntimeError(
        #     "lec directory \"{0}\" must contain at least one mat-file"
        #     " (that contains a neural network).".format(network_directory_path)
        #     )
        # mat_file = mat_file_list[0].absolute()

        return str(filePath)

    def getimage(self):
         
        filepath=  Path(Path(__file__).absolute().parent, "templates","CNN",self.image)

        return str(filepath)

    def invokeattack(self):

        print(self.getimage())
        print(self.getnnfile())
        
        if self.attack == "brightening":
            return self.eng.bright_attack(self.getnnfile(), self.getimage(),self.im_target,self.threshold, self.delta,self.mean, self.std,self.method)
            
        elif self.attack =="darkening":
            return self.eng.darkening_attack(self.getnnfile(), self.getimage(),self.im_target,self.threshold, self.delta,self.mean, self.std,self.method)
        elif self.attack =="randomnoise":
            return self.eng.randomnoise_attack(self.getnnfile(), self.getimage(),self.im_target,self.threshold, self.delta,self.mean, self.std,self.method,self.pixels)

    
    
def main():
        

    # START MATLAB ENGINE
    eng = matlab.engine.start_matlab()
    # eng = matlab.engine.start_matlab('-nojvm')


    # ADD PATHS OF NEEDED FUNCTIONS TO MATLAB ENVIRONMENT
    matlab_function_path_list = []
    local_matlab_function_path = str(Path(Path(__file__).absolute().parent, "templates/CNN/Brightening"))

    matlab_function_path_list.append(local_matlab_function_path)

    local_matlab_function_path = str(Path(Path(__file__).absolute().parent, "templates/CNN/Darkening"))
    matlab_function_path_list.append(local_matlab_function_path)

    local_matlab_function_path = str(Path(Path(__file__).absolute().parent, "templates/CNN/RandomNoise"))
    matlab_function_path_list.append(local_matlab_function_path)


    eng.addpath(*matlab_function_path_list)
    eng.addpath(eng.genpath('/home/ubuntu/yogesh/aatools/diego-nnv/nnv/code/nnv'))
    eng.cd(str(Path(Path(__file__).absolute().parent, "templates/CNN")),nargout=0)
    jsonfile = Path(Path(__file__).absolute().parent, "templates","CNN",'inputJson.json')
    simObj = CNN(eng)
    simObj.parseJson(str(jsonfile))
    simObj.invokeattack()
    
    # simObj.invokeVerifier()
    # simObj.printDebug()
    # simObj.invokeVerifier()

        # simObj.execute()
    # except Exception as e:
    #     print(e)    
    # finally:
    #     print("Finally..")    
    #     eng.exit()
    eng.exit()

if __name__ == "__main__":
    main()