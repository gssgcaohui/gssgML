#!/usr/bin/ env python
# encoding:utf-8
import sys
import math


# 计算MAP
def MAP(item_list):
    v = 0.0
    click = 0 # 总的点击次数
    for i in range(len(item_list)):
        if (item_list[i][1] > 0):
            click += 1
            v += click / (i + 1)
    return v / click

# groupByKey的操作
def groupBy(data):
    if len(data) == 0:
        return data
    # 按sessionId(组)排序
    sorted_data = sorted(data, key=lambda x: x[0])
    last_value = sorted_data[0][0]
    ret = []
    l = []
    for t in sorted_data:
        if t[0] == last_value:
            # 同一组数据，添加到list中
            l.append(t)
        else:
            '''
            开始处理一组新的数据，先把上一组数据l添加到ret集合中
            然后把新的值赋给l集合，并修改last_value
            '''
            ret.append(l)
            l = [t]
            last_value = t[0]
    ret.append(l)
    '''ret集合的值示例
       [[('12', 0.0, 0.8433)],
        [('13', 0.0, 0.8433)],
        [('14', 0.0, 0.6433), ('14', 1.0, 0.1433)]]
    '''
    return ret


def calculateMAP(data):
    m = 0.0
    for d in data:
        # 按预测的值降序排序
        d_sorted = sorted(d, key=lambda x: x[2], reverse=True)
        m += MAP(d_sorted)
    return m / len(data)


def readData(file_name):
    f = open(file_name, 'r')
    # 数据格式：12,0,0.89   第一列为sessionId,第二列是lable值，第三列是预测值
    data = []
    for line in f:
        seg = line.strip().split(",")
        data.append((seg[0], float(seg[1]), float(seg[2])))  # 三元组
    return data


if __name__ == "__main__":
    # data = readData(sys.argv[1])
    data = readData("mapdata.txt")
    group_data = groupBy(data)
    print(calculateMAP(group_data))
