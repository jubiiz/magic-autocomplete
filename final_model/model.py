import tensorflow as tf
from tensorflow.keras.layers import LSTM, LSTMCell, Dense, Embedding

from metadata import VOCAB_SIZE

class FullARModel(tf.keras.Model):
    def __init__(self):
        super.__init__()
        self.units = 128
        self.embedding_dim = 64
        self.embedding = Embedding(input_dim=VOCAB_SIZE, output_dim=self.embedding_dim, mask_zero=True)
        self.lstm = LSTM(self.units)
        self.lstm_cell = LSTMCell(self.units)
        self.dense = Dense(self.units, activation='relu')
        self.softmax = Dense(VOCAB_SIZE, activation='softmax')

    def __call__(self):
        pass

