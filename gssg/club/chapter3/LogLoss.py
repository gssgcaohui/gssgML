#!/usr/bin/ env python
# coding=utf-8
import math


# 公式
# KL(tctr || pctr)=1/impression * [-click*log(pctr)-(impression-click)*log(1-pctr)+const]



def calcloss(loss, click, pctr):
    for i in range(1, len(click)):
        if ( pctr[i] > 1 or pctr[i] < 0 ): # 过滤非法数据
            continue
        if click[i] == 1:
            loss += -math.log(pctr[i])
        else:
            loss += -math.log(1 - pctr[i])
    return loss / len(click)

if __name__ == "__main__":
    loss = 0
    clickDate = [0, 1, 1, 1, 0, 0, 1]
    pctr = [0.005, 0.01, 0.9, 0.03, 0.109, 0.32, 0.73]
    print calcloss(loss, clickDate, pctr)

