import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from keras.preprocessing.sequence import pad_sequences

from metadata import AUG_INDEXES
from utils import load_decklists, process_labels, load_model


def plot_scores(scores):
    """
    ugly plot scores, to redo
    """
    num_known = list(scores.keys())
    score = list(scores.values())
    fig, ax = plt.subplots(1, 1)

    ax.bar(num_known, score)
    ax.set_ylim(0, 1)
    ax.set_title("Final test model #1 (60 epochs)")
    ax.set_xlabel("Number of Known Cards")
    ax.set_ylabel("Accuracy Ratio")
    plt.show()


def percent_matching_pairs(prediction, label):
    rounded_prediction = tf.math.round(prediction)
    matching_pairs = tf.math.minimum(rounded_prediction, label)
    matching_ratio = tf.math.reduce_sum(matching_pairs)/60  # 60 being the number of cards in the labels list
    return matching_ratio.numpy()


def main():
    decklists = load_decklists()
    processed_labels = process_labels(decklists)
    test_set = zip(decklists, processed_labels)

    model = load_model(name='mymodel')
    indexes = list(range(1, 60))
    scores = {index: 0 for index in indexes}
    num_decklists = 0

    for input_decklist, label_decklist in test_set:
        num_decklists += 1
        for index in indexes:
            sliced_input = input_decklist[:index]
            padded_input = pad_sequences([sliced_input], maxlen=59, padding='pre', dtype=np.float32)
            prediction = model(padded_input)
            matching_ratio = percent_matching_pairs(prediction, label_decklist)
            scores[index] += matching_ratio

    averaged_scores = {index: score/num_decklists for index, score in scores.items()}
    print(averaged_scores)
    plot_scores(averaged_scores)
    print('Done.')


if __name__ == "__main__":
    main()
