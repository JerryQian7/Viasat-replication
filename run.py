#!/usr/bin/env python

import sys
import json
import os

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/features')
sys.path.insert(0, 'src/models')

from etl import etl
from generate import get_data
from features import create_features
from train import train_model

def main(targets):

    with open('config/data-generation-params.json') as f:
        generation_params = json.load(f)
    with open('config/test-etl-params.json') as f:
        testdata_params = json.load(f)
    with open('config/etl-params.json') as f:
        etl_params = json.load(f)
    with open('config/feature-params.json') as f:
        feature_params = json.load(f)
    with open('config/model-params.json') as f:
        model_params = json.load(f)
    with open('config/test-feature-params.json') as f:
        test_feature_params = json.load(f)

    if 'generate' in targets:
        # Generates data from network-stats
        get_data(generation_params)
        print('Data generated from network-stats.')

    if 'test-data' in targets:
        # Load, clean and preprocess test data. Then store preprocessed data to data/preprocessed
        etl(**testdata_params)
        print('Test Data ETL Finished.')
        print('Outputting preprocessed data to %s' % testdata_params['out_dir'])
        
    if 'data' in targets:
        # Load, clean, and preprocess data. Then store preprocessed data to data/preprocessed
        etl(**etl_params)
        print('Data ETL Finished.')

    if 'features' in targets:
        # Creates features for preprocessed data and stores feature-engineered data to data/features
        create_features(**feature_params)
        print("Feature engineering finished.")

    if 'test' in targets:
        # Runs all targets on test data
        etl(**testdata_params)
        print('Test Data ETL Finished.')
        print('Outputting preprocessed data to %s' % testdata_params['out_dir'])
        create_features(**test_feature_params)
        print("Feature engineering finished.")
        print('Outputting feature engineered data to %s' % test_feature_params['out_dir'])
        train_model(**model_params)
        print("Model training finished.")
         
    if 'train' in targets:
        # Trains model based on feature-engineeered data
        train_model(**model_params)
        print("Model training finished.")

    return



if __name__ == "__main__":
    targets = sys.argv[1:]
    main(targets)