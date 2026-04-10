from decimal import Decimal
from typing import Callable

from lab_3.methods.method import Method


class TrapezoidRule(Method):
    @property
    def name(self) -> str:
        return "trapezoid"

    def solve(self, func: Callable[[Decimal], Decimal], a: Decimal, b: Decimal, n: int) -> Decimal:
        h = (b - a) / Decimal(n)
        total = (func(a) + func(b)) / Decimal(2)
        for i in range(1, n):
            xi = a + Decimal(i) * h
            total += func(xi)
        return total * h

    @property
    def runge_coefficient(self) -> Decimal:
        return Decimal(3)