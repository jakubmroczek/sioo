from function import MultiNumberFunction, FunctionInterval
from math import fabs

class ConjugateGradientFletcherReevesMethod:
    def __init__(self, one_dimension_optimizer):
        self.one_dimension_optimizer = one_dimension_optimizer


    def optimize(self, function : MultiNumberFunction, x1, epsillon, alpha, n, derivatives):

        # totally random numbers
        max_iterations = 1000
        x_k = x1
        alpha_k = alpha

        # Dodaj jeszcze jedną pętle xD

        for k in range(0, max_iterations):
            print(x_k)
            gradient_k = self.gradient(derivatives, x_k)
            d_k = -1 * gradient_k

            if self.is_converged(d_k, epsillon):
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


        return x

    def gradient(self, derivatives, x):
        assert len(derivatives) == len(x)
        gradient = []
        for derivative, arg in zip(derivatives, x):
            derivative_value = derivatives.evaluate(arg)
            gradient.append(derivative_value)
        return gradient

    def is_converged(self, gradient, epsillon):
        #TODO: Is this ok for the gradient?
        return fabs(gradient) < epsillon

    #TODO: put low high in FuncitonInterval
    def directional_minimization(self, function, x_k, d_k, low, high):
        unary_function_wrapper = lambda alpha : function(x_k + alpha * d_k)
        functionInterval = FunctionInterval(low, high)
        max_iterations = 100
        xtol = 1e-3
        stop_condition = lambda iteration, a, b : iteration >= max_iterations or abs(b - a) < xtol
        return self.one_dimension_optimizer.optimize(unary_function_wrapper, functionInterval, stop_condition, max_iterations)

    def dot_product(self, a, b):
        pass