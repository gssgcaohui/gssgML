#!/usr/bin/ env python
# coding=utf-8
# 使用 requests库
import requests

url ='http://example.com/'
response = requests.get(url)
# 请求返回的状态
response.status_code    #200

# 访问headers里的content-type信息
response.headers['content-type'] #'text/html'
response.content

# 发送请求
requests.get('https://github.com/timeline.json') # get
requests.post('https://httpbin.org/post') # post

# 为 url传递参数
payload = {'key1':'value1','key2':'value2'}
r = requests.get('http://httpbin.org/get',params=payload)
print r.url
# http://httpbin.org/get?key2=value2&key1=value1

# 响应内容
r = requests.get('https://github.com/timeline.json')
print r.text

# 响应状态码
r = requests.get('http://httpbin.org/get')
print r.status_code
# 200 ok   403 禁止访问

# 响应头
print r.headers
print r.headers['Content-Type']

# cookies
print r.coolies['example_cookie_name']

# 超时
requests.get('http://github.com',timtout=0.01)


