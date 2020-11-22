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
    with open('config/test-params.json') as f:
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
        
        get_data(generation_params)

    if 'test-data' in targets:
        
        etl(**testdata_params)
        print('test data ETL')
        
    if 'data' in targets:
        # Load, clean, and preprocess data. Then store preprocessed data to
        # intermediate directory.
        etl(**etl_params)

    if 'features' in targets:
        create_features(**feature_params)

    if 'test' in targets:

        etl(**testdata_params)
        create_features(**test_feature_params)
        train_model(**model_params)
         
    if 'train' in targets:
        train_model(**model_params)

    return



if __name__ == "__main__":
    targets = sys.argv[1:]
    main(targets)