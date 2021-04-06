from function import FunctionRange
from math import sqrt

class GoldenSectionSearchOptimizer(object):

    def optimize(self, function, functionRange, stopCondition, epochs):
        a, b  = functionRange.low, functionRange.high
        intermediate_results = [FunctionRange(a, b)]
        tol = 1e-5

        # Old code belowe
        gr = (sqrt(5) + 1) / 2

        c = b - (b - a) / gr
        d = a + (b - a) / gr
        while abs(b - a) > tol:
            if function.evalute(c) < function.evalute(d):
                b = d
            else:
                a = c

            intermediate_results.append(FunctionRange(a, b))

            # We recompute both c and d here to avoid loss of precision which may lead to incorrect results or infinite loop
            c = b - (b - a) / gr
            d = a + (b - a) / gr

        return (b + a) / 2, (a, b), intermediate_results