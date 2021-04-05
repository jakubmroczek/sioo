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

    def intersects(self, other):
        pass

    # Call only this method is the ranges intersects
    # To nie jest taka suma w sensie matemtycznym
    def sum(self, other):
        self.low = min(self.low, other.low)
        self.high = max(self.high, other.high)

    def __str__(self):
        return f'({self.low}, {self.high})'

def intersects(range1, range2):
    # Case 1
    if range1.high >= range2.low and range1.high <= range2.high:
        return True

    # Case 2
    if range2.low >= range1.low and range2.low <= range1.high and range2.high >= range1.low and range2.high <= \
            range1.high:
        return True

    # Case 3
    if range2.high >= range1.low and range2.high <= range1.high:
        return True

    return False