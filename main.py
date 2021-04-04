#!/usr/bin/env python3

# assume we look for miniums

from enum import Enum

class OptimizerType(Enum):
    BISECTION = 0,
    GOLDEN_DIVISION = 1

class UnaryFunction:
    def __init__(self, expression):
        super().__init__()
        self.expression = expression

    def evalute(self, x):
        self.x = x
        return eval(self.expression)

def get_function(expression):
    return UnaryFunction(expression)


class BisectionOptimzer(object):
    pass


class GoldenDivisionOptimizer(object):
    pass


class Range:
    def __init__(self, low, high):
        super().__init__()
        self.low = low
        self.high = high


def get_optimizer(optimzierType):
    if optimzierType == OptimizerType.BISECTION:
        return BisectionOptimzer()
    else:
        return GoldenDivisionOptimizer()


def is_function_unimodal_in_range(function, range):
    return True


def get_unimodal_range(function, range):
    pass


def optimize(optimizer, function, range, stopCondition):
    result = range.low

    epoch = 0

    while not stopCondition(epoch, result):
        result, range = optimizer.step(function, range)
        epoch = epoch + 1

    return result

def visualize_result(result):
    pass


class ProgramArguments:

    def __init__(self):
        super().__init__()
        self.optimizerType = OptimizerType.BISECTION
        self.expression = 'x ** 2'
        self.range = Range(0, 10)

if __name__ == '__main__':
    arguments = ProgramArguments()

    # cli arguments layer
    optimizer = get_optimizer(arguments.optimizerType)
    function = get_function(arguments.expression)
    range = arguments.range

    if not is_function_unimodal_in_range(function, range):
        range = get_unimodal_range(function, range)

    result =  optimize(optimizer, function, range)
    visualize_result(result)