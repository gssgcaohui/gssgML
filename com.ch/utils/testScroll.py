# coding=utf-8

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
import threading
import time
import shutil

data_imei = []
data_imeimd5 = []
data_mac = []
data_puid = []


def createFile(type):
    # try:
    #     dirname = "tmp/"
    #     if not os.path.exists(dirname):
    #         os.makedirs(dirname)
    # except OSError, osr:
    #     pass
    try:
        os.remove(type + ".txt")
    except:
        open(type + ".txt", "wb")


def writeFile(type, value):
    try:
        f = open(type + ".txt", "a")
        f.write(value + "\n")
    finally:
        f.flush()
        f.close()

def search(sizeNum):
    es = Elasticsearch([{'host': '58.61.152.2', 'port': '9210'}]
                       # refresh nodes after a node fails to respond
                       , sniff_on_connection_fail=True,
                       # and also every 60 seconds
                       sniffer_timeout=60,
                       # set sniffing request timeout to 10 seconds
                       sniff_timeout=30
                       )
    page = es.search(
        index='tagtest5',
        doc_type='taglib',
        scroll='1m',
        search_type='scan',
        size=sizeNum,

        body={
            "fields": ["IMEI", "IMEIMD5", "PUID", "MAC"],
            # Your query's body
            "query": {
                "query_string": {
                    "query": "*"
                    # "query": "flow>0 AND (gender='P01010099')"
                }
            }
        })

    sid = page['_scroll_id']
    scroll_size = page['hits']['total']
    print "total Size:", scroll_size
    return es, sid, scroll_size


def processing(es, sid, scroll_size, threadName, threadLock, totalSize):
    keys = ["PUID", "IMEI", "IMEIMD5", "MAC"]
    for i in keys:
        createFile(threadName + "_" + i)
    print("create file end")
    # Start scrolling
    while (scroll_size > 0):
        print "Scrolling..." #, scroll_size, threadName, "totalsize=", totalSize
        threadLock.acquire()  # 加锁
        try:
            page =  es.scroll(scroll_id=sid, scroll='1m')
            # Update the scroll ID
            sid = page['_scroll_id']
            # Get the number of results that we returned in the last scroll
            scroll_size = len(page['hits']['hits'])
        except  TransportError as e:
            print "errorsss",e[0]
            if e[0] == 404: #
                print "errorssss"
                scroll_size = 0
                # break



        totalSize = totalSize - scroll_size
        threadLock.release()  # 释放
        print threadName, "scroll size: ", str(scroll_size)
        if(scroll_size>0):
            for k in page["hits"]["hits"]:
                if k["_id"] == "_mappping":
                    continue
                #     k["fields"]["MAC"]), "-PUID:", k["fields"]["PUID"]
                if str(k["fields"]["IMEI"][0]).strip():
                    writeFile(threadName + "_" + "IMEI", k["fields"]["IMEI"][0])
                if str(k["fields"]["IMEIMD5"][0]).strip():
                    writeFile(threadName + "_" + "IMEIMD5", k["fields"]["IMEIMD5"][0])
                if str(k["fields"]["MAC"][0]).strip():
                    writeFile(threadName + "_" + "MAC", k["fields"]["MAC"][0])
                if str(k["fields"]["PUID"][0]):
                    writeFile(threadName + "_" + "PUID", k["fields"]["PUID"][0])
                    # print "date:imei:",str(k["_id"]), str(k["_source"]["IMEI"]), "-,imei5:", str(k["_source"]["IMEIMD5"]), "-mac:", str(k["_source"]["MAC"]), "-PUID:", str(k["_source"]["PUID"])


def mergeFiles(type):
    #    path="download/"
    path=os.getcwd()
    import fnmatch
    if os.path.exists(os.path.join(path,type+".txt")):
        os.remove(os.path.join(path, type+".txt"))
    with open(os.path.join(path, type+".tmp"), "ab") as dest:
        for _, _, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, "*_"+type+".txt"):
                print filename
                # with open(filename) as src:
                #     shutil.copyfileobj(src, dest)
                # os.remove(os.path.join(path, filename))
                # print "remove:",filename
    os.rename(os.path.join(path, type+".tmp"), type+".txt")




if __name__ == "__main__":
    sizeNum = 1000
    es, sid, scroll_size = search(sizeNum)
    threadLock = threading.Lock()
    threads = []
    start = time.time()
    for i in range(scroll_size / (sizeNum*5) + 1):
    # for i in range(1):
        threads.append(
            threading.Thread(target=processing, name="thread-" + str(i),
                             args=(es, sid, scroll_size, "thread-" + str(i), threadLock, scroll_size)))

    for thread in threads:
        thread.setDaemon(True)
        thread.start()
        # print "threadName:%s" % thread.getName()

    # 主线程等待所有子线程结束
    for childThread in threads:
        # threading.Thread.join(childThread)
        childThread.join()

        import platform
        import os
        import commands

    totalTime = time.time() - start
    print "totalTime:", totalTime

    # time.sleep(10)
    keys = ["PUID", "IMEI", "IMEIMD5", "MAC"]
    # mergeFiles("PUID")
    for i in keys:
        mergeFiles(i)
    # path = os.getcwd()

    # if(platform.system() == "Windows"):
    #     result = commands.getstatusoutput('type join.sh test 6 queryid_tokensid.txt 1 >train1')
    # else:

