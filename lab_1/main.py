from lab_1.LinearSystemSolver import LinearSystemSolver


def main():
    solver = LinearSystemSolver()
    actions = {
        '1': lambda: solver.update_n(int(input("enter n (1 <= n <= 20): "))),
        '2': solver.update_matrix,
        '3': solver.show_n,
        '4': solver.show_matrix,
        '5': solver.random_matrix,
        '6': solver.show_triangle_matrix,
        '7': solver.solve_matrix_det,
        '8': solver.solve_matrix,
        '9': solver.compute_residual,
    }

    while True:
        print("\n1.update n  2.update matrix  3.show n  4.show matrix  5.random matrix  6.show triangle matrix  7.solve matrix det  8.solve matrix  9.compute residual  0. exit")
        choice = input("choose: ").strip()
        if choice == '0':
            print("exit")
            break
        action = actions.get(choice)
        if action:
            try:
                action()
            except ValueError:
                print("error: incorrect data")
            except Exception:
                print(f"err: incorrect data")
        else:
            print("error choice")

if __name__ == '__main__':
    main()