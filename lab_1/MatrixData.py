from decimal import Decimal


class MatrixData:
    def __init__(self, n=1):
        self.n = n
        self.A = [[Decimal('0')] * n for _ in range(n)]
        self.b = [Decimal('0')] * n