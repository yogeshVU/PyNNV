function [safe,ctE, vT] = DLinearNNCS_verify(NN_path,A,B,C,D,Ts,lb,ub,num_of_steps,reachMethod,num_of_cores,lb_ref,ub_ref,G,g)
    %% Create the NNV class (NNCS class)
    % disp('A value is=')
    % disp(A)
    % disp('B value is=')
    % disp(B)
    % disp('C value is=')
    % disp(C)
    % disp('D value is=')
    % disp(D)
    % disp('Ts value is=')
    % disp(Ts)
    % disp('lb value is=')
    % disp(lb)
    % disp('ub value is=')
    % disp(ub)
    % disp('lb_ref value is=')
    % disp(lb_ref)
    % disp('ub_ref value is=')
    % disp(ub_ref)
    % disp('G value is=')
    % disp(G)
    % disp('g value is=')
    % disp(g)
    



    
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
    % reachPRM.ref_input = input_ref;
    % reachPRM.ref_input = Star(lb_ref,ub_ref);
    % reachPRM.ref_input = [30;1.4]

    if ~isempty(lb_ref) && ~isempty(ub_ref)
        if lb_ref == ub_ref
            reachPRM.ref_input = lb_ref;
        else
            reachPRM.ref_input = Star(lb_ref,ub_ref);% User specifies reference input ([] as default (empty = no reference inputs needed))
        end
    else
        reachPRM.ref_input = [];
    end

    [R,rt] = nncs.reach(reachPRM);
    % disp("R value =")
    % disp(R)
    % disp("rt value=")
    % disp(rt)
    
    unsafeRegion = HalfSpace(G,g);
    
    % disp('unsafeRegion=')
    % disp(unsafeRegion)
    % Formal verification
    % disp('reachPRM=')
    % disp(reachPRM) 
    [safe,ctE, vT] = nncs.verify(reachPRM,unsafeRegion);
    disp(safe)
    % disp(ctE)
    disp(vT)
    end
    