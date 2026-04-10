
from decimal import Decimal
from lab_3.model.integral import Integral
from lab_3.model.solution import Solution


class IntegralSolver:
    def compute(self, integral: Integral, a: Decimal, b: Decimal, eps: Decimal, method) -> Solution:
        disc = integral.point

        if disc is not None and a < disc < b:
            return self.handle_cauchy(integral, a, b, eps, method, disc)

        shift = Decimal('1e-8')
        curr_a = a + shift if disc == a else a
        curr_b = b - shift if disc == b else b

        return self.compute_regular(integral, curr_a, curr_b, eps, method)

    def handle_cauchy(self, integral, a, b, eps, method, c: Decimal) -> Solution:
        dist_l, dist_r = abs(c - a), abs(c - b)

        if dist_l < dist_r:
            res = self.compute_regular(integral, c + dist_l, b, eps, method)
        elif dist_r < dist_l:
            res = self.compute_regular(integral, a, c - dist_r, eps, method)
        else:
            return Solution(method.name, Decimal(0), 4, True)

        res.cauchy_applied = True
        return res

    def compute_regular(self, integral, a, b, eps, method) -> Solution:
        n = 4
        try:
            prev = method.solve(integral.function, a, b, n)
        except Exception:
            raise ValueError("Integral does not exist")

        for i in range(20):
            n *= 2
            try:
                curr = method.solve(integral.function, a, b, n)
            except Exception:
                raise ValueError("Integral does not exist")

            if abs(curr) > 1e12:
                raise ValueError("Integral does not exist")

            if abs(curr - prev) / method.runge_coefficient < eps:
                return Solution(method.name, curr, n)

            prev = curr

        raise ValueError("Integral does not converge within iterations")