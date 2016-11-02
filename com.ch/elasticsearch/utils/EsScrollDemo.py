# coding=utf-8

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
import threading
import time
import fnmatch
import shutil
import os
import zipfile

'''
使用 scroll 深度分页导出数据，结合python多线程
导出完成后压缩
'''


def createFile(tmpPath, type):
    try:
        if not os.path.exists(tmpPath):
            os.mkdir(tmpPath)
    except OSError:
        pass
    try:
        os.remove(tmpPath + type + ".txt")
    except:
        open(tmpPath + type + ".txt", "wb")


def writeFile(tmpPath, type, value):
    try:
        f = open(tmpPath + type + ".txt", "a")
        f.write(value + "\n")
    finally:
        f.flush()
        f.close()


def search(sizeNum):
    es = Elasticsearch([{'host': '58.61.152.2', 'port': '9210'}]
                       # set connection time out
                       , timeout=60
                       # # sniff before doing anything
                       # sniff_on_start = True,
                       # # refresh nodes after a node fails to respond
                       # sniff_on_connection_fail = True,
                       # # and also every 60 seconds
                       # sniffer_timeout = 60,
                       # # set sniffing request timeout to 10 seconds
                       # sniff_timeout = 30
                       )
    page = es.search(
        index='test2',  ##tagtest5
        doc_type='taglib',
        scroll='2h',
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
    return es, sid, scroll_size


def processScanES(es, sid, scroll_size, threadName, threadLock, tmpPath):
    keys = ["PUID", "IMEI", "IMEIMD5", "MAC"]
    for i in keys:
        createFile(tmpPath, threadName + "_" + i)
    # print("create file end")
    # Start scrolling
    while (scroll_size > 0):
        print "Scrolling..."
        threadLock.acquire()  # 加锁
        try:
            page = es.scroll(scroll_id=sid, scroll='2h')
            # Update the scroll ID
            sid = page['_scroll_id']
            # Get the number of results that we returned in the last scroll
            scroll_size = len(page['hits']['hits'])
        except TransportError as e:
            if e[0] == 404:  # 读完了，hits为null了
                print e
                scroll_size = 0
            elif e[0] == "TIMEOUT":
                print "errorsss", e[0], e
                threadLock.release()
                continue
            else:
                print "er", e[0], e
                threadLock.release()
                continue

        except Exception as ex:
            print ex

        threadLock.release()  # 释放
        print threadName, "scroll size: ", str(scroll_size)
        if (scroll_size > 0):
            for k in page["hits"]["hits"]:
                if k["_id"] == "_mappping":
                    continue
                # k["_source"]["MAC"])
                if str(k["fields"]["IMEI"][0]).strip():
                    writeFile(tmpPath, threadName + "_" + "IMEI", k["fields"]["IMEI"][0])
                if str(k["fields"]["IMEIMD5"][0]).strip():
                    writeFile(tmpPath, threadName + "_" + "IMEIMD5", k["fields"]["IMEIMD5"][0])
                if str(k["fields"]["MAC"][0]).strip():
                    writeFile(tmpPath, threadName + "_" + "MAC", k["fields"]["MAC"][0])
                if str(k["fields"]["PUID"][0]):
                    writeFile(tmpPath, threadName + "_" + "PUID", k["fields"]["PUID"][0])


def mergeFiles(tmpPath, locPath, type):
    try:
        if not os.path.exists(locPath):
            os.makedirs(locPath)
    except:
        pass
    try:
        os.remove(os.path.join(locPath, type + ".txt"))
        os.remove(os.path.join(locPath, type + ".tmp"))
    except:
        pass
    with open(os.path.join(locPath, type + ".tmp"), "ab") as dest:
        for _, _, files in os.walk(tmpPath):
            for files in fnmatch.filter(files, "*_" + type + ".txt"):
                with open(os.path.join(tmpPath, files)) as src:
                    shutil.copyfileobj(src, dest)
                    src.close()
        dest.close()
    os.rename(os.path.join(locPath, type + ".tmp"), locPath + type + ".txt")


def zipFiles(dirName, zipFileName):
    filelist = []
    if os.path.isfile(dirName):
        filelist.append(dirName)
    else:
        for root, _, files in os.walk(dirName):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipFileName, "w", zipfile.zlib.DEFLATED)
    # for file in os.listdir(dirName):
    #     zf.write(os.path.join(dirName, file)) ## 带目录结构

    for tar in filelist:
        arcname = tar[len(dirName):]
        zf.write(tar, arcname)
    zf.close()


def processMergeFiles(tmpPath, locPath):
    mergeThreads = []
    keys = ["IMEI", "IMEIMD5", "MAC", "PUID"]
    for i in keys:
        mergeThreads.append(
            threading.Thread(target=mergeFiles, args=(tmpPath, locPath, i,)))

    for thread in mergeThreads:
        thread.setDaemon(True)
        thread.start()

    for childThread in mergeThreads:
        childThread.join()


def calcThreadNum(threadNum):
    if threadNum >= 10000:
        threadNum = threadNum / 100 + 1
    elif threadNum >= 1000:
        threadNum = threadNum / 20 + 1
    elif threadNum > 100:
        threadNum = threadNum / 6 + 1
    elif threadNum > 20:
        threadNum = threadNum / 2 + 1
    else:
        threadNum = threadNum + 1
    return threadNum


if __name__ == "__main__":
    start = time.time()
    print "begintime:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    tmpPath = "tmp/"
    locPath = "downloadzip/zip1/"
    zipFileName = "downloadzip/" + "111" + ".zip"
    sizeNum = 1000
    es, sid, scroll_size = search(sizeNum)
    threadLock = threading.Lock()
    threads = []
    threadNum = scroll_size / (sizeNum * 5)
    threadNum = calcThreadNum(threadNum)
    # threadNum = 10
    print "hit=", scroll_size, "threadNum=", threadNum
    for i in range(threadNum):
        threads.append(
            threading.Thread(target=processScanES, name="thread-" + str(i),
                             args=(es, sid, scroll_size, "thread-" + str(i), threadLock, tmpPath)))

    for thread in threads:
        thread.setDaemon(True)
        thread.start()
        # print "threadName:%s" % thread.getName()

    # 主线程等待所有子线程结束
    for childThread in threads:
        # threading.Thread.join(childThread)
        childThread.join()

    processMergeFiles(tmpPath, locPath)

    zipFiles(locPath, zipFileName)

    if os.path.exists(tmpPath):
        shutil.rmtree(tmpPath)

    totalTime = time.time() - start
    print "totalTime:", totalTime, "s;", "endTime:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
