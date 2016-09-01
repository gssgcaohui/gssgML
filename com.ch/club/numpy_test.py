#!/usr/bin/ env python
# coding:utf-8

import numpy as np
import matplotlib.pyplot as plot

# 胸型图
x = np.arange(1,0,-0.001)
# y = 3*x *np.log(x) +np.exp(-(36*(x-1/np.e))**4)/25
y = (-3*x *np.log(x) +np.exp(-(40*(x-1/np.e))**4)/25)
plot.plot(y,x,'r-',linewidth =2)
plot.grid(True)
plot.show()

# 心型图
# t = np.linspace(0,7,100)
# x = 16* np.sin(t) ** 3
# y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 *np.cos(3*t) - np.cos(4*t)
# plot.plot(x,y,'r-',linewidth =2)
# plot.grid(True)
# plot.show()