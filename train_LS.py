import os
import tensorflow as tf
from gensim.models import Word2Vec
import numpy as np
import random

WV = Word2Vec.load("w2v_models/m3.model")
WV = WV.wv

def load_data():
    """
    returns x_train, y_train (training data)
    """
    lists = []
    lists_path = os.path.join(os.getcwd(), "f_lists")
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
        for i in range(2, 60):
            list_mod = np.array(l[:i])
            np.random.shuffle(list_mod)
            list_mod = np.concatenate([zeros[:60-i], list_mod])
            data.append(np.array(list_mod))
    random.shuffle(data)
    data = np.array(data)
    print("data shape: ", data.shape)

    x_train, y_train = data[:, :-1], data[:, -1]

        # turn each card into a 
    y_train_nums = []
    for card in y_train:
        name = WV.most_similar(card)[0][0]
        y_train_nums.append(F_SINGLES.index(name))

    y_train = tf.keras.utils.to_categorical(y_train_nums, num_classes=len(F_SINGLES))

    return(x_train, y_train)

def load_conversion():
    # returns a conversion table of shape {f_name: uf_name}
    f_temp = []
    uf_temp = []
    with open("f_singles.txt", "r") as r:
        for line in r:
            line = line.rstrip("\n")
            f_temp.append(line)
        
    with open("uf_singles.txt", "r") as r:
        for line in r:
            line = line.rstrip("\n")
            uf_temp.append(line)

    conversion = dict(zip(f_temp, uf_temp))
    return(conversion)

CONVERSION = load_conversion()
F_SINGLES = list(CONVERSION.keys())


def main():    
    # load data
    x_train, y_train = load_data()
    print(x_train.shape)
    print(y_train.shape)    

    # define model
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(100, return_sequences=True))
    model.add(tf.keras.layers.LSTM(100))
    model.add(tf.keras.layers.Dense(100, activation='relu'))
    model.add(tf.keras.layers.Dense(len(F_SINGLES), activation='softmax'))
    # compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # fit model
    model.fit(x_train, y_train, batch_size=800, epochs=300)
    print(model.summary())
    
    # save the model to file
    model.save('lstm_models/L300S.h5')


if __name__ == "__main__":
    main()