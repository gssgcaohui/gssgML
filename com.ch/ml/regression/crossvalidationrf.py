# -*- coding: utf-8 -*-
"""
random forest 的交叉验证
"""

# cross valication
# example data: diabetes
import numpy as np
from sklearn import cross_validation
from sklearn import datasets
from sklearn import svm
from sklearn.ensemble import RandomForestRegressor
diabetes = datasets.load_diabetes()
X_train,X_test,y_train,y_test = cross_validation.train_test_split(diabetes.data,diabetes.target,test_size=0.2,random_state=0)
#check the size of train and test datasets
print X_train.shape, y_train.shape
print X_test.shape,y_test.shape
clf = RandomForestRegressor(n_estimators=3).fit(X_train,y_train)
clf.score(X_test,y_test)
# to see individual predicted outcome
clf.predict(X_test)

##
# use corss_validation module
clf = RandomForestRegressor(n_estimators=3)
scores=cross_validation.cross_val_score(clf,diabetes.data,diabetes.target,cv=4)
print scores
print 'Accuracy %.2f' % scores.mean()