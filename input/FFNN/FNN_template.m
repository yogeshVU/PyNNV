function result = FNN_template(NNpath, lb, ub, procedure, varargin)
%FNN_TEMPLATE Whatwe need to create to run NNV in a general way from the ALC toolchain
% -- INPUTS --  (Or parameters)
%    1) NNpath: path to neural network
%    2) lb: lower bound vector for the input set
%    3) ub: upper bound vector for the input set
%    4) procedure: verify or reach
% -------Other Inputs ------
%    If procedure == verify 
%         5) G: half-space matrix (required)
%         6) g: half-space vector (required)
%         7) reachMethod = 'approx-star' (default) can also be approx-star
%         8) num_cores = 1 (default), can specify more if desired
%         9) num_sims = 0 (default), can specify X number of simulations
%                                    to find counterexamples using the falsify methods
% -------------------------------------
%    If procedure == reach
%         5) reachMethod = 'approx-star'  (Remember, if the network is not
%                                       piecewise-linear, we can only use 'approx-star'
%         6)num_cores = 1 (optional)

input_set = Star(lb,ub);
Nnetwork = Load_nn(NNpath);
if strcmp(procedure,'verify')
    if nargin == 6
        unsafeRegion = HalfSpace(varargin{1},varargin{2});
        reachMethod = 'approx-star';
        num_cores = 1;
        num_sims = 0;
    elseif nargin == 7
        unsafeRegion = HalfSpace(varargin{1},varargin{2});
        reachMethod = varargin{3};
        num_cores = 1;
        num_sims = 0;
    elseif nargin == 8
        unsafeRegion = HalfSpace(varargin{1},varargin{2});
        reachMethod = varargin{3};
        num_cores = varargin{4};
        num_sims = 0;
    elseif nargin == 9
        unsafeRegion = HalfSpace(varargin{1},varargin{2});
        reachMethod = varargin{3};
        num_cores = varargin{4};
        num_sims = varargin{5};
    else
        error('Invalid number of inputs')
    end
    % Compute the verification analysis
    [safe, vt, counterExamples] = Nnetwork.verify(input_set,unsafeRegion,reachMethod,num_cores,num_sims);
    % Return the results (mostly just for the safety of the system)
    result.safe = safe; % safe (1), unsafe (0), unknown (2)
    result.vt = vt;
    result.counterExamples = counterExamples;
    disp(result)
elseif strcmp(procedure,'reach')
    disp('number of arguments=')
    disp(nargin)
    if nargin == 4
        reachMethod = 'approx-star';
        [S,t] = Nnetwork.reach(input_set,reachMethod);
    elseif nargin == 5
        reachMethod = varargin{1};
        [S,t] = Nnetwork.reach(input_set,reachMethod);
    elseif nargin == 6
        reachMethod = varargin{1};
        num_cores = varargin{2};
        [S, t] = Nnetwork.reach(input_set,reachMethod,num_cores);
    else
        error('Invalid number of inputs');
    end
    result.reachSet = S;
    result.t = t;
    disp(result.reachSet)
    save('starset.mat','S','-v7.3')

else
    error('Unknown procedure for the verification of feed-forward neural networks')
end

end
