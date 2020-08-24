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
    return np.array(ast.literal_eval(s))

class NNCSDNonLinear:
    def __init__(self,eng=None):
        self.A =  []
        self.B = []
        self.C=  []
        self.D = []
        self.Ts = None # Integer
        self.nnfile = "" #Path of the NN file
        # Following are needed for reachability and Verification
        self.lb = []
        self.ub = []
        self.method = []
        self.cores = 1
        self.steps = 0
        self.lbRefInput = []
        self.ubRefInput = []

        # Following is needed for verification...
        self.HalfSpaceMatrix = []  # // any matrix (G)
        self.HalfSpaceVector = []  # // any matrix (g)
        self.eng = eng

    def setPlant(self,A,B,C,Ts):
        self.A =  A
        self.B = B
        self.C=  C #[]
        
        self.Ts = Ts #None # Integer


    def setController(self,nnfile):
        self.nnfile = nnfile #Path of the NN file

    def getController(self):
        # controller = Load_nn('NN-path'); % User specifies 
        return self.eng.Load_nn(self.nnfile)

    def getPlant():
        return self.eng.DLinearODE(self,self.A,self.B,self.C,self.D,self.Ts)

    def getNNCS():
        return self.eng.DLinearNNCS(self,getController(),getPlant());

    def setReachParam(self,init_set,numSteps,reachMethod,numCores,refInput, halfSpaceMatrix=None, halfSpaceVector=None):
        self.init_set = init_set
        self.numSteps = numSteps
        self.reach_method = reachMethod
        self.cores = numCores
        self.refInput = refInput
        self.HalfSpaceMatrix = halfSpaceMatrix
        self.HalfSpaceVector = halfSpaceVector

    def parseReachParam(self,lb, ub, numSteps, reachMethod, numCores, lbRef, ubRef,halfSpaceMatrix,halfSpaceVector):
        initSet = None
        refInput = None
        initSet = self.eng.Star(lb,ub)
        # refInput = self.eng.Star(lbRef,ubRef)
        
        self.setReachParam(initSet,numSteps,reachMethod,numCores,refInput,halfSpaceMatrix,halfSpaceVector)    

    def parseJson(self,jsonfile):
        print("parsing file:",jsonfile)
        data = None
        with open(jsonfile) as f:
            data = json.load(f)

        data['A'] = matlab.double(data['A'])
        data['B'] = matlab.double(data['B'])
        data['C'] = matlab.double(data['C'])
        data['Ts'] = data['Ts']
        
        data['lb'] = matlab.double(data['lb'])
        data['ub'] = matlab.double(data['ub'])
        data['lb-refInput'] = matlab.double(data['lb-refInput'])
        data['ub-refInput'] = matlab.double(data['ub-refInput'])
        data['HalfSpace-matrix'] =matlab.double(data['HalfSpace-matrix'])
        data['HalfSpace-vector'] = matlab.double(data['HalfSpace-vector'])

        self.setPlant(data['A'],data['B'], data['C'],data['Ts'])
        self.setController(data['nnfile'])
        self.parseReachParam(lb=data['lb'],ub=data['ub'], numSteps=data['steps'],reachMethod=data['reach-method'],
                            numCores=data['cores'],lbRef=data['lb-refInput'],ubRef=data['ub-refInput'], halfSpaceMatrix= data['HalfSpace-matrix'], halfSpaceVector= data['HalfSpace-vector'])

def main():
        
    # START MATLAB ENGINE
    # eng = matlab.engine.start_matlab()
    eng = matlab.engine.start_matlab('-nojvm')
    # ADD PATHS OF NEEDED FUNCTIONS TO MATLAB ENVIRONMENT
    matlab_function_path_list = []
    local_matlab_function_path = str(Path(Path(__file__).absolute().parent, "templates/CNN/RandomNoise"))
    matlab_function_path_list.append(local_matlab_function_path)

    #
    # EXECUTE MATLAB ENGINE
    #
    # eng.addpath(*matlab_function_path_list)
    eng.addpath(eng.genpath('/home/ubuntu/yogesh/aatools/diego-nnv/nnv/code/nnv'))
    
    
    try:
        jsonfile = Path(Path(__file__).absolute().parent, "templates","NNCS","DLinear",'inputJson.json')
        print(jsonfile)
        simObj = NNCSDNonLinear(eng)
        # simObj = NNCSDLinear()
        simObj.parseJson(str(jsonfile))
    
    finally:
        print("Finally..")    
        # eng.exit()
    # eng.exit()

if __name__ == "__main__":
    main()