function [safe, ctE, vT] = NonlinearNNCS_verify(NN_path,dynamics_func,dim,nI,Ts,controlPeriod,outputMat,feedbackMap,lb,ub,num_of_steps,reachMethod,num_of_cores,lb_ref,ub_ref,G,g)
    %% Create the NNV class (NNCS class)
    % Load controller
    controller = Load_nn(NN_path); % User specifies 
    % Load plant (method 1)
    fcall = str2func(dynamics_func)
    plant = NonLinearODE(dim,nI,fcall,Ts,controlPeriod,outputMat); % User specifies all matrices and time step (Ts)
    % Contruct NNCS object
    nncs = NonlinearNNCS(controller,plant,feedbackMap);
    
    %% Verification
    if ~isempty(lb_ref) && ~isempty(ub_ref)
        if lb_ref == ub_ref
            reachPRM.ref_input = lb_ref;
        else
            reachPRM.ref_input = Star(lb_ref,ub_ref);% User specifies reference input ([] as default (empty = no reference inputs needed))
        end
    else
        reachPRM.ref_input = [];
    end

    % If procedure == reach, generate and execute the following
    reachPRM.init_set = Star(lb,ub); % User specifies lower and upper bounds vectors
    reachPRM.numSteps = num_of_steps; % User specifies number of steps
    reachPRM.reachMethod = reachMethod; % Only allow approximate methods (set as fixed)
    reachPRM.numCores = num_of_cores; % User specifies number of cores (1 as default)
    
    % reachPRM.ref_input = input_ref;
    unsafeRegion = HalfSpace(G,g);
    % Formal verification 
    [safe, ctE, vT] = nncs.verify(reachPRM,unsafeRegion);
    end
    
    