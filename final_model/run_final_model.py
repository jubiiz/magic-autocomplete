import os
import argparse

from metadata import F_SINGLES_PATH, UNF_SINGLES_PATH, F_LISTS_DIR, UNF_LISTS_DIR
import numpy as np
import tensorflow as tf
from utils import load_decklists, train_test_val_split, get_aug_inputs_and_labels, TrainTestValData
from model import FullARModel, compile_and_fit


def run():
    args = get_args()

    decklists = load_decklists()
    raw_train, raw_test, raw_val = train_test_val_split(decklists)

    all_data = TrainTestValData(
        train=get_aug_inputs_and_labels(raw_train),
        test=get_aug_inputs_and_labels(raw_test),
        val=get_aug_inputs_and_labels(raw_val))

    model = FullARModel()
    history = compile_and_fit(model, all_data)
    model.summary()

    tf.keras.models.save_model(model, 'model/mymodel')
    print("saved")


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
        '--hp-tune',
        default=False,
        type=bool,
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

    return args_parser.parse_args()


if __name__ == "__main__":
    # tf.config.run_functions_eagerly(True)
    run()
