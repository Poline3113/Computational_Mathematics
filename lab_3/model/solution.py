from decimal import Decimal


class Solution:
    def __init__(self,  method_name: str, value: Decimal, n: int, cauchy_applied: bool = False):
        self.method_name = method_name
        self.value = value
        self.n = n
        self.cauchy_applied = cauchy_applied

