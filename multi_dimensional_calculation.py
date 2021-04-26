from conjugate_gradient_fletecher_reeves_method import ConjugateGradientFletcherReevesMethod
from golden_section_search_optimizer import GoldenSectionSearchOptimizer
from function import MultiNumberFunction

def multidimensional_calculation(arguments):
    goldenSectionSearchOptimzier = GoldenSectionSearchOptimizer()
    method = ConjugateGradientFletcherReevesMethod(goldenSectionSearchOptimzier)

    function = _get_function(arguments.expression, arguments.argc)
    x = arguments.start_x
    epsilon = arguments.epsilon
    alpha = arguments.alpha
    max_iterations = arguments.max_iterations

    return method.optimize(function, x, epsilon, alpha, max_iterations)

def _get_function(expression, argc):
    return MultiNumberFunction(expression, argc)
