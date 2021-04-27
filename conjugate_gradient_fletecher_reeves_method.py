from function import MultiNumberFunction, FunctionInterval
from math import sqrt
import numpy as np

class ConjugateGradientFletcherReevesMethod:
    def __init__(self, one_dimension_optimizer):
        self.one_dimension_optimizer = one_dimension_optimizer


    def optimize(self, function : MultiNumberFunction, x1, epsillon, alpha, n, derivatives):

        # Step 1
        x_1, e = x1, epsillon

        # Step 2
        k = 1
        gradient_x_1 = self.gradient(derivatives, x_1)
        d_1 = -1 * gradient_x_1

        # TODO: Zla aktualizacja
        # Skąd mam wziąc x_k -> nie jest to jasne
        x_k = x_1
        d_k = d_1
        gradient_x_k = gradient_x_1

        # Step 3
        if self.is_converged(d_1, e):
            return x_k

        # Step 4
        #TODO: Sprecyzuj lepiej zakres, czym jest długośc kroku?
        low = 0
        high = 2 * alpha
        alpha_k = self.directional_minimization(function, x_k, d_k, low, high)
        x_k_1 = x_k + alpha_k * d_k

        # Step 5
        gradient_x_k_1 = self.gradient(derivatives, x_k_1)
        n_k = self.dot_product(gradient_x_k_1, gradient_x_k_1) / self.dot_product(gradient_x_k, gradient_x_k)
        d_k_1 = -1 * gradient_x_k_1 + n_k * d_k

        # Step 6
        if k < n:
            d_k = d_k_1
            x_k = x_k_1
            # Jumpt to step 3

        x_1 = x_k_1
        gradient_x_1 = gradient_x_k_1
        # Jumpt to step 2





        # SOME OLD CODE
        # totally random numbers
        max_iterations = 1000
        x_k = x1
        alpha_k = alpha

        # Dodaj jeszcze jedną pętle xD

        for k in range(0, max_iterations):
            gradient_k = self.gradient(derivatives, x_k)
            d_k = -1 * gradient_k

            if self.is_converged(gradient_k, epsillon):
                return x_k

            #TODO: Sprawdz w notatkach ze spotkania, czy ten zakres ma sens
            low = 0
            high = 2

            alpha_k = self.directional_minimization(function, x_k, d_k, low, high)

            #TODO: Ta zmienna będzie nadpisana
            x_next_k = x_k + alpha_k * d_k
            gradient_next_k = self.gradient(derivatives, x_next_k)

            n_next = self.dot_product(gradient_next_k, gradient_next_k) / self.dot_product(gradient_k, gradient_k)

            d_next_k = -1 * gradient_next_k + n_next * d_k

            if k < n:
                d_k = d_next_k
                x_k = x_next_k
                # k = k + 1
            else:
                #GO TO SECOND STEP XD
                # xjk = x_next_k
                gradient_k = gradient_next_k


        return x_k

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