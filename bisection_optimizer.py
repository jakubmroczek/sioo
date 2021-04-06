from function import FunctionInterval

class BisectionOptimizer(object):
    def optimize(self, function, functionInterval, stopCondition, epochs):
        a, b = functionInterval.low,  functionInterval.high

        if function.evalute(a) * function.evalute(b) >= 0:
            print("Bisection method fails.")
            return None

        a_n = a
        b_n = b
        intermediate_intervals = [FunctionInterval(a_n, b_n)]

        for epoch in range(epochs):
            if stopCondition(epoch, a_n, b_n):
                break

            m_n = (a_n + b_n)/2
            f_m_n = function.evalute(m_n)

            if function.evalute(a_n)*f_m_n < 0:
                a_n = a_n
                b_n = m_n
                intermediate_intervals.append(FunctionInterval(a_n, b_n))
            elif function.evalute(b_n)*f_m_n < 0:
                a_n = m_n
                b_n = b_n
                intermediate_intervals.append(FunctionInterval(a_n, b_n))
            elif f_m_n == 0:
                print("Found exact solution.")
                return m_n
            else:
                print("Bisection method fails.")
                return None

        return (a_n + b_n)/2, (a_n, b_n), intermediate_intervals
