from enum import Enum
from function import FunctionInterval

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
        self.functionInterval = FunctionInterval(-1, 5)
        self.epochs = 25
        self.unimodal_check_n= 100
        self.exhaustive_serach_n = 100
        self.max_iterations = 500
        self.xtol = 1e-3

class MuliDimensionProgramArguments:
    def __init__(self):
        super().__init__()
        self.expression = "x ** 2+ y ** 2"
        self.derivatives_expressions = ["2 * x", "2 * y"]
        # Number of varibales in the expression
        self.argc = 2
        self.start_x = (0, 1)
        self.epsilon = 1e-2
        self.alpha = 0.1
        self.max_iterations = 10_0000