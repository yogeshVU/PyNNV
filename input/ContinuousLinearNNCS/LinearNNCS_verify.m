function [safe, ctE, vT] = LinearNNCS_verify(NN_path,A,B,C,D,controlPeriod,numReachSteps,lb,ub,control_steps,reachMethod,num_of_cores,lb_ref,ub_ref,G,g)
    %% Create the NNV class (NNCS class)
    % Load controller
    controller = Load_nn(NN_path); % User specifies 
    % Load plant 
    plant = LinearODE(A,B,C,D,controlPeriod,numReachSteps); % User specifies all matrices and time step (Ts)
    % Create NNCS 
    nncs = LinearNNCS(controller,plant);
    

    if ~isempty(lb_ref) && ~isempty(ub_ref)
        if lb_ref == ub_ref
            reachPRM.ref_input = lb_ref;
        else
            reachPRM.ref_input = Star(lb_ref,ub_ref);% User specifies reference input ([] as default (empty = no reference inputs needed))
        end
    else
        reachPRM.ref_input = [];
    end

    %% Reachability
    reachPRM.init_set = Star(lb,ub); % User specifies lower and upper bounds vectors
    reachPRM.numSteps = control_steps; % User specifies number of steps
    reachPRM.reachMethod = reachMethod; % User specifies reachability method ('approx-star' or 'exact-star')
    reachPRM.numCores = num_of_cores; % User specifies number of cores (1 as default)
    % reachPRM.ref_input = input_ref;
    unsafeRegion = HalfSpace(G,g); % Create unsafe region
    [safe,ctE, vT] = nncs.verify(reachPRM,unsafeRegion); % Verify wrt the unsafe region
    
    end
    
    