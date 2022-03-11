import tensorflow as tf
import numpy as np
from gensim.models import Word2Vec
import random

W2V = Word2Vec.load("w2v_models/m3.model")
W2V = W2V.wv

LSTM_MODEL_PATH = "lstm_models/m9.h5"
INFO_FILENAME = "info/op1.txt"

ENSURE_LEGAL = True

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

def card_from_pred(pred, pred_names, known_cards):
    exceptions = ["forest", "mountain", "island", "swamp", "plains",
     "snowcovered_forest", "snowcovered_mountain", "snowcovered_island",
     "snowcovered_swamp", "snowcovered_plains"]
    possible_cards = W2V.most_similar(pred, topn=16)
    new_card_name = possible_cards[0][0]
    if ENSURE_LEGAL == False:
        return()
    i = 0
    while (pred_names.count(new_card_name)+known_cards.count(new_card_name)) == 4 and new_card_name not in exceptions:
        # choose another
        i+=1
        new_card_name = possible_cards[i][0]

    return(new_card_name)

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

def pretty_print(known_cards, pred_names, conversion):
    formated_decklist = known_cards + pred_names
    print("len flist, ", len(formated_decklist))
    unformated_decklist = [conversion[card] for card in formated_decklist]
    
    # dictionary that keeps track of how many of each card are in the unformated decklist
    counts_list = {card: unformated_decklist.count(card) for card in set(unformated_decklist)}
    
    for card, count in counts_list.items():
        print(f"{count} {card}")

def w6_insta_stat(model):
    target_list_filename = "f_lists/AmuletTitan/5.txt"
    target_list = load_info_cards(target_list_filename)
    pred_names = []

    score = 0
    remaining = target_list[2:]

    zeros = [[0.]*64]*(60)

    # until the list is complete, predict the next card
    for i in range(2, 60):
        print(i)
        data = np.array(vectorize(target_list[:i]))
        # prepare input
        if len(data) < 59:
            input_data = np.concatenate([zeros[:59-len(data)], data])
        else: 
            input_data = data
        input_data = np.array([input_data])

        # predict next card
        pred = model(input_data)
        next_card_name = card_from_pred(pred.numpy(), pred_names, target_list[:2])

        pred_names.append(next_card_name)
        if next_card_name in remaining:
            score += 1
            remaining.remove(next_card_name)
        print(len(pred_names))

    return(pred_names, (score/58)*100)





def predict_list(known_cards, model):
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
        next_card_name = card_from_pred(pred.numpy(), pred_names, known_cards)
        next_card_vector = W2V[next_card_name]

        # append to prediction lists (names and vectors)
        predictions = np.append(predictions, [next_card_vector], axis=0)
        print(len(predictions))
        pred_names.append(next_card_name)
    return(pred_names)

def main():
    # loads lstm model into memory
    model = tf.keras.models.load_model(LSTM_MODEL_PATH)
    # loads known card names into memory
    known_cards = load_info_cards("f_lists/AmuletTitan/5.txt")
    # predict the list
    #pred_names = predict_list(known_cards, model)
    pred_names, score = w6_insta_stat(model)

    # unformat lookup
    conversion = load_conversion()

    pretty_print(known_cards[:2], pred_names, conversion)

    print(f"This prediction scored: {score}%")
              
    """# to print predictions, we can print either the full list, or just the predicted cards
    # currently known_cards, -----here starts predictions-----, predictions
    for card in known_cards:
        print(card)
    
    print("-------------here starts predictions---------------")

    for card in pred_names:
        print(card)"""

if __name__ == "__main__":
    main()