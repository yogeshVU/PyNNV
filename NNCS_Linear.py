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




class NNCSLinear:
    def __init__(self,eng=None):
        self.A =  []
        self.B = []
        self.C=  []
        self.D = []
        self.Ts = None # Integer
        self.nnfile = "" #Path of the NN file
        self.reachableSteps= 0
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

    def setPlant(self,A,B,C,D,Ts,reachableSteps):
        self.A =  A
        self.B = B
        self.C=  C #[]
        self.D = D
        self.Ts = Ts #None # Integer
        self.reachableSteps=reachableSteps


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
        # initSet = self.eng.Star(lb,ub)
        # self.refInput = self.eng.Star(lbRef,ubRef)
        # print(initSet)
        # print(refInput)
        
        # self.setReachParam(initSet,numSteps,reachMethod,numCores,refInput,halfSpaceMatrix,halfSpaceVector)    

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
        
        newdata['A'] = matlab.double(str2array(data['A']))
        newdata['B'] = matlab.double(str2array(data['B']))
        newdata['C'] = matlab.double(str2array(data['C']))
        newdata['D'] = matlab.double(str2array(data['D']))
        newdata['Ts'] = data['Ts']
        newdata['reachable-steps'] = float(data['reachable-steps'])
        
        
        newdata['lb'] = matlab.double(str2array(data['lb']))
        
        newdata['ub'] = matlab.double(str2array(data['ub']))
        newdata['lb-refInput'] = matlab.double(str2array(data['lb-refInput']))
        newdata['ub-refInput'] = matlab.double(str2array(data['ub-refInput']))
        newdata['HalfSpace-matrix'] =matlab.double(str2array(data['HalfSpace-matrix']))
        newdata['HalfSpace-vector'] =matlab.double(str2array(data['HalfSpace-vector']))

        self.setPlant(newdata['A'],newdata['B'], newdata['C'],newdata['D'],newdata['Ts'],newdata['reachable-steps'])
        self.setController(data['nnfile'])
        self.parseReachParam(lb=newdata['lb'],ub=newdata['ub'], numSteps=data['steps'],reachMethod=data['reach-method'],
                            numCores=data['cores'],lbRef=newdata['lb-refInput'],ubRef=newdata['ub-refInput'], halfSpaceMatrix= newdata['HalfSpace-matrix'], halfSpaceVector= newdata['HalfSpace-vector'])

    def execute(self):
        self.getNNCS()
    
    def invokeReachibility(self):
        return self.eng.LinearNNCS_reach(self.nnfile,self.A,self.B,self.C,self.D,self.Ts,self.reachableSteps,self.lb,self.ub,self.steps,self.reach_method,self.cores,self.lbRefInput,self.ubRefInput)
        # function [R,reachTime] = LinearNNCS_reach(NN_path,A,B,C,D,controlPeriod,numReachSteps,lb,ub,control_steps,reachMethod,num_of_cores,lb_ref,ub_ref)


    def invokeVerifier(self):
        # function [safe, ctE, vT] = LinearNNCS_verify(NN_path,A,B,C,D,controlPeriod,numReachSteps,lb,ub,control_steps,reachMethod,num_of_cores,input_ref,G,g)

        return self.eng.LinearNNCS_verify(self.nnfile,self.A,self.B,self.C,self.D,self.Ts,self.reachableSteps,self.lb,self.ub,self.steps,self.reach_method,self.cores,self.lbRefInput,self.ubRefInput,self.HalfSpaceMatrix,self.HalfSpaceVector)

def main():
        

    # START MATLAB ENGINE
    # eng = matlab.engine.start_matlab()
    eng = matlab.engine.start_matlab('-nojvm')


    # ADD PATHS OF NEEDED FUNCTIONS TO MATLAB ENVIRONMENT
    matlab_function_path_list = []

    # image_path = str(Path(Path(__file__).absolute().parent, "templates/CNN/image40.png"))

    #
    # EXECUTE MATLAB ENGINE
    #
    # eng.addpath(*matlab_function_path_list)
    eng.addpath(eng.genpath('/home/ubuntu/yogesh/aatools/diego-nnv/nnv/code/nnv'))
    matlab_function_path_list = []
    matlab_function_path_list.append(str(Path(Path(__file__).absolute().parent, "templates/NNCS/Linear")))
    eng.addpath(*matlab_function_path_list)

    
    eng.cd(str(Path(Path(__file__).absolute().parent, "templates/NNCS/Linear")),nargout=0)
    jsonfile = Path(Path(__file__).absolute().parent, "templates","NNCS","Linear",'inputJson.json')
    # print(jsonfile)
    simObj = NNCSLinear(eng)
    simObj.parseJson(str(jsonfile))
    simObj.invokeReachibility()
    simObj.printDebug()
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


# A = [0 1 0 0 0 0 0; 0 0 1 0 0 0 0; 0 0 0 0 0 0 1; 0 0 0 0 1 0 0; 0 0 0 0 0 1 0; 0 0 0 0 0 -2 0; 0 0 -2 0 0 0 0];
# B = [0; 0; 0; 0; 0; 2; 0];
# C = [1 0 0 -1 0 0 0; 0 1 0 0 -1 0 0; 0 0 0 0 1 0 0];  % feedback relative distance, relative velocity, longitudinal velocity
# D = [0; 0; 0];
# NN_Path = 'controller.mat';
# lb = [90;29;0;30;30;0;-10];
# ub = [92;30;0;31;30.2;0;-10];
# G = [1 0 0 -1 -1.4 0 0];
# g = 10;
# DLinearNNCS_verify(NN_Path,A,B,C,D,0.2,lb,ub,5,'approx-star',1,[30;1.4],G,g)    
