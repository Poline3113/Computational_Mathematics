import numpy as np
import matplotlib.pyplot as plt
from typing import Callable

class SystemGraph:
    def __init__(self, system_func: Callable, title: str = "System of Equations"):
        self.system_func = system_func
        self.title = title

    def draw(self, x_range=(-2, 2), y_range=(-2, 2), n=400):
        x = np.linspace(x_range[0], x_range[1], n)
        y = np.linspace(y_range[0], y_range[1], n)
        X, Y = np.meshgrid(x, y)

        points = np.array([self.system_func([x_, y_]) for x_, y_ in zip(np.ravel(X), np.ravel(Y))])
        Z1 = points[:, 0].reshape(X.shape)
        Z2 = points[:, 1].reshape(X.shape)

        plt.figure(figsize=(6, 6))
        plt.contour(X, Y, Z1, levels=[0], colors='r', linewidths=1.5, label='Eq1')
        plt.contour(X, Y, Z2, levels=[0], colors='b', linewidths=1.5, label='Eq2')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(self.title)
        plt.legend()
        plt.grid(True)
        plt.axhline(0, color='gray', linewidth=0.5)
        plt.axvline(0, color='gray', linewidth=0.5)
        plt.tight_layout()
        plt.show()