function [safe, counterExamples, verifyTime] = DNonLinear_verify(NN_path,dynamics_func,dim,nI,Ts,outputMat,feedbackMap,lb,ub,num_of_steps,reachMethod,lb_ref,ub_ref,G,g)
    %% Create the NNV class (NNCS class)
    % Load controller
    controller = Load_nn(NN_path); % User specifies 
    % Load plant (method 1)
    plant = DNonLinearODE(dim,nI,str2func(dynamics_func),Ts,outputMat); % User specifies all matrices and time step (Ts)
    % Contruct NNCS objLct
    nncs = DNonlinearNNCS(controller,plant,feedbackMap);
    
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
    reachPRM.init_set = Star(lb,ub);
    reachPRM.numSteps = num_of_steps;
    reachPRM.reachMethod = reachMethod;
    reachPRM.numCores = 1;
    % reachPRM.ref_input = ref_input;
    unsafeRegion = HalfSpace(G,g); % User specifies G and g (Half-space matrix and half-space vector , G*x <= g)
    [safe, counterExamples, verifyTime] = nncs.verify(reachPRM,unsafeRegion); % Execute verification analysis
    
end
% [a,b,c] = DNonLinear_verify('controller_test.mat',@test_dynamicsD,6,1,0.2,[0 0 0 0 1 0;1 0 0 -1 0 0; 0 1 0 0 -1 0],[0],[90;29;0;30;30;0], [92;30;0;31;30.2;0], 5, 'approx-star',[30;1.4], [1 0 0 -1 -1.4 0],10 );