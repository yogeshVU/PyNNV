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




class NNCSDLinear:
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

    def setPlant(self,A,B,C,D,Ts):
        self.A =  A
        self.B = B
        self.C=  C #[]
        self.D = D
        
        self.Ts = Ts #None # Integer


    def setController(self,nnfile):
        self.nnfile = nnfile #Path of the NN file

    def getController(self):
        # controller = Load_nn('NN-path'); % User specifies 
        return self.eng.Load_nn(self.nnfile)

    def getPlant(self):
        return self.eng.DLinearODE(self,self.A,self.B,self.C,self.D,self.Ts)

    def getNNCS(self):
        return self.eng.DLinearNNCS(self.getController(),self.getPlant());

    def setReachParam(self,init_set,numSteps,reachMethod,numCores,refInput, halfSpaceMatrix=None, halfSpaceVector=None):
        self.init_set = init_set
        self.steps = numSteps
        self.reach_method = reachMethod
        self.cores = numCores
        self.refInput = refInput
        self.HalfSpaceMatrix = halfSpaceMatrix
        self.HalfSpaceVector = halfSpaceVector

    def parseReachParam(self,lb, ub, numSteps, reachMethod, numCores, lbRef, ubRef,halfSpaceMatrix,halfSpaceVector):
        initSet = None
        refInput = None
        self.lb = lb
        self.ub= ub
        self.steps = numSteps
        self.reach_method = reachMethod
        self.cores = numCores
        self.lbRefInput = lbRef
        self.ubRefInput = ubRef
        self.HalfSpaceMatrix = halfSpaceMatrix
        self.HalfSpaceVector = halfSpaceVector
        initSet = self.eng.Star(lb,ub)
        self.refInput = self.eng.Star(lbRef,ubRef)
        print(initSet)
        print(refInput)
        
        # self.setReachParam(initSet,numSteps,reachMethod,numCores,refInput,halfSpaceMatrix,halfSpaceVector)    

    def printDebug(self):
        print(self.lb,self.ub)
        print(self.steps)
        print(self.nnfile)
        

    def parseJson(self,jsonfile):
        print("parsing file:",jsonfile)
        data = None
        with open(jsonfile) as f:
            data = json.load(f)

        newdata ={}
        
        newdata['A'] = matlab.double(str2array(data['A']))
        newdata['B'] = matlab.double(str2array(data['B']))
        newdata['C'] = matlab.double(str2array(data['C']))
        newdata['D'] = matlab.double(str2array(data['D']))
        newdata['Ts'] = data['Ts']
        
        
        newdata['lb'] = matlab.double(str2array(data['lb']))
        
        newdata['ub'] = matlab.double(str2array(data['ub']))
        newdata['lb-refInput'] = matlab.double(str2array(data['lb-refInput']))
        newdata['ub-refInput'] = matlab.double(str2array(data['ub-refInput']))
        newdata['HalfSpace-matrix'] =matlab.double(str2array(data['HalfSpace-matrix']))
        newdata['HalfSpace-vector'] =data['HalfSpace-vector']

        self.setPlant(newdata['A'],newdata['B'], newdata['C'],newdata['D'],newdata['Ts'])
        self.setController(data['nnfile'])
        self.parseReachParam(lb=newdata['lb'],ub=newdata['ub'], numSteps=data['steps'],reachMethod=data['reach-method'],
                            numCores=data['cores'],lbRef=newdata['lb-refInput'],ubRef=newdata['ub-refInput'], halfSpaceMatrix= newdata['HalfSpace-matrix'], halfSpaceVector= newdata['HalfSpace-vector'])

    def execute(self):
        self.getNNCS()
        initSet = self.eng.Star(lb,ub)
        refInput = self.eng.Star(lbRef,ubRef)

    
    
    def invokeNNCSDLinear(self):
        return self.eng.DLinearNNCS_reach(self.nnfile,self.A,self.B,self.C,self.D,self.Ts,self.lb,self.ub,self.steps,self.reach_method,self.cores,self.lbRefInput,self.ubRefInput)

    def invokeVerifier(self):
        return self.eng.DLinearNNCS_verify(self.nnfile,self.A,self.B,self.C,self.D,self.Ts,self.lb,self.ub,self.steps,self.reach_method,self.cores,self.refInput,self.HalfSpaceMatrix,self.HalfSpaceVector)

def main():
        

    # START MATLAB ENGINE
    # eng = matlab.engine.start_matlab()
    eng = matlab.engine.start_matlab('-nojvm')


    # ADD PATHS OF NEEDED FUNCTIONS TO MATLAB ENVIRONMENT
    matlab_function_path_list = []
    local_matlab_function_path = str(Path(Path(__file__).absolute().parent, "templates/CNN/Brightening"))
    matlab_function_path_list.append(local_matlab_function_path)
    local_matlab_function_path = str(Path(Path(__file__).absolute().parent, "templates/CNN/Darkening"))
    matlab_function_path_list.append(local_matlab_function_path)
    local_matlab_function_path = str(Path(Path(__file__).absolute().parent, "templates/CNN/RandomNoise"))
    matlab_function_path_list.append(local_matlab_function_path)

    # image_path = str(Path(Path(__file__).absolute().parent, "templates/CNN/image40.png"))

    #
    # EXECUTE MATLAB ENGINE
    #
    # eng.addpath(*matlab_function_path_list)
    eng.addpath(eng.genpath('/home/ubuntu/yogesh/aatools/diego-nnv/nnv/code/nnv'))
    
    meanV, stdV, reach_method  = (matlab.double([0.4914, 0.4822, 0.4465]) , matlab.double([0.2023, 0.1994, 0.2010]) , 'approx-star')
    # eng.cd(str(Path(Path(__file__).absolute().parent, "templates/CNN/Brightening")),nargout=0)
    image_path = str(Path(Path(__file__).absolute().parent, "templates","CNN", 'image40.png').absolute())
    # print(mat_file)
    print(image_path)
    network_directory_path = Path(Path(__file__).absolute().parent, "templates","CNN")
    mat_file_list = sorted(network_directory_path.glob("*.mat"))
    print(mat_file_list)

    if len(mat_file_list) == 0:
        raise RuntimeError(
        "lec directory \"{0}\" must contain at least one mat-file"
        " (that contains a neural network).".format(network_directory_path))
    mat_file = mat_file_list[0].absolute()
    pixels =100

    
    eng.cd(str(Path(Path(__file__).absolute().parent, "templates/NNCS/DLinear")),nargout=0)
    jsonfile = Path(Path(__file__).absolute().parent, "templates","NNCS","DLinear",'inputJson.json')
    print(jsonfile)
    simObj = NNCSDLinear(eng)
    simObj.parseJson(str(jsonfile))
    simObj.printDebug()
    simObj.invokeNNCSDLinear()
    simObj.invokeVerifier()

        # simObj.execute()
    # except Exception as e:
    #     print(e)    
    # finally:
    #     print("Finally..")    
    #     eng.exit()
    eng.exit()

if __name__ == "__main__":
    main()