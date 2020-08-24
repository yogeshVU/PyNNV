%% Load network
net = load('../vgg16nnv.mat'); 
% net = load('path-to-CNN'); 
net =struct2cell(net);
net = net{1};

% Inputs/variables/parameters defined by user
% 1) Path to controller
% 2) Path to image
% 3) mean (normalize image)
% 4) std (normalize image)
% 5) threshold to apply attack
% 6) delta = percentage of attack
% 7) reach-method = 'approx-star' or 'exact-star'

% Load image
% If saved as matlab format
%    load('image_path'); 
% If saved as another format
image = imread('../image40.png');
% image = imread('image_path');
im_target = 6;
% im_target = 'image-label'; 
image = double(image); 
channels = size(image,3);
w = size(image,1);
h = size(image,2);


%% Analysis
% For testing
% threshold = 'input_threshold'; % i.e. threshold = 245;
threshold = 237;
% delta = 'input_percenatge_of_attack'; % i.e. delta = 0.01; (percentage)
delta = 0.01;
% std = 'input_standard_deviation'; % one value or vector with one value for each channel 
std = [0.2023, 0.1994, 0.2010];
% mean = 'inpu_mean'; % One value if greyscale, vector of lebgth three,  one for each channel
mean = [0.4914, 0.4822, 0.4465];
reach_method = 'approx-star'; % or 'exact-star'
% Grayscale -> channels = 1;
% RGB -> channels = 3
if channels == 3 && length(mean) == 1
    mean = [mean mean mean];
elseif channels == 3 && length(mean) ~= 3
    error('Please, select a valid mean vector');
end
% Check std
if channels == 3 && length(std) == 1
    std = [std std std];
elseif channels == 3 && length(std) ~= 3
    error('Please, select a valid mean vector');
end

% Image perturbation
inputStar = [];
for c=1:channels
    IM =image(:,:,c);
    lb = IM;
    ub = IM;
    for p=1:(w*h)
        if  IM(p) >= threshold
            lb(p) = 255-255*delta;
            ub(p) = 255;
        end
    end
    % Normalize input set
    lb = reshape(lb,[w,h]);
    lb = ((lb./255)-mean(c))./std(c);
    ub = reshape(ub,[w,h]);
    ub = ((ub./255)-mean(c))./std(c);
    LB(:,:,c) = lb;
    UB(:,:,c) = ub;
end
S = ImageStar(LB,UB);
inputSetStar = S;

%% Evaluate robustness
c = parcluster('local');
numCores = c.NumWorkers; % specify number of cores used for verification

% Evaluation using approx-star method (timeout 0f 2 minutes for each image)
t = tic;
r_nn = net.verifyRobustness(inputSetStar, im_target, reach_method, numCores);
VT_nn = toc(t);

%% Check results
disp(' ');
disp('Robusteness analysis total time = '+string(VT_nn));
disp('Robust = ' + string (r_nn));