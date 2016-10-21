#!/usr/bin/ env python
# coding=utf-8
# 特征抽取，one hot encoding方法

import sys

file = open(sys.argv[1],"r")
toWrite = open(sys.argv[2],"w+")

feature_map={}
feature_index=0

# 添加前缀标识
def processIdFeature(prefix,id):
  global feature_map
  global feature_index
  str = prefix + "_" + id
  if str in feature_map:
    return feature_map[str]
  else:
    feature_index = feature_index + 1
    feature_map[str] = feature_index
    return feature_index


# 抽取特征
def extractFeature1(seg):
  list = []
  list.append(processIdFeature("url",seg[1]))
  list.append(processIdFeature("ad",seg[2]))
  list.append(processIdFeature("ader",seg[3]))
  list.append(processIdFeature("depth",seg[4]))
  list.append(processIdFeature("pos",seg[5]))
  list.append(processIdFeature("query",seg[6]))
  list.append(processIdFeature("keyword",seg[7]))
  list.append(processIdFeature("title",seg[8]))
  list.append(processIdFeature("desc",seg[9]))
  list.append(processIdFeature("user",seg[10]))
#  list.append(processIdFeature("queryinfo",seg[11]))
#  list.append(processIdFeature("kwinfo",seg[12]))
#  list.append(processIdFeature("tiinfo",seg[13]))
#  list.append(processIdFeature("dinfo",seg[14]))
#  list.append(processIdFeature("uinfo",seg[15]))
#  list.append(processIdFeature("uinfo2",seg[16]))
  return list

# 离散化  广告位排位比例 
def extractFeature2(seg):
  depth = float(seg[4])
  pos = float(seg[5])
  id = int(pos*10/depth)
  return processIdFeature("pos_ratio",str(id))

# 特征组合
def extractFeature3(seg):
  list=[]
  if(len(seg) >= 16):
    str = seg[2] +"_" + seg[15]
    list.append(processIdFeature("user_gender",str))
  return list

# 权重，这里都按1来取值
def toStr(label,list):
  line=label
  for i in list:
    line = line + "\t" + str(i) + ":1"
  return line


for line in file:
  seg = line.strip().split("\t")
  list = extractFeature1(seg)
  list.append(extractFeature2(seg))
  list.extend(extractFeature3(seg))
  toWrite.write(toStr(seg[0],list)+"\n")
 
toWrite.close


