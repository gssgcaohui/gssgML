#!/usr/bin/env python
# coding:utf-8


import time
from PIL import Image
import glob ,os
import numpy as np
from sklearn import preprocessing
import pandas as pd


def dense_to_one_hot(labels_dense,num_classes=25):
  label_size = labels_dense.shape[0]
  enc = preprocessing.OneHotEncoder(sparse=True,n_values=num_classes)
  enc.fit(labels_dense)
  array= enc.transform(labels_dense).toarray()
  return array

def shuffle(*arrs):
    arrs =list(arrs)
    for i ,arr in enumerate(arrs):
        assert len(arrs[0]) == len(arrs[i])
        arrs[i] = np.array(arr)
    p = np.random.permutation(len(arrs[0]))
    return tuple(arr[p] for arr in arrs)

def gettrainmatrix(input_path='/home/s-13/image/train_data/'):
    folderList = os.listdir(input_path)
    size = len(sum([i[2] for i in os.walk(input_path)],[]))
    image_list = np.empty((size,128,128,3),np.float)
    labels_list = np.empty((0,25),np.float)
    for label,folder_name in enumerate(folderList,start=0):
        files = os.path.join(input_path,folder_name)
        print "目录的名字",files,label
        file_size = 0
        index =0
        for parent,dirnames,file_list in os.walk(files):
            file_size = len(file_list)
            print "===目录总文件的个数：",file_size
            for file in file_list:
                image_path = os.path.join(parent,file)
                image = np.array(Image.open(image_path))
                if image.shape == (128,128,3):
                    image_list[index] = image
                    index +=1
        labels = np.array([label]*file_size).reshape(-1,1)
        if labels.size:
            labels_one_hot = dense_to_one_hot(labels)
            labels_list = np.append(labels_list,labels_one_hot,axis = 0)
        print "image的格式：",image_list.shape
        image_list,labels_list = shuffle(image_list,labels_list)
        return image_list,labels_list

def gettestmatrix(input_path='/home/s-13/image/test_data/'):
    test_list = np.empty((1004,128,128,3),np.float)
    index = 0
    for i in range(1004):
        image_path = input_path + str[i] +'.jpg'
        image = np.array(Image.open(image_path))
        if image.shape ==(128,128,3):
            test_list[index] = image
            index += 1
    # test_list = shuffle(test_list)
     return test_list

def weight_variable(shape):
    initial = tf.truncated_normal(shape,stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1,shape=shape)
    return tf.Variable(initial)

def conv2d(x,W):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

def pred(test_xs):
    global prediction
    y_pre = sess.run(prediction,feed_dict={xs:test_xs,keep_prob:1})
    print y_pre
    a = sess.run(tf.argmax(y_pre,1))
    pred = pd.Series(a,name='labels')
    pred.to_csv("result.csv",index=None,header=True)
    return y_pre

# data processing
start_time = time.time()
image_list,labels_list = gettrainmatrix()
test_xs = gettestmatrix()
end_time = time.time()
print "准备数据的时间开销：",end_time - start_time

# define placeholder for inputs to network
xs = tf.placeholder(tf.float32,[None,128,128,3])
ys = tf.placeholder(tf.float32,[None,25])
keep_prob = tf.placeholder(tf.float32)
image_xs = tf.reshape(xs,[-1,128,128,3])

## conv1 layer
W_conv1 = weight_variable([5,5,3,32])
b_conv1 = bias_variable([32])
h_conv1 = tf.nn.relu(conv2d(image_xs,W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

## conv2 layer
W_conv2 = weight_variable([5,5,32,64])
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1,W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

## conv3 layer
# W_conv3 = weight_variable([5,5,64,128])
# b_conv3 = bias_variable([128])
# h_conv3 = tf.nn.relu(conv2d(h_pool2,W_conv3) + b_conv3)
# h_pool3 = max_pool_2x2(h_conv3)

## conv4 layer
# W_conv4 = weight_variable([5,5,128,256])
# b_conv4 = bias_variable([256])
# h_conv4 = tf.nn.relu(conv2d(h_pool3,W_conv4) + b_conv4)
# h_pool4 = max_pool_2x2(h_conv4)

## func1 layer
W_fc1 = weight_variable([32*32*64,1024])
b_fc1 = bias_variable([1024])
# [n_samples,7,7,64] ->> [n_samples,7*7*64]
h_pool2_flat = tf.reshape(h_pool2,[-1,32*32*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat,W_fc1) + b_fc1)
h_fc1_drop = tf.nn.dropout(h_fc1,keep_prob)

## func2 layer
W_fc2 = weight_variable([1024,25])
b_fc2 = bias_variable([25])
prediction = tf.nn.softmax(tf.matmul(h_fc1_drop,W_fc2) + b_fc2)

# the error between prediction and real data
cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction),reduction_indices=[1]))
train_step = tf.train.AdamOptimizer(le-4).minimize(cross_entropy)

sess = tf.Session()

# important step
sess.run(tf.initialize_all_variables())
batch_size = 128
for i in range(20):
    print "第%d轮" % i
    data_size = image_list.shape[0]
    start = 0
    while start < data_size:
        print "第%d轮" % start
        batch_x = image_list[start:start + batch_size]
        batch_y = labels_list[start:start + batch_size]
        # batch_x = tf.reshape(batch_x,[-1,128*128*3])
        sess.run(train_step,feed_dict={xs:batch_x,ys:batch_y,keep_prob:0.5})
        print "lll"
        start += batch_size
        #
        #
        #
        #
        #
        test_xs = gettestmatrix()
        pred(test_xs)





