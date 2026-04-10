import math
import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


from model.integral import Integral
from model.solution import Solution
from methods.midpoin_rule import MidpointRule
from methods.left_rectangle_rule import LeftRectangleRule
from methods.right_rectangle_rule import RightRectangleRule
from methods.trapezoid_rule import TrapezoidRule
from methods.simpson_rule import SimpsonRule
from model.solver import IntegralSolver


def get_integral_library():
    return {
        1: Integral(
            lambda x: x * x,
            "x^2"
        ),
        2: Integral(
            lambda x: Decimal(str(math.sin(float(x)))),
            "sin(x)"
        ),
        3: Integral(
            lambda x: Decimal(4) * x ** 3 - Decimal(5) * x ** 2 + Decimal(6) * x - Decimal(7),
            "4x³ - 5x² + 6x - 7"
        ),
        4: Integral(
            lambda x: Decimal(1) / x,
            "1/x",
            Decimal(0),
            (Decimal(-1), Decimal(1))
        ),
        5: Integral(
            lambda x: Decimal(3) * x ** 3 - Decimal(2) * x ** 2 - Decimal(7) * x - Decimal(8),
            "3x³ - 2x² - 7x - 8"
        ),
        6: Integral(
            lambda x: -x ** 3 - x ** 2 - 2 * x + Decimal(1),
            "-x³ - x² - 2x + 1"
        ),
        7: Integral(
            lambda x: Decimal(1) / (x - Decimal(2)),
            "1/(x - 2)",
            Decimal(2),
            (Decimal(1), Decimal(3))
        ),
        8: Integral(
            lambda x: Decimal(1) / (x*x),
            "1/(x * x)",
        )
    }

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Numerical Integration Solver")
        self.root.geometry("1100x850")

        self.integrals = get_integral_library()
        self.solver = IntegralSolver()

        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        left = ttk.LabelFrame(main_frame, text=" Settings ", padding="10")
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        ttk.Label(left, text="Select function:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        self.int_var = tk.IntVar(value=1)
        for idx, obj in self.integrals.items():
            ttk.Radiobutton(left, text=obj.fun_str, variable=self.int_var, value=idx).pack(anchor=tk.W)

        ttk.Separator(left, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        ttk.Label(left, text="Method:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        self.method_var = tk.IntVar(value=1)
        methods = [("Midpoint rectangle ", MidpointRule), ("Left rectangle", LeftRectangleRule),
                   ("Right rectangle", RightRectangleRule), ("Trapezoid", TrapezoidRule), ("Simpson", SimpsonRule)]
        self.method_map = {i + 1: m[1] for i, m in enumerate(methods)}
        for i, (name, _) in enumerate(methods, 1):
            ttk.Radiobutton(left, text=name, variable=self.method_var, value=i).pack(anchor=tk.W)

        self.a_ent = self._create_input(left, "Lower limit a:", "-1")
        self.b_ent = self._create_input(left, "Upper limit b:", "2")
        self.eps_ent = self._create_input(left, "Precision ε:", "0.001")

        ttk.Button(left, text="CALCULATE", command=self.solve_integral).pack(fill=tk.X, pady=10)
        ttk.Button(left, text="Clear Log", command=self.clear_log).pack(fill=tk.X)

        right = ttk.Frame(main_frame)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.output = tk.Text(right, height=10, state='disabled', bg="#f4f4f4", font=("Consolas", 10))
        self.output.pack(fill=tk.X, pady=5)

    def _create_input(self, parent, label, default):
        ttk.Label(parent, text=label).pack(anchor=tk.W)
        e = ttk.Entry(parent)
        e.insert(0, default)
        e.pack(fill=tk.X, pady=(0, 5))
        return e

    def log(self, msg):
        self.output.config(state='normal')
        self.output.insert(tk.END, str(msg) + '\n')
        self.output.config(state='disabled')
        self.output.see(tk.END)

    def clear_log(self):
        self.output.config(state='normal')
        self.output.delete('1.0', tk.END)
        self.output.config(state='disabled')

    def solve_integral(self):
        try:
            get_dec = lambda ent: Decimal(ent.get().replace(",", "."))
            a, b, eps = get_dec(self.a_ent), get_dec(self.b_ent), get_dec(self.eps_ent)

            integral = self.integrals[self.int_var.get()]
            method = self.method_map[self.method_var.get()]()

            result = self.solver.compute(integral, a, b, eps, method)

            self.log(f"Integral: {integral.fun_str} on [{a}, {b}]")
            self.log(f"Method: {method.name}")
            self.log(f"Result: {result.value}")
            self.log(f"Number of intervals (n): {result.n}")
            if getattr(result, 'cauchy_applied', False):
                self.log("(!) Cauchy principal value applied")
            self.log("")

            self.draw_graph(integral, a, b)
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")

    def draw_graph(self, integral, a, b):
        self.ax.clear()
        x_plot = np.linspace(float(a) - 0.5, float(b) + 0.5, 500)
        y_plot = []
        for val in x_plot:
            try:
                res = float(integral.function(Decimal(str(val))))
                y_plot.append(res if abs(res) < 100 else np.nan)
            except:
                y_plot.append(np.nan)

        self.ax.plot(x_plot, y_plot, label=f"f(x) = {integral.fun_str}", color='blue')
        self.ax.axhline(0, color='black', lw=1)
        self.ax.axvline(float(a), color='red', ls='--')
        self.ax.axvline(float(b), color='red', ls='--')
        self.ax.set_ylim(-10, 10)
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()