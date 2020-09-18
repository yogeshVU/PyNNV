function [R, reachTime] = DLinearNNCS_reach(NN_path,A,B,C,D,Ts,lb,ub,num_of_steps,reachMethod,num_of_cores,lb_ref,ub_ref)
    %% Create the NNV class (NNCS class)
    % Load controller
    controller = Load_nn(NN_path); % User specifies 
    % Load plant (method 1)
    plant = DLinearODE(A,B,C,D,Ts); % User specifies all matrices and time step (Ts)
    % Contruct NNCS object
    nncs = DLinearNNCS(controller,plant);
    
    disp('Now Looking at reachability')
    %% Reachability
    reachPRM.init_set = Star(lb,ub); % User specifies lower and upper bounds vectors
    reachPRM.numSteps = num_of_steps; % User specifies number of steps
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
    disp('Calling reachability')
    disp(reachPRM)
    [R,reachTime] = nncs.reach(reachPRM); % Execute reachability analysis
    disp(reachTime)
    disp(R)
    disp('Finished reachability')
    save('starset.mat','R','-v7.3')

    end
    