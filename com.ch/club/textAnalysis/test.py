#!/usr/bin/ env python
# coding:utf-8

# 矩阵分解code

# our data sets
# example corupus: "I like deep learning." "I like NLP." "I enjoy flying."
# dictionary =["I","like","enjoy","deep","learning","NLP","flying","."]

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
la =np.linalg
dic = ["I","like","enjoy","deep","learning","NLP","flying","."]

# X is the co-occurnace matrix
X = np.array([[0,2,1,0,0,0,0,0],
             [2,0,0,1,0,1,0,0],
             [1,0,0,0,0,0,1,0],
             [0,1,0,0,1,0,0,0],
             [0,0,0,1,0,0,0,1],
             [0,1,0,0,0,0,0,1],
             [0,0,1,0,0,0,0,1],
             [0,0,0,0,1,1,1,0]])

# do SVD decomposition,then U contains the latent representation for each word
U,s,Vh = la.svd(X,full_matrices=False)

# for visualization
#for i in xrange(len(words)):
#  plt.text(U[i,0],U[i,1],words[i])
for i in xrange(len(dic)):
  plt.text(U[i,0],U[i,1],dic[i])
