#!/usr/bin/ env python
# coding:utf-8
import jieba

das="遇难/vi 者/k 致哀/vi ！/wt  视频/n ：/wm 菲/b 警方/n 强攻/v 遭劫/vi "
print das.decode("utf-8").split(" ")
# print list(jieba.cut(das))
da = jieba.cut(das)
db = "<generator object cut at 0x0000000002F63900>"
# print da
# print db
for w in da:
    print "===",w,"\n"


seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
print seg_list
print "Full Mode:", "/ ".join(seg_list)
# 全模式
seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print "Default Mode:", "/ ".join(seg_list)
# #精确模式
seg_list = jieba.cut("他来到了网易杭研大厦")
# #默认是精确模式
print ", ".join(seg_list)
seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")
# 搜索引擎模式
print ", ".join(seg_list)
