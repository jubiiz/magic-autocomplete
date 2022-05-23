import os
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from keras.preprocessing.sequence import pad_sequences

from main_package.scripts.metadata import MODELS_DIR
from main_package.scripts.model import MatchingPairsPercent
from main_package.scripts.utils import load_number_decks_from_local, process_labels, train_test_val_split


def _plot_scores(scores: dict) -> None:
    """
    ugly plot scores, to redo
    """
    num_known = list(scores.keys())
    score = list(scores.values())
    fig, ax = plt.subplots(1, 1)
    ax.bar(num_known, score)
    ax.set_ylim(0, 1)
    ax.set_title("Final test model #19 (300 epochs)")
    ax.set_xlabel("Number of Known Cards")
    ax.set_ylabel("Matching Pairs Percent")
    plt.show()


def _get_matching_pairs_percentage(prediction: np.ndarray, label: np.ndarray) -> float:
    rounded_prediction = tf.math.round(prediction)
    matching_pairs = tf.math.minimum(rounded_prediction, label)
    matching_ratio = tf.math.reduce_sum(matching_pairs)/60  # 60 being the number of cards in the labels list
    return matching_ratio.numpy()


def _load_model(name: str = 'best_19') -> tf.keras.models.Model:
    print('loading model')
    path_to_model = os.path.join(MODELS_DIR, name)
    print('path to model used: ', path_to_model)
    model = tf.keras.models.load_model(path_to_model, custom_objects=MatchingPairsPercent)
    model.summary()
    return model


def _load_test_zip() -> zip:
    print('loading data')
    decklists = load_number_decks_from_local()
    _, __, val_data = train_test_val_split(decklists)
    processed_labels = process_labels(decklists)
    test_set = zip(decklists, processed_labels)
    return test_set


def _get_evaluation_scores_per_slice(indexes: list, model: tf.keras.models.Model, test_set) -> dict:
    scores = {index: 0 for index in indexes}
    num_decklists = 0
    for input_decklist, label_decklist in test_set:
        print(num_decklists)
        num_decklists += 1
        for index in indexes:
            sliced_input = input_decklist[:index]
            padded_input = pad_sequences([sliced_input], maxlen=59, padding='pre', dtype=np.float32)
            prediction = model(padded_input)
            matching_ratio = _get_matching_pairs_percentage(prediction, label_decklist)
            scores[index] += matching_ratio
    averaged_scores = {index: score / num_decklists for index, score in scores.items()}
    return averaged_scores


def main():
    test_set = _load_test_zip()
    model = _load_model('best_19')
    averaged_scores = _get_evaluation_scores_per_slice(indexes=list(range(1, 60)), model=model, test_set=test_set)
    print('averaged scores: ', averaged_scores)
    _plot_scores(averaged_scores)
    print('Done.')


if __name__ == "__main__":
    main()
