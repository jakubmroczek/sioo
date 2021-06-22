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
    
    #TODO: HANDLE ALSO >= SCENARIOS !!
    # TODO: ADD C0 PARAM TO GUI
    # TODO: ADD HISTORY PARAMETER TO THE GUI
    # TODO: VISUALIZE THE SEARCH DOMAIN
    # TODO: SUPPORT FOR THE REMAINING PARAMS
    con1 = "-3 * x - 2 * y + 6"
    con2 = "-1 * x + y - 3"
    con3 = "1 * x + 1 * y - 7"
    con4 = " 0.66 * x - y - (4/3)"
    
    constarints = []
    
    constarints.append(Constraint(con1, '<'))
    constarints.append(Constraint(con2, '<'))
    constarints.append(Constraint(con3, '<'))
    constarints.append(Constraint(con4, '<'))

    function = PenaltyMethodFunction(constarints, expression, argc)

    derivatives = _get_derivatives(arguments.derivatives_expressions, arguments.argc)
    
    x_0 = arguments.start_x
    epsilon = arguments.epsilon
    # TODO: Pass alpha to the SUMT
    alpha = arguments.alpha
    max_iterations = arguments.max_iterations

    growth_param = 1.5
    epsilon = 1e-4
    c_0 = 3

    goldenSectionSearchOptimzier = GoldenSectionSearchOptimizer()
    method = ConjugateGradientFletcherReevesMethod(goldenSectionSearchOptimzier)
    method = SUMT(method, growth_param, epsilon)

    optimum = method.optimize(function, derivatives, x_0, c_0)
    result = MultiDimensionalCalculationResult()
    result.function = function
    result.optimum = optimum
    result.search_history = []

    return result

def _get_derivatives(derivatives_expressions, argc):
    derivative_functions = []
    for expression in derivatives_expressions:
        function = _get_function(expression, argc)
        derivative_functions.append(function)
    return derivative_functions

def _get_function(expression, argc):
    return MultiNumberFunction(expression, argc)