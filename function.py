class UnaryFunction:
    def __init__(self, expression):
        super().__init__()
        self.expression = expression

    def evalute(self, x):
        self.x = x
        return eval(self.expression)

class FunctionRange:
    def __init__(self, low, high):
        super().__init__()
        assert low < high, f'{low}, {high}'
        self.low = low
        self.high = high

    def __str__(self):
        return f'({self.low}, {self.high})'