#!/usr/bin/env python

class Human(object):

  laugh = "hahah"

  def __init__(self,name):
    self.name = name
    print("__init__ is called")

  def show_name(self):
    print "my name is : "+self.name

  def show_laugh(self):
    print self.laugh

  def laugh_10th(self):
    for i in range(10):
      self.show_laugh()


xl = Human("zs")
xl.laugh_10th()
xl.show_name()
