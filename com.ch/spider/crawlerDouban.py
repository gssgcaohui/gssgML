#!/usr/bin/python
# coding=utf-8


import os, requests, sys, urllib2, sys, re
from bs4 import BeautifulSoup
import csv
'''
 豆瓣电视剧
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
    dictionary = "data/douban"
    if not os.path.exists(dictionary):
        os.mkdir(dictionary)
    f_all = open(dictionary + 'all.txt', mode='w')
    f = open(u'data/电视剧.csv', 'wb')
    f.write(unicode('\xEF\xBB\xBF', 'utf-8'))   # 文件头
    writer = csv.writer(f)
    writer.writerow(['电视剧名称','类型', '上映时间', '主演', '评分'])

    for page in range(0, 100):
        print page*15
        url = u'https://www.douban.com/tag/国产电视剧/movie?start='+str(page*15)
        headers = {'User-Agent': 'Mozilla/4.0 (compatible;MSIE 5.5; Windows NT)'}
        try:
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')

            # 到510的时候就被屏蔽了

            # print content
            # content = request.get(url)
            # content = cotent.text.encode(content.encoding).decode('utf-8')
            pattern = re.compile('<a href="https://movie.douban.com/.*?" class="title" target="_blank">(.*?)</a>'
                                 '.*?<div class="desc">(.*?)/(.*?)</div>'
                                 '.*?<span class="rating_nums">(.*?)</span>', re.S)

            items = re.findall(pattern, content)
            for i, item in enumerate(items):
                postings = re.match(r'^(.*?)(\d+)(.*?)$', item[2].strip().replace("/", ' '))
                # 中国大陆 / 剧情 / 悬疑 / 惊悚 / 2016 / 孔笙 / 靳东 / 陈乔恩 / 赵达
                print '电视剧名称:', item[0]
                print '产地:', item[1].strip()
                print '类型:', postings.group(1).strip()
                print '上映时间:', postings.group(2).strip()
                print '主演:', postings.group(3).strip()
                print '评分:', item[3]
                writer.writerow(
            [item[0], postings.group(1).strip(), postings.group(2).strip(), postings.group(3).strip(),item[3]])

        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
            break

    # for page in range(1, 100):
    #     url = u'https://www.douban.com/tag/国产电视剧/?focus=movie'
    #     # url = 'http://www.qiushibaike.com/hot/page/' + str(page)
    #     headers = {'User-Agent': 'Mozilla/4.0 (compatible;MSIE 5.5; Windows NT)'}
    #
    #     try:
    #         request = urllib2.Request(url, headers=headers)
    #         response = urllib2.urlopen(request)
    #         content = response.read().decode('utf-8')
    #         # print content
    #         # content = request.get(url)
    #         # content = cotent.text.encode(content.encoding).decode('utf-8')
    #         pattern = re.compile('<a href="https://movie.douban.com/.*?" class="title" target="_blank">(.*?)</a>'
    #                              '.*?<div class="desc">(.*?)</div>',re.S)
    #
    #         items = re.findall(pattern, content)
    #         for i, item in enumerate(items):
    #             # postings = item[2].replace('<br/>', '\n')
    #             print '电视剧名称:', item[0]
    #             print '内容:', item[1]
    #     #         print '内容:', postings
    #     #         print '点赞:', item[3]
    #     #         print '评论数:', item[4]
    #     #         write_file(item[1], item[0], item[3], item[4], postings)
    #     #         f_all.write(item[0])
    #     #         f_all.write('\n')
    #     #         f_all.write(postings)
    #     #         f_all.write('\n\n')
    #     except urllib2.URLError, e:
    #         if hasattr(e, "code"):
    #             print e.code
    #         if hasattr(e, "reason"):
    #             print e.reason
    #         break
    f_all.close()
