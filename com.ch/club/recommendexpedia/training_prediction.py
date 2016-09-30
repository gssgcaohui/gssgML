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
    processed_train_samples = processed_train_samples.replace([np.inf, -np.inf], np.nan)
    # nan to 0
    processed_train_samples = processed_train_samples.fillna(value=0)

    processed_train_samples_index_lst = processed_train_samples.index.tolist()
    # 之前排过序，这里shuffle一下，效果更好
    random.shuffle(processed_train_samples_index_lst)

    # organize new train samples and targets
    shuffled_train_samples = processed_train_samples.ix[processed_train_samples_index_lst]
    col_names = shuffled_train_samples.columns.tolist()
    col_names.remove("booking_bool")
    features = shuffled_train_samples[col_names].values
    labels = shuffled_train_samples['booking_bool'].values

    # Model training
    # 1 Random Forest Classifier

    print("Training Random Forest Classifier")
    rf_classifier = RandomForestClassifier(n_estimators=150,
                                           verbose=2,
                                           n_jobs=-1,
                                           min_samples_split=10)
    rf_classifier.fit(features, labels)

    print("Saving the Random Forest Classifier")
    data_io.save_model(rf_classifier, model_name='rf_classifier.pkl')

    # 2 Gradient Boosting Classifier
    print("Gradient Boosting  Classifier")
    gb_classifier = GradientBoostingClassifier(n_estimators=150,
                                               verbose=2,
                                               learning_rate=0.1,
                                               min_samples_split=10)
    gb_classifier.fit(features, labels)
    print("Saving the Gradient Boosting  Classifier")
    data_io.save_model(gb_classifier, model_name='gb_classifier.pkl')

    # 3 SGD Classifier
    print("SGD Classifier")
    sgd_classifier = SGDClassifier(loss="modified_huber", verbose=2,
                                   n_jobs=-1)
    sgd_classifier.fit(features, labels)

    print("saved the SGD Classifier")
    data_io.save_model(sgd_classifier, model_name='sgd_classifier.pkl')

    # 4 Logistic Regression  效果不好
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
        print "Loading processed test data done"
    else:
        #  prediction
        print "reading test data..."
        test_samples = data_io.read_test()
        test_samples = test_samples.fillna(value=0)
        print "done."

        # process test samples
        print "processing test data..."
        new_test_samples = process_test_samples(test_samples)
        new_test_samples.to_csv(proc_test_samples_file, index=None)
        print "Processing test data done."

    test_features = new_test_samples.values

    # 5.1 random forest prediction
    print("Loading the random forest classifier")
    rf_classifier = data_io.load_model(model_name='lr_classifier.pkl')
    print("random forest Predicting")
    # 　拿概率值
    rf_predictions = rf_classifier.predict_proba(test_features)[:1]

    # 5.2 Gradient Boosting prediction
    print("Loading the Gradient Boosting  classifier")
    gb_classifier = data_io.load_model(model_name='gb_classifier.pkl')
    print("Gradient Boosting  Predicting")
    gb_predictions = gb_classifier.predict_proba(test_features)[:1]

    # 5.3 SGD prediction
    print("Loading the SGD classifier")
    sgd_classifier = data_io.load_model(model_name='sgd_classifier.pkl')
    print("SGD Predicting")
    sgd_predictions = sgd_classifier.predict_proba(test_features)[:1]

    # 5.4 LR prediction
    # print("Loading the LR classifier")
    # lr_classifier = data_io.load_model(model_name='lr_classifier.pkl')
    # print("Logistic Regression Predicting")
    # lr_predictions = lr_classifier.predict_proba(test_features)[:1]

    # step 6 score fusion  把三组概率放到数组中
    prob_arr = np.vstack((rf_predictions, gb_predictions, sgd_predictions))

    # average mean   取概率的评价值  算术评价
    mean_score = np.mean(prob_arr, axis=0)
    # for sorting  几何评价，效果不太好
    # 前面的排序是升序，乘以-1 改为降序
    mean_score = -1.0 * mean_score
    # geometric mean
    gmean = stats.gmean(prob_arr, axis=0)
    # for sorting
    gmean = -1.0 * gmean

    # step 7 output result
    mean_recommendations = zip(new_test_samples['srch_id'],
                               new_test_samples['prop_id'], mean_score)
    gmean_recommendations = zip(new_test_samples['srch_id'],
                                new_test_samples['prop_id'], gmean)

    print("Writing predictions to file")
    data_io.write_submission(mean_recommendations, submission_file='mean_result_%i.csv' % n_trian_samples)
    data_io.write_submission(gmean_recommendations, submission_file='gmean_result_%i.csv' % n_trian_samples)


if __name__ == "__main__":
    n_train_samples = 8930723
    saved_train_sample_file = 'proc_train_samples_%i.csv' % n_train_samples
    processed_train_csv_file = os.path.join(get_paths()['proc_train_path'], saved_train_sample_file)
    do_training(processed_train_csv_file)
    do_prediction(n_train_samples)
