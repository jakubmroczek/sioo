from function import MultiNumberFunction, FunctionInterval
from math import sqrt
import numpy as np

class ConjugateGradientFletcherReevesMethod:
    def __init__(self, one_dimension_optimizer):
        self.one_dimension_optimizer = one_dimension_optimizer


    def optimize(self, function : MultiNumberFunction, x_1, epsilon, alpha, n, derivatives):
        # Cache variable needed during computation
        x_k_1 = None

        # Step 1
        # Define x_1 and epsilon

        while True:
            # Step 2
            gradient_x_1 = self.gradient(derivatives, x_1)
            d_1 = -1 * gradient_x_1

            x_k = x_1
            d_k = d_1
            alpha_k = alpha

            for k in range(n):
                # Step 3
                gradient_x_k = self.gradient(derivatives, x_k)
                if self.is_converged(gradient_x_k, epsilon):
                    return x_k

                # Step 4
                low = 0
                high = 2 * alpha_k
                alpha_k = self.directional_minimization(function, x_k, d_k, low, high)
                x_k_1 = x_k + alpha_k * d_k

                # Step 5
                gradient_x_k_1 = self.gradient(derivatives, x_k_1)
                n_k = self.dot_product(gradient_x_k_1, gradient_x_k_1) / self.dot_product(gradient_x_k, gradient_x_k)
                d_k_1 = -1 * gradient_x_k_1 + n_k * d_k

                # Step 6
                d_k = d_k_1
                x_k = x_k_1
                # Jump to step 3

            # Jump to step 2
            x_1 = x_k_1

    def gradient(self, derivatives, x):
        assert len(derivatives) == len(x)
        gradient = np.array([derivative.evaluate(x) for derivative in derivatives])
        return gradient

    def is_converged(self, gradient, epsillon):
        return self.vector_length(gradient) < epsillon

    #TODO: put low high in FuncitonInterval
    def directional_minimization(self, function, x_k, d_k, low, high):
        unary_function_wrapper = self._make_unary_function_wrapper(function, x_k, d_k)
        functionInterval = FunctionInterval(low, high)
        max_iterations = 100
        xtol = 1e-3
        stop_condition = lambda iteration, a, b : iteration >= max_iterations or abs(b - a) < xtol
        tuple = self.one_dimension_optimizer.optimize(unary_function_wrapper, functionInterval, stop_condition,
                                                 max_iterations)
        result_x = tuple[0]
        return result_x

    def _make_unary_function_wrapper(self, function, x_k, d_k):
        class UnaryFunctionWrapper:
            def __init__(self, function: MultiNumberFunction, x_k, d_k):
                self.function = function
                self.x_k = np.array(x_k)
                self.d_k = np.array(d_k)

            def evalute(self, alpha):
                arg = self.x_k + alpha * self.d_k
                return self.function.evaluate(arg)

        return UnaryFunctionWrapper(function, x_k, d_k)

    def dot_product(self, a, b):
        return np.dot(a, b)

    def vector_length(self, vector):
        length = 0
        for component in vector:
            length += component ** 2
        length = sqrt(length)
        return length