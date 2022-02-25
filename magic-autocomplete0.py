import tensorflow as tf
import numpy as np
from gensim.models import Word2Vec
import random

W2V = Word2Vec.load("w2v_models/m3.model")
W2V = W2V.wv

def load_info_cards(filename_known):
    """
    user inputs a filename of a text file containing a formatted list
    of known cards

    returns a list of known cardnames
    """

    known_cards = []
    with open(filename_known, "r") as r:
        for line in r:
            cardname = line.rstrip("\n")
            if len(line) == 0:
                continue
            #appending vector, not cardname
            known_cards.append(cardname)
    return(known_cards)

def vectorize(known_cards):
    initial_predictions = []
    for card in known_cards:
        try:
            v = W2V[card]
            initial_predictions.append(v)
        except KeyError:
            print(f"WARNING: CARD '{card}' NOT FOUND.\
                PLEASE MAKE SURE THE FORMAT IS RIGHT")
            initial_predictions.append([0.]*64)
    return(initial_predictions)

def main():
    # loads lstm model into memory
    model = tf.keras.models.load_model("lstm_models/m10.h5")

    # filename of the known cards
    filename_known = "info/op5.txt"   ################# USER INPUT HERE
    # loads known card names into memory
    known_cards = load_info_cards(filename_known)
    
    # predicts the rest of the list. They are be stored as vectors, not cardnames
    # they do get transformed back to cardnames to be shown
    predictions = np.array(vectorize(known_cards.copy()))
    pred_names = [] # stores the actual name of the predicted cards
    # 60 null vectors of len 64 (useful in prediction)
    # MAYBE CHECK NEGATIVE VALUES
    zeros = [[0.]*64]*(60)

    # until the list is complete, predict the next card
    while len(pred_names)+len(known_cards) < 60:
        # prepare input
        if len(predictions) < 59:
            input_data = np.concatenate([zeros[:59-len(predictions)], predictions])
        else:
            input_data = predictions
        input_data = np.array([input_data])

        # predict next card
        pred = model(input_data)
        next_card_name = W2V.most_similar(pred.numpy())
        next_card_name = next_card_name[0][0]
        next_card_vector = W2V[next_card_name]

        # append to prediction lists (names and vectors)
        predictions = np.append(predictions, [next_card_vector], axis=0)
        print(len(predictions))
        pred_names.append(next_card_name)

          
    # to print predictions, we can print either the full list, or just the predicted cards
    # currently known_cards, -----here starts predictions-----, predictions
    for card in known_cards:
        print(card)
    
    print("-------------here starts predictions---------------")

    for card in pred_names:
        print(card)

if __name__ == "__main__":
    main()