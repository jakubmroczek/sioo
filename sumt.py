from math import sqrt
from function import PenaltyMethodFunction

class SUMT:
    def __init__(self, fletcher_reves, growth_param, epsilon, alpha, n):
        self.fletcher_reves = fletcher_reves
        self.growth_param = growth_param
        self.epsilon = epsilon
        self.alpha = alpha
        self.n = n

    def optimize(self, function : PenaltyMethodFunction, derivatives, x_0, c_0, max_iter, sumt_epsilon):
        c_k = c_0
        x_k_prev = x_0
        x_k = x_k_prev
        history = []
        log = []

        for k in range(0, max_iter):
            x_k, steps = self._unconstrained_search(function, x_k_prev, derivatives)
            history += steps

            if self._has_converged(function, x_k_prev, x_k, sumt_epsilon):
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
        alpha = self.alpha
        n = self.n
        epsilon = self.epsilon
        return self.fletcher_reves.optimize(function, x_1, epsilon, alpha, n, derivatives)

    def _has_converged(self, function, x_k_prev, x_k, sumt_epsilon):
        distance = self._distance(x_k_prev, x_k)

        if distance < sumt_epsilon:
            return True

        if abs(function.evaluate(x_k) - function.evaluate(x_k_prev)) < sumt_epsilon:
            return True

        return False

    def _distance(self, a, b):
        # Calculates point in n dimenstional space
        assert len(a) == len(b)
        sum = 0
        for a_i, b_i in zip(a, b):
            sum += (a_i - b_i) ** 2
        return sqrt(sum)

