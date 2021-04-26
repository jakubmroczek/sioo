from conjugate_gradient_fletecher_reeves_method import ConjugateGradientFletcherReevesMethod
from golden_section_search_optimizer import GoldenSectionSearchOptimizer


def multidimensional_calculation(arguments):
    goldenSectionSearchOptimzier = GoldenSectionSearchOptimizer()
    method = ConjugateGradientFletcherReevesMethod(goldenSectionSearchOptimzier)

    function = arguments.function
    x = arguments.start_x
    epsilon = arguments.epsilon
    alpha = arguments.alphas
    max_iterations = arguments.max_iterations

    return method.optimize(function, x, epsilon, alpha, max_iterations)
