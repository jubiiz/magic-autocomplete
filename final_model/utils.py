import os
import random

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences
from dataclasses import dataclass

from metadata import F_LISTS_DIR, F_SINGLES_PATH, AUG_INDEXES


@dataclass
class XYData:
    x: np.ndarray
    y: np.ndarray


@dataclass
class TrainTestValData:
    train: XYData
    test: XYData
    val: XYData


def load_f_singles() -> list[str]:
    """loads the card vocabulary: a list of unique cardnames"""
    _f_singles = ['padding_cardname']
    with open(F_SINGLES_PATH) as f:
        for single in f:
            _f_singles.append(single.strip('\n'))
    return _f_singles


def load_unf_singles():
    # TODO
    pass


def nums_to_cardnames(nums: list[int]) -> list[str]:
    """input a list of card INDEXES, outputs a list of FORMATTED cardnames"""
    return [F_SINGLES[index] for index in nums]


def cardnames_to_nums(cards: list[str]) -> list[int]:
    """input a list of FORMATTED cardnames, outputs a list of ints"""
    return [F_SINGLES.index(cardname) for cardname in cards]


def quantities_to_cardnums(distribution) -> list:
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


def load_decklists() -> list[list[int]]:
    """
    loads all formatted decklists as a list of lists of numbers
    """
    decklists = []
    f_lists_dir = os.scandir(F_LISTS_DIR)
    for archetype_obj in f_lists_dir:
        archetype_dir = os.scandir(archetype_obj.path)
        for decklist_obj in archetype_dir:
            decklist = decklist_from_path(decklist_obj.path)
            # only keep length 60 lists
            # (we don't also want to have to predict the size of the list)
            if len(decklist) == 60:
                decklists.append(cardnames_to_nums(decklist))
            else:
                decklists.append(cardnames_to_nums(decklist[:60]))
    return decklists


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
    labels = np.array(labels, dtype=np.float32)
    categorical_labels = tf.keras.utils.to_categorical(labels, num_classes=579)
    reduced_categorical_labels = tf.reduce_sum(categorical_labels, 1).numpy()
    return XYData(x=padded_inputs, y=reduced_categorical_labels)


F_SINGLES = load_f_singles()
# UNF_SINGLES = load_unf_singles()

if __name__ == "__main__":
    mydata = load_decklists()
    train, test, val = train_test_val_split(mydata)
    aug_train = get_aug_inputs_and_labels(train)
    print(aug_train)

