function r_nn = bright_attack(path_to_CNN, image_path, im_target, threshold, delta, meanV, stdV, reach_method)
    %% Load network
    net = load(path_to_CNN); % net = load('vgg16nnv.mat'); % Load network
    net =struct2cell(net);
    net = net{1};
    % Inputs/variables/parameters defined by user
    % 1) Path to controller
    % 2) Path to image
    % 3) im_target
    % 3) mean (normalize image)
    % 4) std (normalize image)
    % 5) threshold to apply attack
    % 6) delta = percentage of attack
    % 7) reach-method = 'approx-star' or 'exact-star'
    % Load image
    % If saved as matlab format
%     load(image_path); 
    % If saved as another format

    image_path = image_path
    
    image = imread(image_path);
    image = double(image); 
    channels = size(image,3);
    w = size(image,1);
    h = size(image,2);
    %% Analysis
    % For testing
%     threshold = 'input_threshold'; % i.e. threshold = 245;
%     delta = 'input_percenatge_of_attack'; % i.e. delta = 0.01; (percentage)
%     std = 'input_standard_deviation'; % one value or vector with one value for each channel 
%     mean = 'inpu_mean'; % One value if greyscale, vector of lebgth three,  one for each channel
%     reach_method = 'approx-star'; % or 'exact-star'
    % Grayscale -> channels = 1;
    % RGB -> channels = 3

    meanV = meanV
    stdV= stdV
    threshold = threshold
    im_target = im_target
    delta = delta
    reach_method = reach_method

    if channels == 3 && length(meanV) == 1
        meanV = [meanV meanV meanV];
    elseif channels == 3 && length(meanV) ~= 3
        error('Please, select a valid mean vector');
    end
    % Check std
    if channels == 3 && length(stdV) == 1
        stdV = [stdV stdV stdV];
    elseif channels == 3 && length(stdV) ~= 3
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
        lb = ((lb./255)-meanV(c))./stdV(c);
        ub = reshape(ub,[w,h]);
        ub = ((ub./255)-meanV(c))./stdV(c);
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
    
    disp(string(im_target))
    disp(string(reach_method))
    disp(inputSetStar)
    r_nn = net.verifyRobustness(inputSetStar, im_target , reach_method, numCores);
    VT_nn = toc(t);
    
    
    %% Check results
    disp(' ');
    disp('Robusteness analysis total time = '+string(VT_nn));
    disp('Robust = ' + string (r_nn));

end