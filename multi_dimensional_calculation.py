from conjugate_gradient_fletecher_reeves_method import ConjugateGradientFletcherReevesMethod
from golden_section_search_optimizer import GoldenSectionSearchOptimizer
from function import MultiNumberFunction

def multidimensional_calculation(arguments):
    goldenSectionSearchOptimzier = GoldenSectionSearchOptimizer()
    method = ConjugateGradientFletcherReevesMethod(goldenSectionSearchOptimzier)

    function = _get_function(arguments.expression, arguments.argc)
    derivatives = _get_derivatives(arguments.derivatives_expressions, arguments.argc)
    x = arguments.start_x
    epsilon = arguments.epsilon
    alpha = arguments.alpha
    max_iterations = arguments.max_iterations

    result, search_history = method.optimize(function, x, epsilon, alpha, max_iterations, derivatives)

    print('*' * 100)

    print('The result is ')
    print(result)

    print('Search points are')
    print(search_history)

    return result

def _get_function(expression, argc):
    return MultiNumberFunction(expression, argc)

def _get_derivatives(derivatives_expressions, argc):
    derivative_functions = []
    for expression in derivatives_expressions:
        function = _get_function(expression, argc)
        derivative_functions.append(function)
    return derivative_functions
