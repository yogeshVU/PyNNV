%% Example Title
%Test Dnonlinear NNCS class
% Load network
controller = Load_nn('controller_test.mat');
% Load plant
A = [0 1 0 0 0 0 0; 0 0 1 0 0 0 0; 0 0 0 0 0 0 1; 0 0 0 0 1 0 0; 0 0 0 0 0 1 0; 0 0 0 0 0 -2 0; 0 0 -2 0 0 0 0];
B = [0; 0; 0; 0; 0; 2; 0];
C = [1 0 0 -1 0 0 0; 0 1 0 0 -1 0 0; 0 0 0 0 1 0 0];  % feedback relative distance, relative velocity, longitudinal velocity
D = [0; 0; 0]; 
Ts = 0.2;



plant = DLinearODE(A, B, C, D,Ts);
% Create NNCS
nncs = DLinearNNCS(controller,plant);

%% Setup Reachability parameters
lb = [90;29;0;30;30;0;-10];
ub = [92.0;30.0;0;31.0;30.2;0;-10.0];
reachPRM.init_set = Star(lb,ub);
reachPRM.numSteps = 5;
reachPRM.reachMethod = 'approx-star';
reachPRM.numCores = 1;
lb_ref = [30;1.4];
ub_ref = [30;1.4]; % For reachability, it may be a set, but for verify it must be a vector, so just limited to a vector
reachPRM.ref_input = Star(lb_ref,ub_ref);
reachPRM.ref_input = [30;1.4]; % Reference input must be a vector for verification

disp(reachPRM)
%% Reach
% Execute reachability analysis
[R,rt] = nncs.reach(reachPRM);
disp(R)
disp(rt)
%% Verify
% Define unsafe region
G = [1 0 0 -1 -1.4 0 0];
g = 10;

disp('G and g')
disp(G)
disp(g)

disp('A value is=')
disp(A)
disp('B value is=')
disp(B)
disp('C value is=')
disp(C)
disp('D value is=')
disp(D)
disp('Ts value is=')
disp(Ts)
disp('lb value is=')
disp(lb)
disp('ub value is=')
disp(ub)
disp('lb_ref value is=')
disp(lb_ref)
disp('ub_ref value is=')
disp(ub_ref)
disp('G value is=')
disp(G)
disp('g value is=')
disp(g)



unsafeRegion = HalfSpace(G,g);
reachPRM.ref_input = [30;1.4]; % Reference input must be a vector for verification
% Formal verification 
[safe,counterExamples, vT] = nncs.verify(reachPRM,unsafeRegion);
