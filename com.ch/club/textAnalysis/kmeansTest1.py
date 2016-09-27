# !/usr/bin/env python
# coding:utf-8
'''
Kmeans简单实践 - 图片压缩
使用更少的像素表达一张图片
'''
import numpy as np
from sklearn.cluster import KMeans
# 从scipy里导入不行，需要从pylab里导入
#from scipy.misc import imread, imshow  # imsave,
from pylab import imread,imshow,show

image_data = imread('data/all.jpg').astype(np.float32) # test.jpg
[n, m, d] = np.shape(image_data)
# 几个Pixel  （px）
n_cluster = 10
data = image_data.reshape(n * m, d)
model = KMeans(n_clusters=n_cluster, random_state=1).fit(data)
print model.cluster_centers_
print np.unique(model.labels_)
for i in range(n_cluster):
    data[model.labels_ == i, :] = model.cluster_centers_[i]
new_image = data.reshape(n, m, d)
imshow(new_image)
show()
