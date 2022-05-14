import os
import logging
import argparse

import hypertune  # package name is cloudml-hypertune
from metadata import F_SINGLES_PATH, UNF_SINGLES_PATH, F_LISTS_DIR, UNF_LISTS_DIR, BUCKET_NAME
import numpy as np
import tensorflow as tf
from utils import load_f_decks_from_bucket, train_test_val_split, get_aug_inputs_and_labels, TrainTestValData
from model import FullARModel, compile_and_fit


def task():
    args = get_args()
    logging.info("arguments used: ", args)
    logging.info("loading decklists")

    if 'AIP_MODEL_DIR' in os.environ:
        output_directory = os.environ['AIP_MODEL_DIR']
    else:
        output_directory = "model"

    decklists = load_f_decks_from_bucket(BUCKET_NAME, 'data/f_lists')
    logging.info("decklists loaded, preprocessing data")

    raw_train, raw_test, raw_val = train_test_val_split(decklists)

    all_data = TrainTestValData(
        train=get_aug_inputs_and_labels(raw_train),
        test=get_aug_inputs_and_labels(raw_test),
        val=get_aug_inputs_and_labels(raw_val))

    logging.info("data preprocessed, compiling and training model")
    model = FullARModel(num_units=args.num_units, extra_dense=args.extra_dense)
    history = compile_and_fit(model, all_data, epochs=args.num_epochs,
                              batch_size=args.batch_size)
    #model.summary()

    tf.keras.models.save_model(model, output_directory)  # add gcp export path
    print("saved")
    logging.info('saved')

    if args.hptune:
        # Define metric
        hp_metric = history.history['val_matching_pairs_percent'][-1]

        hpt = hypertune.HyperTune()
        hpt.report_hyperparameter_tuning_metric(
            hyperparameter_metric_tag='val_matching_pairs_percent',
            metric_value=hp_metric,
            global_step=args.num_epochs)


def get_args():
    args_parser = argparse.ArgumentParser()

    args_parser.add_argument(
        '--batch-size',
        default=64,
        type=int,
    )
    args_parser.add_argument(
        '--num-epochs',
        default=5,
        type=int,
    )
    args_parser.add_argument(
        '--num-units',
        default=128,
        type=int,
    )
    args_parser.add_argument(
        '--extra-dense',
        help='True: add an extra dense layer in the model, default is false',
        default=False,
        type=bool,
    )
    # Saved model arguments
    args_parser.add_argument(
        '--job-dir',
        default=os.getenv('AIP_MODEL_DIR'),
        help='GCS location to export models')
    args_parser.add_argument(
        '--model-name',
        default="ht-magic-autocomplete",
        help='The name of your saved model')
    args_parser.add_argument(
        '--hptune',
        default=False,
        help='hypertuning, disabled by default')

    return args_parser.parse_args()


if __name__ == "__main__":
    # tf.config.run_functions_eagerly(True)
    task()
