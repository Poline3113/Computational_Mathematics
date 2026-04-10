from decimal import Decimal
import numpy
from methods.method import Method
from model.solution import Solution


count = 100
MAX_ITERS = 1000

class SimpleIterationsMethod(Method):
    name = "simple iterations method"

    def check_data(self):
        if not self.equation.root_exists(self.left, self.right):
            return False, "the root is missing"
        return True, ""

    def solve(self) -> Solution:
        f = self.equation.function
        x = Decimal(str((self.left + self.right) / 2))

        da = abs(Decimal(str(self.equation.derivative(self.left))))
        db = abs(Decimal(str(self.equation.derivative(self.right))))
        max_deriv = max(da, db)

        if max_deriv == 0:
            return Solution(x, f(x), 0)

        lbd = -Decimal('1') / max_deriv

        points = numpy.linspace(float(self.left), float(self.right), count)
        derivatives = [abs(self.equation.derivative(p)) for p in points]
        max_deriv = Decimal(str(max(derivatives)))

        first_deriv = self.equation.derivative(self.left)
        lbd = -Decimal('1' if first_deriv > 0 else '-1') / max_deriv

        phi = lambda x_val: x_val + lbd * Decimal(str(f(float(x_val))))

        q = 0
        for xi in points:
            phi_p = abs(Decimal('1') + lbd * Decimal(str(self.equation.derivative(xi))))
            if phi_p >= 1:
                return Solution(x, f(x), 0)
            q = max(q, phi_p)

        iteration = 0
        while iteration < MAX_ITERS:
            iteration += 1
            x_prev = x
            x = phi(x)

            if abs(x - x_prev) <= self.epsilon:
                break

        return Solution(x, f(x), iteration)