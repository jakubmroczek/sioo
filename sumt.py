from function import PenaltyMethodFunction
from math_utils.vector import vector_length

class SUMT:
    def __init__(self, fletcher_reves, growth_param, epsilon):
        self.fletcher_reves = fletcher_reves
        self.growth_param = growth_param
        self.epsilon = epsilon
        
    def optimize(self, function : PenaltyMethodFunction, derivatives, x_0, c_0):
        # Init step
        # assert function.avoids_any_constraint(x_0)
        
        max_iter = 1_000_000 
        c_k = c_0
        x_k_prev = x_0
        x_k = x_k_prev  

        for k in range(1, max_iter):
            x_k, _ = self._unconstrained_search(function, x_k_prev, derivatives)

            if self._has_converged(function, x_k_prev, x_k):
                return x_k

            c_k = self.growth_param * c_k

            function.set_penalty_parameter(c_k)

    def _unconstrained_search(self, function, x_1, derivatives):
        alpha = 0.01
        n = 10_000
        epsilon = self.epsilon
        return self.fletcher_reves.optimize(function, x_1, epsilon, alpha, n, derivatives)

    def _has_converged(self, function, x_k_prev, x_k):
        print('HAS CONVERGED')
        print(x_k)
        print(x_k_prev)
        
        if abs(vector_length(x_k) - vector_length(x_k_prev)) < self.epsilon:
            return True

        if abs(function.evaluate(x_k) - function.evaluate(x_k_prev)) < self.epsilon:
            return True

        return False