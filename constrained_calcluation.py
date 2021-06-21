from conjugate_gradient_fletecher_reeves_method import ConjugateGradientFletcherReevesMethod
from golden_section_search_optimizer import GoldenSectionSearchOptimizer
from function import MultiNumberFunction, PenaltyMethodFunction
from sumt import SUMT

class MultiDimensionalCalculationResult:

    def __init__(self):
        super().__init__()
        self.function = None
        self.optimum = None
        self.search_history = None

def constrained_caluclation(arguments):    
    function = _get_function(arguments.expression, arguments.argc)

    #TODO: Create more general penalty function
    #TODO: HANDLE ALSO >= SCENARIOS !!
    # TODO: ADD C0 PARAM TO GUI
    # TODO: ADD HISTORY PARAMETER TO THE GUI
    # TODO: VISUALIZE THE SEARCH DOMAIN
    # TODO: SUPPORT FOR THE REMAINING PARAMS
    con1 = "-3 * x - 2 * y + 6"
    con2 = "-1 * x + y - 3"
    con3 = "1 * x + 1 * y - 7"
    con4 = " 0.66 * x - y - (4/3)"
    
    template = 'max(0, (%s)) ** 2'
    con1 = template % con1
    con2 = template % con2
    con3 = template % con3
    con4 = template % con4

    expr = con1 + ' + ' + con2  + ' + ' + con3  + ' + ' + con4

    penalty_function = MultiNumberFunction(expr, 2)
    print('EXPRESSION')
    print(expr)
    function = PenaltyMethodFunction(penalty_function, function, 2)

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

def _get_function(expression, argc):
    return MultiNumberFunction(expression, argc)

def _get_derivatives(derivatives_expressions, argc):
    derivative_functions = []
    for expression in derivatives_expressions:
        function = _get_function(expression, argc)
        derivative_functions.append(function)
    return derivative_functions
