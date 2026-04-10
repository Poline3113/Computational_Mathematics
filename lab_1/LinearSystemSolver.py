from decimal import Decimal, getcontext
import random

from MatrixCalculator import MatrixCalculator
from MatrixData import MatrixData

getcontext().prec = 10


class LinearSystemSolver:
    def __init__(self):
        self.data = MatrixData(1)
        self.calc = MatrixCalculator()

    def update_n(self, new_n):
        if 1 <= new_n <= 20:
            self.data = MatrixData(new_n)
            print(f"n updated to {new_n}")
        else:
            print("n must be in [1; 20]")

    def update_matrix(self):
        n = self.data.n
        print(f"enter {n} rows")

        for i in range(n):
            while True:
                try:
                    row = list(map(Decimal, input(f"row number {i + 1}: ").replace(",", ".").split()))
                    if len(row) != n:
                        print(f"enter {n} numbers")
                        continue
                    self.data.A[i] = row
                    break
                except ValueError:
                    print("enter numbers split")

        print("Enter the vector of free terms")
        while True:
            try:
                b = list(map(Decimal, input().replace(",", ".").split()))
                if len(b) != n:
                    print(f"enter {n} numbers")
                    continue
                self.data.b = b
                break
            except ValueError:
                print("enter numbers split")

    def show_n(self):
        print(f"n = {self.data.n}")

    def show_matrix(self):
        n = self.data.n
        for i in range(n):
            row = []
            for j in range(n):
                if j == 0:
                    row.append(f"{self.data.A[i][j]} * x{j + 1}")
                else:
                    row.append(f"+ {self.data.A[i][j]} * x{j + 1}")
            row_str = " ".join(row) + f" = {self.data.b[i]}"
            print(row_str)

    def random_matrix(self):
        n = self.data.n
        for i in range(n):
            row = [Decimal(random.randint(1, 100)) for _ in range(n)]
            self.data.A[i] = row
        self.data.b = [Decimal(random.randint(1, 100)) for _ in range(n)]

    def show_triangle_matrix(self):
        triangle_A, triangle_b, _ = self.calc.matrix_det(
            self.data.A, self.data.b, self.data.n)

        n = self.data.n
        for i in range(n):
            row = []
            for j in range(n):
                if j == 0:
                    row.append(f"{triangle_A[i][j]} * x{j + 1}")
                else:
                    row.append(f"+ {triangle_A[i][j]} * x{j + 1}")
            row_str = " ".join(row) + f" = {triangle_b[i]}"
            print(row_str)

    def solve_matrix_det(self):
        _, _, det = self.calc.matrix_det(
            self.data.A, self.data.b, self.data.n)
        print(det)
        return det

    def solve_matrix(self):
        triangle_A, triangle_b, _ = self.calc.matrix_det(
            self.data.A, self.data.b, self.data.n)

        x = self.calc.solve_matrix_det(triangle_A, triangle_b, self.data.n)

        if x is None:
            print("\nThe system has no solutions")
            return None

        print("\nx*: ")
        for i in range(len(x)):
            print(f"x{i + 1} = {x[i]}")
        return x

    def compute_residual(self):
        x_star = self.solve_matrix()
        if x_star is None:
            print("Cannot compute residual: system has no unique solution.")
            return None

        n = self.data.n
        r = [Decimal('0')] * n
        for i in range(n):
            s = Decimal('0')
            for j in range(n):
                s += self.data.A[i][j] * x_star[j]
            r[i] = s - self.data.b[i]

        print("\nr = A·x* − b:")
        for i in range(n):
            print(f"r[{i + 1}] = {r[i]}")
        return r