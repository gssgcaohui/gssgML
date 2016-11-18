#!/usr/bin/python
# coding:utf-8

import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression

'''
    LinearRegression
'''
if __name__ == "__main__":
    path = 'data/4.Advertising.csv'

    # 手动读取数据
    # f = file(path)
    # x = []
    # y = []
    # for i, d in enumerate(f):
    #     if i == 0:
    #         continue
    #     d = d.strip()
    #     if not d:
    #         continue
    #     d = map(float, d.split(','))
    #     x.append(d[1:-1])
    #     y.append(d[-1])
    # print x
    # print y
    # x = np.array(x)
    # x = np.array(y)

    # Python 自带库读文件
    # f=file(path,'rb')
    # print f
    # d=csv.reader(f)
    # for line in d:
    #     print line
    # f.close()

    # numpy读文件
    # p = np.loadtxt(path, delimiter=',', skiprows=1)
    # print p

    # pandas 读文件
    data = pd.read_csv(path)
    x = data[['TV', 'Radio', 'Newspaper']]
    y = data[['Sales']]
    print x
    print y

    # 绘制1  第三个参数是颜色和样式
    plt.plot(data['TV'], y, 'ro', label='TV')
    plt.plot(data['Radio'], y, 'g^', label='Radio')
    plt.plot(data['Newspaper'], y, 'b*', label='Newspaer')
    plt.legend(loc='lower right')
    plt.grid()
    plt.show()

    # 绘制2 单独展示
    plt.figure(figsize=(9, 12)) #  高 宽
    plt.subplot(311) # 3行 1列 第一行
    plt.plot(data['TV'], y, 'ro')
    plt.title('TV')
    plt.grid()
    plt.subplot(312)
    plt.plot(data['Radio'], y, 'g^')
    plt.title('Radio')
    plt.grid()
    plt.subplot(313)
    plt.plot(data['Newspaper'], y, 'b*')
    plt.title('Newspaper')
    plt.grid()
    plt.tight_layout() # 样式紧一下
    plt.show()

    # 调用sklearn中交叉验证的包  默认train 75% test 25%
    # x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)
    # # print x_train, y_train
    # linreg = LinearRegression()
    # model = linreg.fit(x_train, y_train)
    # # print x_train.shape
    # # print x_test.shape
    # print model
    # print linreg.coef_  # 系数  y= aX1 + bX2 + cX3 + r
    # print linreg.intercept_  # 误差值，就是r
    #
    # # 均方误差
    # y_hat = linreg.predict(x_test)
    # mse = np.average((y_hat - y_test) ** 2)  # Mean Squared Error
    # rmse = np.sqrt(mse)  # Root Mean Squared Error
    # print mse, rmse

    # 画出来 预测值和真实值
    # t = np.arange(len(x_test))
    # plt.plot(t, y_test, 'r-', linewidth=2, label='Test')
    # plt.plot(t, y_hat, 'g-', linewidth=2, label='Predict')
    # plt.legend(loc='upper right')
    # plt.grid()
    # plt.show()
