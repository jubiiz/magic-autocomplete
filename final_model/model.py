import numpy as np
import tensorflow as tf
from utils import TrainTestValData, XYData
from tensorflow.keras.layers import RNN, LSTMCell, Dense, Embedding

from metadata import VOCAB_SIZE


class FullARModel(tf.keras.Model):
    # good chunks taken from
    # https://www.tensorflow.org/tutorials/structured_data/time_series#advanced_autoregressive_model
    def __init__(self, num_units=128, extra_dense=False):
        super().__init__()
        self.units = num_units
        self.embedding_dim = 64
        self.embedding = Embedding(input_dim=VOCAB_SIZE, output_dim=self.embedding_dim, mask_zero=True)
        self.lstm_cell = LSTMCell(self.units)
        self.lstm = RNN(self.lstm_cell, return_state=True)
        self.dense = Dense(self.units, activation='relu')
        self.extra_dense = extra_dense
        if self.extra_dense:
            self.extra_dense_layer = Dense(self.units, activation='relu', name='extra_dense_layer')
        self.softmax = Dense(VOCAB_SIZE, activation='softmax')

    def _warmup(self, inputs):
        # inputs.shape => (batch, time, features)
        # x.shape => (batch, lstm_units)
        embedded = self.embedding(inputs)
        mask = self.embedding.compute_mask(inputs)
        x, *states = self.lstm(embedded, mask=mask)
        # predictions.shape => (batch, vocab_size)
        prediction = self._deep_layers(x)
        return prediction, states

    def _deep_layers(self, x):
        deep = self.dense(x)
        if self.extra_dense:
            deep = self.extra_dense_layer(deep)
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
        reduced_predictions = tf.reduce_sum(predictions, 1)
        return reduced_predictions


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


def compile_and_fit(model, all_data: TrainTestValData, epochs=10, batch_size=64,
                    checkpoint_filepath='checkpoints'):
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_filepath,
                                                             monitor='val_matching_pairs_percent',
                                                             verbose=1,
                                                             save_best_only=True,
                                                             save_weights_only=False,
                                                             mode='max',
                                                             save_freq='epoch')

    mse = tf.keras.losses.MeanSquaredError

    model.compile(loss=tf.losses.MeanSquaredError(),
                  optimizer=tf.optimizers.Adam(),
                  metrics=[mse(), MatchingPairsPercent()])

    history = model.fit(tf.data.Dataset.from_tensor_slices((all_data.train.x, all_data.train.y)).batch(batch_size),
                        epochs=epochs,
                        validation_data=(all_data.test.x, all_data.test.y),
                        callbacks=[checkpoint_callback],
                        verbose=2)  # verbose = 2 one line per epoch 0 is silent
    return history
