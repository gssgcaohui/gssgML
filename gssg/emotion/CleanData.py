#!/usr/bin/ env python
# coding:utf-8

# 预处理

import os, re, pandas as pd

TRAIN_DATA_PATH = 'K:\chinahadoop\机器学习训练营\训练营作业&代码\文本挖掘项目作业-情感分析\data'


# TRAIN_DATA_PATH='data/'
def clean_train(TRAIN_DATA_PATH='K:\chinahadoop\机器学习训练营\训练营作业&代码\文本挖掘项目作业-情感分析\data', out_train_file_name='thetrain.csv'):
    print 'start cleaning train data'
    train_file_names = os.listdir(TRAIN_DATA_PATH)
    train_data_list = []
    for train_file_name in train_file_names:
        if not train_file_name.endswith('.txt'):
            continue
        train_file = os.path.join(TRAIN_DATA_PATH, train_file_name)

        # draw sentiment lable
        label = int(train_file_name[0])
        with open(train_file, 'r') as f:
            lines = f.read().splitlines()
        labels = [label] * len(lines)
        labels_series = pd.Series(labels)
        lines_series = pd.Series(lines)

        # construct dataframe    axis=1 : 按列拼接
        data_pd = pd.concat([labels_series, lines_series], axis=1)
        train_data_list.append(data_pd)
    # 按行拼接
    train_data_pd = pd.concat(train_data_list, axis=0)

    # output train data
    train_data_pd.columns = ['label', 'text']
    train_data_pd.to_csv(os.path.join(TRAIN_DATA_PATH, out_train_file_name), index=None, encoding='utf-8', header=True)


TEST_DATA_PATH = 'K:\chinahadoop\机器学习训练营\训练营作业&代码\文本挖掘项目作业-情感分析\test'


def clean_test(TEST_DATA_PATH='K:\chinahadoop\机器学习训练营\训练营作业&代码\文本挖掘项目作业-情感分析\test', test_file_name='test1.csv', out_test_file_name='thetest.csv'):
    print 'start cleaning test data'
    test_file = os.path.join(TEST_DATA_PATH, test_file_name)

    with open(test_file, 'r') as f:
        lines = f.read().splitlines()

    lines_series = pd.Series(lines)
    test_data_list = pd.Series(lines_series, name='text')

    # output test data
    test_data_list.to_csv(os.path.join(TEST_DATA_PATH, out_test_file_name), index=None, encoding='utf-8', header=True)

if __name__=="__main__":
    clean_train()
    # clean_test()