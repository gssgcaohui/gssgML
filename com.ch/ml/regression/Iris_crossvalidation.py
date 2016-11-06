#!/usr/bin/python env
# coding:utf-8

import csv
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import cross_validation


def iris_type(s):
    it = {'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2}
    return it[s]


if __name__ == "__main__":
    path = 'data/4.iris.data'

    # 路径，浮点型数据，逗号分隔，第4列使用函数iris_type单独处理
    data = np.loadtxt(path, dtype=float, delimiter=',', converters={4: iris_type})

    # print data
    # 将数据的0到3列组成x，第4列得到y
    x, y = np.split(data, (4,), axis=1)
    # print 'x=\n',x
    # print 'y=\n',y

    # 为了可视化，仅使用前两列特征
    x = x[:, :2]

    # print x
    # print y

    # 特征的简单处理
    X = preprocessing.scale(x)  # 转换成正态分布（0,1）

    # 3. 训练集和测试集的划分
    X_train, X_test, y_train, y_test =cross_validation.train_test_split(X, y, test_size=0.2)

    #  交叉验证
    Cs = [0.01, 0.1, 0.2, 1]
    best_c = 0.01
    best_score = 0
    for c in Cs:  # 对于每一个hyperameter
        logreg = LogisticRegression(fit_intercept=True,C=c,
penalty='l2', tol=0.0001)  # Logistic回归模型
        # score =
        # if best_score < score:
        #     best_c = c


    # logreg.fit(x, y.ravel())  # 根据数据[x,y]，计算回归参数

    # 5. 用选择的参数对模型做训练
    # 定义模型
    lr = LogisticRegression(fit_intercept=True, C=best_c, penalty='l2',
                            tol=0.0001)
    # 在训练集上做模型训练
    lr.fit(X_train, y_train.ravel())
    # 6. 在测试集上计算准确率
    predicted_labels = lr.predict(X_test)

    print X_test
    print  predicted_labels
    #
    #
    #
    # y_hat = logreg.predict(x_test)  # 预测值
    # y_hat = y_hat.reshape(x1.shape)  # 使之与输入的形状相同
    # plt.pcolormesh(x1, x2, y_hat, cmap=plt.cm.Spectral,
    #                alpha=0.6)  # 预测值的显示Paired/Spectral/coolwarm/summer/spring/OrRd/Oranges
    # #  上面画好了网格，下面开始把点也画进去 c = y  用y的类别作为颜色划分  edgecolors 圆圈的颜色，k是黑色   s是圆圈的半径的平方大小
    # plt.scatter(x[:, 0], x[:, 1], c=y, edgecolors='k',s=50, cmap=plt.cm.prism)  # 样本的显示
    # plt.xlabel('Sepal length')
    # plt.ylabel('Sepal width')
    # plt.xlim(x1_min, x1_max)
    # plt.ylim(x2_min, x2_max)
    # plt.grid()
    # # plt.savefig("1.png")
    # plt.show()
    #
    # # 训练集上的预测结果
    # y_hat = logreg.predict(x)
    # y = y.reshape(-1)  # 此转置仅仅为了print时能够集中显示
    # print y_hat.shape  # 不妨显示下y_hat的形状
    # print y.shape
    # result = (y_hat == y)  # True则预测正确，False则预测错误
    # print y_hat
    # print y
    # print result
    # c = np.count_nonzero(result)  # 统计预测正确的个数
    # print c
    # print 'Accuracy: %.2f%%' % (100 * float(c) / float(len(result)))
