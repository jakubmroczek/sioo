from function import FunctionInterval

class GoldenSectionSearchOptimizer(object):
    def optimize(self, function, functionInterval, stopCondition, epochs):
        golden_ratio = 0.61803

        a, b  = functionInterval.low, functionInterval.high
        intermediate_intervals = [FunctionInterval(a, b)]

        x1 = (b - a) * (-golden_ratio) + b
        x2 = (b - a) * golden_ratio + a

        f_x1 = function.evalute(x1)
        f_x2 = function.evalute(x2)

        executed_iterations = 0
        executed_evaluations = 0

        for epoch in range(epochs):
            if stopCondition(epoch, a, b):
                break

            executed_iterations = executed_iterations + 1

            # Simple cache
            if f_x1 == None:
                f_x1 = function.evalute(x1)
                executed_evaluations = executed_evaluations + 1

            if f_x2 == None:
                f_x2 = function.evalute(x2)
                executed_evaluations = executed_evaluations + 1

            if f_x1 > f_x2:
                a = x1
                x1 = x2

                # Cache update
                f_x1 = f_x2
                f_x2 = None

                x2 = (b - a) * golden_ratio + a
                # Dumb, but I like how it corresponds with lectures
                b = b
            else:
                # Dumb, but I like how it corresponds with lectures
                a = a
                b = x2

                # Cache update
                f_x2 = f_x1
                f_x1 = None

                x2 = x1
                x1 = (b - a) * (-golden_ratio) + b

            intermediate_intervals.append(FunctionInterval(a, b))

        return (b + a) / 2, (a, b), intermediate_intervals, executed_iterations, executed_evaluations