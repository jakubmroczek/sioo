from function import FunctionInterval

class BisectionOptimizer(object):
    def optimize(self, function, functionInterval, stopCondition, epochs):
        a_n, b_n = functionInterval.low,  functionInterval.high
        f_a_n, f_b_n, f_m_n = None, None, None
        intermediate_intervals = [FunctionInterval(a_n, b_n)]

        if function.evalute(a_n) * function.evalute(b_n) >= 0:
            print("Bisection method fails.")
            return None

        for epoch in range(epochs):
            if stopCondition(epoch, a_n, b_n):
                break

            m_n = (a_n + b_n) / 2
            f_m_n = function.evalute(m_n)
            f_a_n = f_a_n if f_a_n != None else function.evalute(a_n)

            if f_a_n * f_m_n < 0:
                a_n = a_n
                b_n = m_n
                # Clearing cache
                f_b_n = None
                intermediate_intervals.append(FunctionInterval(a_n, b_n))
                continue

            f_b_n = f_b_n if f_b_n != None else function.evalute(b_n)

            if f_b_n * f_m_n < 0:
                a_n = m_n
                # Clearing cache
                f_a_n = None
                b_n = b_n
                intermediate_intervals.append(FunctionInterval(a_n, b_n))
            elif f_m_n == 0:
                print("Found exact solution.")
                return m_n
            else:
                print("Bisection method fails.")
                return None

        return (a_n + b_n)/2, (a_n, b_n), intermediate_intervals
