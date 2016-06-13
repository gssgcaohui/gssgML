#!/usr/bin/ env python
# coding=utf-8
import math
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
def calcAUC(labels,pctr):
    auc = tp = tp_pre = fp = fp_pre = 0.0
    sortdata = sorted(range(len(pctr)), key=lambda i: pctr[i], reverse=True)

    last_value = pctr[sortdata[0]]
    for i in range(len(labels)):
        if labels[sortdata[i]] == 1:
            tp += 1
        else:
            fp += 1
        if last_value != pctr[sortdata[i]]:
            auc += (tp + tp_pre) * (fp - fp_pre) / 2.0
            tp_pre = tp
            fp_pre = fp
            last_value = pctr[sortdata[i]]
        auc += (tp + tp_pre) * (fp - fp_pre) / 2.0
    return auc, tp, fp, auc / (tp * fp)


if __name__ == "__main__":
    loss = 0
    # 测试数据
    labels = [1, 1, 0, 1, 1, 0, 1, 0, 1]
    pctr = [0.68, 0.9, 0.8, 0.3, 0.9, 0.8, 0.5, 0.1, 0.75]
    print calcloss(loss, labels, pctr)
    print '----------------------------------'
    print calcAUC(labels,pctr)
