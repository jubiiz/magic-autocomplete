
from pytz import NonExistentTimeError
import tensorflow as tf
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
import pandas as pd
import numpy as np
import os
import random

wvmodel = Word2Vec.load("w2v_models/m3.model")
wvmodel = wvmodel.wv




def load_data(filename):
    """
    loads a word vector model (filename) into memory
    returns training data ; testing data
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
                    cards.append(wvmodel[cardname])
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
        for i in range(2, 61):
            list_mod = np.concatenate([zeros[:60-i], np.array(l[:i])])
            data.append(np.array(list_mod))
    random.shuffle(data)
    
    n = len(data)
    data = np.array(data)
    train_d = data
    test_d = data
    print(data[:3, :3])
    print(data.shape)
    

    x_train, y_train = train_d[:, :-1], train_d[:, -1]
    x_test, y_test = test_d[:, :-1], test_d[:,-1]

    #print(train_d)
    #print(x_train)
    #print('ytrain: ', y_train)
    return(x_train, y_train, x_test, y_test)


def complete_lists(x_test, y_test):
    """
    DESCRIPTION TODO
    """

    """
    ####testing wv model: making sure retrieval is ok
    print(x_test[0][0])
    print(wvmodel.most_similar(x_test[0][0]))

    print('ans: ')
    print(wvmodel.most_similar(y_test[0]))
    
    print("list predicted: ")
    #x_test[0] is a list
    for card in x_test[100]:
        sim = wvmodel.most_similar(card)
        print(sim[0][0], sim[0][1])

    print(x_test.shape)
    print(x_test[100].shape)

    pred = lstm_model.predict(x_test)
    print(pred.shape)
    print("prediction is: ------------")
    print(wvmodel.most_similar(pred[100]))

    print("real end-card is:-------------------")
    print(wvmodel.most_similar(y_test[100]))
    """
    lstm_model = tf.keras.models.load_model('lstm_models/m5.h5')


    
    #for i in range(len(y_test)):
    i= 645
    num_known = 0
    # 59 0 vectors of len 64
    zeros = [[0.]*64]*(59-num_known)
    print(zeros)
    dl = np.array(x_test[i][:num_known])
    print(dl)
    dl = np.concatenate([zeros , dl])
    print(type(dl))
    pred = lstm_model.predict(np.array([dl]))
    ans = wvmodel.most_similar(y_test[i])[0][0]
    f_pred = wvmodel.most_similar(pred)[0]
    print(ans,f_pred, wvmodel.distance(ans, f_pred[0]))

def main():
    # load data
    x_train, y_train, x_test, y_test = load_data("w2v_models/m3.model")
    print(x_train.shape)
    print(y_train.shape)

    # if build neural network: insert block here
    # define model
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(100, return_sequences=True))
    model.add(tf.keras.layers.LSTM(100))
    model.add(tf.keras.layers.Dense(100, activation='relu'))
    model.add(tf.keras.layers.Dense(64))
    # compile model
    model.compile(loss='cosine_similarity', optimizer='adam', metrics=['accuracy'])
    # fit model
    model.fit(x_train, y_train, batch_size=800, epochs=10)
    print(model.summary())
    
    # save the model to file
    model.save('lstm_models/m0.h5')


    #complete_lists(x_test, y_test)


    """
     # define model
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(100, return_sequences=True))
    model.add(tf.keras.layers.LSTM(100))
    model.add(tf.keras.layers.Dense(100, activation='relu'))
    model.add(tf.keras.layers.Dense(64))
    # compile model
    model.compile(loss='cosine_similarity', optimizer='adam', metrics=['accuracy'])
    # fit model
    model.fit(x_train, y_train, batch_size=20, epochs=30)
    print(model.summary())
    
    # save the model to file
    model.save('lstm_models/m3.h5')
    """


if __name__ == "__main__":
    main()