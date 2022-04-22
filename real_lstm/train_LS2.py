import os
import tensorflow as tf
from gensim.models import Word2Vec
import numpy as np
import random

WV = Word2Vec.load("m3.model")
WV = WV.wv

def load_data():
    """
    returns x_train, y_train (training data)
    """
    lists = []
    lists_path = os.path.join(os.getcwd(), "../f_lists")
    lists_folder = os.scandir(lists_path)
    # for each archetype, for each deck, load all cards into a list (list of decks (list of cards (vectors)))
    for archetype in lists_folder:
        archetype_folder = os.scandir(archetype.path)
        # loops over decklists of that archetype
        for decklist in archetype_folder:
            cards = []
            # loads every card of the decklist
            with open(decklist.path, "r") as r:
                for line in r:
                    cardname = line.rstrip("\n")
                    if len(line) == 0:
                        continue
                    #appending vector, not cardname
                    cards.append(WV[cardname])
            # only keep length 60 lists
            if(len(cards) == 60):
                lists.append(np.array(cards))
            else:
                lists.append(np.array(cards[:60]))

    # randomizes lists and cuts them up into different shapes
    # make lists = many multisize lists
    # for each list, from 2 to 60, cut it to [:2] -> [:60]
    data = []
    zeros = []
    for i in range(60):
        zeros.append(np.tile([0.], 64))
    zeros = np.array(zeros)

    for l in lists:
        for i in range(59, 60):
            list_mod = np.array(l[:i])
            np.random.shuffle(list_mod)
            list_mod = np.concatenate([zeros[:60-i], list_mod])
            data.append(np.array(list_mod))
    random.shuffle(data)
    data = np.array(data)
    print("data shape: ", data.shape)

    x_train, y_train = data[:, :-1], data[:, -1]

    # turn each label into a categorical representation (one hot)
    y_train_nums = []
    print("y train card shape: ", y_train[0][0].shape)
    for card in y_train:
        name = WV.most_similar(card)[0][0]
        y_train_nums.append(F_SINGLES.index(name))

    y_train = tf.keras.utils.to_categorical(y_train_nums, num_classes=len(F_SINGLES))
    y_train = tf.reshape(y_train, [data.shape[0], 1, 578])
    x_train = tf.reshape(x_train, [data.shape[0], 1, 59, 64])

    return(x_train, y_train)

def load_conversion():
    # returns a conversion table of shape {f_name: uf_name}
    f_temp = []
    uf_temp = []
    with open("../f_singles.txt", "r") as r:
        for line in r:
            line = line.rstrip("\n")
            f_temp.append(line)
        
    with open("../uf_singles.txt", "r") as r:
        for line in r:
            line = line.rstrip("\n")
            uf_temp.append(line)

    conversion = dict(zip(f_temp, uf_temp))
    return(conversion)

CONVERSION = load_conversion()
F_SINGLES = list(CONVERSION.keys())

class MyModel(tf.keras.Model):

  def __init__(self, batch_size, units):
    super().__init__()
    self.batch_size = batch_size
    self.units = units
    self.lstm_cell1 = tf.keras.layers.LSTMCell(units)
    self.dense1 = tf.keras.layers.Dense(units, activation=tf.nn.relu)
    self.dense2 = tf.keras.layers.Dense(578,  activation=tf.nn.softmax, name="dense2")

  def call(self, inputs, training=None):
    predictions = []

    pad_num = 0

    # warmup: 
    state1= self.lstm_cell1.get_initial_state(inputs = inputs, batch_size=self.batch_size)
    #x = tf.zeros([1, self.units])
    # else just =
    state2 = state1
    inputs = tf.reshape(inputs, shape=[59, 1, 64])
    
    print("INPUTS: ", inputs)
    for input in inputs:
      
      print("INPUT: ", input)
      print("INPUT: ", input.shape)
      x, state1 = self.lstm_cell1(input, states=state1,training=training)
    
    # prediction (just 1, it's the input)
    #prediction, state2 = self.lstm_cell2(x, states=state2, training=training)
    #prediction = self.dense1(x)
    prediction = self.dense2(x)
    predictions.append(prediction)
    predictions = tf.stack(predictions)
    # taken from ts tutorial (see link above), supposedly output is in wrong shape
    predictions = tf.transpose(predictions, [1, 0, 2])

    return(predictions)



def main():    
    # load data
    x_train, y_train = load_data()
    print(x_train.shape)
    print("y_train shape: ", y_train.shape)    

    # define model
    model = MyModel(batch_size=1, units=100)
    # compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    # fit model
    print(x_train.shape)
    model.fit(x_train, y_train, batch_size=model.batch_size, epochs=1)
    #print(model.summary())
    
    # save the model to file
    print("saving")
    model.save('L300R', save_format="tf")
    print("saved")


if __name__ == "__main__":
    main()