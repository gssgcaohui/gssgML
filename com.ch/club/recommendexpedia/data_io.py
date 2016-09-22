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
        paths[key]=os.path.expandvars(paths[key])
    return paths

def read_train(nrows=None):
    train_path=get_paths()["train_path"]

    # get column names
    col_names = pd.read_csv(train_path,nrows=1).columns.tolist()

    # extract useful column
    col_names.remove("click_bool")
    col_names.remove("gross_bookings_usd")
    col_names.remove("date_time")
    col_names.remove("position")
    # col_names.remove("booking_bool")

    if nrows == None:
        train_samples = pd.read_csv(train_path,usecols=col_names)
        # targets = pd.read_csv(train_path,usecols=['booking_bool'])
    else:
        train_samples = pd.read_csv(train_path,usecols=col_names,nrows=nrows)
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














