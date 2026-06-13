class Solution:
    def __init__(self, name, func, coeffs, mse, r2, s, phi_x, eps, pearson=None):
        self.name = name
        self.func = func
        self.coeffs = coeffs
        self.mse = mse
        self.r2 = r2
        self.s = s
        self.phi_x = phi_x
        self.eps = eps
        self.pearson = pearson