from decimal import Decimal

class MatrixCalculator:

    @staticmethod
    def matrix_det(A, b, n):
        matrix_A = [row[:] for row in A]
        matrix_b = b[:]
        swaps = 0

        for i in range(n - 1):
            max_row = i
            for k in range(i + 1, n):
                if abs(matrix_A[k][i]) > abs(matrix_A[max_row][i]):
                    max_row = k
            if max_row != i:
                matrix_A[i], matrix_A[max_row] = matrix_A[max_row], matrix_A[i]
                matrix_b[i], matrix_b[max_row] = matrix_b[max_row], matrix_b[i]
                swaps += 1
            if matrix_A[i][i] == Decimal('0'):
                print("Matrix is singular, determinant = 0")
                return matrix_A, matrix_b, Decimal('0')
            else:
                for k in range(i + 1, n):
                    c = matrix_A[k][i] / matrix_A[i][i]
                    for j in range(i, n):
                        matrix_A[k][j] -= c * matrix_A[i][j]
                    matrix_b[k] -= c * matrix_b[i]

        det_sign = (-1) ** swaps
        det_value = 1
        for i in range(n):
            det_value *= matrix_A[i][i]
        determinant = det_sign * det_value

        return matrix_A, matrix_b, determinant

    @staticmethod
    def solve_matrix_det(triangle_A, triangle_b, n):
        x = [Decimal('0')] * n

        for i in range(n):
            is_zero_row = all(triangle_A[i][j] == Decimal('0') for j in range(n))
            if is_zero_row and triangle_b[i] != Decimal('0'):
                print("\nThe system has no solutions")
                return None

        for i in range(n - 1, -1, -1):
            s = Decimal('0')
            for j in range(i + 1, n):
                s += triangle_A[i][j] * x[j]
            if triangle_A[i][i] == Decimal('0'):
                print("\nThe system has infinitely many solutions")
                return None
            x[i] = (triangle_b[i] - s) / triangle_A[i][i]

        return x