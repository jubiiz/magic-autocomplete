import tensorflow as tf
from keras.sequences import pad_sequences

from metadata import AUG_INDEXES
from utils import load_decklists, process_labels, load_model


def percent_matching_pairs(prediction, label):
    prediction = tf.math.round(prediction)


def main():
    decklists = load_decklists()
    processed_labels = process_labels(decklists)
    test_set = dict(zip(decklists, processed_labels))

    model = load_model(name='mymodel')
    indexes = list(range(1, 60))
    scores = {index:0 for index in indexes}

    for input_decklist, label_decklist in test_set.items():
        for index in indexes:
            sliced_input = input_decklist[:index]
            padded_input = pad_sequences([sliced_input], maxlen=59, padding='pre', dtype=np.float32)
            prediction = model(padded_input)
            percent_matching_pairs = percent_matching_pairs(prediction, label_decklist)

if __name__ == "__main__":
    main()