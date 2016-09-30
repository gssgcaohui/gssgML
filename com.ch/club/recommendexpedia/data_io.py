#!/usr/bin/ env python
# coding:utf-8
import csv
from operator import itemgetter
import os
import json
import pickle
import pandas as pd

'''
expedia推荐项目
python版本
'''


def get_paths():
    paths = json.loads(open("SETTINGS.json").read())
    for key in paths:
        paths[key] = os.path.expandvars(paths[key])
    return paths

# 读取train文件
def read_train(nrows=None):
    train_path = get_paths()["train_path"]

    # get column names  获取列名
    col_names = pd.read_csv(train_path, nrows=1).columns.tolist()

    # extract useful column 去除不需要的列
    col_names.remove("click_bool")
    col_names.remove("gross_bookings_usd")
    col_names.remove("date_time")
    col_names.remove("position")
    # col_names.remove("booking_bool")

    if nrows == None:
        train_samples = pd.read_csv(train_path, usecols=col_names)
        # targets = pd.read_csv(train_path,usecols=['booking_bool'])
    else:
        # 如果设置了行数，就是进行小批量的数据进行测试
        train_samples = pd.read_csv(train_path, usecols=col_names, nrows=nrows)
        # targets = pd.read_csv(train_path,usecols=['booking_bool'],nrows=nrows)

    # return train_samples,tragets
    return train_samples


def read_test(nrows=None):
    test_path = get_paths()["test_path"]

    # get column names
    col_names = pd.read_csv(test_path, nrows=1).columns.tolist()

    # extract useful column
    col_names.remove("date_time")
    col_names.remove("position")
    # col_names.remove("booking_bool")

def load_model(model_name=None):
    if model_name is None:
        in_path = get_paths()["model_path"]
    else:
        path,_ = os.path.split(get_paths()["model_path"])
        in_path = os.path.join(path,model_name)
    return pickle.load(open(in_path))

def write_submission(recommendations,submission_file=None):
    if submission_file is None:
        submission_path = get_paths()["submission_path"]
    else:
        path,file_name = os.path.split(get_paths()["submission_path"])
        submission_path = os.path.join(path,submission_file)
    path,_ = os.path.split(submission_path)
    if not os.path.exists(path):
        os.makedirs(path)

    # 要强制转为int型
    rows =[(int(srch_id),int(prop_id))
           for srch_id,prop_id,rank_float
           # 在一组里面，
           # 0是srch_id 1 是prop_id 2是按照什么排序 这里是说在一组里，按照rank_float进行排序，默认升序
           in sorted(recommendations,key=itemgetter(0,2))]
    writer = csv.writer(open(submission_path,"w"),lineterminator="\n")
    writer.writerow(["TARGET"])
    writer.writerow(rows)