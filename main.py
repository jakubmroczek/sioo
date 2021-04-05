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
    x0 = x
    delta = abs(delta)
    k = 0

    f_x0_minus_delta =  function.evalute(x0 - delta)
    f_x0 = function.evalute(x0)
    f_x0_plus_delta = function.evalute(x0 + delta)
    #TODO: Oblicz funckje jednokrotnie

    if f_x0_minus_delta >= f_x0 and f_x0 >= f_x0_plus_delta:
        delta = -delta
    if f_x0_minus_delta <= f_x0 and f_x0 <= f_x0_plus_delta:
        delta = delta
    else:
        # Powinniśmy skoczyc do poczatku funkcji
        raise Exception('bounding_phase_method should jump to case 1, but it is not implemented')

    # Krok 3
    while True:
        x1 = x0 + 2 * k * delta
        if function.evalute(x1) < function.evalute(x0):
            k = k + 1
            x0 = x1
        else:
            # Upewnij się, czy to k jest dobre
            low = x0 - 2 * (k - 1) * delta
            high = x1
            return FunctionRange(low, high)

def intersects(range1, range2):
    pass

def get_unimodal_range(function, functionRange, delta):
    # Szukamy począwszy od a i b (low, high)
    # Jeśli wyliczone przedziały mają cześc wspolna to zwracamy ich sume.
    left_range = bounding_phases_method(function, functionRange.low, delta)
    right_range = bounding_phases_method(function, functionRange.high, delta)

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
        self.expression = 'x ** 2 - 1'
        self.functionRange = FunctionRange(1, 10)
        self.stopCondition = lambda epoch, result :  False
        self.epochs = 25
        self.unimodal_check_n= 100
        self.delta = 0.01

if __name__ == '__main__':
    arguments = ProgramArguments()

    # cli arguments layer
    optimizer = get_optimizer(arguments.optimizerType)
    function = get_function(arguments.expression)
    functionRange = arguments.functionRange
    stopCondition = arguments.stopCondition
    epochs = arguments.epochs
    unimodal_check_n = arguments.unimodal_check_n
    delta = arguments.delta

    if not is_function_unimodal_in_range(function, functionRange, unimodal_check_n):
        range = get_unimodal_range(function, functionRange, delta)

    result_x =  optimizer.optimize(function, functionRange, stopCondition, epochs)
    visualize_result(result_x)
