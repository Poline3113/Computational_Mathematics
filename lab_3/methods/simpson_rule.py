
from decimal import Decimal
from typing import Callable

from lab_3.methods.method import Method


class SimpsonRule(Method):
    @property
    def name(self) -> str:
        return "simpson"

    def solve(self, func: Callable[[Decimal], Decimal], a: Decimal, b: Decimal, n: int) -> Decimal:
        h = (b - a) / Decimal(n)
        total = func(a) + func(b)
        for i in range(1, n):
            xi = a + Decimal(i) * h
            total += func(xi) * (4 if i % 2 else 2)
        return total * h / Decimal(3)

    @property
    def runge_coefficient(self) -> Decimal:
        return Decimal(15)