from decimal import Decimal


class Solution:
    def __init__(self, root: Decimal, function_value: Decimal, iteration_count: int):
        self.root = root
        self.iteration_count = iteration_count
        self.function_value = function_value

    def string_solution(self):
        return "Solution:\n" \
               f"Root: {self.root}\n" \
               f"Function value: {self.function_value}\n" \
               f"Iteration count: {self.iteration_count}"