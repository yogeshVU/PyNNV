
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





class FFNN:
    def __init__(self,eng=None):
        
        self.nnfile = "" #Path of the NN file
        # Following are needed for reachability and Verification
        self.lb = []
        self.ub = []
        self.method = []
        self.cores = 1
        self.num_sims =0
        
        # Following is needed for verification...
        self.HalfSpaceMatrix = []  # // any matrix (G)
        self.HalfSpaceVector = []  # // any matrix (g)
        self.eng = eng
        self.verify = False
        self.reach = False

    def str2matlabArray(self,strmat):
        return self.eng.str2num(strmat)

    def setController(self,nnfile):
        self.nnfile = nnfile #Path of the NN file

    def parseReachParam(self,lb, ub, simCount, reachMethod, numCores, halfSpaceMatrix,halfSpaceVector,doReachability,doVerify):
        self.lb = lb
        self.ub= ub
        self.reach_method = reachMethod
        self.HalfSpaceMatrix = halfSpaceMatrix
        self.HalfSpaceVector = halfSpaceVector
        self.simCount = simCount
        self.reach = doReachability
        self.verify = doVerify
        self.cores = numCores

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
        
        newdata['lb'] = matlab.double(self.str2matlabArray(data['lb']))
        newdata['ub'] = matlab.double(self.str2matlabArray(data['ub']))
        newdata['HalfSpace-matrix'] =matlab.double(self.str2matlabArray(data['HalfSpace-matrix']))
        newdata['HalfSpace-vector'] =matlab.double(self.str2matlabArray(data['HalfSpace-vector']))

        if data['reach']==1:
            newdata['reach'] = True
        else:
            newdata['reach']= False

        if data['verify']==1:
            newdata['verify'] = True
        else:
            newdata['verify']= False

        self.setController(data['nnfile'])
        self.parseReachParam(lb=newdata['lb'],ub=newdata['ub'], simCount=data['simCount'],reachMethod=data['reach-method'],
                            numCores=data['cores'], halfSpaceMatrix= newdata['HalfSpace-matrix'], halfSpaceVector= newdata['HalfSpace-vector'], doReachability=newdata['reach'],doVerify=newdata['verify'])

    def execute(self):
        self.getNNCS()
    
    def invokeReachibility(self):
        
        print("invokereachability")
        result = self.eng.FNN_template(self.nnfile,self.lb,self.ub,'reach',self.reach_method,self.cores)    
        print(result)
        return result
        # return self.eng.DLinearNNCS_reach(self.nnfile,self.A,self.B,self.C,self.D,self.Ts,self.lb,self.ub,self.steps,self.reach_method,self.cores,self.lbRefInput,self.ubRefInput)

    def invokeVerifier(self):
        print("invokeVerifier")
        # result7 = FNN_template('controller_test.mat',lb,ub,'verify',G,g,'exact-star',4,10);
        result=  self.eng.FNN_template(self.nnfile,self.lb,self.ub,'verify',self.HalfSpaceMatrix,self.HalfSpaceVector,self.reach_method,self.cores,self.simCount)    
        print(result)
        return result
        # return self.eng.DLinearNNCS_verify(self.nnfile,self.A,self.B,self.C,self.D,self.Ts,self.lb,self.ub,self.steps,self.reach_method,self.cores,self.lbRefInput,self.ubRefInput,self.HalfSpaceMatrix,self.HalfSpaceVector)

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
        

    # START MATLAB ENGINE
    eng = matlab.engine.start_matlab()
    # eng = matlab.engine.start_matlab('-nojvm')


    # ADD PATHS OF NEEDED FUNCTIONS TO MATLAB ENVIRONMENT
    matlab_function_path_list = []
    matlab_function_path_list.append(str(Path(Path(__file__).absolute().parent, "templates/FFNN/")))
    #
    # EXECUTE MATLAB ENGINE
    #
    eng.addpath(*matlab_function_path_list)
    eng.addpath(eng.genpath('/home/ubuntu/yogesh/aatools/diego-nnv/nnv/code/nnv'))
    eng.cd(str(Path(Path(__file__).absolute().parent, "templates/FFNN")),nargout=0)
    jsonfile = Path(Path(__file__).absolute().parent, "templates","FFNN",'inputJson.json')
    simObj = FFNN(eng)
    simObj.parseJson(str(jsonfile))
    print(simObj.compute())
    # if simObj.doReach():
    #     result = simObj.invokeReachibility()

    # if simObj.doVerify():
    #     result = simObj.invokeVerifier()
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