# This function will be a wrapper for the NNV tools...
# It will have functions for CNN, FNN, NNCS_DLinear, NNCS_DNonLinear, NNCS_Linear, NNCS_NonLinear

# It is going to load the json file and invoke appropriate functions..

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class NNV():
    """
    The Context defines the interface of interest to clients.
    """

    def __init__(self, strategy: Strategy) -> None:
        """
        Usually, the Context accepts a strategy through the constructor, but
        also provides a setter to change it at runtime.
        """

        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        """
        The Context maintains a reference to one of the Strategy objects. The
        Context does not know the concrete class of a strategy. It should work
        with all strategies via the Strategy interface.
        """

        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        """
        Usually, the Context allows replacing a Strategy object at runtime.
        """

        self._strategy = strategy

    def do_reachability(self) -> None:
        """
        The Context delegates some work to the Strategy object instead of
        implementing multiple versions of the algorithm on its own.
        """

        # ...

        print("Context: do_reachability using strategy")
        result = self._strategy.do_reachability()
        return result

    def do_verification(self) -> None:
        """
        The Context delegates some work to the Strategy object instead of
        implementing multiple versions of the algorithm on its own.
        """
        # ...

        print("Context: do_reachability using strategy")
        result = self._strategy.do_verification()
        return result
    

    def do_algorithm(self) -> None:
        """
        The Context delegates some work to the Strategy object instead of
        implementing multiple versions of the algorithm on its own.
        """
        # ...

        print("Context: do_algorithm using strategy")
        result = self._strategy.do_algorithm()
        return result
        # ...


class Strategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @abstractmethod
    def do_algorithm(self):
        pass

    @abstractmethod
    def do_reachability(self):
        pass
    
    @abstractmethod
    def do_verification(self):
        pass

    @abstractmethod
    def do_parse(self):
        pass
    

"""
Concrete Strategies implement the algorithm while following the base Strategy
interface. The interface makes them interchangeable in the Context.
"""


class ConcreteStrategyA(Strategy):
    def do_algorithm(self):
        return print("ConcreteStrategyA")

    def do_parse(self):
        pass

    def do_reachability(self):
        pass

    def do_verification(self):
        pass




class ConcreteStrategyB(Strategy):
    def do_algorithm(self):
        return print("ConcreteStrategyB")

    def do_parse(self):
        pass

    def do_reachability(self):
        pass

    def do_verification(self):
        pass
    
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
    config = configparser.ConfigParser()
    config.read('config.ini')
    jsonfile = Path(config['JOB_INPUT']['PARAMETER_JSON'])
    # jsonfile = Path("./input/template_parameters.json")
    
    with open(jsonfile) as f:
            data = json.load(f)

    strategy = data['NNType']
    # eng = matlab.engine.start_matlab('-nojvm')
    eng = matlab.engine.start_matlab()

    # strategy = NNVKeys.template_NN_CNN_key
    # strategy = NNVKeys.template_NN_FFNN_key
    print("The current strategy is:", strategy)

    if strategy == NNVKeys.template_NN_CNN_key:
        context = CNN(eng)
    elif strategy == NNVKeys.template_NN_FFNN_key:
        context = FFNN(eng)
    elif strategy == NNVKeys.template_NN_NNCS_ContinuousLinear_key:
        context = NNCS_Linear(eng)
    elif strategy == NNVKeys.template_NN_NNCS_ContinuousNonLinear_key:
        context = NNCS_NonLinear(eng)
    elif strategy == NNVKeys.template_NN_NNCS_DiscreteLinear_key:
        context = NNCS_Dlinear(eng)
    elif strategy == NNVKeys.template_NN_NNCS_DiscreteNonLinear_key:
        context = NNCS_DNonLinear(eng)
    else:
        print("Invalid NNType... Handler Missing for: ", strategy)
        exit()

    matlab_function_path_list = []
    for paths in config['MATLAB']['FUNCTION_PATHS'].split("\n"):
        print(paths)
        matlab_function_path_list.append(str(Path(paths)))

    eng.addpath(*matlab_function_path_list)
    NNV_PATH = str(Path(config['MATLAB']['NNV_PATH']))
    eng.addpath(eng.genpath(NNV_PATH))

    INPUT_DIR_PATH = str(Path(config['JOB_INPUT']['INPUT_DIRECTORY']))
    eng.cd(INPUT_DIR_PATH)

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

    context.parseJson(str(jsonfile))
    print(context.compute())
    eng.exit()

