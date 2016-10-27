# coding=utf-8
'''
Thread Test
'''

import thread
import time

'''通过thread模块中的start_new_thread(func,args)创建线程：'''


# 为线程定义一个函数
def print_time(threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print "%s: %s" % (threadName, time.ctime(time.time()))


def createDemo1():
    # 创建两个线程
    try:
        thread.start_new_thread(print_time, ("Thread-1", 2,))
        thread.start_new_thread(print_time, ("Thread-2", 4,))
    except:
        print "Error: unable to start thread"


"""通过继承threading.Thread创建线程，以下示例创建了两个线程"""
import threading


class CreateThread(threading.Thread):
    def __init__(self, threadName, interval):
        threading.Thread.__init__(self, name=threadName)
        self.interval = interval
        self.isrunning = True

    # 重写threading.Thread中的run()
    def run(self):
        while self.isrunning:
            print 'thread %s is running,time:%s\n' % (self.getName(), time.ctime())  # 获得线程的名称和当前时间
            time.sleep(self.interval)

    def stop(self):
        self.isrunning = False


def createDemo2():
    thread1 = CreateThread('A', 1)
    thread2 = CreateThread('B', 2)
    thread1.start()
    thread2.start()
    time.sleep(5)
    thread1.stop()
    thread2.stop()


'''在threading.Thread中指定目标函数作为线程处理函数'''


def run_thread(n):
    for i in range(n):
        print "\n", i


def createDemo3():
    threads = []
    for i in range(10):
        threads.append(threading.Thread(target=run_thread, name="thread-" + str(i), args=(15,)))

    for thread in threads:
        thread.setDaemon(True)
        thread.start()
        # print "threadName:%s" % thread.getName()

    # 主线程等待所有子线程结束
    for childThread in threads:
        # threading.Thread.join(childThread)
        childThread.join()

    for i in range(10):
        print "\nhahah%s" % i


import threading
import time  # 导入time模块

'''join test'''


class Mythread(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name=threadname)

    def run(self):
        time.sleep(2)
        for i in range(5):
            print '%s is running····' % self.getName()


def joinTest():
    t2 = Mythread('B')
    t1 = Mythread('A')
    t2.start()
    t1.start()
    t2.join()
    t1.join()
    for i in range(5):
        print 'the program is running···'


def daemonTest():
    t = Mythread('son thread')
    t.setDaemon(True)
    t.start()
    if t.isDaemon():
        print "the father thread and the son thread are done"
    else:
        print "the father thread is waiting the son thread····"


if __name__ == "__main__":
    # createDemo1()
    # createDemo2()
    createDemo3()
    # joinTest()
    # daemonTest()
