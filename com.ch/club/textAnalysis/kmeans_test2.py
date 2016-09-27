#!/usr/bin/env python
# coding:utf-8
'''
PIL的Image模块

# If mode is omitted, a mode is chosed so that all information in the image and the palette can be representedwithout a palette .
# when from a colour image to black and white, the library uses the ITU-R 601-2 luma transfrom:
# L = R * 299/1000 + G * 587/1000 + B * 114/1000
im.convert( mode ) => image

 # Converts an "RGB" image to "L" or "RGB" using a conversion matrix. The matrix is 4- or 16-tuple.
 im.convert( mode, matrix ) => image
 '''
from PIL import Image
from pylab import *

im = array(Image.open('data/test.jpg').convert('L'))
imshow(im)
show()

# 旋转45度角
Image.open('data/test.jpg').rotate(45).show()
