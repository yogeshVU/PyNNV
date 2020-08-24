%% How I would setup the NNCS verification
% 1) Create two verification pages, one for FNN and other for NNCS
% 2) Divided NNCS into 4 pages (linear, DLinear, nonlinear, Dnonlinear)
% 3) Inside each specific NNCS class, create two separate json files with
%      parameters for the user to specify. One to create the NNCS class, the
%      other one for reachability.verification analysis.
% 4) Choose parameters, create template in jupyter notebook and run

%% How I picture it to be in the toolchain exactly
% This can be general, does not have to be tied into any specific project,
% although depends on the complexity of the system, we may need to modify
% the templates and create specific ones like we did for the UUV. 
% 1) Go to the main page for V&V
% 2) Choose between 2 options (FNN and NNCS)
% 3) If FNN, then select either verify or reach
%    a)For each option, display a table with parameters for the user to define
% 3) If NNCS, then display 4 options (linear, Dlinear, nonlinear, Dnonlinear)
%    a) For each option, create 3 tables, one for the reachability analysis
%    or verification (similar manner as for the FNN), one table for the FNN
%    and the other for the plant dynamics). Then, depend on what has been
%    chosen by the user, create the notebook and run NNV