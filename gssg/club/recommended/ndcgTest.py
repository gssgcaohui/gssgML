#!/usr/bin/ env python
import sys
import math


def dcg(item_list):
    v = 0.0
    for i in range(len(item_list)):
            v += (math.pow(2,item_list[i][1])-1) / math.log(i+2,2)
    return v


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


def calculateNdcg(data):
    ndcg = 0.0
    for d in data:
        d_sorted1 = sorted(d, key=lambda x: x[1], reverse=True)
        d_sorted2 = sorted(d, key=lambda x: x[2], reverse=True)
        ndcg += dcg(d_sorted2)/dcg(d_sorted1)
    return ndcg / len(data)


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
    print(calculateNdcg(group_data))
