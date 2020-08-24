%% Example Title
%Test Dnonlinear NNCS class
% Load network
controller = Load_nn('controller_test.mat');
% Load plant
Ts = 0.2; % time step
output_mat = [0 0 0 0 1 0;1 0 0 -1 0 0; 0 1 0 0 -1 0]; % feedback: relative distance, relative velocity and ego-car velocity
plant = DNonLinearODE(6,1,@test_dynamicsD,Ts,output_mat);
% Create NNCS
feedbackMap = [0];
nncs = DNonlinearNNCS(controller,plant,feedbackMap);

%% Setup Reachability parameters
lb = [90;29;0;30;30;0];
ub = [92;30;0;31;30.2;0];
reachPRM.init_set = Star(lb,ub);
reachPRM.numSteps = 5;
reachPRM.reachMethod = 'approx-star';
reachPRM.numCores = 1;
lb_ref = [30;1.4];
ub_ref = [30;1.4]; % For reachability, it may be a set, but for verify it must be a vector, so just limited to a vector
reachPRM.ref_input = Star(lb_ref,ub_ref);

disp(reachPRM)
%% Reach
% Execute reachability analysis
[R,rt] = nncs.reach(reachPRM);

%% Verify
% Define unsafe region
G = [1 0 0 -1 -1.4 0];
g = 10;
unsafeRegion = HalfSpace(G,g);
reachPRM.ref_input = [30;1.4]; % Reference input must be a vector for verification
% Formal verification 
[safe,counterExamples, vT] = nncs.verify(reachPRM,unsafeRegion);
