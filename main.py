#!/usr/bin/env python3

from bisection_optimizer import BisectionOptimizer
from golden_section_search_optimizer import GoldenSectionSearchOptimizer
from function import UnaryFunction
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

def visualize_result(result):
    print(f'The result is {result}')

def calculate(arguments: ProgramArguments):
    optimizer = get_optimizer(arguments.optimizerType)
    function = get_function(arguments.expression)
    functionRange = arguments.functionRange
    stopCondition = arguments.stopCondition
    epochs = arguments.epochs
    unimodal_check_n = arguments.unimodal_check_n
    n = arguments.n

    if not is_function_unimodal_in_range(function, functionRange, unimodal_check_n):
        print('Function is NOT unimodal')
        functionRange = get_unimodal_range(function, functionRange, n)

    result_x =  optimizer.optimize(function, functionRange, stopCondition, epochs)
    visualize_result(result_x)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.setOnCalculationStart(calculate)
    gui.show()
    sys.exit(app.exec_())