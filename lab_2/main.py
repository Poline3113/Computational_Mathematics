import math
import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from methods.half_division_method import HalfDivisionMethod
from methods.newton_method import NewtonMethod
from methods.simple_iterations_method import SimpleIterationsMethod
from model.equation import Equation


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Nonlinear Equations & Systems Solver")
        self.root.geometry("1100x800")

        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.left_panel = ttk.LabelFrame(self.main_frame, text=" Control ", padding="10")
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        ttk.Label(self.left_panel, text="Select equation:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        self.eq_var = tk.IntVar(value=1)
        self.eq_list = [
            "3.00*x^3 + 1.70*x^2 - 15.42*x + 6.89",
            "-1.80*x^3 - 2.94*x^2 + 10.37*x + 5.38",
            "x^3 - 3.125*x^2 - 3.50*x + 2.458",
            "4.45*x^3 + 7.81*x^2 - 9.62*x - 8.17",
            "x - cos(x) = 0"
        ]
        for i, text in enumerate(self.eq_list, 1):
            ttk.Radiobutton(self.left_panel, text=text, variable=self.eq_var, value=i).pack(anchor=tk.W)

        ttk.Separator(self.left_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        ttk.Label(self.left_panel, text="Method and parameters:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        self.method_var = tk.IntVar(value=1)
        ttk.Radiobutton(self.left_panel, text="Half division method", variable=self.method_var, value=1,
                        command=self.toggle_x0).pack(anchor=tk.W)
        ttk.Radiobutton(self.left_panel, text="Newton\'s method", variable=self.method_var, value=2,
                        command=self.toggle_x0).pack(anchor=tk.W)
        ttk.Radiobutton(self.left_panel, text="Simple iteration method", variable=self.method_var, value=3,
                        command=self.toggle_x0).pack(anchor=tk.W)

        self.inputs_frame = ttk.Frame(self.left_panel)
        self.inputs_frame.pack(fill=tk.X, pady=5)
        self.a_entry = self.create_input("Boundary a:", "0")
        self.b_entry = self.create_input("Boundary b:", "1")
        self.eps_entry = self.create_input("Precision ε:", "0.01")
        self.x0_label = ttk.Label(self.inputs_frame, text="Initial x0:")
        self.x0_entry = ttk.Entry(self.inputs_frame)

        ttk.Button(self.left_panel, text="SOLVE EQUATION", command=self.solve_equation).pack(fill=tk.X, pady=(10, 2))
        ttk.Button(self.left_panel, text="clear", command=self.clear_log).pack(fill=tk.X, pady=(0, 10))

        ttk.Separator(self.left_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        ttk.Label(self.left_panel, text="Select system:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        self.sys_var = tk.IntVar(value=1)
        self.sys_list = [
            "1: tan(x)*y = x^2, 0.8*x^2 + 2*y^2 = 1",
            "2: sin(x + y) - 1.1*x = 0.1, x^2 + y^2 = 1"
        ]
        for i, text in enumerate(self.sys_list, 1):
            ttk.Radiobutton(self.left_panel, text=text, variable=self.sys_var, value=i).pack(anchor=tk.W)

        ttk.Separator(self.left_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(self.left_panel, text="System parameters:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)

        self.sys_inputs_frame = ttk.Frame(self.left_panel)
        self.sys_inputs_frame.pack(fill=tk.X, pady=5)

        self.sys_x0_entry = self.create_sys_input(self.sys_inputs_frame, "Initial x0:", "0.5")
        self.sys_y0_entry = self.create_sys_input(self.sys_inputs_frame, "Initial y0:", "0.5")
        self.sys_eps_entry = self.create_sys_input(self.sys_inputs_frame, "Precision ε:", "0.001")

        ttk.Button(self.left_panel, text="SOLVE SYSTEM", command=self.solve_system).pack(fill=tk.X, pady=10)

        self.right_panel = ttk.Frame(self.main_frame)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.figure, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.output = tk.Text(self.right_panel, height=12, state='disabled', background="#f0f0f0")
        self.output.pack(fill=tk.X, pady=(10, 0))

        self.toggle_x0()

    def create_input(self, label_text, default_val):
        ttk.Label(self.inputs_frame, text=label_text).pack(anchor=tk.W)
        entry = ttk.Entry(self.inputs_frame)
        entry.insert(0, default_val)
        entry.pack(fill=tk.X, pady=(0, 5))
        return entry

    def create_sys_input(self, parent, label_text, default_val):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        ttk.Label(frame, text=label_text, width=15).pack(side=tk.LEFT)
        entry = ttk.Entry(frame)
        entry.insert(0, default_val)
        entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        return entry

    def toggle_x0(self):
        if self.method_var.get() == 2:
            self.x0_label.pack(anchor=tk.W)
            self.x0_entry.pack(fill=tk.X, pady=(0, 5))
        else:
            self.x0_label.pack_forget()
            self.x0_entry.pack_forget()

    def log(self, msg: str):
        self.output.config(state='normal')
        self.output.insert(tk.END, msg + '\n')
        self.output.see(tk.END)
        self.output.config(state='disabled')

    def clear_log(self):
        self.output.config(state='normal')
        self.output.delete('1.0', tk.END)
        self.output.config(state='disabled')

    def solve_system(self):
        try:
            x0_val = float(self.sys_x0_entry.get())
            y0_val = float(self.sys_y0_entry.get())
            eps = float(self.sys_eps_entry.get())

            from methods.nonlinear_system_solver import system1, system2, check_convergence, solve as run_solver
            from methods.nonlinear_system_solver import phi1_sys1, phi2_sys1, phi1_sys2, phi2_sys2

            choice = self.sys_var.get()
            sys_func, p1, p2 = (system1, phi1_sys1, phi2_sys1) if choice == 1 else (system2, phi1_sys2, phi2_sys2)

            converges, norm = check_convergence(choice, x0_val, y0_val)
            self.log(f" System {choice}")
            self.log(f"Convergence: {'Yes' if converges else 'No'} (norm={norm})")

            sol, iters, err = run_solver(sys_func, p1, p2, (x0_val, y0_val), eps)

            if sol is not None:
                self.log(f"Solution: x = {sol[0]}, y = {sol[1]}")
                self.log(f"Iteration: {iters}, Error: {err}\n")

                self.draw_system_graph(sys_func, sol)
            else:
                self.log("Error: failed to find solution")

        except Exception as e:
            messagebox.showerror("System Error", str(e))

    def draw_system_graph(self, sys_func, solution):

        self.ax.clear()

        x_min, x_max = solution[0] - 2, solution[0] + 2
        y_min, y_max = solution[1] - 2, solution[1] + 2

        x_range = np.linspace(x_min, x_max, 100)
        y_range = np.linspace(y_min, y_max, 100)
        X, Y = np.meshgrid(x_range, y_range)

        Z1 = np.array([[sys_func([x, y])[0] for x in x_range] for y in y_range])
        Z2 = np.array([[sys_func([x, y])[1] for x in x_range] for y in y_range])

        self.ax.contour(X, Y, Z1, levels=[0], colors='blue', linestyles='solid')
        self.ax.contour(X, Y, Z2, levels=[0], colors='red', linestyles='solid')

        self.ax.plot(solution[0], solution[1], 'ko', label=f'Root: ({solution[0]}, {solution[1]})')

        self.ax.set_title("System Plot")
        self.ax.grid(True, ls='--')
        self.ax.legend()
        self.canvas.draw()

    def get_equation_by_number(self, num: int) -> Equation:
        def safe_f(f): return lambda x: f(float(x))

        eqs = {
            1: Equation(
                safe_f(lambda x: 3.00 * x ** 3 + 1.70 * x ** 2 - 15.42 * x + 6.89),
                "3.00*x^3 + 1.70*x^2 - 15.42*x + 6.89",
                safe_f(lambda x: 9.00 * x ** 2 + 3.40 * x - 15.42),
                safe_f(lambda x: 18.00 * x + 3.40)
            ),
            2: Equation(
                safe_f(lambda x: -1.80 * x ** 3 - 2.94 * x ** 2 + 10.37 * x + 5.38),
                "-1.80*x^3 - 2.94*x^2 + 10.37*x + 5.38",
                safe_f(lambda x: -5.40 * x ** 2 - 5.88 * x + 10.37),
                safe_f(lambda x: -10.80 * x - 5.88)
            ),
            3: Equation(
                safe_f(lambda x: 1.00 * x ** 3 - 3.125 * x ** 2 - 3.50 * x + 2.458),
                "x^3 - 3.125*x^2 - 3.50*x + 2.458",
                safe_f(lambda x: 3.00 * x ** 2 - 6.25 * x - 3.50),
                safe_f(lambda x: 6.00 * x - 6.25)
            ),
            4: Equation(
                safe_f(lambda x: 4.45 * x ** 3 + 7.81 * x ** 2 - 9.62 * x - 8.17),
                "4.45*x^3 + 7.81*x^2 - 9.62*x - 8.17",
                safe_f(lambda x: 13.35 * x ** 2 + 15.62 * x - 9.62),
                safe_f(lambda x: 26.70 * x + 15.62)
            ),
            5: Equation(
                safe_f(lambda x: x - math.cos(x)),
                "x - cos(x) = 0",
                safe_f(lambda x: 1 + math.sin(x)),
                safe_f(lambda x: math.cos(x))
            ),
        }
        return eqs[num]

    def draw_graph(self, eq, a, b):
        self.ax.clear()
        import numpy as np
        a_f, b_f = float(a), float(b)
        margin = abs(b_f - a_f) * 0.2
        x = np.linspace(a_f - margin, b_f + margin, 400)
        y = [eq.function(val) for val in x]

        self.ax.plot(x, y, label=eq.fun_str, color='blue')
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)
        self.ax.grid(True, linestyle='--')
        self.ax.legend()
        self.canvas.draw()

    def solve_equation(self):
        try:
            eq = self.get_equation_by_number(self.eq_var.get())
            a = Decimal(self.a_entry.get().replace(",", "."))
            b = Decimal(self.b_entry.get().replace(",", "."))
            eps = Decimal(self.eps_entry.get().replace(",", "."))

            x0 = None
            if self.method_var.get() == 2:
                x0 = Decimal(self.x0_entry.get().replace(",", "."))

            method_map = {1: HalfDivisionMethod, 2: NewtonMethod, 3: SimpleIterationsMethod}
            method = method_map[self.method_var.get()](eq, a, b, eps, x0)

            result = method.solve()
            self.log(result.string_solution())

            self.draw_graph(eq, a, b)

        except Exception as e:
            messagebox.showerror("Error", f"input problem: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()