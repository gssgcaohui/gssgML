#!/usr/bin/env python
# coding:utf-8
# kmeans 练习 图片压缩

import numpy as np
from scipy.misc import imread,imshow
import matplotlib.pyplot as pl

image_data=imread('./test.jpg').astype(np.float32)
[n,m,d] = np.shape(image_data)
from sklearn.cluster import KMeans
n_cluster=2
 
data = image_data.reshape(n*m,d)
model = KMeans(n_clusters=n_cluster,random_state=1).fit(data)
print model.cluster_centers_
print np.unique(model.labels_)
for i in range(n_cluster):
  data[model.labels_ == i,:] = model.cluster_centers_[i]

new_image=data.reshape(n,m,d)

#imshow(new_image)
imshow(new_image)
pl.show()