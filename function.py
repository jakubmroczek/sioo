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
        'max': max
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

class Constraint:
    # TODO: We assume the rhs is equal to 0
    def __init__(self, expression, sign) -> None:
        self.expression = expression
        self.sign = sign

    def normalize(self):
        if self.sign == '<' or self.sign == '<=':
            return self.expression
        elif self.sign == '>' or self.sign == '>=':
            # TODO: Check how do we behave for large coefficients
            raise Exception(f'{self.sign} is not yet supported, please mulitply the constraint by -1')
        else:  
            raise Exception(f'Unsupported sign in Contraint, which is {self.sign}')

class MaxFunction:
    
    template = 'max(0, (%s)) ** 2'

    def __init__(self, constraints, argc) -> None:
        expression = self._make_expression(constraints)
        # print(f'Constrained expression is {expression}')
        self.expression = expression
        self.function = MultiNumberFunction(expression, argc)
        
    def _make_expression(self, constraints):
        expression = ''
        for constraint in constraints:
            expression += ' + '
            expression += self.template % constraint.normalize()

        return expression

    def evaluate(self, argv):
        return self.function.evaluate(argv)

class PenaltyMethodFunction:

    def __init__(self, constraints, expression, argc, c0):
        self.penalty_function = MaxFunction(constraints, argc)
        self.oryginal_fun = MultiNumberFunction(expression, argc)
        self.penalty_coeff = c0
        self.expression = self.oryginal_fun.expression + self.penalty_function.expression
    
    def evaluate(self, argv):
        function_value = self.oryginal_fun.evaluate(argv)
        penalty_value = self.penalty_function.evaluate(argv)
        return function_value + self.penalty_coeff * penalty_value

    def set_penalty_parameter(self, coef):
        self.penalty_coeff = coef    

class MaxDerivative:
    def __init__(self, constraint, constraint_derivative_sqrt, argc, c0) -> None:
        '''
        constraint is a derivative string of constarint sqrt
        '''
        print(f'max der for {constraint}')
        self.constraint_fun = MultiNumberFunction(constraint, argc)
        self.derivative_fun = MultiNumberFunction(constraint_derivative_sqrt, argc)
        self.c0 = c0

    def evaluate(self, argv):
        print('evaluating!')
        print(self.constraint_fun.expression)
        print(f'function value is {self.constraint_fun.evaluate(argv)}')
        if self.constraint_fun.evaluate(argv) > 0:
            return self.derivative_fun.evaluate(argv) * self.c0
        else:
            return 0

    def set_penalty_parameter(self, c0):
        self.c0 = c0

class ConstrainedDerivativesWrapper:

    def __init__(self, function, max_derivatives) -> None:
        '''
        All functions must have the same argc
        '''
        self.function = function
        self.max_derivatives = max_derivatives

    def evaluate(self, argv):
        print('o co chodzi?')
        sum = self.function.evaluate(argv)
        for fun in self.max_derivatives:
            sum += fun.evaluate(argv)
        return sum

    def set_penalty_parameter(self, c0):
        for der in self.max_derivatives:
            der.set_penalty_parameter(c0)

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


