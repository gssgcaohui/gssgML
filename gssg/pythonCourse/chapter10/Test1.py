#!/usr/bin/ env python
# coding=utf-8
# 使用urllib2 库的使用和说明   post方式
import urllib,urllib2

url = 'http://www.zhihu.com/login'

user_agent = 'Mozilla/5.0(compatible;MSIE 5.5;Windows NT)'
values = {'username':'Lee','password':'XXXX'}
headers ={'User-Agent':user_agent}
data = urllib.urlencode(values)
request = urllib2.Request(url,data,headers)
response = urllib2.urlopen(request)
page = response.read()