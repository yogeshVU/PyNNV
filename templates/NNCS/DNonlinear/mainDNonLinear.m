%% Create the NNV class (NNCS class)
% Load controller
controller = Load_nn('NN-path'); % User specifies 
% Load plant (method 1)
plant = DNonLinearODE(dim,nI,@dynamics_func,Ts,outputMat); % User specifies all matrices and time step (Ts)
% Contruct NNCS objLct
nncs = DNonLinearNNCS(controller,plant,feedbackMap);

%% Reachability/Verification
% If procedure == reach
reachPRM.init_set = Star(lb,ub); % User specifies lower and upper bounds vectors
reachPRM.numSteps = num_of_steps; % User specifies number of steps
reachPRM.reachMethod = 'approx-star'; % Only allow approximate methods (set as fixed)
reachPRM.numCores = num_of_cores; % User specifies number of cores (1 as default)
reachPRM.ref_input = Star(lb_ref,ub_ref);% User specifies reference input ([] as default (empty = no reference inputs needed))
[R,reachTime] = nncs.reach(reachPRM); % Execute reachability analysis
% If procedure == verify
reachPRM.init_set = Star(lb,ub);
reachPRM.numSteps = num_of_steps;
reachPRM.reachMethod = 'approx-star';
reachPRM.numCores = num_of_cores;
reachPRM.ref_input = Star(lb_ref,ub_ref);
unsafeRegion = HalfSpace(G,g); % User specifies G and g (Half-space matrix and half-space vector , G*x <= g)
[safe, counterExamples, verifyTime] = nncs.reach(reachPRM,unsafeRegion); % Execute verification analysis
