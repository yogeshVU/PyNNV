function [safe,ctE, vT] = DLinearNNCS_verify(NN_path,A,B,C,D,Ts,lb,ub,num_of_steps,reachMethod,num_of_cores,ref_input,G,g)
    %% Create the NNV class (NNCS class)
    % Load controller
    controller = Load_nn(NN_path); % User specifies 
    % Load plant (method 1)
    plant = DLinearODE(A,B,C,D,Ts); % User specifies all matrices and time step (Ts)
    % Contruct NNCS object
    nncs = DLinearNNCS(controller,plant);
    
    %% Reachability
    reachPRM.init_set = Star(lb,ub); % User specifies lower and upper bounds vectors
    reachPRM.numSteps = num_of_steps; % User specifies number of steps
    reachPRM.reachMethod = reachMethod; % User specifies reachability method ('approx-star' or 'exact-star')
    reachPRM.numCores = num_of_cores; % User specifies number of cores (1 as default)
    reachPRM.ref_input = input_ref;
    unsafeRegion = HalfSpace(G,g);
    % Formal verification 
    [safe,ctE, vT] = nncs.verify(reachPRM,unsafeRegion);
    
    end
    
    