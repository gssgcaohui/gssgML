#!/usr/bin/ env python
# coding=utf-8
import math
'''
计算LogLoss
KL距离
KL(tctr|pctr)=tctr*log(tctr/pctr)+(1-tctr)*log((1-tctr)/(1-pctr))
KL(tctr|pctr)=-tctr*log(pctr) - (1-tctr)*log(1-pctr) + const
KL(tctr|pctr) = - click/impression * log(pctr) - (1-click/impression) *log(1-pctr) + const
'''
def calcloss(click, pctr):
    loss = 0
    for i in range(1, len(click)):
        # 过滤非法数据 无效的值
        if (pctr[i] > 1 or pctr[i] < 0):
            continue
        if click[i] == 1:
            loss += -math.log(pctr[i])
        else:
            loss += -math.log(1 - pctr[i])
    return loss / len(click)

if __name__ == "__main__":
    # 测试数据
    labels = [1, 1, 0, 1, 1, 0, 1, 0, 1]
    pctr = [0.68, 0.9, 0.8, 0.3, 0.9, 0.8, 0.5, 0.1, 0.75]
    print calcloss(labels, pctr)

# 计算auc
def calcAUC(labels,pctr):
    auc = tp = tp_pre = fp = fp_pre = 0.0
    sortData = sorted(range(len(pctr)), key=lambda i: pctr[i], reverse=True)

    last_value = pctr[sortData[0]]
    for i in range(len(labels)):
        if labels[sortData[i]] == 1:
            tp += 1
        else:
            fp += 1
        if last_value != pctr[sortData[i]]:
            # （上底+下底) * 高 / 2
            auc += (tp + tp_pre) * (fp - fp_pre) / 2.0
            tp_pre = tp
            fp_pre = fp
            last_value = pctr[sortData[i]]
    auc += (tp + tp_pre) * (fp - fp_pre) / 2.0
    # x * F = FP，y * T = TP
    # 这里为啥要除以tp*fp呢，这里的计算公式用的是tp 和 fp  ，而真正画的AUC曲线，横轴和纵轴是tp rate 和fp rate,
    # 真实的计算公式是这种：(tp*fp)S=(x2−x1)∗(y2+y1)/2=(x2−x1)∗y1+0.5∗(x2−x1)∗(y2−y1)
    #因为 x*F=FP，y*T=TP ，所以 再除以tp*fp 就得到真正的答案了
    return auc / (tp * fp)


if __name__ == "__main__":
    # 测试数据
    # labels = [1, 1, 0, 1, 1, 0, 1, 0, 1]
    # pctr = [0.68, 0.9, 0.8, 0.3, 0.9, 0.8, 0.5, 0.1, 0.75]
    labels = [1, 1, 0, 1]
    pctr = [0.5, 0.25, 0.5, 0.3]
    # print calcloss(labels, pctr)
    print '----------------------------------'
    print calcAUC(labels, pctr)
