# this method tries to use LSTM networks in a more conventional way
# this file contains functions to train and test the neural network. 
# useful link: https://www.tensorflow.org/api_docs/python/tf/keras/Model?version=nightly
# program architecture inspired by https://www.tensorflow.org/tutorials/structured_data/time_series#1_indexes_and_offsets

import numpy as np
import os
import tensorflow as tf
from gensim.models import Word2Vec
from utils import load_data, split_data, augment_data

WV = Word2Vec.load("w2v_models/m3.model")
WV = WV.wv

lists_path = os.path.join(os.getcwd(), f"..{os.sep}f_lists")

class Decklists_manager:
  def __init__(self, train_names, test_names, val_names):
    self.train_names = train_names
    self.test_names = test_names
    self.val_names = val_names

    # a list containing the number of known cards into which a list will be split
    # here, every list is augmented into len(self.known_list_sizes) different pairs of input/label
    self.known_list_sizes = [1, 5, 15, 25, 35, 45, 55, 59]

  


class MyModel(tf.keras.Model):

  def __init__(self):
    super().__init__()
    self.dense1 = tf.keras.layers.Dense(4, activation=tf.nn.relu)
    self.dense2 = tf.keras.layers.Dense(5, activation=tf.nn.softmax)
    self.dropout = tf.keras.layers.Dropout(0.5)

  def call(self, inputs, training=False):
    x = self.dense1(inputs)
    if training:
      x = self.dropout(x, training=training)
    return self.dense2(x)

model = MyModel()