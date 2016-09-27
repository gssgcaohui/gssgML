#!/usr/bin/ env python
# coding:utf-8

# 特征提取
import jieba
import pandas as pd
import os, re

from itsdangerous import NoneAlgorithm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

#from CleanData import clean_train, clean_test
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.feature_extraction.text import HashingVectorizer


def words_to_features(raw_line, stopwords_path='ChineseStopWords2.txt'):
    # convert a raw line to a string
    # filtrate = re.compile(u'[^\u4E00-\u9FDS]+')
    stopwords = {}.fromkeys(
        [line.rstrip() for line in open(stopwords_path)]
    )
    # 1 remove non-Chinese characters
    # chinese_only = filtrate.sub(r'',raw_line.decode('utf-8'))
    chinese_only = raw_line
    # 2 cut words
    #words_lst = jieba.cut(chinese_only)

    # 因为数据集已经是分过词的，所以直接用空格分开就行了
    words_lst = chinese_only.decode("utf-8").split(" ")

    # print words_lst
    # 3 remove stop words
    meaninful_words = []
    for word in words_lst:
        word = word.encode('utf-8')
        if word not in stopwords:
            meaninful_words.append(word)
    return ' '.join(meaninful_words)


def drawfeature(TRAIN_DATA_PATH='data', train_file_name='thetrain.csv', TEST_DATA_PATH='test',
                test_file_name='thetest.csv'):
    train_file = os.path.join(TRAIN_DATA_PATH, train_file_name)
    train_data = pd.read_csv(train_file)
    n_data_train = train_data['text'].size

    test_file = os.path.join(TEST_DATA_PATH, test_file_name)
    test_data = pd.read_csv(test_file)
    n_data_test = test_data['text'].size

    # bag of words model + tfidf
    # 5000是特征的数量，如果任务失败，可以改小到1000-2000
    # vectorizer = CountVectorizer(analyzer='word', tokenizer=None, preprocessor=None, stop_words=None, max_features=5000)
    # 还可以使用HashVectorizer
    vectorizer = HashingVectorizer(analyzer='word', tokenizer=None, preprocessor=None, stop_words=None,
                                   non_negative=True, n_features=5000)
    transformer = TfidfTransformer()

    # train
    print "start cut words in train data set"
    train_data_words = []
    for i in xrange(n_data_train):
        if ((i + 1) % 1000 == 0):
            print 'DrawFeatures Line %d of %d' % (i + 1, n_data_train)
        train_data_words.append(words_to_features(train_data['text'][i]))
    # draw labels
    # train_data_label = pd.Series(train_data['label'],name = 'label')
    # train_data_labels.to_csv(os.path.join(TRAIN_DATA_PATH,'train_data_label.csv'),index =None,header=True)

    print "start bag of word in train data set"
    # draw features
    train_data_features = vectorizer.fit_transform(train_data_words)
    # 内存不足  toarray()执行不完，必须加上()
    # train_data_features = train_data_features.toarray()
    # train_data_features = pd.DataFrame(train_data_features)
    # train_data_features.tocsv(os.path.join(TRAIN_DATA_PATH,"train_data_features1.csv"),index=None,header=None,encoding = 'utf-8')

    print "start tfidf in train data set"
    train_data_features = transformer.fit_transform(train_data_features)
    train_data_features = train_data_features.toarray()
    # train_data_features = pd.DataFrame(train_data_features)
    # train_data_features.tocsv(os.path.join(TRAIN_DATA_PATH,"train_data_features2.csv"),index=None,header=None,encoding = 'utf-8')

    # test
    print "start cut words in test data set"
    test_data_words = []
    for i in xrange(n_data_test):
        if ((i + 1) % 1000 == 0):
            print 'DrawFeatures line %d of %d' % (i + 1, n_data_test)
        test_data_words.append(words_to_features(test_data['text'][i]))

    # draw features
    print "Start bag of word in test data set"
    test_data_features = vectorizer.fit_transform(test_data_words)
    test_data_features = test_data_features.toarray()
    # test_data_features = pd.DataFrame(test_data_features)
    # test_data_features.tocsv(os.path.join(TEST_DATA_PATH,"test_data_features1.csv"),index=None,header=None,encoding = 'utf-8')

    print "Start tfidf in test data set"
    test_data_features = transformer.fit_transform(test_data_features)
    test_data_features = test_data_features.toarray()
    # test_data_features = pd.DataFrame(test_data_features)
    # test_data_features.tocsv(os.path.join(TEST_DATA_PATH,"test_data_features2.csv"),index=None,header=None,encoding = 'utf-8')

    # random forest
    print "random forest"
    forest = RandomForestClassifier(n_estimators=100)
    forest = forest.fit(train_data_features, train_data['label'])
    pred = forest.predict(test_data_features)
    pred = pd.Series(pred, name='TARGET')
    pred.to_csv("BOW_TFIDF_RF3.csv", index=None, header=True)

    # multinomial naive bayes
    print "multinomial naive bayes"
    mnb = MultinomialNB(alpha=0.01)
    mnb = mnb.fit(train_data_features, train_data['label'])
    pred = mnb.predict(test_data_features)
    pred = pd.Series(pred, name='TARGET')
    pred.to_csv("BOW_TFIDF_MNB3.csv", index=None, header=True)

    # 下面的方法都没有跑成功过
    # KNN
    print "knn"
    knn = KNeighborsClassifier()
    knn = knn.fit(train_data_features, train_data['label'])
    pred = knn.predict(test_data_features)
    pred = pd.Series(pred, name='TARGET')
    pred.to_csv("BOW_TFIDF_KNN3.csv", index=None, header=True)

    # SVM
    print "svm"
    svm = SVC(kernel='linear')
    svm = svm.fit(train_data_features, train_data['label'])
    pred = svm.predict(test_data_features)
    pred = pd.Series(pred, name='TARGET')
    pred.to_csv("BOW_TFIDF_SVM3.csv", index=None, header=True)


drawfeature()
