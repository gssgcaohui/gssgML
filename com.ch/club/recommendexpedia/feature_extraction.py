#!/usr/bin/ env python
# coding:utf-8


def extract_features:
    ## 1 price_usd processing
    price_usd_series = samples_in_one_srch['price_usd']
    # 1.1 normalization of price_usd
    norm_price_usd_series = normalize_series(price_usd_series)
    # 1.2 mean value of price_usd 拿均值
    mean_price_usd_series = price_usd_series.mean()
    # 1.3 standard deviation of price_usd   拿方差
    std_price_usd_series = price_usd_series.std()
    # 1.4 median value of price_usd 拿中位数
    median_price_usd_series = price_usd_series.median()

    ## 2 orig_destination_distance processing
    orig_destination_distance = samples_in_one_srch['orig_destination_distance']
    # 2.1 normalization of orig_destination_distance
    norm_destination_distance_series = normalize_series(orig_destination_distance_series)
    # 2.2 mean value of orig_destination_distance
    mean_destination_distance_series = orig_destination_distance_series.mean()
    # 2.3 standard deviation of orig_destination_distance
    std_destination_distance_series = orig_destination_distance_series.std()
    # 2.4 median value of orig_destination_distance
    median_destination_distance_series = orig_destination_distance_series.median()

    ## update samples
    ext_samples_in_one_srch = samples_in_one_srch.copy()
    # replace price_usd and orig_destination_distance with normalized ones
    ext_samples_in_one_srch['price_usd'] = norm_price_usd_series
    ext_samples_in_one_srch['orig_destination_distance'] = norm_destination_usd_series


