from function import FunctionInterval
from math import sqrt

class GoldenSectionSearchOptimizer(object):
    def optimize(self, function, functionInterval, stopCondition, epochs):
        golden_ratio = 0.61803

        a, b  = functionInterval.low, functionInterval.high
        intermediate_intervals = [FunctionInterval(a, b)]

        x1 = (b - a) * (-golden_ratio) + b
        x2 = (b - a) * golden_ratio + a

        for epoch in range(epochs):
            if stopCondition(epoch, a, b):
                break

            f_x1 = function.evalute(x1)
            f_x2 = function.evalute(x2)

            if f_x1 > f_x2:
                a = x1
                x1 = x2
                x2 = (b - a) * golden_ratio + a
                # Dumb, but I like how it corresponds with lectures
                b = b
            else:
                # Dumb, but I like how it corresponds with lectures
                a = a
                b = x2
                x2 = x1
                x1 = (b - a) * (-golden_ratio) + b

            intermediate_intervals.append(FunctionInterval(a, b))

        return (b + a) / 2, (a, b), intermediate_intervals