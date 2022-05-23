import os
import random
import logging

import numpy as np
import tensorflow as tf
from google.cloud import storage
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences

from .metadata import F_LISTS_DIR, F_SINGLES_PATH, AUG_INDEXES, MODELS_DIR, BUCKET_NAME


@dataclass
class XYData:
    x: np.ndarray
    y: np.ndarray


@dataclass
class TrainTestValData:
    train: XYData
    test: XYData
    val: XYData


def load_f_singles() -> list:
    """loads the card vocabulary: a list of unique cardnames"""
    _f_singles = ['padding_cardname']
    with open(F_SINGLES_PATH) as f:
        for single in f:
            _f_singles.append(single.strip('\n'))
    return _f_singles


def nums_to_cardnames(nums: np.ndarray) -> list:
    """input a list of card INDEXES, outputs a list of FORMATTED cardnames"""
    return [F_SINGLES[index] for index in nums]


def card_names_to_nums(cards: list) -> list:
    """input a list of FORMATTED cardnames, outputs a list of ints"""
    return [F_SINGLES.index(cardname) for cardname in cards]


def quantities_to_cardnums(distribution: np.ndarray) -> np.ndarray:
    """input a reduced decklist like: [4 0 0 3 0 0 2 0 1 0 0 ... 2 ... 0], outputs a decklist of cardnums"""
    cardnums = []
    for index, quantity in enumerate(distribution):
        cardnums += [index]*round(quantity)
    return np.array(cardnums)


def decklist_from_path(path: str) -> list:
    """loads a decklist as a list of formatted cardnames from a specified path"""
    decklist = []
    with open(path, "r") as f:
        for line in f:
            cardname = line.rstrip("\n")
            if len(line) == 0:
                continue
            decklist.append(cardname)
    return decklist


def load_number_decks_from_local() -> list:
    """
    loads all formatted decklists as a list of lists of numbers
    """
    logging.info("loading decklists from local source")
    decklists = []
    list_dir = os.scandir(F_LISTS_DIR)
    for archetype_dir in list_dir:
        archetype_dir = os.scandir(archetype_dir.path)
        for decklist_file in archetype_dir:
            decklist = decklist_from_path(decklist_file.path)
            # only keep length 60 lists
            # (we don't also want to have to predict the size of the list)
            decklists.append(card_names_to_nums(decklist[:60]))
    logging.info("decklists loaded, preprocessing data")
    return decklists


def load_decks_from_bucket(bucket_name: str, data_folder: str) -> list:
    logging.info("loading decklists from cloud")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    decklists = []
    for blob in bucket.list_blobs(prefix=data_folder):
        list_as_text = blob.download_as_text()
        decklist = list_as_text.strip("\n").split("\n")
        decklists.append(card_names_to_nums(decklist[:60]))
    logging.info("decklists loaded")
    return decklists


def load_f_singles_from_bucket(bucket_name: str, path_to_f_singles: str) -> list:
    logging.info("loading formatted singles from cloud")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    _f_singles = ['padding_cardname']
    singles_text = bucket.blob(path_to_f_singles).download_as_text()
    _f_singles += singles_text.strip("\n").split("\n")
    return _f_singles


def train_test_val_split(data: list, train_len=0.7, test_len=0.2, val_len=0.1) -> tuple:
    """
    Takes a list of decks (lists of ints) as input,
    Splits it in proportions defined by train_len, test_len, val_len (1-train_len-test_len, implied)
    Returns a tuple containing the three lists of data
    """
    train_data, test_data = train_test_split(data, test_size=(test_len+val_len), random_state=42)
    test_data, val_data = train_test_split(test_data, test_size=(val_len/(test_len+val_len)), random_state=42)
    return train_data, test_data, val_data


def get_aug_inputs_and_labels(decklists) -> XYData:
    """
    Takes as input a list of decklists
    Augments the data and splits it into input/label pairs
    Returns a tuple containing two np.array: padded input decklists and padded label decklists
    """
    inputs = []
    labels = []
    for decklist in decklists:
        for index in AUG_INDEXES:
            inputs.append(decklist[:index])
            labels.append(decklist[:])  # 60 cards is what model needs
    padded_inputs = pad_sequences(inputs, maxlen=59, padding='pre', dtype=np.float32)
    reduced_categorical_labels = process_labels(labels)
    return XYData(x=padded_inputs, y=reduced_categorical_labels)


def process_labels(labels) -> np.ndarray:
    labels = np.array(labels, dtype=np.float32)
    categorical_labels = tf.keras.utils.to_categorical(labels, num_classes=579)
    reduced_categorical_labels = tf.reduce_sum(categorical_labels, 1).numpy()
    return reduced_categorical_labels


def load_model(name: str = 'mymodel') -> tf.keras.models.Model:
    path_to_model = os.path.join(MODELS_DIR, name)
    return tf.keras.models._load_model(path_to_model)


if os.getenv('AIP_MODEL_DIR'):  # then we're probably on the cloud
    F_SINGLES = load_f_singles_from_bucket(BUCKET_NAME, 'data/f_singles.txt')
else:
    F_SINGLES = load_f_singles()


if __name__ == "__main__":
    mydata = load_number_decks_from_local()
    print(mydata)
    train, test, val = train_test_val_split(mydata)
    aug_train = get_aug_inputs_and_labels(train)
    print(aug_train)

