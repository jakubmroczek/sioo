#!/usr/bin/env python3

from bisection_optimizer import BisectionOptimizer
from golden_section_search_optimizer import GoldenSectionSearchOptimizer
from scipy_bisection_optimzer import SciPyBisectionOptimizer
from scipy_golden_section_search_optimizer import SciPyGoldenSectionSearchOptimizer
from function import UnaryFunction, FunctionInterval
from program_arguments import ProgramArguments, OptimizerType
from unimodality import  is_function_unimodal_in_interval, exhaustive_search_method
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
    elif optimzierType == OptimizerType.SCIPY_BISECTION:
        return SciPyBisectionOptimizer()
    else:
        return SciPyGoldenSectionSearchOptimizer()

def get_unimodal_range(function, functionInterval, n):
    unimodal_range = exhaustive_search_method(function, functionInterval, n)
    return unimodal_range

class CalculationResult:
    def __init__(self, function, user_interval, unimodal_interval, result_x, minimum_interval, intermediate_intervals):
        super().__init__()
        self.function = function
        self.user_interval = user_interval
        self.result_x = result_x
        self.unimodal_interval = unimodal_interval
        if not minimum_interval == None:
            self.minimum_end_interval = FunctionInterval(minimum_interval[0], minimum_interval[1])
        else:
            self.minimum_end_interval = None
        self.intermediate_intervals = intermediate_intervals

    def __str__(self) -> str:
        result = ''
        result += f'Function: "{self.function.expression}"\n'
        result += f'User interval: "{self.user_interval}"\n'
        result += f'Unimodal interval: "{self.unimodal_interval}"\n'
        result += f'Result x: "{self.result_x}"\n'
        result += f'Minimum interval: "{self.minimum_end_interval}"\n'
        result += f'Intermediate intervals: "{self.intermediate_intervals}"'
        return result

def log_to_console(obj):
    print('--' * 10)
    print(obj)
    print('\n')

def is_scipy_optimzier(optimizerType):
    return optimizerType == OptimizerType.SCIPY_BISECTION or optimizerType == OptimizerType.SCIPY_GOLDEN_SECTION_SEARCH


def make_stop_conditon(max_iterations, xtol):
    # >= cause iterations start from 0
    stop_condition = lambda iteration, a, b : iteration >= max_iterations or abs(b - a) < xtol
    return stop_condition

def calculate(arguments: ProgramArguments):
    optimizer = get_optimizer(arguments.optimizerType)
    function = get_function(arguments.expression)
    user_function_interval = arguments.functionInterval
    unimodal_interval = user_function_interval
    max_iterations = arguments.max_iterations
    unimodal_check_n = arguments.unimodal_check_n
    xtol = arguments.xtol
    n = arguments.n
    stopCondition = make_stop_conditon(max_iterations, xtol)

    if not is_function_unimodal_in_interval(function, user_function_interval, unimodal_check_n):
        print('Function is NOT unimodal')
        unimodal_interval = get_unimodal_range(function, user_function_interval, n)


    if not is_scipy_optimzier(arguments.optimizerType):
        result_x, minimum_end_interval, intermediate_intervals =  optimizer.optimize(function, unimodal_interval,
                                                                                     stopCondition, max_iterations)
        calculationResult = CalculationResult(function, user_function_interval, unimodal_interval, result_x,
                                              minimum_end_interval, intermediate_intervals)
    else:
        # I have not fonud any explicit information in the SciPy documentation that the function interval got to be
        # unimodal
        result_x = optimizer.optimize(function, user_function_interval, xtol, max_iterations)
        calculationResult = CalculationResult(function, user_function_interval, unimodal_interval, result_x, None, None)


    log_to_console(calculationResult)

    return calculationResult

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.setOnCalculationStart(calculate)
    gui.show()
    sys.exit(app.exec_())