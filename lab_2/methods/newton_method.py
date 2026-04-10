from methods.method import Method
from model.solution import Solution
from decimal import Decimal

class NewtonMethod(Method):
    name = "Newton method"

    def check_data(self):
        if self.equation.derivative(self.left) == 0 or self.equation.derivative(self.right) == 0:
            return False, "derivative = 0"

        f_a = self.equation.function(self.left)
        f_b = self.equation.function(self.right)
        d2f_a = self.equation.second_derivative(self.left)
        d2f_b = self.equation.second_derivative(self.right)

        if f_a * d2f_a > 0:
            self.x0 = Decimal(str(self.left))
        elif f_b * d2f_b > 0:
            self.x0 = self.right
        else:
            self.x0 = Decimal(str((self.left + self.right) / 2))

        return True, ""

    def solve(self) -> Solution:
        f = self.equation.function
        x0 = self.x0

        epsilon = self.epsilon
        iteration = 0

        while True:
            iteration += 1

            df = self.equation.derivative(x0)
            x1 = x0 - Decimal(str(f(x0))) / Decimal(str(df))


            if abs(x1 - x0) < epsilon and abs(f(x1)) < epsilon:
                break

            x0 = x1

        return Solution(x1, f(x1), iteration)