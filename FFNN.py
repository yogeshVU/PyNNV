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

    
    def setController(self,nnfile):
        self.nnfile = nnfile #Path of the NN file

    def parseReachParam(self,lb, ub, numSims, reachMethod, numCores, lbRef, ubRef,halfSpaceMatrix,halfSpaceVector):
        self.lb = lb
        self.ub= ub
        self.reach_method = reachMethod
        self.lbRefInput = lbRef
        self.ubRefInput = ubRef
        self.HalfSpaceMatrix = halfSpaceMatrix
        self.HalfSpaceVector = halfSpaceVector
        self.num_sims = numSims

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
        
        newdata['lb'] = matlab.double(str2array(data['lb']))
        newdata['ub'] = matlab.double(str2array(data['ub']))
        newdata['HalfSpace-matrix'] =matlab.double(str2array(data['HalfSpace-matrix']))
        newdata['HalfSpace-vector'] =matlab.double(str2array(data['HalfSpace-vector']))

        self.setController(data['nnfile'])
        self.parseReachParam(lb=newdata['lb'],ub=newdata['ub'], numSteps=data['sims'],reachMethod=data['reach-method'],
                            numCores=data['cores'], halfSpaceMatrix= newdata['HalfSpace-matrix'], halfSpaceVector= newdata['HalfSpace-vector'])

    def execute(self):
        self.getNNCS()
    
    def invokeReachibility(self):
        return self.eng.DLinearNNCS_reach(self.nnfile,self.A,self.B,self.C,self.D,self.Ts,self.lb,self.ub,self.steps,self.reach_method,self.cores,self.lbRefInput,self.ubRefInput)

    def invokeVerifier(self):
        return self.eng.DLinearNNCS_verify(self.nnfile,self.A,self.B,self.C,self.D,self.Ts,self.lb,self.ub,self.steps,self.reach_method,self.cores,self.lbRefInput,self.ubRefInput,self.HalfSpaceMatrix,self.HalfSpaceVector)
