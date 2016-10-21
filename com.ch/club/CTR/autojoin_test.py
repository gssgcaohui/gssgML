#!/usr/bin/ env python
# coding=utf-8

import os,commands,sys

auc_pctr = 0
auc_testpctr = 0
flag = True

result=commands.getstatusoutput('bash join.sh test 6 queryid_tokensid.txt 1 >train1')

if result[0] != 0:
  flag = False
  sys.exit()

result=commands.getstatusoutput('bash join.sh train1 7 purchasedkeywordid_tokensid.txt 1 >train2')

if result[0] != 0:
  flag = False
  sys.exit()

result=commands.getstatusoutput('bash join.sh train2 8 titleid_tokensid.txt 1 >train3')

if result[0] != 0:
  flag = False
  sys.exit()

result=commands.getstatusoutput('bash join.sh train3 9 descriptionid_tokensid.txt 1 >train4')

if result[0] != 0:
  flag = False
  sys.exit()

result=commands.getstatusoutput('bash join.sh train4 10 userid_profile.txt 1 >train5')

if result[0] != 0:
  flag = False
  sys.exit()

result=commands.getstatusoutput("cat train5 | awk '{print \"0\"\"\t\"$0}' >test_combined")

if result[0] != 0:
  flag = False
  sys.exit()

os.system('rm -rf train1')
os.system('rm -rf train2')
os.system('rm -rf train3')
os.system('rm -rf train4')
os.system('rm -rf train5')

print "successed!"



'''if result[0] == 0:
  # 计算auc
  pctr = commands.getstatusoutput('python auc.py pctr')
  testpctr = commands.getstatusoutput('python auc.py test_pctr')
  if pctr[0]== 0:
    auc_pctr = pctr[1]
  if testpctr[0] == 0:
    auc_testpctr = testpctr[1]

  os.system("sed -i '1i TARGET'  test_pctr.csv")

  print "auc_pctr=",auc_pctr,"==auc_testpctr=",auc_testpctr
'''
