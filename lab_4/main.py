import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
import os

from model.solver import Solver
from methods.method import *


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Function Approximation Pro")
        self.root.geometry("1200x850")

        self.solver = Solver()
        self.methods = [
            LinearMethod(), Poly2Method(), Poly3Method(),
            ExponentialMethod(), LogarithmicMethod(), PowerMethod()
        ]

        self.point_rows = []

        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_panel = ttk.Frame(main_frame, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        input_group = ttk.LabelFrame(left_panel, text=" Data Points (7-12) ", padding="10")
        input_group.pack(fill=tk.BOTH, expand=True)

        btn_frame = ttk.Frame(input_group)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(btn_frame, text="+", width=3, command=self.add_row).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="-", width=3, command=self.remove_row).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Clear", command=self.clear_points).pack(side=tk.RIGHT, padx=2)
        ttk.Button(btn_frame, text="Random", width=10, command=self.fill_random).pack(side=tk.LEFT, padx=2)

        file_btn_frame = ttk.Frame(input_group)
        file_btn_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Button(file_btn_frame, text="Save to File", width=12, command=self.save_to_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_btn_frame, text="Load from File", width=12, command=self.load_from_file).pack(side=tk.LEFT,
                                                                                                      padx=2)

        self.canvas_pts = tk.Canvas(input_group, width=220, highlightthickness=0)
        self.scrollbar_pts = ttk.Scrollbar(input_group, orient="vertical", command=self.canvas_pts.yview)
        self.scroll_frame = ttk.Frame(self.canvas_pts)

        self.scroll_frame.bind("<Configure>",
                               lambda e: self.canvas_pts.configure(scrollregion=self.canvas_pts.bbox("all")))
        self.canvas_pts.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas_pts.configure(yscrollcommand=self.scrollbar_pts.set)

        self.canvas_pts.pack(side="left", fill="both", expand=True)
        self.scrollbar_pts.pack(side="right", fill="y")

        ttk.Button(left_panel, text="RUN ANALYSIS", style="Accent.TButton", command=self.process).pack(fill=tk.X,
                                                                                                       pady=10)

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.tab_graph = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_graph, text=" Visualization ")
        self.figure, self.ax = plt.subplots(figsize=(6, 5), dpi=100)
        self.canvas_graph = FigureCanvasTkAgg(self.figure, master=self.tab_graph)
        self.canvas_graph.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.tab_table = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_table, text=" Comparison Table ")

        columns = ("method", "s", "mse", "r2")
        self.tree = ttk.Treeview(self.tab_table, columns=columns, show="headings")
        self.tree.heading("method", text="Approximation Method")
        self.tree.heading("s", text="S")
        self.tree.heading("mse", text="MSE")
        self.tree.heading("r2", text="R^2")

        for col in columns:
            self.tree.column(col, width=150, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tab_log = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_log, text=" Detailed Report ")
        self.output = tk.Text(self.tab_log, state='disabled', font=("Consolas", 11), bg="#fdfdfd")
        self.output.pack(fill=tk.BOTH, expand=True)

        self.init_default_data()

    def init_default_data(self):
        data = [(1.1, 2.73), (1.3, 5.12), (1.5, 7.74), (1.7, 8.91), (1.9, 10.59), (2.1, 12.75), (2.3, 13.43),
                (2.5, 16.03), (1.0, 1.1)]
        for x, y in data: self.add_row(x, y)

    def add_row(self, x="", y=""):
        if len(self.point_rows) >= 12: return
        f = ttk.Frame(self.scroll_frame)
        f.pack(fill=tk.X, pady=1)
        ttk.Label(f, text=f"{len(self.point_rows) + 1}:", width=3).pack(side=tk.LEFT)
        ex = ttk.Entry(f, width=10);
        ex.insert(0, str(x));
        ex.pack(side=tk.LEFT, padx=2)
        ey = ttk.Entry(f, width=10);
        ey.insert(0, str(y));
        ey.pack(side=tk.LEFT, padx=2)
        self.point_rows.append((ex, ey, f))

    def remove_row(self):
        if len(self.point_rows) > 7:
            ex, ey, f = self.point_rows.pop()
            f.destroy()

    def clear_points(self):
        for _, _, f in self.point_rows: f.destroy()
        self.point_rows = []
        for _ in range(7): self.add_row()

    def save_to_file(self):
        try:
            data_lines = []
            for ex, ey, _ in self.point_rows:
                vx = ex.get().strip().replace(',', '.')
                vy = ey.get().strip().replace(',', '.')
                if vx and vy:
                    float(vx)
                    float(vy)
                    data_lines.append(f"{vx},{vy}")

            if not data_lines:
                messagebox.showwarning("Warning", "No valid data points to save.")
                return

            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("All Files", "*.*")],
                title="Save Approximation Data"
            )

            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for line in data_lines:
                        f.write(line + "\n")
                messagebox.showinfo("Success", f"Data saved to {os.path.basename(file_path)}")

        except ValueError:
            messagebox.showerror("Error", "Please ensure all filled fields contain valid numbers before saving.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")


    def load_from_file(self):
        file_path = filedialog.askopenfilename(
            title="Load Approximation Data",
            filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("All Files", "*.*")]
        )

        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            new_data = []
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split(',')
                if len(parts) >= 2:
                    try:
                        x_val = float(parts[0].replace(',', '.'))
                        y_val = float(parts[1].replace(',', '.'))
                        new_data.append((x_val, y_val))
                    except ValueError:
                        continue

            if not new_data:
                messagebox.showwarning("Warning", "No valid data found in the file.")
                return

            for _, _, f in self.point_rows:
                f.destroy()
            self.point_rows = []

            for x, y in new_data:
                self.add_row(x, y)

            while len(self.point_rows) < 7:
                self.add_row()

            messagebox.showinfo("Success", f"Loaded {len(new_data)} points from {os.path.basename(file_path)}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")


    def process(self):
        try:
            x, y = [], []
            for ex, ey, _ in self.point_rows:
                vx, vy = ex.get().strip().replace(',', '.'), ey.get().strip().replace(',', '.')
                if vx and vy:
                    x.append(float(vx))
                    y.append(float(vy))

            if len(x) < 7:
                raise ValueError("Enter at least 7 points")

            all_results = self.solver.compute_all(x, y, self.methods)

            valid_results = [r for r in all_results if not isinstance(r, dict)]

            if not valid_results:
                messagebox.showwarning("Warning", "No methods could be applied to this data.")
                return

            best = min(valid_results, key=lambda r: r.mse)

            for i in self.tree.get_children(): self.tree.delete(i)

            sorted_all = sorted(valid_results, key=lambda r: r.mse)
            errors = [r for r in all_results if isinstance(r, dict)]

            for r in sorted_all:
                tag = "best" if r == best else ""
                self.tree.insert("", tk.END, values=(r.name, f"{r.s}", f"{r.mse}", f"{r.r2}"), tags=(tag,))

            for err in errors:
                self.tree.insert("", tk.END, values=(err['name'], "N/A", "N/A", "N/A", "Skipped"), tags=("error",))

            self.tree.tag_configure("best", background="#e1f5fe", font=('Segoe UI', 9, 'bold'))
            self.tree.tag_configure("error", foreground="gray")

            self.output.config(state='normal')
            self.output.delete('1.0', tk.END)
            self.output.insert(tk.END, f"Best Method: {best.name.upper()}\n\n")

            for r in all_results:
                if isinstance(r, dict):
                    self.output.insert(tk.END, f"{r['name']}\n")
                    self.output.insert(tk.END, f"  STATUS: SKIPPED\n")
                    self.output.insert(tk.END, f"  EXPLANATION: {r['msg']}\n\n")
                else:
                    self.output.insert(tk.END, f"{r.name}\n")
                    self.output.insert(tk.END, f"  Formula Coefficients: {[c for c in r.coeffs]}\n")
                    self.output.insert(tk.END, f"  Determination coefficient: {r.r2}\n")

                    if r.pearson is not None:
                        self.output.insert(tk.END, f"  Pearson Correlation: {r.pearson}\n")

                    self.output.insert(tk.END, f"  Standard Deviation: {r.s}\n")
                    self.output.insert(tk.END, f"  MSE: {r.mse}\n")
                    self.output.insert(tk.END, f"  Residuals: {[e for e in r.eps]}\n\n")
            self.output.config(state='disabled')

            self.draw_graph(x, y, valid_results, best)

            self.notebook.select(self.tab_table)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def draw_graph(self, x, y, results, best):
        self.ax.clear()
        self.ax.scatter(x, y, color='#2c3e50', s=40, label='Source Points', zorder=5)

        xmin, xmax = min(x), max(x)
        margin = (xmax - xmin) * 0.2
        xr = [xmin - margin + i * (xmax - xmin + 2 * margin) / 200 for i in range(201)]

        for r in results:
            is_best = (r == best)
            plot_x, plot_y = [], []

            for xi in xr:
                try:
                    yi = r.func(xi)

                    if isinstance(yi, complex):
                        continue

                    if not np.isfinite(yi):
                        continue

                    plot_x.append(xi)
                    plot_y.append(yi)
                except:
                    continue

            if plot_x:
                self.ax.plot(plot_x, plot_y,
                             label=r.name + (" (Best)" if is_best else ""),
                             lw=2.5 if is_best else 1,
                             alpha=1.0 if is_best else 0.4,
                             ls='-' if is_best else '--')

        self.ax.set_title("Function Approximation Comparison")
        self.ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize='small')
        self.ax.grid(True, linestyle=':', alpha=0.6)

        y_min, y_max = min(y), max(y)
        y_margin = (y_max - y_min) * 0.5
        self.ax.set_ylim(y_min - y_margin, y_max + y_margin)

        self.figure.tight_layout()
        self.canvas_graph.draw()

    def fill_random(self):
        num_points = random.randint(7, 12)

        for _, _, f in self.point_rows: f.destroy()
        self.point_rows = []
        for _ in range(num_points): self.add_row()

        xs = sorted(random.sample([round(0.1 + i * 0.5 + random.uniform(0, 0.3), 2) for i in range(25)], num_points))

        ys = [round(random.uniform(1.0, 30.0), 2) for _ in range(num_points)]

        for i, (ex, ey, _) in enumerate(self.point_rows):
            ex.delete(0, tk.END)
            ex.insert(0, str(xs[i]))
            ey.delete(0, tk.END)
            ey.insert(0, str(ys[i]))

        self.process()


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    if "vista" in style.theme_names(): style.theme_use("vista")
    app = App(root)
    root.mainloop()