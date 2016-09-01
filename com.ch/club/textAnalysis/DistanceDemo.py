#!/usr/bin/env python
# coding:utf-8


# 距离计算算法
'''
二维：ρ = sqrt( (x1-x2)^2+(y1-y2)^2 )
三维：ρ = sqrt( (x1-x2)^2+(y1-y2)^2+(z1-z2)^2 )
n维欧氏空间是一个点集,它的每个点 X 可以表示为 (x[1]，x[2]，…，x[n]) ，其中 x[i](i = 1，2，…，n) 是实数，称为 X 的第i个坐标，
两个点 A = (a[1]，a[2]，…，a[n]) 和 B = (b[1]，b[2]，…，b[n]) 之间的距离 ρ(A，B) 定义为下面的公式。
ρ(A，B) =sqrt [ ∑( a[i] - b[i] )^2 ] (i = 1，2，…，n)
'''
# 测试 zip
x = [1, 2, 3]
y = [4, 5, 6]
z = [7, 8, 9]
print zip(x, y, z)  # [(1, 4, 7), (2, 5, 8), (3, 6, 9)]


# 欧式距离
def euclideanDist(vector1, vector2):
    d = 0
    for a, b in zip(vector1, vector2):
        d += (a - b) ** 2
    return d ** 0.5  # 平方根


# 测试 二维
v1 = (1, 1)
v2 = (-1, -1)

# 测试 3维
v3 = (1, 1, 1)
v4 = (-1, -1, -1)
print euclideanDist(v1, v2)
print euclideanDist(v3, v4)

# 欧式距离 demo2
from numpy import *

vector1 = mat([1, 1])
vector2 = mat([-1, -1])
print sqrt((vector1 - vector2) * ((vector1 - vector2).T))

import scipy.spatial.distance as dist  # 导入scipy距离公式

'''使用Matlab计算欧氏距离
Matlab计算距离主要使用pdist函数。若X是一个M×N的矩阵，则pdist(X)将X矩阵M行的每一行作为一个N维向量，然后计算这M个向量两两间的距离
'''
# 计算向量(0,0)、(1,0)、(0,2)两两间的欧式距离
X = [(0, 0),
     (1, 0),
     (0, 2)]
D = dist.pdist(X, 'euclidean')
print D

X = [(1.0, 1.2),
     (1.4, 1.1),
     (1.1, 1.1)]
D = dist.pdist(X, 'euclidean')
print D   # [ 0.41231056  0.14142136  0.3       ]
# 第一个和第二个，第一个和第3个， 第二个和第3个




# 余弦相似度
def cos(vector1, vector2):
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return None
    else:
        return dot_product / ((normA * normB) ** 0.5)


v1 = (1, 1)
v2 = (-1, -1)
v3 = (0, 1, 1)
v4 = (0, -1, 1)
print cos(v1, v2)
print cos(v3, v4)
'''
v1=(1,1)与v2=(-1,-1)是两个互为平行，从原点反方向延伸出来的两个向量，夹角显然为180度，cos 180度=-1
v3=(0,1,1)与v4=(0,-1,1)是三维坐标系上互为垂直的两个向量，cos 90度=0
这可以说明v1与v2两个向量简直就是两个不可调和的矛盾，而v3与v4则是毫无关系的两个向量
'''
# 计算(1,0)、( 1,1.732)、( -1,0)两两间的夹角余弦
X = [(1, 0), (1, 1.732), (-1, 0)]
D = 1 - dist.pdist(X, 'cosine')
print D