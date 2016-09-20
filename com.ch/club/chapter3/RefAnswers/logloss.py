# -*- coding: utf-8 -*-

import numpy as np
# logloss 示例代码
def logloss(true_labels, pred_labels, eps=1e-15):
    """
		 计算logloss
		参数
        -----
        true_labels: array-like
			真实值
        pred_labels: array-like
			预测值
        eps: float
            Log loss在p=0或 p=1是没有值的，所以概率p需要转换到 max(eps, min(1 - eps, p))
		返回
        -----
            log loss： float
				log loss值
		示例
        -----
        >>> true_labels = [ [1, 0], [1, 0], [0, 1]]
        >>> pred_labels = [ [.8, .2], [.7, .3], [.6, .4]]
        >>> logloss(true_labels, pred_labels) 
    """
    # 对预测值进行处理
    # 输出类似这种 分隔符是\n [[ 0.8  0.2] [ 0.7  0.3] [ 0.6  0.4]]
    pred_labels = np.clip(pred_labels, eps, 1 - eps)


    # logloss公式
    n_samples = len(true_labels)
    logloss_val = sum(true_labels * np.log(pred_labels) +
                      np.subtract(1, true_labels) * np.log(np.subtract(1, pred_labels)))
    logloss_val = -1.0 / n_samples * logloss_val
    return logloss_val
