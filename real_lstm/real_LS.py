# this method tries to use LSTM networks in a more conventional way
# this file contains functions to train and test the neural network. 
# useful link: https://www.tensorflow.org/api_docs/python/tf/keras/Model?version=nightly
# program architecture inspired by https://www.tensorflow.org/tutorials/structured_data/time_series#1_indexes_and_offsets

import numpy as np
import os
import tensorflow as tf
from gensim.models import Word2Vec
from utils import DataUtil

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


  def make_dataset(data):
    """
    for each list in data,
      perform n splits (split data into input and label along n points)
      for each augmented input/label pair: convert inputs to vectors, 
        convert labels to one-hot
      pad inputs to size 59 with null vectors
      append input/label pair to new data
    turn new data to dataset
    """
    splits = [1, 5, 15, 25, 35, 45, 55, 59]
    new_data = []
    for decklist in data:
      # checks if list is size 60
      if len(decklist) != 60:
        raise ValueError(f'decklist must be size 60, instead is size {len(decklist)}')
      
      # perform each of n split as a new decklist
      for split_index in splits:
        inputs = decklist[:split_index+1]
        labels = decklist[split_index+1:]

        # convert inputs to vectors, then pad to len 60
        inputs = DataUtil.inputs_to_vec(inputs, WV)
        #TODO


def compile_and_fit(model, deck_manager):
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  history = model.fit(deck_manager.x_train, deck_manager.y_train, batch_size=model.batch_size, epochs=300)
  return(history)

class MyModel(tf.keras.Model):

  def __init__(self, batch_size):
    super().__init__()
    self.batch_size = batch_size
    self.lstm_cell1 = tf.keras.layers.LSTMCell(100)
    self.lstm_cell2 = tf.keras.layers.LSTMCell(100)
    self.dense1 = tf.keras.layers.Dense(100, activation=tf.nn.relu)
    self.dense2 = tf.keras.layers.Dense(578, activation=tf.nn.softmax)

  def call(self, inputs, training=None):
    predictions = []

    pad_num = 0

    # warmup: 
    state1= self.lstm_cell1.get_initial_state(inputs = inputs, batch_size=self.batch_size)
    # else just =
    state2 = self.lstm_cell2.get_initial_state(inputs =inputs, batch_size=self.batch_size)
    for input in inputs:
      print(input)
      x, state1 = self.lstm_cell1(input, states=state1,training=training)
      x, state2 = self.lstm_cell2(x, states=state2, training=training)
      x = self.dense1(x)
      x = self.dense2(x)
    
    # prediction (just 1, it's the input)
    predictions.append(x)
    predictions = tf.stack(predictions)
    # taken from ts tutorial (see link above), supposedly output is in wrong shape
    predictions = tf.transpose(predictions, [1, 0, 2])

    return(predictions)

model = MyModel()