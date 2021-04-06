from scipy import optimize

class SciPyBisectionOptimizer(object):
    def optimize(self, function, functionInterval):
        functionWrapper = lambda x : function.evalute(x)
        return optimize.bisect(functionWrapper, functionInterval.low, functionInterval.high)