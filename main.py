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
        print(eval(self.expression))
        return eval(self.expression)

def get_function(expression):
    return UnaryFunction(expression)


class BisectionOptimzer(object):

    def step(self, f, a, b):
        if f.evalute(a)*f.evalute(b) >= 0:
            print("Bisection method fails.")
            return None

        print(a, b)

        a_n = a
        b_n = b

        m_n = (a_n + b_n)/2
        f_m_n = f.evalute(m_n)

        if f.evalute(a_n)*f_m_n < 0:
            a_n = a_n
            b_n = m_n
        elif f.evalute(b_n)*f_m_n < 0:
            a_n = m_n
            b_n = b_n
        elif f_m_n == 0:
            print("Found exact solution.")
            return m_n
        else:
            print("Bisection method fails.")
            return None

        return (a_n + b_n)/2



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
    result_x = range.low

    epoch = 0

    while not stopCondition(epoch, result_x):
        result_x = optimizer.step(function, range.low, range.high)
        epoch = epoch + 1

    return result_x

def visualize_result(result):
    pass


class ProgramArguments:

    def __init__(self):
        super().__init__()
        self.optimizerType = OptimizerType.BISECTION
        self.expression = 'x ** 2 - 1'
        self.range = Range(0, 10)
        self.stopCondition = lambda epoch, result :  False

if __name__ == '__main__':
    arguments = ProgramArguments()

    # cli arguments layer
    optimizer = get_optimizer(arguments.optimizerType)
    function = get_function(arguments.expression)
    range = arguments.range
    stopCondition = arguments.stopCondition

    if not is_function_unimodal_in_range(function, range):
        range = get_unimodal_range(function, range)

    result =  optimize(optimizer, function, range, stopCondition)
    visualize_result(result)