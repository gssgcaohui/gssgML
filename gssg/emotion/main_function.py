#!/usr/bin/ env python
# coding:utf-8

# 特征提取
import jieba
import pandas as pd
import os,re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from CleanData import clean_train,clean_test
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.naive_bayes import  MultinomialNB
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn import  SVC

def words_to_features(raw_line,stopwords_path='ChineseStopWords.txt'):
  # convert a raw line to a string
  # filtrate = re.compile(u'[^\u4E00-\u9FDS]+')
  stopwords = {}.fromkeys(
      [line.rstrip() for line in open(stopwords_path)]
  )
  # 1 remove non-Chinese characters
  # chinese_only = filtrate.sub(r'',raw_line.decode('utf-8'))


