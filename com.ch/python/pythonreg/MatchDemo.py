#!/usr/bin/python
# coding=utf-8
'''
@Time    : 2017/1/13 11:21
@Author  : ch
@desc    :python正则，Match匹配
'''
import os
import re

if __name__ == '__main__':

    m = re.match(r'^(.*?)(\d+)(.*?)$', u"剧情 / 喜剧 / 爱情 / 奇幻 / 古装 / 2003 / 孙太泉 / 张庭 / 徐峥 / 万弘杰")
    print "m.string:", m.string
    print "m.re:", m.re
    print "m.pos:", m.pos
    print "m.endpos:", m.endpos
    print "m.lastindex:", m.lastindex
    print "m.lastgroup:", m.lastgroup

    print "m.group(0):", m.group(0)
    print "m.group(1):", m.group(1)
    print "m.group(2):", m.group(2)
    print "m.group(3):", m.group(3)
    print "m.group(1,2):", m.group(1, 2)
    print "m.groups():", m.groups()
    print "m.groupdict():", m.groupdict()
    print "m.start(2):", m.start(2)
    print "m.end(2):", m.end(2)
    print "m.span(2):", m.span(2)
    print r"m.expand(r'\2 \1\3'):", m.expand(r'\2 \1\3')
