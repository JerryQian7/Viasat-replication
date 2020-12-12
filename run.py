#!/usr/bin/env python

import sys
import json
import os
import pathlib
from pathlib import Path

import src
from src.data import collect_data
from src.data import preprocess_data
from src.features import create_features
from src.models import train_model

import logging

def main(targets):

    # Will change to test config path if test target is seen
    config_dir = 'config'
    run_all = False

    if 'all' in targets or len(targets) == 0:
        run_all = True

    if 'clean' in targets:
        # Would probably just delete the data folder... but should truly look at
        # the configuration to decide what to delete.
        raise NotImplementedError
    
    if 'test' in targets:
        # If `test` is the only target seen, then run all targets with the 
        # configs and data found in the test directory.
        #
        # Otherwise, if additional targets are specified then only run those
        # targets but still use test config (and therefore test data).
        print('Test target recognized. Will use test configuration files.')
        config_dir = 'test/config'

        if len(targets) == 1:
            print('Testing all targets: `data`, `features`, `train`.')
            run_all = True
    
    if 'data' in targets or run_all:
        # Load, clean, and preprocess data. Then store preprocessed data to
        # configured intermediate directory.
        print('Data target recognized.')

        with open(Path(config_dir, 'data-params.json'), 'r') as f:
            data_params = json.load(f)

        print('Running ETL pipeline.')
        preprocess_data(**data_params)
        print('ETL pipeline complete.')

    if 'features' in targets or run_all:
        # Creates features for preprocessed data and stores feature-engineered
        # data to a configured csv and directory.
        print('Features target recognized.')

        with open(Path(config_dir, 'features-params.json'), 'r') as f:
            features_params = json.load(f)

        print('Engineering features.')
        create_features(**features_params)
        print('Feature engineering complete.')
         
    if 'train' in targets or run_all:
        # Trains model based on feature-engineeered data, report some of its
        # scores, and save the model.
        print('Train target recognized.')

        with open(Path(config_dir, 'train-params.json'), 'r') as f:
            train_params = json.load(f)

        print('Training model.')
        train_model(**train_params)
        print('Model training complete.')

    if 'generate' in targets:
        # Generates data from network-stats
        #
        # NOTE: This target should *not* be included in `all`.
        print('Generate target recognized.')

        with open(Path(config_dir, 'generate-params.json'), 'r') as f:
            generate_params = json.load(f)

        print('Collecting data with network-stats.')
        collect_data(**generate_params)
        print('Data collection complete.')

    return

if __name__ == "__main__":
    targets = sys.argv[1:]
    main(targets)
