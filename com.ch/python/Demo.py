#!/usr/bin/python env
# coding:utf-8

import csv
import numpy as np
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import time
from scipy.optimize import leastsq
import scipy.optimize as opt
import scipy
import matplotlib.pyplot as plot
from scipy.stats import norm, poisson
from scipy.interpolate import BarycentricInterpolator
# from scipy.interpolate import CubicSpline
import math


def residual(t, x, y):
    return y - (t[0] * x ** 2 + t[1] * x + t[2])


def residual2(t, x, y):
    print t[0], t[1]
    return y - t[0] * np.sin(t[1] * x)


# x ** x        x > 0
# (-x) ** (-x)  x <0
def f(x):
    y = np.ones_like(x)
    i = x > 0
    y[i] = np.power(x[i], x[i])
    i = x < 0
    y[i] = np.power(-x[i], -x[i])
    return y


if __name__ == "__main__":
    # [[ 0  1  2  3  4  5]
    #  [10 11 12 13 14 15]
    #  [20 21 22 23 24 25]
    #  [30 31 32 33 34 35]
    #  [40 41 42 43 44 45]
    #  [50 51 52 53 54 55]]
    # a = np.arange(0, 60, 10).reshape((-1, 1)) + np.arange(6)
    # print a

    # L = [1, 2, 3, 4, 5]
    # a = np.array(L)
    # print a
    # print type(a)


    # 5.绘图
    # 5.1 绘制正态分布概率密度函数
    # mu = 2
    # sigma = 32
    # x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 50)
    # y = np.exp(-(x - mu) ** 2 / (2 * sigma ** 2)) / (math.sqrt(2 * math.pi) * sigma)
    # # plot.plot(x, y, 'ro-', linewidth=2)
    # plot.plot(x, y, 'r-', x, y, 'go', linewidth=2, markersize=8)
    # plot.grid(True)
    # plot.show()

    # 5.3 x ^ x
    # x = np.linspace(-1.3, 1.3, 101) # 101 保证是个尖
    # y = f(x)
    # plot.plot(x, y, 'g-', label='x^x', linewidth=2)
    # plot.grid()
    # plot.legend(loc='upper left')
    # plot.show()


    # # 5.4 胸型线
    # x = np.arange(1, 0, -0.001)
    # y = (-3 * x * np.log(x) + np.exp(-(40 * (x - 1 / np.e)) ** 4) / 25) / 2
    # plot.figure(figsize=(5, 7))  # 指定宽高
    # plot.plot(y, x, 'r-', linewidth=2)  # 此处x y 换位置
    # plot.grid(True)
    # plot.show()

    # # 5.5 心形线
    # t = np.linspace(0, 7, 100)  # 7 是2 π
    # x = 16 * np.sin(t) ** 3
    # y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
    # plot.plot(x, y, 'r-', linewidth=2)
    # plot.grid(True)
    # plot.show()

    # # 5.6 渐开线
    # t = np.linspace(0, 50, num=1000)
    # x = t*np.sin(t) + np.cos(t)
    # y = np.sin(t) - t*np.cos(t)
    # plot.plot(x, y, 'r-', linewidth=2)
    # plot.grid()
    # plot.show()


    ## Bar
    matplotlib.rcParams['font.sans-serif'] = [u'SimHei']  # 黑体 FangSong/KaiTi  控制字体显示
    matplotlib.rcParams['axes.unicode_minus'] = False  # 显示- 负号
    # x = np.arange(0, 10, 0.1)
    # y = np.sin(x)
    # plot.bar(x, y, width=0.04, linewidth=0.2)
    # plot.plot(x, y, 'r--', linewidth=2)
    # plot.title(u'Sin曲线')
    # plot.xlabel('X')
    # plot.ylabel('Y')
    # plot.grid()
    # plot.show()


    # # 6. 概率分布
    # # 6.1 均匀分布
    # x = np.random.rand(10000)
    # t = np.arange(len(x))
    # # plot.hist(x, 50, color='m', alpha=0.5)
    # plot.plot(t, x, 'r--', label=u'均匀分布')
    # plot.legend(loc='upper left')
    # plot.grid()
    # plot.show()

    # # 6.2 验证中心极限定理
    # t = 10000
    # a = np.zeros(1000)
    # for i in range(t):
    #     a += np.random.uniform(-5, 5, 1000)
    # a /= t
    # plot.hist(a, bins=30, color='g', alpha=0.75)
    # plot.grid()
    # plot.show()

    # # 6.3 Poisson分布
    x = np.random.poisson(lam=5, size=10000)
    # print x
    pillar = 15
    a = plot.hist(x, bins=pillar, normed=True, range=[0, pillar], color='g', alpha=0.5)
    plot.grid()
    # plot.show()
    print a
    # 加上折线
    b=a[0]
    plot.plot(np.arange(pillar),b,'r--',linewidth=2)
    plot.show()
    print a[0].sum()

    # # 6.4 直方图的使用
    # mu = 2
    # sigma = 3
    # data = mu + sigma * np.random.randn(1000)
    # h = plot.hist(data, 30, normed=1, color='#a0a0ff')
    # x = h[1]
    # y = norm.pdf(x, loc=mu, scale=sigma)
    # plot.plot(x, y, 'r--', x, y, 'ro', linewidth=2, markersize=4)
    # plot.grid()
    # plot.show()

    # # 6.5 插值
    # rv = poisson(5)
    # x1 = a[1]
    # y1 = rv.pmf(x1)
    # itp = BarycentricInterpolator(x1, y1)  # 重心插值
    # x2 = np.linspace(x.min(), x.max(), 50)
    # y2 = itp(x2)
    # cs = scipy.interpolate.CubicSpline(x1, y1)       # 三次样条插值
    # plot.plot(x2, cs(x2), 'm--', linewidth=5, label='CubicSpine')           # 三次样条插值
    # plot.plot(x2, y2, 'g-', linewidth=3, label='BarycentricInterpolator')   # 重心插值
    # plot.plot(x1, y1, 'r-', linewidth=1, label='Actural Value')             # 原始值
    # plot.legend(loc='upper right')
    # plot.grid()
    # plot.show()

    # 7. 绘制三维图像
    # x, y = np.ogrid[-3:3:100j, -3:3:100j]
    # # u = np.linspace(-3, 3, 101)
    # # x, y = np.meshgrid(u, u)
    # z = x*y*np.exp(-(x**2 + y**2)/2) / math.sqrt(2*math.pi)
    # # z = x*y*np.exp(-(x**2 + y**2)/2) / math.sqrt(2*math.pi)
    # fig = plot.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # # ax.plot_surface(x, y, z, rstride=5, cstride=5, cmap=cm.coolwarm, linewidth=0.1)  #
    # ax.plot_surface(x, y, z, rstride=3, cstride=3, cmap=cm.Accent, linewidth=0.5)
    # plot.show()
    # # cmaps = [('Perceptually Uniform Sequential',
    # #           ['viridis', 'inferno', 'plasma', 'magma']),
    # #          ('Sequential', ['Blues', 'BuGn', 'BuPu',
    # #                          'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd',
    # #                          'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu',
    # #                          'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd']),
    # #          ('Sequential (2)', ['afmhot', 'autumn', 'bone', 'cool',
    # #                              'copper', 'gist_heat', 'gray', 'hot',
    # #                              'pink', 'spring', 'summer', 'winter']),
    # #          ('Diverging', ['BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr',
    # #                         'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral',
    # #                         'seismic']),
    # #          ('Qualitative', ['Accent', 'Dark2', 'Paired', 'Pastel1',
    # #                           'Pastel2', 'Set1', 'Set2', 'Set3']),
    # #          ('Miscellaneous', ['gist_earth', 'terrain', 'ocean', 'gist_stern',
    # #                             'brg', 'CMRmap', 'cubehelix',
    # #                             'gnuplot', 'gnuplot2', 'gist_ncar',
    # #                             'nipy_spectral', 'jet', 'rainbow',
    # #                             'gist_rainbow', 'hsv', 'flag', 'prism'])]

    # # # 8.1 scipy
    # # 线性回归例1
    # x = np.linspace(-2, 2, 50)
    # A, B, C = 2, 3, -1
    # y = (A * x ** 2 + B * x + C) + np.random.rand(len(x))*0.75
    #
    # t = leastsq(residual, [0, 0, 0], args=(x, y))zw
    # theta = t[0]
    # print '真实值：', A, B, C
    # print '预测值：', theta
    # y_hat = theta[0] * x ** 2 + theta[1] * x + theta[2]
    # plot.plot(x, y, 'r-', linewidth=2, label='Actual')
    # plot.plot(x, y_hat, 'g-', linewidth=2, label='Predict')
    # plot.legend(loc='upper left')
    # plot.grid()
    # plot.show()

    # # 线性回归例2
    # x = np.linspace(0, 5, 100)
    # A = 5
    # w = 1.5
    # y = A * np.sin(w*x) + np.random.rand(len(x)) - 0.5
    #
    # t = leastsq(residual2, [3, 1], args=(x, y))
    # theta = t[0]
    # print '真实值：', A, w
    # print '预测值：', theta
    # y_hat = theta[0] * np.sin(theta[1] * x)
    # plot.plot(x, y, 'r-', linewidth=2, label='Actual')
    # plot.plot(x, y_hat, 'g-', linewidth=2, label='Predict')
    # plot.legend(loc='lower left')
    # plot.grid()
    # plot.show()

    # # 8.2 使用scipy计算函数极值
    # a = opt.fmin(f, 1)
    # b = opt.fmin_cg(f, 1)
    # c = opt.fmin_bfgs(f, 1)
    # print a, 1/a, np.e
    # print b
    # print c
