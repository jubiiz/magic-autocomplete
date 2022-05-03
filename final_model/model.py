import tensorflow as tf
from tensorflow.keras.layers import LSTM, LSTMCell, Dense, Embedding

from metadata import VOCAB_SIZE

class FullARModel(tf.keras.Model):
    def __init__(self):
        super.__init__()
        self.units = 128
        self.embedding_dim = 64
        self.embedding = Embedding(input_dim=VOCAB_SIZE, output_dim=self.embedding_dim, mask_zero=True)
        self.lstm = LSTM(self.units, return_state=True)
        self.lstm_cell = LSTMCell(self.units)
        self.dense = Dense(self.units, activation='relu')
        self.softmax = Dense(VOCAB_SIZE, activation='softmax')

    def warmup(self, inputs):
        # taken from https://www.tensorflow.org/tutorials/structured_data/time_series#advanced_autoregressive_model
        # inputs.shape => (batch, time, features)
        # x.shape => (batch, lstm_units)
        embedded = self.embedding(inputs, mask_zero=True)
        mask = embedded._keras_mask
        tf.print(mask)
        x, *state = self.lstm_rnn(embedded)
        # predictions.shape => (batch, vocab_size)
        prediction = self.deep_layers(x)
        return prediction, state

    def deep_layers(self, x):
        deep = self.dense(x)
        prediction = self.softmax(deep)
        return prediction

    def call(self, inputs, training=None):
        predictions = []

        prediction, states = self.warmup(inputs)

        predictions.append(prediction)

        for i in

