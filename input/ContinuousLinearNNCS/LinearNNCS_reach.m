function [R,reachTime] = LinearNNCS_reach(NN_path,A,B,C,D,controlPeriod,numReachSteps,lb,ub,control_steps,reachMethod,num_of_cores,lb_ref,ub_ref)
    %% Create the NNV class (NNCS class)
    % Load controller
    controller = Load_nn(NN_path); % User specifies 
    % Load plant (method 1)
    plant = LinearODE(A,B,C,D,controlPeriod,numReachSteps); % User specifies all matrices and time step (Ts)
    % If user provides matlab dynamics object (method 2)
    % Load system (like the sys-ID object)
    % load('plantMATLAB-path'); % User specifies path
    % plant = LinearODE(sys.A,sys.B,sys.C,sys.D,controlPeriod,numReachSteps);
    % Contruct NNCS object
    nncs = LinearNNCS(controller,plant);
    
    %% Reachability
    reachPRM.init_set = Star(lb,ub); % User specifies lower and upper bounds vectors
    reachPRM.numSteps = control_steps; % User specifies number of steps
    reachPRM.reachMethod = reachMethod; % User specifies reachability method ('approx-star' or 'exact-star')
    reachPRM.numCores = num_of_cores; % User specifies number of cores (1 as default)
    if ~isempty(lb_ref) && ~isempty(ub_ref)
        if lb_ref == ub_ref
            reachPRM.ref_input = lb_ref;
        else
            reachPRM.ref_input = Star(lb_ref,ub_ref);% User specifies reference input ([] as default (empty = no reference inputs needed))
        end
    else
        reachPRM.ref_input = [];
    end

    disp(reachPRM)
    [R,reachTime] = nncs.reach(reachPRM); % Execute reachability analysis
    
    disp(R)
    disp(reachTime)
    save('starset.mat','R','-v7.3')

    end