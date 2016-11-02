#!/usr/bin/env python

class Bird(object):
  have_feather=True
  way_of_reproduction="egg"

  def move(self,dx,dy):
    position=[0,0]
    position[0] = position[0]+dx
    position[1] = position[1]+dy
    return position

class Chicken(Bird):
  way_of_move="walk"
  possible_in_kFC=True

class Swan(Bird):
  way_of_move="fly"
  possible_in_KFC=False

summer=Chicken()
print summer.have_feather
print summer.move(5,7)

