from math import sqrt

from matplotlib.pyplot import step
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
        
        max_iter = 8
        c_k = c_0
        x_k_prev = x_0
        x_k = x_k_prev
        history = []
        log = []

        for k in range(1, max_iter):
            print(k)

            x_k, steps = self._unconstrained_search(function, x_k_prev, derivatives)
            history += steps

            if self._has_converged(function, x_k_prev, x_k):
                return x_k, history, log

            log.append((x_k, c_k))

            x_k_prev = x_k
            c_k = self.growth_param * c_k

            function.set_penalty_parameter(c_k)
            for der in derivatives:
                der.set_penalty_parameter(c_k)

        print('WARNING EXCEEDED THE MAX NUMBER OF ITERATIONS WITHOUT CONVERGING')

        return x_k, history, log

    def _unconstrained_search(self, function, x_1, derivatives):
        alpha = 0.01
        n = 10_000
        epsilon = self.epsilon
        return self.fletcher_reves.optimize(function, x_1, epsilon, alpha, n, derivatives)

    def _has_converged(self, function, x_k_prev, x_k):
        distance = self._distance(x_k_prev, x_k)
        if distance < self.epsilon:
            return True

        if abs(function.evaluate(x_k) - function.evaluate(x_k_prev)) < self.epsilon:
            return True

        return False

    def _distance(self, a, b):
        # Calculates point in n dimenstional space
        assert len(a) == len(b)
        sum = 0
        for a_i, b_i in zip(a, b):
            sum += (a_i - b_i) ** 2
        return sqrt(sum)

