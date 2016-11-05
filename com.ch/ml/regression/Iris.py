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


def iris_type(s):
    it = {'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2}
    return it[s]


if __name__ == "__main__":
    path = 'data/4.iris.data'

    # 手动读取数据
    # f = file(path)
    # x = []
    # y = []
    # for d in f:
    #     print d
    #     d = d.strip()
    #     if d:
    #         d=d.split(',')
    #         y.append(d[-1])
    #         x.append(map(float, d[:-1]))
    #     else:
    #         print "err:"+d
    # print '原始数据x:\n',x
    # print '原始数据y:\n',y
    # x=np.array(x)
    # print 'Numpy格式X:\n',x
    # y=np.array(y)
    # print 'Numpy格式Y-1:\n',y
    # y[y=='Iris-setosa'] = 0
    # y[y=='Iris-versicolor'] = 1
    # y[y=='Iris-virginica'] = 2
    # print 'Numpy格式Y-2:\n',y
    # y=y.astype(dtype=np.int)
    # print 'Numpy格式Y-3:\n',y

    # 使用sklearn的数据预处理
    # df = pd.read_csv(path)
    # x = df.values[:, :-1]  # 取所有行，列去掉最后一列
    # y = df.values[:, -1]  # 所有行，最后一列
    # print "x=\n", x
    # # print "y=\n", y
    # # 调库转换
    # le = preprocessing.LabelEncoder()  # 把标记进行编码
    # le.fit(['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'])
    # print le.classes_
    # y = le.transform(y)
    # print "Last Version,y=\n", y


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

    # 标准化  均值变为0 ，方差为1
    x = StandardScaler().fit_transform(x)
    logreg = LogisticRegression()  # Logistic回归模型
    logreg.fit(x, y.ravel())  # 根据数据[x,y]，计算回归参数

    # 上面三行代码等价于下面这两行   等价形式
    # logreg = Pipeline([('sc',StandardScaler(),('clf',LogisticRegression()))])
    # logreg.fit(x,y.ravel()) # ravel 类似于reshape

    # 画图
    N, M = 500, 500  # 横纵各采样多少个值
    x1_min, x1_max = x[:, 0].min(), x[:, 0].max()  # 第0列的范围
    x2_min, x2_max = x[:, 1].min(), x[:, 1].max()  # 第1列的范围
    t1 = np.linspace(x1_min, x1_max, N)
    t2 = np.linspace(x2_min, x2_max, M)
    x1, x2 = np.meshgrid(t1, t2)  # 生成网格采样点
    x_test = np.stack((x1.flat, x2.flat), axis=1)  # 测试点

    # # 无意义，只是为了凑另外两个维度
    # x3 = np.ones(x1.size) * np.average(x[:, 2])
    # x4 = np.ones(x1.size) * np.average(x[:, 3])
    # x_test = np.stack((x1.flat, x2.flat, x3, x4), axis=1)  # 测试点

    y_hat = logreg.predict(x_test)  # 预测值
    y_hat = y_hat.reshape(x1.shape)  # 使之与输入的形状相同
    plt.pcolormesh(x1, x2, y_hat, cmap=plt.cm.Spectral,
                   alpha=0.6)  # 预测值的显示Paired/Spectral/coolwarm/summer/spring/OrRd/Oranges
    #  上面画好了网格，下面开始把点也画进去 c = y  用y的类别作为颜色划分  edgecolors 圆圈的颜色，k是黑色   s是圆圈的半径的平方大小
    plt.scatter(x[:, 0], x[:, 1], c=y, edgecolors='k',s=50, cmap=plt.cm.prism)  # 样本的显示
    plt.xlabel('Sepal length')
    plt.ylabel('Sepal width')
    plt.xlim(x1_min, x1_max)
    plt.ylim(x2_min, x2_max)
    plt.grid()
    # plt.savefig("1.png")
    plt.show()

    # 训练集上的预测结果
    y_hat = logreg.predict(x)
    y = y.reshape(-1)  # 此转置仅仅为了print时能够集中显示
    print y_hat.shape  # 不妨显示下y_hat的形状
    print y.shape
    result = (y_hat == y)  # True则预测正确，False则预测错误
    print y_hat
    print y
    print result
    c = np.count_nonzero(result)  # 统计预测正确的个数
    print c
    print 'Accuracy: %.2f%%' % (100 * float(c) / float(len(result)))
