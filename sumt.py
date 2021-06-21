from function import PenaltyMethodFunction


class SUMT:
    def __init__(self, fletcher_reves, growth_param, epsilon):
        self.fletcher_reves = fletcher_reves
        self.growth_param = growth_param
        self.epsilon = epsilon
        # TODO: Check that x0 avoids at least one constraint

    def optimize(self, function : PenaltyMethodFunction, derivatives, x_0, c_0):
        # Init step
        assert function.avoids_any_constraint(x_0)
        
        max_iter = 1_000_000 
        c_k = c_0
        x_k_prev = x_0
        x_k = x_k_prev  

        for k in range(1, max_iter):
            # TODO: set c0 of the constarained function
         
            # TODO: Pass additional params
            x_k = self._unconstrained_search()

            if self._should_stop(function, x_k, x_k_prev):
                return x_k

            c_k = self.growth_param * c_k

            function.set_penalty_parameter(c_k)

    def _unconstrained_search(self,  x_1, epsilon, derivatives):
        alpha = 0.01
        n = 10_000
        return self.fletcher_reves.optimize(x_1, epsilon, alpha, n, derivatives)

    def _should_stop(self, function, x_k_1, x_k):
        if abs(x_k_1 - x_k) < self.epsilon:
            return True

        if abs(function.evaluate(x_k_1) - function.evaluate(x_k)) < self.epsilon:
            return True

        return False