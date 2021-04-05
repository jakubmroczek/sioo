#!/usr/bin/env python3

# assume we look for miniums

from enum import Enum
from bisection_optimizer import BisectionOptimizer
from golden_section_search_optimizer import GoldenSectionSearchOptimizer

class OptimizerType(Enum):
    BISECTION = 0,
    GOLDEN_SECTION_SEARCH = 1

class UnaryFunction:
    def __init__(self, expression):
        super().__init__()
        self.expression = expression

    def evalute(self, x):
        self.x = x
        return eval(self.expression)

def get_function(expression):
    return UnaryFunction(expression)

class FunctionRange:
    def __init__(self, low, high):
        super().__init__()
        self.low = low
        self.high = high

    def intersects(self, other):
        pass

    # Call only this method is the ranges intersects
    def sum(self, other):
        pass


def get_optimizer(optimzierType):
    if optimzierType == OptimizerType.BISECTION:
        return BisectionOptimizer()
    else:
        return GoldenSectionSearchOptimizer()


def is_function_unimodal_in_range(function, functionRange, unimodal_check_n):
    x1, x2 = functionRange.low, functionRange.high
    function_x1, function_x2 = function.evalute(x1), function.evalute(x2)
    step = abs(x2 - x1) / unimodal_check_n

    minimum_found = False

    for i in range(1, unimodal_check_n + 1):
        x = x1 + step * i
        function_x = function.evalute(x)

        if not minimum_found:
            if function_x1 < function_x:

                minimum_found = True
                # Minimum can NOT be in the x1
                if i == 1:
                    return False

        else:
            if not function_x1 <= function_x:
                return False

        function_x1 = function_x

    # Function can NOT also be only declaining
    return minimum_found

def bounding_phases_method(function, x, delta):

    case0:

    x0 = x
    delta = abs(delta)
    k = 0

    if f(x (0) − |∆|) ≥ f(x (0)) ≥ f(x (0) + |∆|):
        ∆ > 0
    if f(x (0) − |∆|) ≤ f(x (0)) ≤ f(x (0) + |∆|):
        ∆ < 0;
    else
        jump case0

    # krok 3
    x1 = x0 + 2 * k * delta
    if f(x (k+1)) < f(x (k) ):
        ustal k = k + 1
        jump krok3

    else:
        return (x (k−1), x(k+1))

def intersects(range1, range2):
    pass

def get_unimodal_range(function, functionRange):
    # Szukamy począwszy od a i b (low, high)
    # Jeśli wyliczone przedziały mają cześc wspolna to zwracamy ich sume.
    left_range = bounding_phases_method(function, functionRange.low)
    right_range = bounding_phases_method(function, functionRange.high)

    if left_range.intersects(right_range):
        return left_range.sum(right_range)
    else:
        return [left_range, right_range]

def visualize_result(result):
    print(f'The result is {result}')


class ProgramArguments:

    def __init__(self):
        super().__init__()
        self.optimizerType = OptimizerType.GOLDEN_SECTION_SEARCH
        self.expression = '-x- 1'
        self.functionRange = FunctionRange(-0.1, 10)
        self.stopCondition = lambda epoch, result :  False
        self.epochs = 25
        self.unimodal_check_n= 100

if __name__ == '__main__':
    arguments = ProgramArguments()

    # cli arguments layer
    optimizer = get_optimizer(arguments.optimizerType)
    function = get_function(arguments.expression)
    functionRange = arguments.functionRange
    stopCondition = arguments.stopCondition
    epochs = arguments.epochs
    unimodal_check_n = arguments.unimodal_check_n

    if not is_function_unimodal_in_range(function, functionRange, unimodal_check_n):
        range = get_unimodal_range(function, functionRange)

    result_x =  optimizer.optimize(function, functionRange, stopCondition, epochs)
    visualize_result(result_x)
