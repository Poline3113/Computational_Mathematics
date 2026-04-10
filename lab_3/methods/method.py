from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Callable


class Method(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def solve(self, func: Callable[[Decimal], Decimal], a: Decimal, b: Decimal, n: int) -> Decimal:
        pass

    @property
    @abstractmethod
    def runge_coefficient(self) -> Decimal:
        pass