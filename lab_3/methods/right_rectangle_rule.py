from decimal import Decimal
from typing import Callable

from lab_3.methods.method import Method


class RightRectangleRule(Method):
    @property
    def name(self) -> str:
        return "rectangle_right"

    def solve(self, func: Callable[[Decimal], Decimal], a: Decimal, b: Decimal, n: int) -> Decimal:
        h = (b - a) / Decimal(n)
        total = Decimal(0)
        for i in range(1, n + 1):
            xi = a + Decimal(i) * h
            total += func(xi)
        return total * h

    @property
    def runge_coefficient(self) -> Decimal:
        return Decimal(3)