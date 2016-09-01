# -*- coding: utf-8 -*-

'''
Created on 3 Jul 2016

@author: Bin Liang (bliang@csu.edu.au)
'''

import numpy as np
import pylab as pl
from sklearn import datasets
from knn_classification import knn_predict


def plot_knn_boundary():
    ## Training dataset preparation
    # use sklearn iris dataset
    iris_dataset = datasets.load_iris()


    # first two dimensions as the features
    # it's easy to plot boundary in 2D
    train_data = iris_dataset.data[:,:2] 
    print "init:",train_data

    # get labels
    labels = iris_dataset.target # labels
    print "init2:",labels

    
    ## Test dataset preparation
    h = 0.1
    
    x0_min = train_data[:,0].min() - 0.5
    x0_max = train_data[:,0].max() + 0.5
    
    x1_min = train_data[:,1].min() - 0.5
    x1_max = train_data[:,1].max() + 0.5
    
    x0_features, x1_features = np.meshgrid(np.arange(x0_min, x0_max, h), 
                                           np.arange(x1_min, x1_max, h))
    
    # test dataset are samples from the whole regions of feature domains
    test_data = np.c_[x0_features.ravel(), x1_features.ravel()]
    
    ## KNN classification
    p_labels = []   # prediction labels
    for test_sample in test_data:
        # knn prediction
        p_label = knn_predict(train_data, labels, test_sample, n_neighbors = 6)
        p_labels.append(p_label)
    
    # list to array
    p_labels = np.array(p_labels)
    p_labels = p_labels.reshape(x0_features.shape)
    
    ## Boundary plotting  边界策划
    pl.figure(1)
    pl.set_cmap(pl.cm.Paired)
    pl.pcolormesh(x0_features, x1_features, p_labels)
    
    pl.scatter(train_data[:,0], train_data[:,1], c = labels)
    # x y轴的名称
    pl.xlabel('feature 0')
    pl.ylabel('feature 1')

    # 设置x,y轴的上下限
    pl.xlim(x0_features.min(), x0_features.max())
    pl.ylim(x1_features.min(), x1_features.max())
    # 设置x,y轴记号
    pl.xticks(())
    pl.yticks(())
    
    pl.show()


if __name__ == '__main__':
    plot_knn_boundary()
