#!/usr/bin/env python3

from bisection_optimizer import BisectionOptimizer
from golden_section_search_optimizer import GoldenSectionSearchOptimizer
from function import UnaryFunction, FunctionRange
from program_arguments import ProgramArguments, OptimizerType
from unimodality import  is_function_unimodal_in_range, exhaustive_search_method
from gui import GUI
from PyQt5.QtWidgets import QApplication
import sys

def get_function(expression):
    return UnaryFunction(expression)

def get_optimizer(optimzierType):
    if optimzierType == OptimizerType.BISECTION:
        return BisectionOptimizer()
    elif optimzierType == OptimizerType.GOLDEN_SECTION_SEARCH:
        return GoldenSectionSearchOptimizer()
    else:
        raise Exception('Unsupported optimzier type')

def get_unimodal_range(function, functionRange, n):
    unimodal_range = exhaustive_search_method(function, functionRange, n)
    return unimodal_range

class CalculationResult:

    def __init__(self, function, user_interval, unimodal_interval, minimum_interval, intermediate_intervals):
        super().__init__()
        self.function = function
        self.user_interval = user_interval
        self.unimodal_interval = unimodal_interval
        self.minimum_end_interval = FunctionRange(minimum_interval[0], minimum_interval[1])
        self.intermediate_intervals = intermediate_intervals


def calculate(arguments: ProgramArguments):
    optimizer = get_optimizer(arguments.optimizerType)
    function = get_function(arguments.expression)
    user_function_interval = arguments.functionRange
    unimodal_interval = user_function_interval
    stopCondition = arguments.stopCondition
    epochs = arguments.epochs
    unimodal_check_n = arguments.unimodal_check_n
    n = arguments.n

    if not is_function_unimodal_in_range(function, user_function_interval, unimodal_check_n):
        print('Function is NOT unimodal')
        unimodal_interval = get_unimodal_range(function, user_function_interval, n)

    result_x, minimum_end_interval, intermediate_intervals =  optimizer.optimize(function, unimodal_interval,
                                                                                 stopCondition, epochs)

    return CalculationResult(function, user_function_interval, unimodal_interval, minimum_end_interval, intermediate_intervals)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.setOnCalculationStart(calculate)
    gui.show()
    sys.exit(app.exec_())