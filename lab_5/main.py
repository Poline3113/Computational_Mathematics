import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from model.solver import Solver
from methods.method import *


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Интерполяция функций")
        self.root.geometry("900x700")

        self.solver = Solver()
        self.methods = [
            LagrangeMethod(), NewtonMethod(), GaussMethod(),
            StirlingMethod(), BesselMethod()
        ]

        self.point_rows = []
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_panel = ttk.Frame(main_frame, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        config_group = ttk.LabelFrame(left_panel, text=" Параметры интерполяции ", padding="10")
        config_group.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(config_group, text="Точка x:").grid(row=0, column=0, sticky=tk.W)
        self.target_x_entry = ttk.Entry(config_group, width=10)
        self.target_x_entry.insert(0, "1.5")
        self.target_x_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(config_group, text="Функция:").grid(row=1, column=0, sticky=tk.W)
        self.func_combo = ttk.Combobox(config_group, values=["Ручной ввод", "sin(x)", "2*x^2 - 5*x", "sqrt(x)", "x^3"],
                                       width=15)
        self.func_combo.current(0)
        self.func_combo.grid(row=1, column=1, padx=5, pady=2)

        self.func_combo.bind("<<ComboboxSelected>>", self.toggle_func_params)

        self.func_params_frame = ttk.Frame(config_group)

        ttk.Label(self.func_params_frame, text="Интервал [a, b]:").grid(row=0, column=0, sticky=tk.W, pady=2)
        interval_inner = ttk.Frame(self.func_params_frame)
        interval_inner.grid(row=0, column=1, pady=2, sticky=tk.W)
        self.a_entry = ttk.Entry(interval_inner, width=5);
        self.a_entry.insert(0, "0")
        self.a_entry.pack(side=tk.LEFT)
        self.b_entry = ttk.Entry(interval_inner, width=5);
        self.b_entry.insert(0, "3")
        self.b_entry.pack(side=tk.LEFT, padx=2)

        ttk.Label(self.func_params_frame, text="Кол-во точек:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.n_entry = ttk.Entry(self.func_params_frame, width=10);
        self.n_entry.insert(0, "8")
        self.n_entry.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)

        ttk.Button(self.func_params_frame, text="Подставить по функции", command=self.on_func_generate).grid(row=2, column=0, columnspan=2, pady=10)

        self.toggle_func_params()

        input_group = ttk.LabelFrame(left_panel, text=" Узлы интерполяции ", padding="10")
        input_group.pack(fill=tk.BOTH, expand=True)

        btn_frame = ttk.Frame(input_group)
        btn_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Button(btn_frame, text="+", width=3, command=self.add_row).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="-", width=3, command=self.remove_row).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Clear", command=self.clear_points).pack(side=tk.RIGHT, padx=2)

        file_frame = ttk.Frame(input_group)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(file_frame, text="Загрузить файл", command=self.load_from_file).pack(side=tk.LEFT, fill=tk.X,
                                                                                        expand=True, padx=2)
        ttk.Button(file_frame, text="Сохранить файл", command=self.save_to_file).pack(side=tk.LEFT, fill=tk.X,
                                                                                      expand=True, padx=2)

        self.canvas_pts = tk.Canvas(input_group, width=220, highlightthickness=0)
        self.scrollbar_pts = ttk.Scrollbar(input_group, orient="vertical", command=self.canvas_pts.yview)
        self.scroll_frame = ttk.Frame(self.canvas_pts)
        self.canvas_pts.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas_pts.configure(yscrollcommand=self.scrollbar_pts.set)
        self.canvas_pts.pack(side="left", fill="both", expand=True)
        self.scrollbar_pts.pack(side="right", fill="y")

        ttk.Button(left_panel, text="ВЫЧИСЛИТЬ", command=self.process).pack(fill=tk.X, pady=10)

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.tab_graph = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_graph, text=" График ")
        self.figure, self.ax = plt.subplots(figsize=(6, 5), dpi=100)
        self.canvas_graph = FigureCanvasTkAgg(self.figure, master=self.tab_graph)

        self.toolbar = NavigationToolbar2Tk(self.canvas_graph, self.tab_graph)
        self.toolbar.update()
        self.canvas_graph.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.tab_table = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_table, text=" Результаты ")
        columns = ("method", "value")
        self.tree = ttk.Treeview(self.tab_table, columns=columns, show="headings")
        self.tree.heading("method", text="Метод интерполяции")
        self.tree.heading("value", text="Значение P(x)")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tab_log = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_log, text=" Таблица разностей")
        self.output = tk.Text(self.tab_log, state='disabled', font=("Consolas", 10))
        self.output.pack(fill=tk.BOTH, expand=True)

        self.init_default_data()

    def on_func_generate(self):
        func = self.func_combo.get()
        if func == "Ручной ввод":
            messagebox.showinfo("Инфо", "Выберите функцию из списка для генерации")
            return

        try:
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            n = int(self.n_entry.get())
            if n < 2: raise ValueError("Нужно минимум 2 точки")

            h = (b - a) / (n - 1)
            x_nodes = [a + i * h for i in range(n)]

            f_map = {
                "sin(x)": math.sin,
                "2*x^2 - 5*x": lambda x: 2 * x ** 2 - 5 * x,
                "sqrt(x)": lambda x: math.sqrt(x) if x >= 0 else 0,
                "x^3": lambda x: x ** 3
            }
            f = f_map[func]

            self.clear_points()
            for x_val in x_nodes:
                self.add_row(round(x_val, 6), round(f(x_val), 6))
        except Exception as e:
            messagebox.showerror("Ошибка параметров", str(e))

    def load_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
        if file_path:
            try:
                self.clear_points()
                with open(file_path, 'r') as f:
                    for line in f:
                        line = line.replace(';', ',').strip()
                        if not line: continue
                        parts = line.split(',')
                        if len(parts) == 2:
                            self.add_row(parts[0], parts[1])
                messagebox.showinfo("Успех", "Данные загружены из файла.")
            except Exception as e:
                messagebox.showerror("Ошибка файла", f"Не удалось прочитать файл")

    def save_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    for ex, ey, _ in self.point_rows:
                        vx, vy = ex.get().strip(), ey.get().strip()
                        if vx and vy:
                            f.write(f"{vx},{vy}\n")
                messagebox.showinfo("Успех", "Данные сохранены")
            except Exception as e:
                messagebox.showerror("Ошибка сохранения", str(e))

    def process(self):
        try:
            target_x = float(self.target_x_entry.get().replace(',', '.'))
            x, y = [], []
            for ex, ey, _ in self.point_rows:
                vx, vy = ex.get().strip().replace(',', '.'), ey.get().strip().replace(',', '.')
                if vx and vy:
                    x.append(float(vx))
                    y.append(float(vy))

            if len(x) < 2: raise ValueError("Нужно минимум 2 точки")

            data = sorted(zip(x, y))
            x = [p[0] for p in data]
            y = [p[1] for p in data]

            if len(set(x)) != len(x):
                raise ValueError("Узлы интерполяции не должны повторяться")

            all_results = self.solver.compute_all(x, y, target_x, self.methods)

            for i in self.tree.get_children(): self.tree.delete(i)
            for r in all_results:
                if not r.get('is_error'):
                    self.tree.insert("", tk.END, values=(r['name'], f"{r['value_at_x']:.6f}"))
                else:
                    self.tree.insert("", tk.END, values=(r['name'], "Пропущен"))

            self.output.config(state='normal')
            self.output.delete('1.0', tk.END)
            for r in all_results:
                if not r.get('is_error') and r.get('diff_table'):
                    self.output.insert(tk.END, f"ТАБЛИЦА КОНЕЧНЫХ РАЗНОСТЕЙ ({r['name']}):\n")
                    table = r['diff_table']
                    n_table = len(table)
                    header = "i\tx_i\t" + "\t".join([f"Δ^{j}y" for j in range(n_table)]) + "\n"
                    self.output.insert(tk.END, header + "-" * 80 + "\n")
                    for i in range(n_table):
                        row_str = f"{i}\t{x[i]:.6f}\t"
                        for j in range(n_table - i):
                            row_str += f"{table[i][j]:.6f}\t"
                        self.output.insert(tk.END, row_str + "\n")
                    break
            self.output.config(state='disabled')
            self.draw_graph(x, y, target_x, all_results)
            self.notebook.select(self.tab_graph)

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def draw_graph(self, x_nodes, y_nodes, target_x, results):
        self.ax.clear()
        self.ax.scatter(x_nodes, y_nodes, color='blue', label='Узлы', zorder=5)
        colors = ['red', 'green', 'orange', 'purple', 'brown']
        xmin, xmax = min(x_nodes), max(x_nodes)
        margin = (xmax - xmin) * 0.1
        xr = np.linspace(xmin - margin, xmax + margin, 300)
        for i, r in enumerate(results):
            if r.get('is_error'): continue
            yr = [r['func'](xi) for xi in xr]
            self.ax.plot(xr, yr, label=r['name'], color=colors[i % len(colors)], alpha=0.7)
            self.ax.scatter(target_x, r['value_at_x'], color='red', marker='x', s=100, zorder=10)
        self.ax.set_title(f"Интерполяция в точке x={target_x}")
        self.ax.legend(fontsize='small')
        self.ax.grid(True, linestyle=':')
        self.canvas_graph.draw()

    def add_row(self, x="", y=""):
        f = ttk.Frame(self.scroll_frame)
        f.pack(fill=tk.X, pady=1)
        ex = ttk.Entry(f, width=10);
        ex.insert(0, str(x));
        ex.pack(side=tk.LEFT, padx=2)
        ey = ttk.Entry(f, width=10);
        ey.insert(0, str(y));
        ey.pack(side=tk.LEFT, padx=2)
        self.point_rows.append((ex, ey, f))

    def clear_points(self):
        for _, _, f in self.point_rows: f.destroy()
        self.point_rows = []

    def remove_row(self):
        if len(self.point_rows) > 0:
            ex, ey, f = self.point_rows.pop()
            f.destroy()

    def init_default_data(self):
        data = [(0.1, 1.25), (0.2, 2.38), (0.3, 3.79), (0.4, 5.44), (0.5, 7.14)]
        for x_val, y_val in data: self.add_row(x_val, y_val)

    def toggle_func_params(self, event=None):
        if self.func_combo.get() == "Ручной ввод":
            self.func_params_frame.grid_remove()
        else:
           self.func_params_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()