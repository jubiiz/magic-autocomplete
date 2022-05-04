import numpy as np
import tensorflow as tf
from utils import TrainTestValData, XYData
from tensorflow.keras.layers import LSTM, LSTMCell, Dense, Embedding

from metadata import VOCAB_SIZE


class FullARModel(tf.keras.Model):
    # good chunks taken from
    # https://www.tensorflow.org/tutorials/structured_data/time_series#advanced_autoregressive_model
    def __init__(self):
        super().__init__()
        self.units = 128
        self.embedding_dim = 64
        self.embedding = Embedding(input_dim=VOCAB_SIZE, output_dim=self.embedding_dim, mask_zero=True)
        self.lstm = LSTM(self.units, return_state=True)
        self.lstm_cell = LSTMCell(self.units)
        self.dense = Dense(self.units, activation='relu')
        self.softmax = Dense(VOCAB_SIZE, activation='softmax')

    def _warmup(self, inputs):
        # inputs.shape => (batch, time, features)
        # x.shape => (batch, lstm_units)
        #tf.print("these are the inputs: ", inputs)
        embedded = self.embedding(inputs)
        mask = self.embedding.compute_mask(inputs)
        #tf.print(mask)
        x, *states = self.lstm(embedded, mask=mask)
        # predictions.shape => (batch, vocab_size)
        prediction = self._deep_layers(x)
        return prediction, states

    def _deep_layers(self, x):
        deep = self.dense(x)
        softmax_output = self.softmax(deep)
        return softmax_output

    def call(self, inputs, training=None):
        predictions = []

        prediction, states = self._warmup(inputs)

        predictions.append(prediction)

        for i in range(59):
            previous_num = tf.cast(tf.argmax(prediction, axis=1), tf.dtypes.float32)
            lstm_input = self.embedding(previous_num)
            x, states = self.lstm_cell(lstm_input, states=states, training=training)
            prediction = self._deep_layers(x)
            predictions.append(prediction)

        predictions = tf.stack(predictions)
        predictions = tf.transpose(predictions, [1, 0, 2])
        predictions = tf.cast(predictions, dtype=tf.dtypes.float32)
        return predictions


def compile_and_fit(model, all_data: TrainTestValData, epochs=2, patience=10):
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                      patience=patience,
                                                      mode='min')

    model.compile(loss=tf.losses.SparseCategoricalCrossentropy(),
                  optimizer=tf.optimizers.Adam(),
                  metrics=[])

    history = model.fit(tf.data.Dataset.from_tensor_slices((all_data.train.x, all_data.train.y)).batch(32), epochs=epochs,
                        validation_data=(all_data.val.x, all_data.val.y),
                        callbacks=[early_stopping])
    return history
