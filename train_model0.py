import tensorflow as tf
from matplotlib import pyplot as plt
from gensim.models import Word2Vec
import numpy as np
import os

# created with help from https://www.tensorflow.org/tutorials/structured_data/time_series
class WindowCreator():
    def __init__(self, input_width, label_width, shift, train_df,
                val_df, test_df, label_columns=None):
        self.train_df = train_df
        self.val_df = val_df
        self.test_df = test_df

         # Work out the label column indices.
        self.label_columns = label_columns
        if label_columns is not None:
            self.label_columns_indices = {name: i for i, name in enumerate(label_columns)}
            self.column_indices = {name: i for i, name in enumerate(train_df.columns)}

            # Work out the window parameters.
        self.input_width = input_width
        self.label_width = label_width
        self.shift = shift

        self.total_window_size = input_width + shift

        self.input_slice = slice(0, input_width)
        self.input_indices = np.arange(self.total_window_size)[self.input_slice]

        self.label_start = self.total_window_size - self.label_width
        self.labels_slice = slice(self.label_start, None)
        self.label_indices = np.arange(self.total_window_size)[self.labels_slice]

    def __repr__(self):
        return '\n'.join([
            f'Total window size: {self.total_window_size}',
            f'Input indices: {self.input_indices}',
            f'Label indices: {self.label_indices}',
            f'Label column name(s): {self.label_columns}'])

def load_vectors(singles_path, vec_path, wv):        
    """
    creates a mapping of the card names to their corresponding vector
    """
    mapping ={}

    with open(singles_path, "r") as r:
        for card in r:
            card = card.rstrip()
            mapping[card] = wv.wv[card]

    return(mapping)

def main():
    # map cards to their index, into a dictionary
    # need txt file maping cards to their vectors
    # list of vectors, in order of card mapping

    singles_path = "f_singles.txt"
    vec_path = "vec_map.txt"
    wv_model_path = "w2v_models/m3.model"

    # loads model into memory, vec_map being a mapping of cardname:vector
    wv = Word2Vec.load(wv_model_path)
    vec_map = wv.wv



if __name__ == "__main__":
    main()

"""
# model compile info

model.compile(loss=tf.losses.MeanSquaredError(),
                optimizer=tf.optimizers.Adam(),
                metrics=[tf.metrics.MeanAbsoluteError()])
"""