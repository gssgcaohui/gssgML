#!/usr/bin/ env python
# coding=utf-8
# 计算auc

import sys

def auc(labels,predicted_ctr):
  # 对pctr结果进行倒排序
  i_sorted =  sorted(range(len(predicted_ctr)),key=lambda i:predicted_ctr[i],reverse=True)
  auc_temp = 0.0
  tp = 0.0
  tp_pre = 0.0
  fp = 0.0
  fp_pre = 0.0
  last_value = predicted_ctr[i_sorted[0]]
  for i in range(len(labels)):
    if labels[i_sorted[i]] > 0 :
      tp += 1
    else:
      fp += 1
    if last_value != predicted_ctr[i_sorted[i]]:
      auc_temp += (tp + tp_pre) * (fp - fp_pre) / 2.0
      tp_pre = tp
      fp_pre = fp
      last_value = predicted_ctr[i_sorted[i]]
  auc_temp += (tp + tp_pre) * (fp - fp_pre) / 2.0
  return auc_temp / ( tp * fp)  

def evaluate(ids,true_values,predict_values):
  labels = []
  predicted_ctr = []
  # 分别生成两个集合
  for i in range(len(ids)):
    labels.append(int(true_values[i]))
    predicted_ctr.append(float(predict_values[i]))
  return auc(labels,predicted_ctr)


if __name__ == "__main__":
  f = open(sys.argv[1],"r")
  ids = []
  true_values = []
  predict_values = []
  for line in f:
    seg = line.strip().split(",")
    # 三列分别为序号列，真实值lable，预测值pctr
    ids.append(seg[0])
    true_values.append(seg[1])
    predict_values.append(seg[2])
  print evaluate(ids,true_values,predict_values)
