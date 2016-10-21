#!/usr/bin/ env python
# coding=utf-8

import os,commands,sys,subprocess 
#import feature_map

# 自动化生成 train_feature validate_feature test_feature
# 接收两个文件，train和test,如果需要join,则先调用autojoin.py生成两个combined文件

# 调用join操作
if len(sys.argv)==2 and sys.argv[1]== 'join':
  # os.popen('python autojoin.py train')
  ''' 
  # 使用os.popen时报如下错误
  close failed in file object destructor
  sys.excepthook is missing
  lost sys.stderr 
  '''
  # join train集
  result=commands.getstatusoutput("python autojoin.py train")
  if result[0] != 0:
    print "An error occurs",result
    os._exit(1)
  # os.popen('python autojoin.py test')
  # join test集
  result=commands.getstatusoutput("python autojoin.py test")
  if result[0] != 0:
    print "An error occurs",result
    os._exit(1)
  # 合并 train_combined 和 test_combined 前100000行为train集，后100000为test集
  result=commands.getstatusoutput("cat train_combined >tmp")
  if result[0] != 0:
    print "An error occurs",result
    os._exit(1)
  result=commands.getstatusoutput("cat test_combined >>tmp")
  if result[0] != 0:
    print "An error occurs",result
    os._exit(1)
else:
#  因为管道只能获取后面的结果，不能获取前面的结果，所以得先判断一下文件是否存在
  if not os.path.isfile(os.path.join(os.getcwd(),"test")):
    print "An error occurs: file test is not exist"
    os._exit(1)
  result=commands.getstatusoutput("cat test | awk '{print NR\"\t\"$0}' >test_1")
  if result[0] != 0:
    print "An error occurs",result
    os._exit(1)
  # 合并
  result=commands.getstatusoutput("cat train >tmp")
  if result[0] != 0:
    print "An error occurs",result
    os._exit(1)
  result=commands.getstatusoutput("cat test_1 >>tmp")
  if result[0] != 0:
    print "An error occurs",result
    os._exit(1)
  os.system('rm -rf test_1')


# 特征抽取
# os.popen('python feature_map.py tmp t_feature')
result=commands.getstatusoutput("python feature_map.py tmp t_feature")
if result[0] != 0:
  print "An error occurs:",result
  os._exit(1)

# 提取test集 后100000行
result=commands.getstatusoutput("tail -n 1000000 t_feature >test_feature")
if result[0] != 0:
  print "An error occurs:",result
  os._exit(1)
# 提取train集 前70000行
result=commands.getstatusoutput("head -n 700000 t_feature >train_feature")
if result[0] != 0:
  print "An error occurs:",result
  os._exit(1)
# 提取validate集 70001到100000行
result=commands.getstatusoutput("head -n 1000000 t_feature|tail -n 300000 >validate_feature")
if result[0] != 0:
  print "An error occurs:",result
  os._exit(1)

os.system('rm -rf tmp')
os.system('rm -rf t_feature')

print "generate feature successed!"
