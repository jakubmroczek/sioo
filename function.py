# Do not delete this, otherwise the app will not support many standard math_utils function!!
from math import *

class UnaryFunction:
    def __init__(self, expression):
        super().__init__()
        self.expression = expression

    def evalute(self, x):
        self.x = x
        return eval(self.expression)

class MultiNumberFunction:
    '''
    Supports up to 8 arguments
    '''
    ARGUMENTS = ['x', 'y', 'z', 'v', 'w', 'q', 'r', 't']

    # We have to pass this map in eval functions, cause otherwise some math stuff is not visible
    GLOBALS = {
        'sin': sin,
        'cos': cos,
        'log': log,
    }

    def __init__(self, expression, argc):
        self.expression = expression
        self.argc = argc
        assert argc <= len(self.ARGUMENTS)

    def evaluate(self, argv):
        assert len(argv) == self.argc
        arguments = {}
        for index in range(self.argc):
            argument_name = self.ARGUMENTS[index]
            argument_value = argv[index]
            arguments[argument_name] = argument_value
        return eval(self.expression, self.GLOBALS, arguments)


class FunctionInterval:
    def __init__(self, low, high):
        super().__init__()
        assert low <= high, f'{low}, {high}'
        self.low = low
        self.high = high

    def __str__(self):
        return f'({self.low}, {self.high})'

    def __repr__(self) -> str:
        return self.__str__()


