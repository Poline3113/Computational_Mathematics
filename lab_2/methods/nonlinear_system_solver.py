

from model.system_graph import SystemGraph
import math

def system1(xy):
    x, y = float(xy[0]), float(xy[1])
    return [
        math.tan(x * y) - x**2,
        0.8 * x**2 + 2 * y**2 - 1
    ]

def system2(xy):
    x, y = float(xy[0]), float(xy[1])
    return [
        math.sin(x + y) - 1.1 * x - 0.1,
        x**2 + y**2 - 1
    ]

def phi1_sys1(xy):
    x, y = float(xy[0]), float(xy[1])
    return math.sqrt(abs(math.tan(x * y)))

def phi2_sys1(xy):
    x, y = float(xy[0]), float(xy[1])
    return math.sqrt(abs((1 - 0.8 * x**2) / 2))


def phi1_sys2(xy):
    x, y = float(xy[0]), float(xy[1])
    return (math.sin(x + y) - 0.1) / 1.1

def phi2_sys2(xy):
    x, y = float(xy[0]), float(xy[1])
    return math.sqrt(abs(1 - x**2))

def check_convergence(system_num: int, x0, y0):
    x, y = float(x0), float(y0)

    if system_num == 1:
        d_phi1 = abs(y / (math.cos(x*y)**2 * 2 * math.sqrt(abs(math.tan(x*y) + 1e-9))))
        d_phi2 = abs((0.8 * x) / (2 * math.sqrt(abs((1 - 0.8 * x**2) / 2 + 1e-9))))
    elif system_num == 2:
        d_phi1 = abs(math.cos(x + y) / 1.1)
        d_phi2 = abs(x / math.sqrt(abs(1 - x**2) + 1e-9))
    else:
        return False, 0.0

    norm = float(max(d_phi1, d_phi2))
    return norm < 1.0, norm


def solve(system_func, phi1, phi2, x0, epsilon, max_iterations=500):
    try:
        curr_x = float(x0[0])
        curr_y = float(x0[1])
        eps = float(epsilon)

        for i in range(1, max_iterations + 1):
            next_x = float(phi1([curr_x, curr_y]))
            next_y = float(phi2([curr_x, curr_y]))

            diff = max(abs(next_x - curr_x), abs(next_y - curr_y))

            res = system_func([next_x, next_y])
            res_val = max(abs(float(res[0])), abs(float(res[1])))

            if diff < eps and res_val < eps:
                return [next_x, next_y], i, diff

            curr_x, curr_y = next_x, next_y

        return [curr_x, curr_y], max_iterations, diff

    except Exception as e:
        print(f"Error: {e}")
        return None, None, None

def choose_system_of_equations(functions):
    print("choose a system of equations:")
    for key, value in functions.items():
        print(f"{key}: {value[1]}")

    try:
        num = int(input("enter the system number: "))
        if num not in functions:
            raise ValueError
        return num
    except ValueError:
        print("invalid number")
        return choose_system_of_equations(functions)


def run():
    systems = {
        1: (system1, "tan(x)*y = x^2, 0.8*x^2 + 2*y^2 = 1"),
        2: (system2, "sin(x + y) - 1.1*x = 0.1, x^2 + y^2 = 1")
    }

    eq_num = choose_system_of_equations(systems)
    system_func, title = systems[eq_num]

    graph = SystemGraph(system_func, title)
    graph.draw()

    x0, y0 = map(float, input("enter initial approximations x0, y0: ").split())
    epsilon = float(input("enter calculation tolerance (ε): "))

    converges, norm = check_convergence(eq_num, x0, y0)
    if not converges:
        print(f"convergence condition not satisfied: max|φ'| = {norm} >= 1")

    if eq_num == 1:
        solution, iters, error = solve(system1, phi1_sys1, phi2_sys1, (x0, y0), epsilon)
    elif eq_num == 2:
        solution, iters, error = solve(system2, phi1_sys2, phi2_sys2, (x0, y0), epsilon)
    else:
        print("unknown system")
        return

    if solution is not None:
        print(f"\nSolution:")
        print(f"x = {solution[0]}")
        print(f"y = {solution[1]}")
        print(f"iterations: {iters}")
        print(f"last step error ||x^(k) − x^(k−1)|| = {error}")
        print(f"residual: [{system_func(solution)[0]}, {system_func(solution)[1]}]")
    else:
        print("failed to find solution")