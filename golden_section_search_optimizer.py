from function import FunctionInterval
from math import sqrt

class GoldenSectionSearchOptimizer(object):
    def optimize(self, function, functionInterval, stopCondition, epochs):
        a, b  = functionInterval.low, functionInterval.high
        intermediate_intervals = [FunctionInterval(a, b)]

        gr = (sqrt(5) + 1) / 2

        c = b - (b - a) / gr
        d = a + (b - a) / gr

        for epoch in range(epochs):
            if stopCondition(epoch, a, b):
                break

            if function.evalute(c) < function.evalute(d):
                b = d
            else:
                a = c

            intermediate_intervals.append(FunctionInterval(a, b))

            # Recompute both c and d here to avoid loss of precision which may lead to incorrect results or infinite
            # loop
            c = b - (b - a) / gr
            d = a + (b - a) / gr

        return (b + a) / 2, (a, b), intermediate_intervals