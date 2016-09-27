# -*- coding: utf-8 -*-

'''
Created on 4 Jul 2016

@author: Bin Liang (bliang@csu.edu.au)
KNN分类，决策边界

'''
from scipy.spatial import distance
import operator
    
def findNearestNeighbors(train_data, sample, n_neighbors):
    """
        FUNC:
            Get the k nearest neighbors of sample in the training data
        PARAM:
            train_data:      training data in the shape of 
                             [n_samples, n_features]
            sample:          one sample in the shape of [1, n_features]
            n_neighbors:     the number of neighbors
        RETURN:
            neighbors_index: the index of the k nearest neighbors in the 
                             training data
    """
    distances = []
    neighbors_index = []
    
    for i, data in enumerate(train_data):
        dist = distance.euclidean(data, sample)
        distances.append({'index':i, 'distance':dist})
    distances.sort(key = operator.itemgetter('distance'))
    
    for i in range(n_neighbors):
        index = distances[i].get('index')
        neighbors_index.append(index)
    
    return neighbors_index

        
def knn_predict(train_data, labels, test_sample, n_neighbors = 2):
    """
        FUNC:
            KNN classifier implementing the k-nearest neighbors voting
        PARAM:
            train_data:  training data in the shape of [n_samples, n_features]
            labels:      labels of training data in the shape of [n_samples, 1]
            test_sample: one test sample in the shape of [1, n_features]
            n_neighbors: the number of neighbors, default 5
        RETURN:
            p_label:     return the prediction label of the test sample
    """
    neighbors_index = findNearestNeighbors(train_data, test_sample, n_neighbors)
    
    label_votes = {}
    for index in neighbors_index:
        label = labels[index]
        if label in label_votes.keys():
            label_votes[label] += 1
        else:
            label_votes[label] = 1
    
    p_label = max(label_votes, key = label_votes.get)  
    return p_label