#!/usr/bin/ env python
# coding=utf-8

import os,commands,sys

auc_pctr = 0
auc_testpctr = 0
isTest = True

# 如果没有参数，默认join test集，带train参数，join train集
if len(sys.argv)== 1 or (len(sys.argv) == 2 and sys.argv[1] == 'test'):
  # 先把test集增加一列，然后处理操作的列同train集一样
  result=commands.getstatusoutput("cat test | awk '{print NR\"\t\"$0}' >test_1")
  if result[0] != 0:
    print "An error occurs, the program terminates",result
    os._exit(1)
  result=commands.getstatusoutput('bash join.sh test_1 7 queryid_tokensid.txt 1 >train1')
elif len(sys.argv)== 2 and sys.argv[1] == 'train':
  result=commands.getstatusoutput('bash join.sh train 7 queryid_tokensid.txt 1 >train1')
  isTest = False
else:
  print "validate arguments!"
  os._exit(1)

if result[0] != 0:
  print "An error occurs",result
  os._exit(1)

result=commands.getstatusoutput('bash join.sh train1 8 purchasedkeywordid_tokensid.txt 1 >train2')

if result[0] != 0:
  print "An error occurs",result
  os._exit(1)

result=commands.getstatusoutput('bash join.sh train2 9 titleid_tokensid.txt 1 >train3')

if result[0] != 0:
  print "An error occurs",result
  os._exit(1)

result=commands.getstatusoutput('bash join.sh train3 10 descriptionid_tokensid.txt 1 >train4')

if result[0] != 0:
  print "An error occurs",result
  os._exit(1)

result=commands.getstatusoutput('bash join.sh train4 11 userid_profile.txt 1 >train5')

if result[0] != 0:
  print "An error occurs",result
  os._exit(1)

if isTest:
  result=commands.getstatusoutput("sort -n -t $'\t' -k 1,1 train5 >test_combined")
else:
  result=commands.getstatusoutput("mv train5 train_combined")


if result[0] != 0:
  print "An error occurs",result
  os._exit(1)

if isTest:
  path1 = os.path.join(os.getcwd(),"train5")
  path2 = os.path.join(os.getcwd(),"test_1")
  if os.path.isfile(path1):
    os.remove(path1)
  if os.path.isfile(path2):
    os.remove(path2)
  
os.system('rm -rf train1')
os.system('rm -rf train2')
os.system('rm -rf train3')
os.system('rm -rf train4')


print " join successed!"
