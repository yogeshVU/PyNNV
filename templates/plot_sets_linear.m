function plot_sets_linear(starSet,method,varargin)

    %% plot_sets(starSet,method,varargin)
    % Generates a reachable set plot for NNV integration
    % Inputs:
    %   - starSet: reachable set to plot (Star)
    %   - method: choose from ['exact','boxes2d', 'boxes3d', 'ranges', 'nofill']
    %   - varagin:
    %      1) color: color for the reach sets (e.g. 'r')
    %      2) x-dim: dimension of set to plot in x-axis
    %      3) y-dim: dimension of set to plot in y-axis
    %      4) z-dim: dimension of set to plot in z-axis (only for 'boxes3d')
    %
    % NOTES
    % If method == exact, starSet must be a 2 dimensional set. Only first 2
    % inputs required.
    % For all other methods, user must specified color, x-dim and y-dim.
    % If method = 'ranges', y-dim corresponds to the times vector.
    starSet = starSet{1}
    z_dim = 0
    x_dim = 0
    y_dim = 0

    if nargin == 2
        color = 'r';
    elseif nargin == 3
        color = varargin{1};
    elseif nargin == 4
        color = varargin{1};
        x_dim = varargin{2};
        y_dim = x_dim;
    elseif nargin == 5
        color = varargin{1};
        x_dim = varargin{2};
        y_dim = varargin{3};
    elseif nargin == 6
        color = varargin{1};
        x_dim = varargin{2};
        y_dim = varargin{3};
        z_dim = varargin{4};
    else
        error('Number of inputs must be 2,3,4,5 or 6. For more info, >>help plot_sets.m')
    end
    %f = figure;
    f = figure('visible', 'off');

    if contains(method,'exact')
        Star.plots(starSet,color);
        xlabel('x_1');
        ylabel('x_2');
    elseif contains(method,'boxes2d')
        Star.plotBoxes_2D(starSet,x_dim,y_dim,color);
        xlabel('x_'+string(x_dim));
        ylabel('x_'+string(y_dim));
    elseif contains(method,'boxes3d')
        Star.plotBoxes_3D(starSet,x_dim,y_dim,z_dim,color);
        xlabel('x_'+string(x_dim));
        ylabel('x_'+string(y_dim));
        zlabel('x_'+string(z_dim));
    elseif contains(method,'nofill')
        Star.plotBoxes_2D_noFill(starSet,x_dim,y_dim,color);
        xlabel('x_'+string(x_dim));
        ylabel('x_'+string(y_dim));
    elseif contains(method,'ranges')
        times = 0:1:(length(starSet)-1);
        Star.plotRanges_2D(starSet,x_dim,times,color);
        ylabel('x_'+string(x_dim));
        xlabel('Time');
    else
        error('Unrecognize method. Please, select one of the following: exact, boxes2d, boxes3d, nofill or ranges');
    end
    % Save figure
    A = [x_dim y_dim z_dim];
    ttmp = sprintf('%d',A);
    filename_ = append('NNVFigure',ttmp,'.svg')
    disp(filename_)
    saveas(f,filename_);
    end
