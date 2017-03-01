#!/usr/bin/python
# coding=utf-8


import os, requests, sys, urllib2, sys, re
from bs4 import BeautifulSoup
import csv

'''
 百度风云榜   娱乐 / 人物
'''
reload(sys)
# 写中文
sys.setdefaultencoding('utf-8')


def write_file(file_name, writer_name, agree, comment, postings):
    f = open(dictionary + file_name + '.txt', mode='w')
    f.write(writer_name + '\t' + agree + '\t' + comment + '\n')
    f.write(postings)
    f.close()


if __name__ == '__main__':
    dictionary = "data/baidutop/"
    if not os.path.exists(dictionary):
        os.mkdir(dictionary)
    f_tv = open(dictionary + 'tvName.txt', mode='w')
    f_star = open(dictionary + 'starRole.txt', mode='w')

    url_main = 'http://top.baidu.com'
    starSet = set()  # 人物列表

    for i in range(1, 10, 8):  # 知道需要的类别值分别是1 和 9
        res = requests.get('http://top.baidu.com/category?c=' + str(i))
        res = res.text.encode(res.encoding).decode('gbk')
        soup = BeautifulSoup(res, 'html.parser')
        # print soup.prettify()
        # 找到二级 nav
        for nav in soup.find('ul', {'id': 'sub-nav'}).find_all(name='a'):
            # print nav['href'].replace('.', '')
            # print nav
            # 去重娱乐模块的动漫和音乐
            if (i == 1) & (nav['href'].endswith('33') | nav['href'].endswith('5')):
                continue
            url = '%s%s' % (url_main, nav['href'].replace('.', ''))
            # print "url=", url
            res = requests.get(url)
            res = res.text.encode(res.encoding).decode('gbk')
            soup = BeautifulSoup(res, 'html.parser')
            # content = soup.find_all(name='td', attrs={'class': 'keyword'})
            # 找到最终每个模块下的值
            for value in soup.find_all(name='a', attrs={'class': 'list-title'}):
                # title="爆裂直播之全城追缉">爆裂直播之全城..    要使用title的值，text的值有简写
                print value.text  # ,value['title'],value
                if i == 1:  # 娱乐
                    f_tv.write(value['title'])
                    f_tv.write('\n')
                else:  # 人物，利用set去重
                    starSet.add(value.text)
    for star in starSet:
        f_star.write(star.strip())
        f_star.write('\n')
    f_tv.close()
    f_star.close()



    # for i in range(1, 5):  # 知道需要的三个值分别是１２３
    #     res = requests.get('http://top.baidu.com/category?c=' + str(i))
    #     res = res.text.encode(res.encoding).decode('gbk')
    #     soup = BeautifulSoup(res, 'html.parser')
    #     # print soup.prettify()
    #     more = soup.find('a', {'class': 'more'})
    #     url = '%s%s' % (url_main, more['href'].replace('.', ''))
    #     # print "url=",url
    #     res = requests.get(url)
    #     res = res.text.encode(res.encoding).decode('gbk')
    #     soup = BeautifulSoup(res, 'html.parser')
    #     # print soup
    #     content = soup.find_all(name='td', attrs={'class': 'keyword'})
    #     for value in soup.find_all(name='a', attrs={'class': 'list-title'}):
    #         # print content
    #         print value.text
    #         f_tv.write(value.text)
    #         f_tv.write('\n')

    # 直接找到更多的href，省得再找两遍
    # districts = soup.find(name='ul', attrs={'id': 'sub-nav'})  # <ul id="sub-nav">
    # for district in districts.find_all(name='a'):
    #     # district_name = district.text
    #     # print district #,district_name
    #     url = '%s%s' % (url_main, district['href'].replace('.', ''))
    #     # print url
    #     res = requests.get(url)
    #     res = res.text.encode(res.encoding).decode('gbk')
    #     soup = BeautifulSoup(res, 'html.parser')
    #     # print soup.prettify()
    #     more = soup.find('a', {'class':'more'})
    #     print more
    #     url = '%s%s' % (url_main, more['href'].replace('.', ''))
    #     print url
