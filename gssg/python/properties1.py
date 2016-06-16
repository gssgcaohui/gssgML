#!/usr/bin/env python

class Bird(object):
  feather=True

class Chicken(Bird):
  fly=False
  def __init__(self,age):
    self.age=age
  def __getattr__(self,name):
    if name == 'adult':
      if self.age > 1.0: return True
      else: return False
    else:raise AttributeError(name)

chick=Chicken(2)

print(chick.adult)
chick.age=0.5
print(chick.adult)
print(chick.male)
