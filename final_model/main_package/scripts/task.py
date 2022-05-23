import os
import logging
import argparse
from argparse import Namespace


import tensorflow as tf

from .model import FullARModel, compile_and_fit
from .metadata import BUCKET_NAME, BUCKET_DATA_PREFIX
from .utils import load_number_decks_from_local, load_decks_from_bucket, train_test_val_split, get_aug_inputs_and_labels,\
                   TrainTestValData


def _build_cloud_model(args: Namespace):
    unprocessed_data = load_decks_from_bucket(BUCKET_NAME, BUCKET_DATA_PREFIX)
    prepared_data = _prepare_data(unprocessed_data)
    history = _make_train_save_model(prepared_data, args)
    _report_metric_to_google(args, history)


def _build_local_model(args: Namespace):
    unprocessed_data = load_number_decks_from_local()
    prepared_data = _prepare_data(unprocessed_data)
    _make_train_save_model(prepared_data, args)


def _prepare_data(data: list):
    logging.info("preprocessing data")
    raw_train, raw_test, raw_val = train_test_val_split(data)
    all_data = TrainTestValData(
        train=get_aug_inputs_and_labels(raw_train),
        test=get_aug_inputs_and_labels(raw_test),
        val=get_aug_inputs_and_labels(raw_val))
    logging.info("data preprocessed")
    return all_data


def _make_train_save_model(all_data: TrainTestValData, args: Namespace):
    logging.info("compiling and training model")
    model = FullARModel(num_units=args.num_units, extra_dense=args.extra_dense)
    history = compile_and_fit(model, all_data, epochs=args.num_epochs, batch_size=args.batch_size,
                              checkpoint_filepath=os.path.join(args.output_directory, 'checkpoints'))
    # model.summary()
    _save_named_model(model, args)
    logging.info("model saved in path: ", args.output_directory)

    return history


def _save_named_model(model: tf.keras.models.Model, args: Namespace):
    model_path = os.path.join(args.output_directory, args.model_name)
    tf.keras.models.save_model(model, model_path)
    logging.info('model saved in path: ', model_path)


def _report_metric_to_google(args: Namespace, history):
    import hypertune
    hypertuning_metric = max(history.history['val_matching_pairs_percent'])
    hpt = hypertune.HyperTune()
    hpt.report_hyperparameter_tuning_metric(
        hyperparameter_metric_tag='val_matching_pairs_percent',
        metric_value=hypertuning_metric,
        global_step=args.num_epochs)


def _get_args():
    args_parser = argparse.ArgumentParser()
    # tunable hyperparameters
    args_parser.add_argument(
        '--batch-size',
        default=64,
        type=int,
        help='size of a batch of data',
    )
    args_parser.add_argument(
        '--num-epochs',
        default=5,
        type=int,
        help='number of epochs during which the model is trained',
    )
    args_parser.add_argument(
        '--num-units',
        default=128,
        type=int,
        help='number of units in each deep layer of the neural network',
    )
    args_parser.add_argument(
        '--extra-dense',
        default=False,
        type=bool,
        help='True: add an extra dense layer in the model, default is false',
    )
    # Saved model arguments
    args_parser.add_argument(
        '--model-name',
        default="ht-magic-autocomplete",
        help='The name of the saved model')
    args_parser.add_argument(
        '--gcloud-training',
        default=False,
        help='hypertuning, disabled by default')
    args_parser.add_argument(
        '--output-directory',
        default=os.getenv('AIP_MODEL_DIR'),
        help='directory to which model is saved, defaults to Google Cloud Storage bucket location for online training')

    return args_parser.parse_args()


def main():
    """
    Entry point function to create, train and save a model capable of predicting Magic: the Gathering decklists from
    a subset of those lists. All necessary parameters are defined via arguments.
    """
    args = _get_args()
    print(args)
    logging.info("arguments used: ", args)
    if args.gcloud_training:
        logging.info("initiating cloud training sequence")
        _build_cloud_model(args)
    else:
        logging.info("initiating local training sequence")
        _build_local_model(args)


if __name__ == "__main__":
    # tf.config.run_functions_eagerly(True)  # makes debugging easier
    main()
