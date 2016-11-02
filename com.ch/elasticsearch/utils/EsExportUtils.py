# coding=utf-8
'''
    Export and Import ElasticSearch Data.
    导出数据测试正确，使用的是浅分页，效率太低，
    导入数据未测试
'''

import json
import os
import sys
import time
import urllib2

reload(sys)
sys.setdefaultencoding('utf-8')  # @UndefinedVariable


class exportEsData():
    size = 1000

    def __init__(self, url, index, type):
        self.url = url + "/" + index + "/" + type + "/_search"
        self.index = index
        self.type = type

    def exportData(self):
        print("export data begin...")
        begin = time.time()
        try:
            os.remove(self.index + "_" + self.type + ".json")
        except:
            # os.mknod(self.index+"_"+self.type+".json")
            open(self.index + "_" + self.type + ".txt", "wb");
        msg = urllib2.urlopen(self.url).read()
        print(msg)
        obj = json.loads(msg)
        num = obj["hits"]["total"]
        start = 0
        end = num / self.size + 1
        print "122num=", num, end
        while (start < end):
            print self.url + "?from=" + str(start * self.size) + "&size=" + str(self.size);
            msg = urllib2.urlopen(self.url + "?from=" + str(start * self.size) + "&size=" + str(self.size)).read()
            self.writeFile(msg)
            start = start + 1
        print("export data end!!!\n\t total consuming time:" + str(time.time() - begin) + "s")

    def writeFile(self, msg):
        obj = json.loads(msg)
        vals = obj["hits"]["hits"]
        try:
            f = open(self.index + "_" + self.type + ".txt", "a")
            for val in vals:
                a = json.dumps(val["_source"], ensure_ascii=False)
                f.write(a + "\n")
        finally:
            f.flush()
            f.close()


class importEsData():
    def __init__(self, url, index, type):
        self.url = url + "/" + index + "/" + type
        self.index = index
        self.type = type

    def importData(self):
        print("import data begin...")
        begin = time.time()
        try:
            f = open(self.index + "_" + self.type + ".json", "r")
            for line in f:
                self.post(line)
        finally:
            f.close()
        print("import data end!!!\n\t total consuming time:" + str(time.time() - begin) + "s")

    def post(self, data):
        req = urllib2.Request(self.url, data, {"Content-Type": "application/json; charset=UTF-8"})
        urllib2.urlopen(req)


if __name__ == '__main__':
    '''
        Export Data
        e.g.
                            URL                    index        type
        exportEsData("http://10.100.142.60:9200","watchdog","mexception").exportData()

        export file name: watchdog_mexception.json
    '''
    exportEsData("http://58.61.152.2:9210", "test2", "taglib").exportData()

    '''
        Import Data

        *import file name:watchdog_test.json    (important)
                    "_" front part represents the elasticsearch index
                    "_" after part represents the  elasticsearch type
        e.g.
                            URL                    index        type
        mportEsData("http://10.100.142.60:9200","watchdog","test").importData()
    '''
    # importEsData("http://10.100.142.60:9200","watchdog","test").importData()
    # importEsData("http://10.100.142.60:9200","watchdog","test").importData()
