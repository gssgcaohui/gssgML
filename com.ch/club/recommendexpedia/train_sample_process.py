#!/usr/bin/ env python
# coding:utf-8

import data_io
import pandas as pd
import numpy as np
import os
from data_io import get_paths
from feature_extraction import extract_features

'''
数据预处理

'''


def process_train_samples(samples, max_srch_size=10, each_saved_size=1000000):
    '''
    func:
    Process samples including feature extraction and downsampling
    MB:samples with the same srch_id that have one positive traget
    are treated as one positive sample,otherwise,are negative samples
   max_srch_size  就是每一个srch_id最多有几行数据，
   比如 train数据集中，一个srch_id有20行，但是我们只随机取到10行就可以了，这就做了个downsampling
    因为训练集很大，所以就每处理100万条，就生成一个文件，并训练
    '''

    # 训练集数据乱序，这里先拍下序，相同srch_id的数据放一块
    sorted_samples = samples.sort_values(by=['srch_id'])  # grou by srch_id
    sorted_samples = sorted_samples.reset_index(drop=True)  # reset row index
    processed_samples = pd.DataFrame()

    samples_in_one_srch = pd.DataFrame()
    # for 循环处理的就是下一个srch_id是不是与上一个相同
    for r_idx, sample in sorted_samples.iterrows():
        if (r_idx + 1) % 1000 == 0:
            print "processed %i sample of %i " % (r_idx + 1, sorted_samples.shape[0])

        is_next_in_same_search = True
        samples_in_one_srch = pd.concat((sample.to_frame().transpose(), samples_in_one_srch), axis=0)

        current_srch_id = sample['srch_id']

        # 最后一行
        if (r_idx + 1) == sorted_samples.shape[0]:
            is_next_in_same_search = False
        else:
            next_srch_id = sorted_samples['srch_id'][r_idx + 1]
            if current_srch_id != next_srch_id:
                is_next_in_same_search = False

        # 正好是一组srch_id ，进行特征提取
        if not is_next_in_same_search:
            ## if next one is not in the same search process the samples in the same search

            # feature extraction for samples
            ext_samples_in_one_srch = extract_features(samples_in_one_srch)

            # downsample samples
            n_samples = ext_samples_in_one_srch.shape[0]


def do_train_samples_processing():
    ## step1 read training data
    print "reading training data..."
    # train_samples = data_io.read_train(nrows= 100000)
    train_samples = data_io.read_train()
    print "Done"

    ## step2 Data preprocessing
    print "Processing training data..."
    # replace NAN with 0    fillna函数
    train_samples = train_samples.fillna(value=0)
    # processing training samples
    process_train_samples(train_samples)

    print "Processing training data done"


if __name__ == "main":
    do_train_samples_processing()
