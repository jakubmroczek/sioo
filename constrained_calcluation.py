import enum
from conjugate_gradient_fletecher_reeves_method import ConjugateGradientFletcherReevesMethod
from golden_section_search_optimizer import GoldenSectionSearchOptimizer
from function import Constraint, MultiNumberFunction, PenaltyMethodFunction
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
    # c0 = arguments.c0
    c0 = 10_000

    #TODO: HANDLE ALSO >= SCENARIOS !!
    # TODO: STUFF DOES NOT WORK BECAUSE OF LACK OF MAX DERIVATIVESS
    # TODO: ADD C0 PARAM TO GUI
    # TODO: ADD HISTORY PARAMETER TO THE GUI
    # TODO: VISUALIZE THE SEARCH DOMAIN
    # TODO: SUPPORT FOR THE REMAINING PARAMS
    # TODO: Add stuff to the gui
    con1 = "-3 * x - 2 * y + 6"
    con2 = "-1 * x + y - 3"
    con3 = "1 * x + 1 * y - 7"
    con4 = " 0.66 * x - y - (4/3)"
    
    constarints = []
    
    constarints.append(Constraint(con1, '<'))
    constarints.append(Constraint(con2, '<'))
    constarints.append(Constraint(con3, '<'))
    constarints.append(Constraint(con4, '<'))

    # argc * constraints
    # functions raised to sqrt ** 2
    # TODO: Take it as constraint derivaties from program args
    constraints_derivatives = []
    constraint_number =  4
    derivatives = _get_derivatives(arguments.derivatives_expressions, constraints_derivatives, arguments.argc, constraint_number)

    function = PenaltyMethodFunction(constarints, expression, argc, c0)

    x_0 = arguments.start_x
    epsilon = arguments.epsilon
    # TODO: Pass alpha to the SUMT
    alpha = arguments.alpha
    max_iterations = arguments.max_iterations

    growth_param = 2    
    c_0 = 0.5

    goldenSectionSearchOptimzier = GoldenSectionSearchOptimizer()
    method = ConjugateGradientFletcherReevesMethod(goldenSectionSearchOptimzier)
    method = SUMT(method, growth_param, epsilon)

    optimum = method.optimize(function, derivatives, x_0, c_0)
    result = MultiDimensionalCalculationResult()
    result.function = function
    result.optimum = optimum
    result.search_history = []

    return result

def _get_derivatives(derivatives_expressions, constraints_derivatives, argc, constraint_number):
    assert len(constraints_derivatives) == argc * constraint_number
    
    derivative_functions = []
    for i, expression in enumerate(derivatives_expressions):
        function = _get_function(expression, argc)
        
        start = i * constraint_number
        end = start + argc
        
        derivatives = [function]
        for j in range(start, end):
            constraint = constraints_derivatives[j]
            derivative = MaxDerivative(constraint, argc)
            derivatives.append(derivative)

        function = SumFunction(derivatives, argc)
        derivative_functions.append(function)
    return derivative_functions

def _get_function(expression, argc):
    return MultiNumberFunction(expression, argc)