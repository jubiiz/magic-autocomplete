import os
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from keras.preprocessing.sequence import pad_sequences

from main_package.trainer.metadata import AUG_INDEXES, MODELS_DIR
from main_package.trainer.utils import load_decklists, process_labels, train_test_val_split


def plot_scores(scores):
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


def percent_matching_pairs(prediction, label):
    rounded_prediction = tf.math.round(prediction)
    matching_pairs = tf.math.minimum(rounded_prediction, label)
    matching_ratio = tf.math.reduce_sum(matching_pairs)/60  # 60 being the number of cards in the labels list
    return matching_ratio.numpy()


class MatchingPairsPercent(tf.keras.metrics.Metric):
    # custom metric training code found here: https://www.tensorflow.org/guide/keras/train_and_evaluate#custom_metrics
    def __init__(self, name='matching_pairs_percent', **kwargs):
        super(MatchingPairsPercent, self).__init__(name=name, **kwargs)
        self.matching_pairs_percent = self.add_weight(name='mpp', initializer='zeros')
        self.num_predictions = self.add_weight(name='num_preds', initializer='zeros')

    def update_state(self, y_true, y_pred, sample_weight=None):
        rounded_prediction = tf.math.round(y_pred)
        matching_pairs = tf.math.minimum(y_true, rounded_prediction)
        num_matching_pairs = tf.math.reduce_sum(matching_pairs, axis=1)
        avg_matching_pairs = tf.math.reduce_mean(num_matching_pairs)
        self.matching_pairs_percent.assign_add(avg_matching_pairs / 60)  # 60 cards in a deck
        self.num_predictions.assign_add(1)

    def result(self):
        return self.matching_pairs_percent / self.num_predictions

    def reset_state(self):
        # The state of the metric will be reset at the start of each epoch.
        self.matching_pairs_percent.assign(0.0)
        self.num_predictions.assign(0.0)


def load_model(name: str = 'best_3') -> tf.keras.models.Model:
    path_to_model = os.path.join(MODELS_DIR, name)
    print(path_to_model)
    return tf.keras.models.load_model(path_to_model, custom_objects={'MatchingPairsPercent': MatchingPairsPercent})


def main():
    decklists = load_decklists()
    _, __, val_data = train_test_val_split(decklists)
    processed_labels = process_labels(decklists)
    test_set = zip(decklists, processed_labels)

    print('loading model')

    model = load_model('best_19')
    model.summary()
    indexes = list(range(1, 60))
    scores = {index: 0 for index in indexes}
    num_decklists = 0

    for input_decklist, label_decklist in test_set:
        print(num_decklists)
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
