from methods.method import Method
from model.solution import Solution


class HalfDivisionMethod(Method):
    name = "half division method"

    def check_if_root_exists(self):
        root_exists = self.equation.root_exists(self.left, self.right)
        return root_exists, "the root is missing" if not root_exists else ""

    def solve(self) -> Solution:
        f = self.equation.function
        a, b = self.left, self.right
        eps = self.epsilon

        fa, fb = f(a), f(b)
        if fa * fb > 0:
            raise ValueError(f"No root in [{a}, {b}]: f(a)={fa}, f(b)={fb} have same sign.")

        iteration = 0
        while True:
            iteration += 1
            x = (a + b) / 2

            if abs(a - b) <= eps or abs(f(x)) <= eps:
                return Solution(x, f(x), iteration)

            if fa * f(x) < 0:
                b, fb = x, f(x)
            else:
                a, fa = x, f(x)

            if iteration > 1000:
                print("too many iterations, breaking")
                break