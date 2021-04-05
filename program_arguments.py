from enum import Enum
from function import FunctionRange

class OptimizerType(Enum):
    BISECTION = 0,
    GOLDEN_SECTION_SEARCH = 1
    SCIPY_BISECTION = 2
    SCIPY_GOLDEN_SECTION_SEARCH = 3

class ProgramArguments:
    def __init__(self):
        super().__init__()
        self.optimizerType = OptimizerType.GOLDEN_SECTION_SEARCH
        self.expression = 'x ** 3 - 6 * x** 2 + 4 * x + 12'
        self.functionRange = FunctionRange(-1, 5)
        self.stopCondition = lambda epoch, result :  False
        self.epochs = 25
        self.unimodal_check_n= 100
        self.n = 100000