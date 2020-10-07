# This function will be a wrapper for the NNV tools...
# It will have functions for CNN, FNN, NNCS_DLinear, NNCS_DNonLinear, NNCS_Linear, NNCS_NonLinear

# It is going to load the json file and invoke appropriate functions..
from os.path import expandvars


class NNVExec:
    # obj = NNVExec(jsonfile, INPUT_DIR_PATH, config_file)
    def __init__(self, parameter_json, input_dir_path, config_file='config.ini'):
        print('config file',config_file)
        config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        config.read(config_file)
        jsonfile = parameter_json
        with open(jsonfile) as f:
            data = json.load(f)

        strategy = data['NNType']
        
        # eng = matlab.engine.start_matlab('-nojvm')
        eng = matlab.engine.start_matlab()
        # This is the input directory generated from the webgme path

        # Add all the MATLAB functions....
        matlab_function_path_list = []
        for paths in config['MATLAB']['FUNCTION_PATHS'].split("\n"):
            print(expandvars(paths))
            matlab_function_path_list.append(str(expandvars(paths)))

        eng.addpath(*matlab_function_path_list)

        ## Add the NNV path...
        NNV_PATH = str(Path(config['MATLAB']['NNV_PATH']))
        eng.addpath(eng.genpath(NNV_PATH))

        print("The current strategy is:", strategy)

        eng.cd(input_dir_path)
        context = None
        if strategy == NNVKeys.template_NN_CNN_key:
            context = CNN(eng)
        elif strategy == NNVKeys.template_NN_FFNN_key:
            context = FFNN(eng)
        elif strategy == NNVKeys.template_NN_NNCS_ContinuousLinear_key:
            context = NNCS_Linear(eng)
        elif strategy == NNVKeys.template_NN_NNCS_ContinuousNonLinear_key:
            func_file_name = Path(input_dir_path,str(data['dynamic_func'] + ".m"))
            print(func_file_name)
            with func_file_name.open("w", encoding="utf-8") as file_fp:
                try:
                    file_fp.write(data['file'])
                    file_fp.close()
                except Exception as err1:
                    print(err1)

            context = NNCS_NonLinear(eng)
        elif strategy == NNVKeys.template_NN_NNCS_DiscreteLinear_key:
            context = NNCS_Dlinear(eng)
        elif strategy == NNVKeys.template_NN_NNCS_DiscreteNonLinear_key:
            func_file_name = Path(input_dir_path,str(data['dynamic_func'] + ".m"))
            print(func_file_name)
            with func_file_name.open("w", encoding="utf-8") as file_fp:
                try:
                    file_fp.write(data['file'])
                except Exception as err1:
                    print(err1)
            context = NNCS_DNonLinear(eng)
        else:
            print("Invalid NNType... Handler Missing for: ", strategy)
            exit()

        context.parseJson(str(jsonfile))
        print(context.compute())
        eng.exit()

        # INPUT_DIR_PATH = str(Path(config['JOB_INPUT']['INPUT_DIRECTORY']))
        # jsonfile = Path(config['JOB_INPUT']['PARAMETER_JSON'])
        # jsonfile = Path("./input/template_parameters.json")

        # strategy = NNVKeys.template_NN_CNN_key
        # strategy = NNVKeys.template_NN_FFNN_key

        # For CNN we need to have the imagefile and the controller mat-file
        # jsonfile = Path("./input/CNN/inputJson.json")
        # eng.cd(str(Path("./input/CNN")))

        # FNN
        # jsonfile = Path("./input/FFNN/inputJson.json")
        # eng.cd(str(Path("./input/FFNN")))

        # ContinuousLinearNNCS
        # jsonfile = Path("./input/ContinuousLinearNNCS/inputJson.json")
        # eng.cd(str(Path("./input/ContinuousLinearNNCS")))

        # ContinuousNonLinearNNCS
        # jsonfile = Path("./input/ContinuousNonLinearNNCS/inputJson.json")
        # eng.cd(str(Path("./input/ContinuousNonLinearNNCS")))

        # DiscreteLinearNNCS
        # jsonfile = Path("./input/DiscreteLinearNNCS/inputJson.json")
        # eng.cd(str(Path("./input/DiscreteLinearNNCS")))

        # DiscreteNonLinearNNCS
        # jsonfile = Path("./input/DiscreteNonLinearNNCS/inputJson.json")
        # eng.cd(str(Path("./input/DiscreteNonLinearNNCS")))



