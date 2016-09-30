#!/usr/bin/ env python
# coding:utf-8

import data_io
import pandas as pd
import numpy as np
import os, random
from data_io import get_paths
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
from  sklearn.linear_model.stochastic_gradient import SGDClassifier
from feature_extraction import extract_features
from scipy import stats
from sklearn.linear_model.logistic import LogisticRegression


def process_test_samples(test_samples):
    processed_samples = pd.DataFrame()

    samples_in_one_srch = pd.DataFrame()
    for r_idx, sample in test_samples.iterrows():
        if (r_idx + 1) % 1000 == 0:
            print "Processed %i sample of %i" % (r_idx + 1, test_samples.shape[0])
        is_next_in_same_search = True
        samples_in_one_srch = pd.concat((sample.to_frame().transpose(), samples_in_one_srch), axis=0)
        current_srch_id = sample['srch_id']

        if (r_idx + 1) == test_samples.shape[0]:
            is_next_in_same_search = False
        else:
            next_srch_id = test_samples['srch_id'][r_idx + 1]
            if current_srch_id != next_srch_id:
                is_next_in_same_search = False

        if not is_next_in_same_search:
            ## if next one is not in the same search process the samples in the same search

            # feature extraction for samples
            ext_samples_in_one_srch = extract_features(samples_in_one_srch)
            processed_samples = pd.concat((processed_samples, ext_samples_in_one_srch), axis=0)

            # create new samples for the next search
            samples_in_one_srch = pd.DataFrame()

    return processed_samples


def do_training(processed_train_csv_file):
    ## Processed train samples reading
    # read saved processed train samples from the given csv file
    processed_train_samples = pd.read_csv(processed_train_csv_file)

    # inf to nan
    processed_train_samples = procesed_train_samples.replace([np.inf, -np.inf], np.nan)
    # nan to 0
    processed_train_samples = processed_train_samples.fillna(value=0)

    processed_train_samples_index_lst = processed_train_samples.index.tolist()
    random.shuffle(processed_train_samples_index_lst)

    # organize new train samples and targets
    shuffled_train_samples = processed_train_samples.ix[processed_train_samples_index_lst]
    col_names = shuffled_train_samples.columns.tolist()
    col_names.remove("booking_bool")
    features = shuffled_train_samples[col_names].values
    labels = shuffled_train_samples['booking_bool'].values

    ## Model training
    # 1 Random Forest Classifier

    print("Training Random Forest Classifier")
    rf_classifier = RandomForestClassifier(n_estimators=150,
                                           verbose=2,
                                           n_jobs=-1,
                                           min_samples_split=10)
    rf_classifier.fit(features, labels)

    # 3 SGD Classifier
    print("SGD Classifier")
    sgd_classifier = SGDClassifier(loss="modified_huber", verbose=2,
                                   n_jobs=-1)
    sgd_classifier.fit(features, labels)

    print("saved the SGD Classifier")
    data_io.save_model(sgd_classifier, model_name='sgd_classifier.pkl')

    # 4 Logistic Regression
    # print("Logistic Regression")
    # lr_classifier = LogisticRegression(verbose=2, n_jobs=-1)
    # lr_classifier.fit(features, labels)
    # print("saved the Logistic Regression")
    # data_io.save_model(lr_classifier, model_name='lr_classifier.pkl')

def do_prediction(n_trian_samples):
    proc_test_samples_file = get_paths()['proc_test_samples_path']

    if os.path.exists(proc_test_samples_file):
        print "Loading processed test data..."
        new_test_samples = pd.read_csv(proc_test_samples_file)