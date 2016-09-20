#!/usr/bin/python
# encoding:utf-8

# 利用python实现queue

class queue:
    def __init__(self, size=20):
        self.size = size
        self.queue = []
        self.end = -1

    def setsize(self, size):
        self.size = size

    def In(self, n):
        if self.end < self.size - 1:
            self.queue.append(n)
            self.end = self.end + 1
        else:
            raise "Queue is full"

    def Out(self):
        if self.end != -1:
            ret = self.queue[0]
            self.queue = self.queue[1:]
            self.end = self.end - 1
            return ret
        else:
            raise "Queue is empty"

    def End(self):
        return self.end

    def empty(self):
        self.queue = []
        self.end = -1

    def getsize(self):
        return self.end + 1


if __name__ == "__main__":
    q = queue()
    for i in xrange(15):
        q.In(i)

    print q.getsize()

    for i in xrange(15):
        print q.Out(),

    print
    q.empty()
    print q.getsize()
    q.setsize(100)
    for i in xrange(30):
        try:
            q.In(i)
        except:
            print "Error"
        else:
            print str(i) + " OK"