from pathlib import Path
import json
from CNN import CNN
from FFNN import FFNN
from NNCS_NonLinear import NNCS_NonLinear  # Continuous Non Linear
from NNCS_Dlinear import NNCS_Dlinear # Discrete Linear
from NNCS_DNonLinear import NNCS_DNonLinear # Discrete NonLinear
from NNCS_Linear import NNCS_Linear

import matlab.engine


import NNVKeys
import configparser

if __name__ == "__main__":
    config_file = 'config.ini'


    config = configparser.ConfigParser()
    config.read(config_file)

    jsonfile = Path(config['JOB_INPUT']['PARAMETER_JSON']) or None
    INPUT_DIR_PATH = str(Path(config['JOB_INPUT']['INPUT_DIRECTORY'])) or None

    # jsonfile = Path("./input/template_parameters.json")
    obj = NNVExec(jsonfile,INPUT_DIR_PATH,config_file)

    # with open(jsonfile) as f:
    #         data = json.load(f)
    #
    # strategy = data['NNType']
    # # eng = matlab.engine.start_matlab('-nojvm')
    # eng = matlab.engine.start_matlab()
    #
    # # strategy = NNVKeys.template_NN_CNN_key
    # # strategy = NNVKeys.template_NN_FFNN_key
    # print("The current strategy is:", strategy)
    #
    # if strategy == NNVKeys.template_NN_CNN_key:
    #     context = CNN(eng)
    # elif strategy == NNVKeys.template_NN_FFNN_key:
    #     context = FFNN(eng)
    # elif strategy == NNVKeys.template_NN_NNCS_ContinuousLinear_key:
    #     context = NNCS_Linear(eng)
    # elif strategy == NNVKeys.template_NN_NNCS_ContinuousNonLinear_key:
    #     context = NNCS_NonLinear(eng)
    # elif strategy == NNVKeys.template_NN_NNCS_DiscreteLinear_key:
    #     context = NNCS_Dlinear(eng)
    # elif strategy == NNVKeys.template_NN_NNCS_DiscreteNonLinear_key:
    #     context = NNCS_DNonLinear(eng)
    # else:
    #     print("Invalid NNType... Handler Missing for: ", strategy)
    #     exit()
    #
    # matlab_function_path_list = []
    # for paths in config['MATLAB']['FUNCTION_PATHS'].split("\n"):
    #     print(paths)
    #     matlab_function_path_list.append(str(Path(paths)))
    #
    # eng.addpath(*matlab_function_path_list)
    # eng.addpath(eng.genpath(NNV_PATH))
    #
    # eng.cd(INPUT_DIR_PATH)

    # For CNN we need to have the imagefile and the controller mat-file
    # jsonfile = Path("./input/CNN/inputJson.json")
    # eng.cd(str(Path("./input/CNN")))

    # FNN
    # jsonfile = Path("./input/FFNN/inputJson.json")
    # eng.cd(str(Path("./input/FFNN")))

    # ContinuousLinearNNCS
    # jsonfile = Path("./input/ContinuousLinearNNCS/inputJson.json")
    # eng.cd(str(Path("./input/ContinuousLinearNNCS")))

    # ContinuousNonLinearNNCS
    # jsonfile = Path("./input/ContinuousNonLinearNNCS/inputJson.json")
    # eng.cd(str(Path("./input/ContinuousNonLinearNNCS")))

    #DiscreteLinearNNCS
    # jsonfile = Path("./input/DiscreteLinearNNCS/inputJson.json")
    # eng.cd(str(Path("./input/DiscreteLinearNNCS")))

    #DiscreteNonLinearNNCS
    # jsonfile = Path("./input/DiscreteNonLinearNNCS/inputJson.json")
    # eng.cd(str(Path("./input/DiscreteNonLinearNNCS")))

    # context.parseJson(str(jsonfile))
    # print(context.compute())
    # eng.exit()

