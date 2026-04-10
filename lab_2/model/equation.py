from decimal import Decimal
from typing import Callable


class Equation:
    def __init__(self, function: Callable, fun_str: str, derivative : Callable, second_derivative: Callable):
        self.function = function
        self.fun_str = fun_str
        self.derivative = derivative
        self.second_derivative = second_derivative

    def root_exists(self, left: Decimal, right: Decimal) -> bool:
        f_a = self.function(left)
        f_b = self.function(right)

        sign_change = f_a * f_b < 0

        deriv_at_left = self.derivative(left)
        non_zero_derivative = deriv_at_left != 0

        return sign_change and non_zero_derivative
