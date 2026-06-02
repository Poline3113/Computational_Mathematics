from math import sqrt
from lab_4.model.solution import Solution


class Solver:
    def compute_all(self, x, y, methods):
        results = []
        n = len(x)
        for m in methods:
            try:
                func, coeffs = m.solve(x, y)
                phi_x = [func(xi) for xi in x]
                eps = [phi_xi - yi for phi_xi, yi in zip(phi_x, y)]
                s = sum(e ** 2 for e in eps)
                mse = sqrt(s / n)

                mean_y = sum(y) / n
                ss_res = sum((yi - phi_xi) ** 2 for yi, phi_xi in zip(y, phi_x))
                ss_tot = sum((yi - mean_y) ** 2 for yi in y)
                r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

                pearson = None
                if m.name == "Linear approximation":
                    mean_x = sum(x) / n
                    num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
                    den = sqrt(sum((xi - mean_x) ** 2 for xi in x) * sum((yi - mean_y) ** 2 for yi in y))
                    pearson = num / den if den != 0 else 0

                results.append(Solution(m.name, func, coeffs, mse, r2, s, phi_x, eps, pearson))
            except ValueError as ve:
                results.append({'name': m.name, 'is_error': True, 'msg': str(ve)})
        return results