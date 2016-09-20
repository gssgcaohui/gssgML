#!/usr/bin/env python

class Num(object):
  def __init__(self,value):
    self.value = value
  def getNeg(self):
    return -self.value
  def setNeg(self,value):
    self.value = -value
  def delNeg(self):
    print("value alse deleted")
    del self.value
  neg = property(getNeg,setNeg,delNeg,"I'm negative")

x=Num(1.1)
print(x.neg)
x.neg = -22
print(x.value)
print(Num.neg.__doc__)
del x.neg
