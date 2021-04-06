from scipy import optimize

class SciPyBisectionOptimizer(object):
    def optimize(self, function, functionInterval, xtol, max_iterations):
        functionWrapper = lambda x : function.evalute(x)
        return optimize.bisect(functionWrapper, functionInterval.low, functionInterval.high, xtol=xtol,
                               maxiter=max_iterations)