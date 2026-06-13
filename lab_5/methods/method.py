import math
from abc import ABC, abstractmethod


class InterpolationMethod(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def solve(self, x_nodes, y_nodes):
        pass


class FiniteDifferenceMethod(InterpolationMethod):
    def get_table(self, y):
        n = len(y)
        table = [[0] * n for _ in range(n)]
        for i in range(n):
            table[i][0] = y[i]
        for j in range(1, n):
            for i in range(n - j):
                table[i][j] = table[i + 1][j - 1] - table[i][j - 1]
        return table

    def get_params(self, x_nodes, y_nodes):
        n = len(x_nodes)
        h = x_nodes[1] - x_nodes[0]
        table = self.get_table(y_nodes)
        return n, h, table

    def compute_gauss(self, t, n, mid, table, mode, dts):
        res = table[mid][0]
        t_prod = 1
        print(dts)
        for k in range(1, n):
            if mode == 1:
                t_prod *= (t + dts[k - 1])
                row = mid - k // 2
            else:
                t_prod *= (t - dts[k - 1])
                row = mid - (k + 1) // 2
            if 0 <= row < n - k:
                res += (t_prod * table[row][k]) / math.factorial(k)
        return res

    def generate_offsets(self, n):
        offsets = []
        for i in range(n):
            if i % 2 == 0:
                offsets.append(i // 2)
            else:
                offsets.append(-(i + 1) // 2)
        return offsets


class LagrangeMethod(InterpolationMethod):
    @property
    def name(self) -> str:
        return "Многочлен Лагранжа"

    def solve(self, x_nodes, y_nodes):
        n = len(x_nodes)

        def poly(x):
            res = 0
            for i in range(n):
                basis = 1
                for j in range(n):
                    if i != j:
                        basis *= (x - x_nodes[j]) / (x_nodes[i] - x_nodes[j])
                res += y_nodes[i] * basis
            return res

        return poly, None


class NewtonMethod(FiniteDifferenceMethod):
    @property
    def name(self) -> str:
        return "Многочлен Ньютона"

    def solve(self, x_nodes, y_nodes):
        n, h, table = self.get_params(x_nodes, y_nodes)

        def poly(x):
            mid_point = (x_nodes[0] + x_nodes[-1]) / 2
            if x <= mid_point:
                t = (x - x_nodes[0]) / h
                res, t_prod = table[0][0], 1
                for i in range(1, n):
                    t_prod *= (t - i + 1)
                    res += (t_prod * table[0][i]) / math.factorial(i)
            else:
                t = (x - x_nodes[-1]) / h
                res, t_prod = table[n - 1][0], 1
                for i in range(1, n):
                    t_prod *= (t + i - 1)
                    res += (t_prod * table[n - 1 - i][i]) / math.factorial(i)
            return res

        return poly, table


class GaussMethod(FiniteDifferenceMethod):
    @property
    def name(self) -> str:
        return "Многочлен Гаусса"

    def solve(self, x_nodes, y_nodes):
        n, h, table = self.get_params(x_nodes, y_nodes)
        mid = n // 2
        dts = self.generate_offsets(n)


        def poly(x):
            t = (x - x_nodes[mid]) / h
            mode = 1 if x > x_nodes[mid] else 2
            return self.compute_gauss(t, n, mid, table, mode, dts)

        return poly, table


class StirlingMethod(FiniteDifferenceMethod):
    @property
    def name(self) -> str:
        return "Многочлен Стирлинга"

    def solve(self, x_nodes, y_nodes):
        if len(x_nodes) % 2 == 0:
            raise ValueError("Нужно нечетное число узлов")

        n, h, table = self.get_params(x_nodes, y_nodes)
        mid = n // 2
        dts = self.generate_offsets(n)

        def poly(x):
            t = (x - x_nodes[mid]) / h
            g1 = self.compute_gauss(t, n, mid, table, 1, dts)
            g2 = self.compute_gauss(t, n, mid, table, 2, dts)
            return (g1 + g2) / 2

        return poly, table


class BesselMethod(FiniteDifferenceMethod):
    @property
    def name(self) -> str:
        return "Многочлен Бесселя"

    def solve(self, x_nodes, y_nodes):
        if len(x_nodes) % 2 != 0:
            raise ValueError("Нужно четное число узлов")

        n, h, table = self.get_params(x_nodes, y_nodes)
        mid = n // 2 - 1

        def poly(x):
            t = (x - x_nodes[mid]) / h
            u = t - 0.5
            res = (table[mid][0] + table[mid + 1][0]) / 2 + u * table[mid][1]

            t_prod = 1
            for k in range(1, mid + 1):
                t_prod *= (t - k) * (t + k - 1)
                if 2 * k < n:
                    f_avg = (table[mid - k][2 * k] + table[mid - k + 1][2 * k]) / 2
                    res += (t_prod * f_avg) / math.factorial(2 * k)
                    if 2 * k + 1 < n:
                        res += (u * t_prod * table[mid - k][2 * k + 1]) / math.factorial(2 * k + 1)
            return res

        return poly, table