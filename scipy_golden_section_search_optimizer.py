from scipy import optimize

class SciPyGoldenSectionSearchOptimizer(object):
    def optimize(self, function, functionInterval):
        functionWrapper = lambda x : function.evalute(x)
        return optimize.golden(functionWrapper, brack=(functionInterval.low, functionInterval.high))