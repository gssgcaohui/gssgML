#!/usr/bin/env python

class Human:

  laugh = "hahah"

  def show_laugh(self):
    print self.laugh

  def laugh_10th(self):
    for i in range(10):
      self.show_laugh()


xl = Human()
xl.laugh_10th()
