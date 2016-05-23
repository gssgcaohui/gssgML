#!/usr/bin/ env python
# coding=utf-8
import math


# 公式
# KL(tctr || pctr)=1/impression * [-click*log(pctr)-(impression-click)*log(1-pctr)+const]


# 计算LogLoss
def calcloss(loss, click, pctr):
    for i in range(1, len(click)):
        if (pctr[i] > 1 or pctr[i] < 0):  # 过滤非法数据
            continue
        if click[i] == 1:
            loss += -math.log(pctr[i])
        else:
            loss += -math.log(1 - pctr[i])
    return loss / len(click)


# 计算auc
def calcAUC(data):
    auc = tp = tp_pre = fp = fp_pre = 0
    last_value = data[0]['pctr']
    for i in range(0, len(data) - 1):
        if data[i]['label'] == 1:
            tp += 1
        else:
            fp += 1
        if last_value != data[i]['pctr']:
            auc = (tp + tp_pre) * (fp - fp_pre) / 2.0
            tp_pre = fp_pre = fp
            last_value = data[i]['pctr']
        auc += (tp + tp_pre) * (fp - fp_pre) / 2.0

    return auc, tp, fp, auc / (tp * fp)


if __name__ == "__main__":
    loss = 0
    clickDate = [0, 1, 1, 1, 0, 0, 1]
    pctr = [0.005, 0.01, 0.9, 0.03, 0.109, 0.32, 0.73]
    print calcloss(loss, clickDate, pctr)
    print '----------------------------------'

    # true_data = [0, 1, 1, 1, 0, 0, 1]  # 真实值
    # pctr_data = [1, 0, 1, 1, 0, 1, 1]  # 预测值
    # data = [{'label': 1, 'pctr': 0.1}, {'label': 0, 'pctr': 0.2}, {'label': 0, 'pctr': 0.3}, {'label': 1, 'pctr': 0.3},
    #        {'label': 0, 'pctr': 0.5}, {'label': 1, 'pctr': 0.9}, {'label': 1, 'pctr': 1}]
    data = [{'label': 1, 'pctr': 1}, {'label': 1, 'pctr': 0.9}, {'label': 0, 'pctr': 0.5}, {'label': 0, 'pctr': 0.3},
            {'label': 1, 'pctr': 0.3}, {'label': 0, 'pctr': 0.2}, {'label': 1, 'pctr': 0.1}
            ]
    print calcAUC(data)
