# -*- coding: utf-8 -*-
# auc示例代码
def auc(true_labels, pred_labels):
    """
		 计算AUC
		参数
        -----
        true_labels: array-like
			真实值
        pred_labels: array-like
			预测值
		返回
        -----
            auc_score： float
				AUC值
		示例
        -----
        >>> true_labels = [1, 1, 0, 0]
        >>> pred_labels = [0.1, 0.4, 0.35, 0.8]
        >>> auc(true_labels, pred_labels) 
    """
    #对pred_labels进行排序
    pred_sorted = sorted(xrange(len(pred_labels)), key=lambda i: pred_labels[i],
                      reverse=True)
    auc_score = 0.0
    tp = 0.0
    tp_pre = 0.0
    fp = 0.0
    fp_pre = 0.0
    last_pred = pred_labels[pred_sorted[0]] 
    
    for i in xrange(len(pred_labels)):
        
        if true_labels[pred_sorted[i]] == 1:
            tp = tp + 1
        else:
            fp = fp + 1
        
        if last_pred != pred_labels[pred_sorted[i]]: 
            # 计算梯形面积，即(下底+上底) * 高  / 2，然后再叠加
            auc_score += (tp+tp_pre) * (fp-fp_pre) / 2.0        
            tp_pre = tp
            fp_pre = fp
            last_pred = pred_labels[pred_sorted[i]]
        
    auc_score += (tp+tp_pre) * (fp-fp_pre) / 2.0
    auc_score = auc_score / (tp * fp)
    return auc_score