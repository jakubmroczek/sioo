from conjugate_gradient_fletecher_reeves_method import ConjugateGradientFletcherReevesMethod
from golden_section_search_optimizer import GoldenSectionSearchOptimizer
from function import Constraint, MultiNumberFunction, PenaltyMethodFunction, MaxDerivative, ConstrainedDerivativesWrapper
from sumt import SUMT

class MultiDimensionalCalculationResult:

    def __init__(self):
        super().__init__()
        self.function = None
        self.optimum = None
        self.search_history = None

def constrained_caluclation(arguments):
    expression = arguments.expression
    argc = arguments.argc
    x_0 = arguments.start_x
    epsilon = arguments.epsilon
    alpha = arguments.alpha
    n = arguments.max_iterations
    max_iterations = 8
    growth_param = 2    
    c0 = 0.5

    constraint_expressions = arguments.constraints
    constarints = []
    for c in constraint_expressions:
        constarints.append(Constraint(c, '<'))
    constraints_derivatives = arguments.constraints_derivatives
    derivatives = _get_derivatives(constraint_expressions, arguments.derivatives_expressions, constraints_derivatives, arguments.argc, c0)

    function = PenaltyMethodFunction(constarints, expression, argc, c0)

    goldenSectionSearchOptimzier = GoldenSectionSearchOptimizer()
    method = ConjugateGradientFletcherReevesMethod(goldenSectionSearchOptimzier)
    method = SUMT(method, growth_param, epsilon, alpha, n)

    optimum, history, log = method.optimize(function, derivatives, x_0, c0, max_iterations)
    result = MultiDimensionalCalculationResult()
    result.function = function
    result.optimum = optimum
    result.search_history = history
    result.log = log

    return result

def _get_derivatives(constraints_expression, derivatives_expressions, constraints_derivatives, argc, c0):
    assert len(constraints_derivatives) == argc * len(constraints_expression)
    
    constraint_number = len(constraints_expression)

    print('in _Get_deri')
    print(constraints_expression)
    derivative_functions = []
    for i, expression in enumerate(derivatives_expressions):
        function = _get_function(expression, argc)

        start = i * constraint_number
        end = start + constraint_number
        
        derivatives = []
        index = 0
        for j in range(start, end):
            constraint = constraints_expression[index]
            index += 1
            constraint_derivatvie = constraints_derivatives[j]
            derivative = MaxDerivative(constraint, constraint_derivatvie, argc, c0)
            derivatives.append(derivative)

        function = ConstrainedDerivativesWrapper(function, derivatives)
        derivative_functions.append(function)
    
    return derivative_functions

def _get_function(expression, argc):
    return MultiNumberFunction(expression, argc)