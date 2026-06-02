from math import exp, log
from abc import ABC, abstractmethod
from lab_4.methods.matrix_utils import solve_sle


class ApproximationMethod(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def solve(self, x, y):
        pass


def solve_polynomial(x, y, n: int):
    points_count = len(x)
    size = n + 1

    x_sums = []
    xy_sums = []
    matrix = []
    vector = []

    for k in range(2 * n + 1):
        current_x_sum = 0
        for i in range(points_count):
            current_x_sum += x[i] ** k
        x_sums.append(current_x_sum)

    for k in range(n + 1):
        current_xy_sum = 0
        for i in range(points_count):
            current_xy_sum += (x[i] ** k) * y[i]
        xy_sums.append(current_xy_sum)

    for i in range(size):
        row = []
        for j in range(size):
            index = (n - i) + (n - j)
            row.append(x_sums[index])
        matrix.append(row)

    for i in range(size):
        vector.append(xy_sums[n - i])

    coeffs = solve_sle(matrix, vector)

    return coeffs


class LinearMethod(ApproximationMethod):
    @property
    def name(self) -> str:
        return "Linear approximation"

    def solve(self, x, y):
        coeffs = solve_polynomial(x, y, 1)
        return lambda xi: coeffs[0] * xi + coeffs[1], coeffs


class Poly2Method(ApproximationMethod):
    @property
    def name(self) -> str:
        return "Quadratic approximation"

    def solve(self, x, y):
        coeffs = solve_polynomial(x, y, 2)
        return lambda xi: coeffs[0] * xi ** 2 + coeffs[1] * xi + coeffs[2], coeffs


class Poly3Method(ApproximationMethod):
    @property
    def name(self) -> str:
        return "Cubic approximation"

    def solve(self, x, y):
        coeffs = solve_polynomial(x, y, 3)
        return lambda xi: coeffs[0] * xi ** 3 + coeffs[1] * xi ** 2 + coeffs[2] * xi + coeffs[3], coeffs


class ExponentialMethod(ApproximationMethod):
    @property
    def name(self) -> str:
        return "Exponential approximation"

    def solve(self, x, y):
        if any(yi <= 0 for yi in y):
            raise ValueError("Y must be > 0 for exponential approximation")

        y_ln = [log(yi) for yi in y]
        coeffs = solve_polynomial(x, y_ln, 1)
        b, ln_a = coeffs
        a = exp(ln_a)
        return lambda xi: a * exp(b * xi), [a, b]


class LogarithmicMethod(ApproximationMethod):
    @property
    def name(self) -> str:
        return "Logarithmic approximation"

    def solve(self, x, y):
        if any(xi <= 0 for xi in x):
            raise ValueError("X must be > 0 for logarithmic approximation")

        x_ln = [log(xi) for xi in x]
        coeffs = solve_polynomial(x_ln, y, 1)
        a, b = coeffs
        return lambda xi: a * log(xi) + b, [a, b]


class PowerMethod(ApproximationMethod):
    @property
    def name(self) -> str:
        return "Power approximation"

    def solve(self, x, y):
        if any(xi <= 0 for xi in x) or any(yi <= 0 for yi in y):
            raise ValueError("X, Y must be > 0 for power approximation")

        x_ln = [log(xi) for xi in x]
        y_ln = [log(yi) for yi in y]
        coeffs = solve_polynomial(x_ln, y_ln, 1)
        b, ln_a = coeffs
        a = exp(ln_a)
        return lambda xi: a * xi ** b, [a, b]