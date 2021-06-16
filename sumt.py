from function import PenaltyMethodFunction


class SUMT:
    def __init__(self, fletcher_reves, growth_param):
        self.fletcher_reves = fletcher_reves
        self.growth_param = growth_param
        # TODO: Check that x0 avoids at least one constraint

    def optimize(self, function : PenaltyMethodFunction, x_0, epsilon, c_0, derivatives):
        # Init step
        assert function.avoids_any_constraint(x_0)
        
        max_iter = 1_000_000 
        c = c_0

        for k in range(1, max_iter):
            # TODO: set c0 of the constarained function
            function.set_penalty_parameter(c)
            optimum = self.fletcher_reves.optimize('some args')
            