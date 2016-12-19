#!/usr/bin/ env python
# coding=utf-8
# sgd训练

import random
import math

# 步长
alpha = 0.1

# 迭代轮次
iter = 1

# 正则项
l2 = 1

file = open("train_feature", "r")

max_index = 0
# 遍历出特征向量的维度,拿到一个最大值
for f in file:
    seg = f.strip().split("\t")
    for st in seg[1:]:
        index = int(st.split(":")[0])
        if index > max_index:
            max_index = index

# 把上述值都映射为-0.01到0.01之间的一个值
weight = range(max_index + 1)
# adagrad
# delta = range(max_index + 1)

for i in range(max_index + 1):
    weight[i] = random.uniform(-0.01, 0.01)

# 训练的次数 
for i in range(iter):
    file = open("train_feature", "r")
    # 对每条数据进行处理
    for f in file:
        seg = f.strip().split("\t")
        label = int(seg[0])
        s = 0.0
        for st in seg[1:]:
            index = int(st.split(":")[0])
            # 随机梯度下降，这里我们设置的val值都是1，可以省去不写
            # 此处计算w*x
            # val =float(st.split(":")[1])
            # s += weight[index] * val
            s += weight[index]
        p = 1.0 / (1 + math.exp(-s))
        # 梯度g
        g = p - label
        for st in seg[1:]:
            index = int(st.split(":")[0])
            weight[index] -= alpha * (g + l2 * weight[index])

# 生成validate的pctr,用于计算auc      
c = 0
file = open("validate_feature", "r")
toWrite = open("pctr", "w+")
for f in file:
    c += 1
    seg = f.strip().split("\t")
    s = 0.0
    for st in seg[1:]:
        index = int(st.split(":")[0])
        if index <= max_index:
            s += weight[index]
    p = 1.0 / (1 + math.exp(-s))
    s = str(c) + "," + seg[0] + "," + str(p) + "\n"
    toWrite.write(s)

toWrite.close()

# 生成test集的pctr,test_pctr是改造过的结果，添加了预测的lable列，以0.5为阈值来判断lable，并用于本地计算auc
# test_pctr.csv 只有一列，为test集的预测结果值，与test集一一对应     
c = 0
filet = open("test_feature", "r")
toWrite2 = open("test_pctr", "w+")
toWrite3 = open("test_pctr.csv", "w+")
for f in filet:
    c += 1
    seg = f.strip().split("\t")
    s2 = 0.0
    for st in seg[1:]:
        index = int(st.split(":")[0])
        if index <= max_index:
            s2 += weight[index]
    p = 1.0 / (1 + math.exp(-s2))
    label = 0
    if p > 0.5:
        label = 1
    s2 = str(c) + "," + str(label) + "," + str(p) + "\n"
    s3 = str(p) + "\n"
    toWrite2.write(s2)
    toWrite3.write(s3)

toWrite2.close()
toWrite3.close()
