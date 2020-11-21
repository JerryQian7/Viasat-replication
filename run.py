#!/usr/bin/env python

import sys
import json
import os

import src


def main(targets):

    if 'collect' in targets:
        with open('config/data-generation-params.json') as f:
            generation_params = json.load(f)
            src.data.generate.get_data(generation_params)
        
    if 'data' in targets:
        # Load, clean, and preprocess data. Then store preprocessed data to
        # intermediate directory.

        with open('config/data-params.json', 'r') as f:
            data_params = json.load(f)

        src.data.etl(**data_params)

    # if 'features' in targets:
    #     with open('config/features-params.json') as f:
    #         features_params = json.load(f)

    #     src.features.apply_features(**features_params)

    # if 'train' in targets:
    #     with open('config/train-params.json') as f:
    #         train_params = json.load(f)

    #     src.models.train(**train_params)

        
        
    return



if __name__ == "__main__":
    targets = sys.argv[1:]
    main(targets)