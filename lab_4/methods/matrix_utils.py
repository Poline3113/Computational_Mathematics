def solve_sle(A, B):
    n = len(A)

    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(A[i][j])
        row.append(B[i])
        matrix.append(row)

    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k

        temp = matrix[i]
        matrix[i] = matrix[max_row]
        matrix[max_row] = temp

        pivot = matrix[i][i]
        if abs(pivot) < 1e-15:
            raise ValueError("Matrix is singular")

        for k in range(i + 1, n):
            factor = matrix[k][i] / pivot
            for j in range(i, n + 1):
                matrix[k][j] = matrix[k][j] - factor * matrix[i][j]

    x = []
    for i in range(n):
        x.append(0)

    for i in range(n - 1, -1, -1):
        sum_val = 0
        for j in range(i + 1, n):
            sum_val = sum_val + matrix[i][j] * x[j]
        x[i] = (matrix[i][n] - sum_val) / matrix[i][i]

    return x