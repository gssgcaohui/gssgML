#!/usr/bin/ env python
# coding=utf-8

import random
import math

alpha = 0.1

iter = 1

l2 = 0.01

file = open("train_feature", "r")

max_index = 0
for f in file:
    seg = f.strip().split("\t")
    for st in seg[1:]:
        index = int(st.split(":")[0])
        if index > max_index:
            max_index = index

weight = range(max_index + 1)
delta = range(max_index + 1)
for i in range(max_index + 1):
    weight[i] = random.uniform(-0.01, 0.01)
    delta[i] = 0

for i in range(iter):
    file = open("train_feature", "r")
    for f in file:
        seg = f.strip().split("\t")
        label = int(seg[0])
        s = 0.0
        for st in seg[1:]:
            index = int(st.split(":")[0])
            # val =float(st.split(":")[1])
            # s += weight[index] * val
            s += weight[index]

        p = 1.0 / (1 + math.exp(-s))

        g = p - label

        for st in seg[1:]:
            index = int(st.split(":")[0])
            delta[index] += g * g
            weight[index] -= alpha * (g + l2 * weight[index]) / math.sqrt(1 + delta[index])

file = open("validate_feature", "r")
toWrite = open("pctr", "w+")
c = 0
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
