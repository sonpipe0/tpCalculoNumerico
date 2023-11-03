from decimal import Decimal
from typing import List

import numpy as np
import matplotlib.pyplot as plt

m = Decimal(9700)
K = Decimal(615)
F = Decimal(850)
x_adm = Decimal(0.00125)
P = Decimal(0.7890929760279801)
c = Decimal(1)


def force_periodic(x, P, F):  # gives the value of F in x time
    normalized_x = Decimal(x) % P  # Normalize x to the range [0, P)
    if x < 0: return Decimal(0)
    if normalized_x < P / 10:
        return F
    else:
        return Decimal(0)


class Vibrations:
    def __init__(self, m, K, x_adm, P, F):
        self.m = m
        self.K = K
        self.x_adm = x_adm
        self.P = P
        self.F = F

    t_points = np.linspace(0, float(2 * P), 1000)
    F_points = [force_periodic(xi, P, F) for xi in t_points]
    x_points: List[Decimal] = [Decimal(0)]
    v_points: List[Decimal] = [Decimal(0)]
    a_points = [0]

    def f(self, i):
        if i < 0: return 0
        if i == 0: return F / m
        return self.F_points[i] / m - K * self.x_points[i] - c * self.v_points[i]

    def Adams_BashfordSpeed(self, i):
        if i <= 0:
            self.v_points.append((P / 1000) * (3 * self.f(i - 1) - self.f(i - 2)))
        else:
            self.v_points.append(self.v_points[i - 1] + (P / 1000) * (3 * self.f(i - 1) - self.f(i - 2)))

    def Adam_BashfordXpos(self, i):
        if i <= 0:
            self.x_points.append((P / 1000) * (3 * self.v_points[i - 1] - self.v_points[i - 2]))
        else:
            self.x_points.append(self.x_points[i - 1] + (P / 1000) * (3 * self.v_points[i - 1] - self.v_points[i - 2]))

    def calculate(self):
        for x in range(len(self.t_points) - 1):
            self.Adams_BashfordSpeed(x)
            self.Adam_BashfordXpos(x)

    def graph(self):
        plt.plot(self.t_points, self.F_points, label='Force')
        plt.xlabel('Time')
        plt.ylabel('Force')
        plt.legend()
        plt.show()
        plt.plot(self.t_points, self.v_points, color='blue', label='V(t)')
        plt.plot(self.t_points, self.x_points, color='Red', label='X(t)')
        plt.legend()
        plt.show()


if __name__ == '__main__':
    vibrations = Vibrations(m, K, x_adm, P, F)
    vibrations.calculate()
    print(len(vibrations.t_points))
    print(len(vibrations.x_points))
    print(len(vibrations.v_points))
    vibrations.graph()
