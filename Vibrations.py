import decimal
import time
from decimal import Decimal
import decimal as d
from typing import List

import numpy as np
import matplotlib.pyplot as plt

m = Decimal(9700)
K = Decimal(615000)
F = Decimal(850)
x_adm = Decimal(0.00125)
P = Decimal(0.7890929760279801)
c = Decimal(1)  # test value


def force_periodic(x, P, F):  # gives the value of F in x time
    normalized_x = Decimal(x) % P  # Normalize x to the range [0, P)
    if x < 0:
        return Decimal(0)
    if normalized_x < P / 10:
        return F
    else:
        return Decimal(0)


class Vibrations:
    def __init__(self, m, K, P, F, c):
        self.m = m
        self.K = K
        self.x_adm = x_adm
        self.P = P
        self.F = F
        self.c = c
        self.t_points = np.linspace(0, float(20*P), 10000) #cambiar ambos valores proporcionalmente para obtener diferentes graficos
        self.F_points = [force_periodic(xi, P, F) for xi in self.t_points]
        self.x_points: List[Decimal] = [Decimal(0)]
        self.v_points: List[Decimal] = [Decimal(0)]
        self.a_points = []

    def f(self, i):
        if i < 0:
            return 0
        if i == 0:
            return self.F / self.m
        return (self.F_points[i] - self.K * self.x_points[i] - self.c * self.v_points[i]) / self.m

    def Adams_BashfordSpeed(self, i):
        if i <= 0:
            self.v_points.append((self.P / 1000) * (3 * self.f(i - 1) - self.f(i - 2)))
        else:
            self.v_points.append(self.v_points[i - 1] + (self.P / 1000) * (3 * self.f(i - 1) - self.f(i - 2)))

    def Adam_BashfordXpos(self, i):
        if i <= 0:
            self.x_points.append((self.P / 1000) * (3 * self.v_points[i - 1] - self.v_points[i - 2]))
        else:
            self.x_points.append(self.x_points[i - 1] + (self.P / 1000) * (3 * self.v_points[i] - self.v_points[i - 1]))

    def calculate(self):
        for x in range(1, len(self.t_points)):
            self.Adams_BashfordSpeed(x)
            self.Adam_BashfordXpos(x)
        self.a_points = [self.f(i) for i in range(len(self.t_points))]

    def graph(self):
        plt.plot(self.t_points, self.F_points, label='Force')
        plt.xlabel('Time')
        plt.ylabel('Force')
        plt.legend()
        plt.show()
        plt.axhline(y=x_adm, color='red', linestyle='dashed')
        plt.axhline(y=-x_adm, color='red', linestyle='dashed')
        plt.plot(self.t_points, self.v_points, color='blue', label='V(t)', drawstyle='steps')
        plt.plot(self.t_points, self.x_points, color='Red', label='X(t)', drawstyle='steps')

        plt.legend()
        plt.show()

    def x_max(self):
        x_max: Decimal = d.Decimal(0)
        for x in self.x_points:
            if x.copy_abs() > x_max:
                x_max = x.copy_abs()
        return x_max

    def g(self):
        return self.x_max() - x_adm

    def secantMethod(self, cAnt, gAnt):
        nextC = self.c - ((self.g()) * (self.c - cAnt) / (self.g() - gAnt))
        return nextC


if __name__ == '__main__':
    cList: List[Decimal] = [Decimal(0.001), Decimal(19000)]
    i: int = 1
    while (cList[i] - cList[i - 1]).copy_abs() > 0.001 or newvibrations.x_max() > x_adm:
        vibrations = Vibrations(m, K, P, F, cList[i])
        vibrations.calculate()
        vibrations.graph()
        VibrationsAnterior = Vibrations(m, K, P, F, cList[i - 1])
        VibrationsAnterior.calculate()
        gAnterior = VibrationsAnterior.g()
        print(vibrations.x_max())
        cList.append(vibrations.secantMethod(cList[i - 1], gAnterior))
        i += 1
        newvibrations = Vibrations(m, K, P, F, cList[i])
        newvibrations.calculate()
    finalVibrations = Vibrations(m, K, P, F, cList[len(cList) - 1])
    print(cList[len(cList) - 1])
    print(cList)
    finalVibrations.calculate()
    print(f"Xmax = {finalVibrations.x_max()}  c = {finalVibrations.c}")
    finalVibrations.graph()
    print(f"xMax<xAdm ={finalVibrations.x_max() < x_adm}")
    print(f"Xmax-Xadm = {finalVibrations.x_max() - x_adm}")
