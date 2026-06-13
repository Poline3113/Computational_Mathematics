from methods.method import LagrangeMethod

class Solver:
    def compute_all(self, x_nodes, y_nodes, target_x, methods):
        results = []
        h_values = [x_nodes[i + 1] - x_nodes[i] for i in range(len(x_nodes) - 1)]
        is_equidistant = all(abs(h - h_values[0]) < 1e-3 for h in h_values)

        for m in methods:
            try:
                if not is_equidistant and not isinstance(m, LagrangeMethod):
                    raise ValueError("Узлы должны быть равноотстоящими для этого метода")

                poly_func, diff_table = m.solve(x_nodes, y_nodes)
                y_interpolated = poly_func(target_x)

                results.append({
                    'name': m.name,
                    'func': poly_func,
                    'value_at_x': y_interpolated,
                    'diff_table': diff_table,
                    'is_error': False
                })
            except Exception as e:
                results.append({'name': m.name, 'is_error': True, 'msg': str(e)})
        return results