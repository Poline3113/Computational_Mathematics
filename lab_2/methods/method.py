from typing import Tuple

from model.equation import Equation
from model.solution import Solution
from decimal import Decimal


class Method:
    name = None

    def __init__(self, equation: Equation, left: Decimal, right: Decimal,
                 epsilon: Decimal, x0: Decimal| None):
        self.right = right
        self.left = left
        self.equation = equation
        self.epsilon = epsilon
        self.x0 = x0


    def solve(self) -> Solution:
        pass

    def check_data(self) -> Tuple[bool, str]:
        return True, ""