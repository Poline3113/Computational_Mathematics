from decimal import Decimal
from typing import Callable

from lab_3.methods.method import Method


class MidpointRule(Method):
    @property
    def name(self) -> str:
        return "rectangle_middle"

    def solve(self, func: Callable[[Decimal], Decimal], a: Decimal, b: Decimal, n: int) -> Decimal:
        h = (b - a) / Decimal(n)
        total = Decimal(0)
        for i in range(n):
            xi = a + (Decimal(i) + Decimal('0.5')) * h
            total += func(xi)
        return total * h

    @property
    def runge_coefficient(self) -> Decimal:
        return Decimal(3)