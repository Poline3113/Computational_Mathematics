from decimal import Decimal
from typing import Callable, List, Optional
import math


class Integral:
    def __init__(self, function: Callable[[Decimal], Decimal], fun_str: str, point: Optional[Decimal] = None, symmetric_interval: Optional[tuple[Decimal, Decimal]] = None):
        self.function = function
        self.fun_str = fun_str
        self.point = point
        self.symmetric_interval = symmetric_interval