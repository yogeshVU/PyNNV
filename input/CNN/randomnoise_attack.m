
function r_nn = randomnoise_attack(path_to_CNN, image_path, im_target, threshold, noise, meanV, stdV, reach_method, pixels)

    %% Load network
    % net = load('path-to-CNN'); % Load network
    % net = load('../vgg16nnv.mat'); 
    net = load(path_to_CNN)
    net =struct2cell(net); 
    net = net{1};

    % Inputs/variables/parameters defined by user
    % 1) Path to controller
    % 2) Path to image
    % 3) mean (normalize image)
    % 4) std (normalize image)
    % 5) noise (max value applied to each pixel)
    % 6) reach-method = 'approx-star' or 'exact-star'
    % 7) pixels = number of pixels to attack

    % Load image
    % If saved as matlab format
    %    load('image_path'); 
    % If saved as another format
    % image = imread('../image40.png');
    image = imread(image_path);
    % image = imread('image_path');
    % im_target = 6;
    im_target = im_target;
    % im_target = 'image-label'; 
    image = double(image); 
    channels = size(image,3);
    w = size(image,1);
    h = size(image,2);


    %% Analysis
    % For testing
    noise = noise;
    % noise = 0.001;
    % std = 'input_standard_deviation'; % one value or vector with one value for each channel 
    std = stdV
    % std = [0.2023, 0.1994, 0.2010];
    % mean = 'inpu_mean'; % One value if greyscale, vector of lebgth three,  one for each channel
    % mean = [0.4914, 0.4822, 0.4465];
    % reach_method = 'approx-star'; % or 'exact-star'
    reach_method = reach_method;
    pixels = pixels;
    % pixels = 100;
    pixels_random = randi([1 h*w],channels,pixels);
    % Grayscale -> channels = 1;
    % RGB -> channels = 3
    mean = meanV
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

    pixel_attack = [];
    rng(20); % set random variable to reproduce results (could set this as optional in the future)
    % Image perturbation
    inputStar = [];
    for c=1:channels
        IM =image(:,:,c);
        lb = IM;
        ub = IM;
        for p=pixels_random(c,:)
            lb(p) = max(0, IM(p) - rand*noise);
            ub(p) = min(255, IM(p)+ rand*noise);
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

end