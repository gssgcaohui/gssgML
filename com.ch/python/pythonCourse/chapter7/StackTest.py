#!/usr/bin/env python
# encoding:utf-8

'''
使用python实现stack
stack通常的操作：
Stack() 建立一个空的栈对象
push() 把一个元素添加到栈的最顶层
pop() 删除栈最顶层的元素，并返回这个元素
peek() 返回最顶层的元素，并不删除它
isEmpty() 判断栈是否为空
size() 返回栈中元素的个数
'''

class stack:
    def __init__(self, size=20):
        self.stack = []
        self.size = size
        self.top = -1

    def setsize(self, size):
        self.size = size

    def push(self, data):
        if self.isFull():
            raise "stack already full"
        else:
            self.stack.append(data)
            self.top += 1

    def pop(self):
        if self.isEmpty():
            raise "stack is empty"
        else:
            data = self.stack[-1];
            self.top -= 1
            del self.stack[-1]
            return data

    def Top(self):
        return self.top

    def isEmpty(self):
        if self.top == -1:
            return True
        else:
            return False

    def empty(self):
        self.stack = []
        self.top = -1

    def isFull(self):
        if self.top == self.size - 1:
            return True
        else:
            return False


if __name__ == '__main__':
    st = stack()
    for i in xrange(16):
        st.push(i)
    print st.Top()
    for i in xrange(16):
        print st.pop()
    st.empty()
    st.setsize(101)
    for i in xrange(100):
        st.push(i)
    for i in xrange(100):
        print st.pop()
