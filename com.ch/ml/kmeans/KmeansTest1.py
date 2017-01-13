#!/usr/bin/python env
# coding:utf-8

from sklearn.datasets import make_blobs
from matplotlib import pyplot

if __name__ == "__main__":
    data, label = make_blobs(n_samples=100, n_features=2, centers=5)
    # 绘制样本显示
    pyplot.scatter(data[:, 0], data[:, 1], c=label)
    pyplot.show()
