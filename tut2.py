import matlab.engine
from pathlib import Path
import json

# START MATLAB ENGINE
eng = matlab.engine.start_matlab()
# eng = matlab.engine.start_matlab('-nojvm')





# ADD PATHS OF NEEDED FUNCTIONS TO MATLAB ENVIRONMENT
matlab_function_path_list = []
local_matlab_function_path = str(Path(Path(__file__).absolute().parent, "templates/NNCS/DLinear"))
matlab_function_path_list.append(local_matlab_function_path)
# local_matlab_function_path = str(Path(Path(__file__).absolute().parent, "templates/NNCS/DNonlinear"))
# matlab_function_path_list.append(local_matlab_function_path)

#
# EXECUTE MATLAB ENGINE
#
eng.addpath(*matlab_function_path_list)
# nnv_dir = Path("home","ubuntu","yogesh","aatools","diego-nnv","nnv", "code","nnv")
eng.addpath(eng.genpath('/home/ubuntu/yogesh/aatools/diego-nnv/nnv/code/nnv'))
# eng.addpath(str(nnv_dir))





# meanV, stdV, reach_method  = (matlab.double([0.4914, 0.4822, 0.4465]) , matlab.double([0.2023, 0.1994, 0.2010]) , 'approx-star')
# eng.cd(str(Path(Path(__file__).absolute().parent, "templates/CNN/Brightening")),nargout=0)
# mat_file = str(Path(Path(__file__).absolute().parent, "templates","CNN", 'vgg16nnv.mat').absolute())
# image_path = str(Path(Path(__file__).absolute().parent, "templates","CNN", 'image40.png').absolute())
# print(mat_file)
# print(image_path)

# network_directory_path = Path(Path(__file__).absolute().parent, "templates","NNCS","DLinear")
# mat_file_list = sorted(network_directory_path.glob("*.mat"))
# print(mat_file_list)
# if len(mat_file_list) == 0:
#     raise RuntimeError(
#         "lec directory \"{0}\" must contain at least one mat-file"
#         " (that contains a neural network).".format(network_directory_path)
#     )
# mat_file = mat_file_list[0].absolute()

try:
    # rnn = eng.randomnoise_attack(str(mat_file), image_path, 6 , 245 , 0.01 ,meanV, stdV, reach_method, pixels)
    eng.cd(str(Path(Path(__file__).absolute().parent, "templates/NNCS/DLinear")),nargout=0)
    # rnn = eng.example1(nargout=0)
    rnn = eng.DLinearNNCS_verify(nargout=0)
    
    # x = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # x_matlab = matlab.double(x)
    # eng.test_array(x_matlab)
#     x = [[0 ,1 , 0 , 0 , 0 , 0 , 0],
#  [ 0,  0,  1,  0 , 0 , 0 , 0],
#  [ 0,  0 , 0,  0 , 0 , 0 , 1],
#  [ 0 , 0 , 0 , 0 , 1,  0  ,0],
#  [ 0 , 0,  0,  0 , 0,  1  ,0],
#  [ 0 , 0 , 0 , 0 , 0, -2  ,0],
#  [ 0 , 0 ,-2 , 0,  0,  0  ,0]]
#     x_matlab = matlab.double(x)
#     eng.test_array(x_matlab)

except:
    print("An exception occurred")
    eng.exit()

eng.exit()