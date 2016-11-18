#!/usr/bin/python
# coding:utf-8

'''
测试梯度下降里的代码
'''

import matplotlib.pyplot as plot
import numpy as np

# 函数 f(x)
def f(x):
    return 1.0 * x ** 4


# 　函数f(x)的导数
def df(x):
    return 4.0 * x ** 3


# 回溯线性搜索
def GetA_Armigo(x, d, a):
    c1 = 0.3
    now = f(x)
    nValue = f(x - a * d)

    count = 30
    # 找出一个h’(α)大于0 的
    while nValue < now:
        a *= 2
        nValue = f(x - a * d)
        count -= 1
        # print "now=", now,",df=",d, "nValue=", nValue, ",x=", x, "a=", a, ",count=", count
        if count == 0:
            break

    count = 50
    # while nValue > (now - (c1 * a * d * d)):
    while 1 > 0:
        a /= 2
        nValue = f(x - a * d)
        count -= 1
        print "count=", count, "a=", a, ",x0=", x, "x1=", x - a * d, "f(x0)=", f(x), "f(x1)=", nValue
        if count == 0:
            break

    return a


# 二次插值法
def GetA_Quad(x, d, a):
    c1 = 0.3
    now = f(x)
    nValue = f(x - a * d)

    count = 30
    while nValue < now:
        a *= 2
        nValue = f(x - a * d)
        count -= 1
        if count == 0:
            break

    count = 50
    b = 1.0
    while nValue > (now - (c1 * a * d * d)):
        b = d * a * a / (now + d * a - nValue)
        b /= 2
        if b < 0:
            a /= 2
        else:
            a = b
        nValue = f(x - a * d)
        count -= 1
        if count == 0:
            break

    return a


if __name__ == "__main__":
    # print GetA_Armigo(1.5, df(1.5), 0.08)
    # print GetA_Quad(1.5, df(1.5), 0.001)
    x = 1.5
    # a=0.01
    # d = df(1.5)
    # for i in range(100):
    #     x -= a * d
    #     print x
    xx = []
    for i in range(100):
        d = df(x)
        x -= d * 0.02
        print x
        xx.append(x)


    t = np.arange(len(xx))
    print type(xx)
    print type(t)
    # plot.hist(x, 50, color='m', alpha=0.5)
    plot.plot(t, xx, 'g.', label='value')
    # # 加上折线
    # b=a[0]
    plot.plot(t,xx,'r-',linewidth=1)
    # plot.legend(loc='upper left')
    plot.grid()
    plot.show()
