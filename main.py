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


    def optimize(self, function, functionRange, stopCondition, epochs):
        a, b = functionRange.low,  functionRange.high


        if function.evalute(a) * function.evalute(b) >= 0:
            print("Bisection method fails.")
            return None

        a_n = a
        b_n = b

        for epoch in range(epochs):
            if stopCondition(epoch, a):
                break

            m_n = (a_n + b_n)/2
            f_m_n = function.evalute(m_n)

            if function.evalute(a_n)*f_m_n < 0:
                a_n = a_n
                b_n = m_n
            elif function.evalute(b_n)*f_m_n < 0:
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

    def optimize(self):
        pass


class FunctionRange:
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


def visualize_result(result):
    print(f'The result is {result}')


class ProgramArguments:

    def __init__(self):
        super().__init__()
        self.optimizerType = OptimizerType.BISECTION
        self.expression = 'x ** 2 - 1'
        self.functionRange = FunctionRange(0, 10)
        self.stopCondition = lambda epoch, result :  False
        self.epochs = 25

if __name__ == '__main__':
    arguments = ProgramArguments()

    # cli arguments layer
    optimizer = get_optimizer(arguments.optimizerType)
    function = get_function(arguments.expression)
    functionRange = arguments.functionRange
    stopCondition = arguments.stopCondition
    epochs = arguments.epochs

    if not is_function_unimodal_in_range(function, range):
        range = get_unimodal_range(function, range)

    result_x =  optimizer.optimize(function, functionRange, stopCondition, epochs)
    visualize_result(result_x)