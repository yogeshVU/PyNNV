% Test the FNN_template
%% 1) Use the reach procedure
lb = [30;10;30;100;5];
ub = [31;10;30.2;101;5.1];
% result1 = FNN_template('controller_test.mat',lb,ub,'reach');
% result2 = FNN_template('controller_test.mat',lb,ub,'reach','exact-star');
% result3 = FNN_template('controller_test.mat',lb,ub,'reach','exact-star',4);
% This method returns the reachability time (result.t) and the output reach set (result.reachSet)


%% 2) Use the verify procedure
G = [-1]; % just one output
g = [-10];
% result4 = FNN_template('controller_test.mat',lb,ub,'verify',G,g);
% result5 = FNN_template('controller_test.mat',lb,ub,'verify',G,g,'exact-star');
% result6 = FNN_template('controller_test.mat',lb,ub,'verify',G,g,'exact-star',4);
result7 = FNN_template('controller_test.mat',lb,ub,'verify',G,g,'exact-star',4,10);
disp(result7)

% All of these results are meaningless, just a proof of concept