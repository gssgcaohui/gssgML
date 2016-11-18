#!/usr/bin/python env
# coding:utf-8
import numpy as np
import random
import matplotlib.pyplot as plt
import math
from PIL import Image

'''
奇异值分解

'''


def restore1(sigma, u, v, K):  # 奇异值 左特征向量  右特征向量
    m = len(u)
    n = len(v[0])
    a = np.zeros((m, n))
    for k in range(K + 1):
        uk = u[:, k].reshape(m, 1)
        vk = v[k].reshape(1, n)
        a += sigma[k] * np.dot(uk, vk)
    a[a < 0] = 0
    a[a > 255] = 255
    # a.clip(0, 255)
    return np.rint(a).astype('uint8')


def restore2(sigma, u, v, K):  # 奇异值 左特征向量  右特征向量
    m = len(u)
    n = len(v[0])
    a = np.zeros((m, n))
    for k in range(K + 1):
        for i in range(m):
            a[i] += sigma[k] * u[i][k] * v[k]
    a[a < 0] = 0
    a[a > 255] = 255
    Image.fromarray(a.astype('uint8')).save("svd2_" + str(K) + ".png")


if __name__ == "__main__":
    A = Image.open("image/me.jpeg", 'r')
    a = np.array(A)
    K = 100
    for k in range(K):
        print k
        u, sigma, v = np.linalg.svd(a[:, :, 0])
        R = restore1(sigma, u, v, k)

        u, sigma, v = np.linalg.svd(a[:, :, 1])
        G = restore1(sigma, u, v, k)

        u, sigma, v = np.linalg.svd(a[:, :, 0])
        B = restore1(sigma, u, v, k)

        I = np.stack((R, G, B), 2)
        Image.fromarray(I).save(".\\test\\svd_" + str(k) + ".png")
