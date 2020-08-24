%% Example Title
%Test Dnonlinear NNCS class
% Load network
controller = Load_nn('controller_test.mat');
% Load plant
A = [0 1 0 0 0 0 0; 0 0 1 0 0 0 0; 0 0 0 0 0 0 1; 0 0 0 0 1 0 0; 0 0 0 0 0 1 0; 0 0 0 0 0 -2 0; 0 0 -2 0 0 0 0];
B = [0; 0; 0; 0; 0; 2; 0];
C = [1 0 0 -1 0 0 0; 0 1 0 0 -1 0 0; 0 0 0 0 1 0 0];  % feedback relative distance, relative velocity, longitudinal velocity
D = [0; 0; 0]; 
controlPeriod = 0.1;
numReachSteps = 5;
plant = LinearODE(A, B, C, D, controlPeriod, numReachSteps);
% Create NNCS
nncs = LinearNNCS(controller,plant);

%% Setup Reachability parameters
lb = [90;29;0;30;30;0;-10];
ub = [92;30;0;31;30.2;0;-10];
reachPRM.init_set = Star(lb,ub);
reachPRM.numSteps = 5;
reachPRM.reachMethod = 'approx-star';
reachPRM.numCores = 1;
reachPRM.ref_input = [30;1.4]; % Reference input must be a vector for verification

%% Reach
% Execute reachability analysis
[R,rt] = nncs.reach(reachPRM);

%% Verify
% Define unsafe region
G = [1 0 0 -1 -1.4 0 0];
g = 10;
unsafeRegion = HalfSpace(G,g);
% Formal verification 
[safe,counterExamples, vT] = nncs.verify(reachPRM,unsafeRegion);
