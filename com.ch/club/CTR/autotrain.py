#!/usr/bin/ env python
# coding=utf-8

import os,commands,sys

auc_pctr = 0
auc_testpctr = 0

#os.popen('python train.py')
if len(sys.argv)==1:
  result=commands.getstatusoutput('python train.py')
#  print "train.py"
elif sys.argv[1] == "ad":
  result=commands.getstatusoutput('python train_adagrad.py')
#  print "train_adagrad.py"
elif sys.argv[1] == "ftrl":
  result=commands.getstatusoutput('python train_ftrl.py')
elif sys.argv[1] == "bpr":
  result=commands.getstatusoutput('python train_bpr.py')
else:
  result=commands.getstatusoutput('python train.py')

print result[1]
if result[0] == 0:
  # 计算auc
  pctr = commands.getstatusoutput('python auc.py pctr')
#  testpctr = commands.getstatusoutput('python auc.py test_pctr')
  if pctr[0]== 0:
    auc_pctr = pctr[1]
#  if testpctr[0] == 0:
#    auc_testpctr = testpctr[1]

# os.system("sed -i '1i TARGET'  test_pctr.csv")

  print "auc_pctr=",auc_pctr # ,"==auc_testpctr=",auc_testpctr
else:
  print "An error occurs",result
  os._exit(1)
