#!/usr/bin/ env python
import sys
import math


def MAP(item_list):
    v = 0.0
    click = 0
    for i in range(len(item_list)):
        if (item_list[i][1] > 0):
            click += 1
            v += click / (i + 1)
    return v / click


def groupBy(data):
    if len(data) == 0:
        return data
    sorted_data = sorted(data, key=lambda x: x[0])
    last_value = sorted_data[0][0]
    ret = []
    l = []
    for t in sorted_data:
        if t[0] == last_value:
            l.append(t)
        else:
            ret.append(l)
            l = [t]
            last_value = t[0]
    ret.append(l)
    return ret


def calculateMAP(data):
    m = 0.0
    for d in data:
        d_sorted = sorted(d, key=lambda x: x[2], reverse=True)
        m += MAP(d_sorted)
    return m / len(data)


def readData(file_name):
    f = open(file_name, 'r')
    data = []
    for line in f:
        seg = line.strip().split(",")
        data.append(seg[0], float(seg[1]), float(seg[2]))
    return data


if __name__ == "__main__":
    data = readData(sys.argv[1])
    group_data = groupBy(data)
    print(calculateMAP(group_data))
