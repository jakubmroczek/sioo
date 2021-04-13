from function import FunctionInterval

class BisectionOptimizer(object):
    def optimize(self, function, functionInterval, stopCondition, epochs):
        a, b = functionInterval.low, functionInterval.high
        intermediate_intervals = [FunctionInterval(a, b)]

        executed_iterations = 0
        executed_evaluations = 0

        f_x_m, f_x_1, f_x_2 = None, None, None

        for epoch in range(epochs):
            if stopCondition(epoch, a, b):
                break

            executed_iterations = executed_iterations + 1

            L = abs(b - a)

            x_1 = a + L / 4
            x_m = (a + b) / 2
            x_2 = b - L / 4

            f_x_1 = function.evalute(x_1)
            executed_evaluations = executed_evaluations + 1
            if epoch == 0:
                f_x_m = function.evalute(x_m)
                executed_evaluations = executed_evaluations + 1

            if f_x_1 < f_x_m:
                # Dumb, but I like how it corresponds with lectures
                a = a
                b = x_m
                x_m = x_1
                f_x_m = f_x_1
                intermediate_intervals.append(FunctionInterval(a, b))
                continue

            f_x_2 = function.evalute(x_2)
            executed_evaluations = executed_evaluations + 1

            if f_x_2 < f_x_m:
                a = x_m
                x_m = x_2
                f_x_m = f_x_2
                # Dumb, but I like how it corresponds with lectures
                b = b
                intermediate_intervals.append(FunctionInterval(a, b))
                continue

            # We choose [x1, x2]
            a = x_1
            # Dumb, but I like how it corresponds with lectures
            x_m = x_m
            b = x_2
            intermediate_intervals.append(FunctionInterval(a, b))

        return (a + b) / 2, (a, b), intermediate_intervals, executed_iterations, executed_evaluations
