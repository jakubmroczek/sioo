from scipy import optimize

class SciPyGoldenSectionSearchOptimizer(object):
    def optimize(self, function, functionInterval, xtol, max_iterations):
        functionWrapper = lambda x : function.evalute(x)
        return optimize.golden(functionWrapper, brack=(functionInterval.low, functionInterval.high), tol=xtol,
                               maxiter=max_iterations)