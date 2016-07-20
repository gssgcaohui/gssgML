#!/usr/bin/ env python
# coding: utf-8
import os,sys,urllib2,sys,re
#import requests
from lxml import etree


def StringListSave(save_path,filename,slist):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path+"/"+filename+".txt"
    with open(path,"w+") as fp:
        for s in slist:
            fp.write("%s\t\t%s\n" % (s[0].encode("utf8"),s[1].encode("utf8")))


# 一级页面  使用正则表达式
def Page_Info(myPage):
    '''Regex'''
    mypage_Info = re.findall(r'<div class="titleBar" id=".*?"><h2>(.*?)</h2><div class="more"><a href="(.*?)">.*?</a></div></div>',myPage,re.S)
    return mypage_Info

# 二级页面，使用xpath来分析
def New_Page_Info(new_page):
    '''Regex(slowly) or xpath(fast)'''
    # new_page_Info = re.findall(r'<td class=".*?"'>.*?<a href="(.*?)\.html".*?>(.*?)</a></td>',new_page,re.S)
    # new_page_Info = re.findall(r'<td class=".*?"'>.*?<a href="(.*?)">(.*?)</a></td>',new_page,re.S)
    # results =[]
    #for url,item in new_page_Info:
    #    results.append((item,url+".html"))
    #return results
 # xpath 使用路径表达式来选取文档中的节点或节点集
    dom = etree.HTML(new_page)
    new_items = dom.xpath('//tr/td/a/text()')
    new_urls = dom.xpath('//tr/td/a/@href')
    assert(len(new_items) == len(new_urls))
    return zip(new_items,new_urls) # return a tuple list


# 抓取，使用urllib2 或 requests
def Spider(url):
    i =0
    print "downloading",url
    # 抓取内容并解码
    #myPage =requests.get(url).content.decode("gbk")
    myPage =urllib2.urlopen(url).read().decode("gbk")

    # find all intersted page info
    myPageResults = Page_Info(myPage)
    save_path = 'wyNews'
    filename = str(i) +"_" +u"新闻排行榜"
    StringListSave(save_path,filename,myPageResults)
    i += 1
    for item,url in myPageResults:
        print "downloading ",url
        # new_page = requests.get(url).content.decode("gbk")
        new_page =urllib2.urlopen(url).read().decode("gbk")
        newPageResults = New_Page_Info(new_page)
        filename = str(i) + "_" +item
        StringListSave(save_path, filename, newPageResults)
        i += 1




if __name__ == '__main__':
  print "start"
  start_url = "http://news.163.com/rank/"
  Spider(start_url)
  print "end"