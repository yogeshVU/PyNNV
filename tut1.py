import matlab.engine
from pathlib import Path

# START MATLAB ENGINE
eng = matlab.engine.start_matlab()
# eng = matlab.engine.start_matlab('-nojvm')


# ADD PATHS OF NEEDED FUNCTIONS TO MATLAB ENVIRONMENT
matlab_function_path_list = []

local_matlab_function_path = str(Path(Path(__file__).absolute().parent, "templates/CNN/Brightening"))

matlab_function_path_list.append(local_matlab_function_path)

local_matlab_function_path = str(Path(Path(__file__).absolute().parent, "templates/CNN/Darkening"))
matlab_function_path_list.append(local_matlab_function_path)

local_matlab_function_path = str(Path(Path(__file__).absolute().parent, "templates/CNN/RandomNoise"))
matlab_function_path_list.append(local_matlab_function_path)

# image_path = str(Path(Path(__file__).absolute().parent, "templates/CNN/image40.png"))

#
# EXECUTE MATLAB ENGINE
#
eng.addpath(*matlab_function_path_list)
# nnv_dir = Path("home","ubuntu","yogesh","aatools","diego-nnv","nnv", "code","nnv")
eng.addpath(eng.genpath('/home/ubuntu/yogesh/aatools/diego-nnv/nnv/code/nnv'))
# eng.addpath(str(nnv_dir))

# network_directory_path = Path(Path(__file__).absolute().parent,"templates/CNN")
# mat_file_list = sorted(network_directory_path.glob("*.mat"))

try:

    meanV, stdV, reach_method  = (matlab.double([0.4914, 0.4822, 0.4465]) , matlab.double([0.2023, 0.1994, 0.2010]) , 'approx-star')
    eng.cd(str(Path(Path(__file__).absolute().parent, "templates/CNN/Brightening")),nargout=0)
    # mat_file = str(Path(Path(__file__).absolute().parent, "templates","CNN", 'vgg16nnv.mat').absolute())
    image_path = str(Path(Path(__file__).absolute().parent, "templates","CNN", 'image40.png').absolute())
    # print(mat_file)
    print(image_path)

    network_directory_path = Path(Path(__file__).absolute().parent, "templates","CNN")
    mat_file_list = sorted(network_directory_path.glob("*.mat"))
    print(mat_file_list)
    if len(mat_file_list) == 0:
        raise RuntimeError(
            "lec directory \"{0}\" must contain at least one mat-file"
            " (that contains a neural network).".format(network_directory_path)
        )
    mat_file = mat_file_list[0].absolute()

    
    # print(mat_file)
    # net = eng.load(str(mat_file))

    # eng.example(nargout=0)
    # rnn = eng.example(nargout=0)
    # rnn = eng.test_attach(str(mat_file), '../image40.png', 6 , 245 , 0.01 ,meanV, stdV, reach_method)
    # Works
    rnn = eng.darkening_attack(str(mat_file), image_path, 6 , 245 , 0.01 ,meanV, stdV, reach_method)
    # Works
    # rnn = eng.bright_attack(str(mat_file), image_path, 6 , 245 , 0.01 ,meanV, stdV, reach_method)

    # RandomNoise_example:
    # pixels =100
    # rnn = eng.randomnoise_attack(str(mat_file), image_path, 6 , 245 , 0.01 ,meanV, stdV, reach_method, pixels)

    # To delete
    # rnn = eng.bright_attack('../vgg16nnv.mat','../image40.png',6,245,0.01,[0.4914, 0.4822, 0.4465],[0.2023, 0.1994, 0.2010],'approx-star')
    print(rnn)

except:
    print("An exception occurred")
    eng.exit()

eng.exit()