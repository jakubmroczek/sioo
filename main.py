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
    return eval(expression)


def get_function_range():
    pass


def is_function_unimodal_in_range(function, range):
    pass


def get_unimodal_range(function, range):
    pass


def run_function(function, range):
    pass


def visualize_result(result):
    pass


if __name__ == '__main__':
    function = get_function()
    range = get_function_range()


    if not is_function_unimodal_in_range(function, range):
        range = get_unimodal_range(function, range)


    result =  run_function(function, range)
    visualize_result(result)