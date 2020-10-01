import configparser
import json
from os.path import expandvars

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




class NNCS_DNonLinear:
    def __init__(self,eng=None):
        self.dim = 0
        self.nI = 0
        self.dynamics_func = ""
        self.outputMat  = []
        self.feedbackMap = []
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
        self.verify = False
        self.reach = False

    def setController(self,nnfile):
        self.nnfile = nnfile #Path of the NN file

    def getController(self):
        # controller = Load_nn('NN-path'); % User specifies 
        return self.eng.Load_nn(self.nnfile)

    def getPlant(self):
        return self.eng.DLinearODE(self,self.A,self.B,self.C,self.D,self.Ts)

    def getNNCS(self):
        return self.eng.DLinearNNCS(self.getController(),self.getPlant());

    def str2matlabArray(self,strmat):
        return self.eng.str2num(strmat)

    def setPlant(self,dim,nI,dynamics_func,Ts, outputMat,feedbackMap):
        self.dim =  dim
        self.nI = nI
        self.dynamics_func=  dynamics_func #[]
        self.Ts = Ts #None # Integer
        self.outputMat = outputMat
        self.feedbackMap = feedbackMap

    def parseReachParam(self,lb, ub, numSteps, reachMethod, numCores, lbRef, ubRef,halfSpaceMatrix,halfSpaceVector,doReachability,doVerify):
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
        self.reach = doReachability
        self.verify = doVerify
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
                
        newdata['dim'] = data['dim']
        newdata['nI'] = data['nI']
        newdata['dynamic_func'] = data['dynamic_func']
        newdata['outputMat'] =self.str2matlabArray( data['outputMat'])
        newdata['feedbackMap'] = self.str2matlabArray(data['feedbackMap'])
        newdata['Ts'] = data['Ts']
        
        
        newdata['lb'] = self.str2matlabArray(data['lb'])
        
        newdata['ub'] = self.str2matlabArray(data['ub'])
        newdata['lb-refInput'] = self.str2matlabArray(data['lb-refInput'])
        newdata['ub-refInput'] = self.str2matlabArray(data['ub-refInput'])
        newdata['HalfSpace-matrix'] =self.str2matlabArray(data['HalfSpace-matrix'])
        newdata['HalfSpace-vector'] =self.str2matlabArray(data['HalfSpace-vector'])

        if data['reach']==1:
            newdata['reach'] = True
        else:
            newdata['reach']= False

        if data['verify']==1:
            newdata['verify'] = True
        else:
            newdata['verify']= False

        self.setController(data['nnfile'])
        self.setPlant(dim=newdata['dim'],nI=newdata['nI'], dynamics_func=newdata['dynamic_func'],Ts=newdata['Ts'],outputMat=newdata['outputMat'], feedbackMap=newdata['feedbackMap'])
        self.parseReachParam(lb=newdata['lb'],ub=newdata['ub'], numSteps=data['steps'],reachMethod=data['reach-method'],
                            numCores=data['cores'],lbRef=newdata['lb-refInput'],ubRef=newdata['ub-refInput'], halfSpaceMatrix= newdata['HalfSpace-matrix'], halfSpaceVector= newdata['HalfSpace-vector'], doReachability=newdata['reach'],doVerify=newdata['verify'])

    def execute(self):
        self.getNNCS()
    
    def invokeReachibility(self):
        # function [R, reachTime] = DNonLinear_reach(NN_path,dynamics_func,dim,nI,Ts,outputMat,feedbackMap,lb,ub,num_of_steps,reachMethod,lb_ref,ub_ref)
        # %% [r,rt] = DNonLinear_reach('controller_test.mat',@test_dynamicsD,6,1,0.2,[0 0 0 0 1 0;1 0 0 -1 0 0; 0 1 0 0 -1 0],[0],[90;29;0;30;30;0], [92;30;0;31;30.2;0], 5, 'approx-star',[30;1.4],[30;1.4]);
        return self.eng.DNonLinear_reach(self.nnfile,self.dynamics_func,self.dim,self.nI,self.Ts,self.outputMat,self.feedbackMap, self.lb,self.ub,self.steps,self.reach_method,self.lbRefInput,self.ubRefInput)

    def invokeVerifier(self):
        # function [safe, counterExamples, verifyTime] = DNonLinear_verify(NN_path,dynamics_func,dim,nI,Ts,outputMat,feedbackMap,lb,ub,num_of_steps,reachMethod,ref_input,G,g)
        # % [a,b,c] = DNonLinear_verify('controller_test.mat',@test_dynamicsD,6,1,0.2,[0 0 0 0 1 0;1 0 0 -1 0 0; 0 1 0 0 -1 0],[0],[90;29;0;30;30;0], [92;30;0;31;30.2;0], 5, 'approx-star',[30;1.4], [1 0 0 -1 -1.4 0],10 );
#                     DNonLinear_verify(NN_path,dynamics_func,dim,nI,Ts,outputMat,feedbackMap,lb,ub,num_of_steps,reachMethod,ref_input,G,g)

        return self.eng.DNonLinear_verify(self.nnfile,self.dynamics_func,self.dim,self.nI,self.Ts,self.outputMat,self.feedbackMap,self.lb,self.ub,self.steps,self.reach_method,self.lbRefInput,self.ubRefInput,self.HalfSpaceMatrix,self.HalfSpaceVector)
    
    def doVerify(self):
        return self.verify

    def doReach(self):
        return self.reach  
    
    def compute(self):
        result = {}
        if self.doReach():
            result['reachability'] = self.invokeReachibility()

        if self.doVerify():
            result['verification'] = self.invokeVerifier()
        return result    

def main():

    ## Todo: need to add examples_inputs for this..
    jsonfile = Path(Path(__file__).absolute().parent, "templates","NNCS","DNonlinear",'inputJson.json')
    input_dir_path = Path(Path(__file__).absolute().parent, "templates/NNCS/DNonlinear")
    config_file = 'config.ini'

    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    config.read(config_file)

    with open(jsonfile) as f:
        data = json.load(f)

    eng = matlab.engine.start_matlab()
    matlab_function_path_list = []
    for paths in config['MATLAB']['FUNCTION_PATHS'].split("\n"):
        print(expandvars(paths))
        matlab_function_path_list.append(str(expandvars(paths)))

    eng.addpath(*matlab_function_path_list)

    ## Add the NNV path...
    NNV_PATH = str(Path(config['MATLAB']['NNV_PATH']))
    eng.addpath(eng.genpath(NNV_PATH))

    eng.cd(str(input_dir_path))


    simObj = NNCS_DNonLinear(eng)
    simObj.parseJson(str(jsonfile))
    print(simObj.compute())
    # simObj.invokeReachibility()
    # simObj.invokeVerifier()

    # if simObj.doReach():
    #     result = simObj.invokeReachibility()

    # if simObj.doVerify():
    #     result = simObj.invokeVerifier()
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


# [a,b,c] = DNonLinear_verify('controller_test.mat',@test_dynamicsD,6,1,0.2,[0 0 0 0 1 0;1 0 0 -1 0 0; 0 1 0 0 -1 0],[0],[90;29;0;30;30;0], [92;30;0;31;30.2;0], 5, 'approx-star',[30;1.4], [1 0 0 -1 -1.4 0],10 );