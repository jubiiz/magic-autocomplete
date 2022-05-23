from gensim.models import Word2Vec
from matplotlib import pyplot as plt
import tensorflow as tf
import numpy as np
import os
import random

LS = tf.keras.models._load_model("lstm_models/L1000S.h5")
# loads Word2Vec model
wv = Word2Vec.load("w2v_models/m3.model")
wv = wv.wv

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
PRED_INDEXES = list(range(len(F_SINGLES)))

def card_from_LS(known_names, known_vecs, correction): 
    """
    takes as input a list of card vectors ("known")
    outputs a next card name and next card vector
    applies correction if "correction" is True
    """
    zeros = [[0.]*64]*(60)
    # prepare input
    if len(known_names) < 59:
        input_data = np.concatenate([zeros[:59-len(known_vecs)], known_vecs])
    else:
        input_data = known_vecs
    input_data = np.array([input_data])

    pred = LS(input_data)
    pred = pred.numpy()         

    if correction == True:
        pred_index = pred.argmax()
        cardname = F_SINGLES[pred_index]
        if known_names.count(cardname) >= 4:
            cardnames = np.random.choice(F_SINGLES, size=20, replace=False, p=pred[0])
            for cardname in cardnames:
                if known_names.count(cardname) <4: 
                    break                            
            
        cardvec = wv[cardname]
    else:
        cardname = F_SINGLES[pred.argmax()]
        cardvec = wv[cardname]    
    
    return(cardname, cardvec)

def list_from_LV(pred_names):
    """
    predicts a list of cards using an LSTM network with an output layer outputting a vector
    """
    len_input_names = len(pred_names)
    # we also want a list of card vectors
    pred_vecs = [wv[cardname] for cardname in pred_names]

    while len(pred_names) < 60:
        next_cardname, next_cardvec = card_from_LS(pred_names, pred_vecs, True)
        pred_vecs.append(next_cardvec)
        pred_names.append(next_cardname)

    return(pred_names[len_input_names:])

def get_accuracy(prediction, target):
    """
    computes the accuracy of prediction based on target
    returns the ratio of unique pairs of cards between the two
    """
    score = 0
    verbose_target = target.copy()
    len_target = len(target)
    for card in prediction:
        if card in target:
            score += 1
            target.remove(card)
    if(True): # verbose predictions
        print("PREDICTION ---------------")
        print(prediction)
        print("TARGET---------------")
        print(verbose_target)
        print("ACCURACY: ", end=" ") 
        print(score/len_target)
        print("PREDICTION SIZE: ", end=" ")
        print(len_target)
    return(score/len_target)

def update_scores(scores, cards):
    """
    for a given decklist "cards", makes predictions with 1, 5, 15..., 55, 59 cards
    updates the prediction accuracy dictionary "scores" after each prediction
    """
    random.shuffle(cards)
    # must find a list given "len_inputs" input cards
    for len_inputs in scores:
        random.shuffle(cards)        
        inputs, target = cards[:len_inputs], cards[len_inputs:]
        prediction = list_from_LV(inputs)
        accuracy = get_accuracy(prediction, target)
        scores[len_inputs] += accuracy

    return(scores)



def plot_scores(scores):
    """
    takes in a dictionary of prediction accuracy per number of input cards
    plots a bar graphs of the accuracy per number of input cards
    """
    num_known, score = list(scores.keys()), list(scores.values())
    fig, ax = plt.subplots(1, 1)

    ax.bar(num_known, score)

    ax.set_ylim(0, 1)

    ax.set_title("L1000SN")
    ax.set_xlabel("Number of Known Cards")
    ax.set_ylabel("Accuracy Ratio")

    plt.show()


def main():
    lists_path = os.path.join(os.getcwd(), "f_lists")
    lists_dir = os.scandir(lists_path)

    # how well does the algorithm perform when we give it i=1->59 cards
    scores = {i:0 for i in range(5, 60, 10)}
    scores[1] = 0
    scores[59] = 0
    numlists = 0
    i=0
    # update scores for each list
    for archetype in lists_dir:
        archetype_dir = os.scandir(archetype.path)
        # loops over decklists of that archetype
        for decklist in archetype_dir:
            cards = []
            # loads every card of the decklist
            with open(decklist.path, "r") as r:
                for line in r:
                    cardname = line.rstrip("\n")
                    if len(line) == 0:
                        continue
                    cards.append(cardname)
                # only keep length 60 lists
                if(len(cards) != 60):
                    cards = cards[:60]
            # calculate efficiency with this list, update scores
            if i%1 == 0:
                scores = update_scores(scores, cards)
                numlists += 1
                #print(numlists)
            i+=1
            print(i)

    # normalize scores (average them: up to now accuracies were just added up. Now we divide by the number of attempts)
    print(scores)
    for num_cards, score in scores.items():
        scores[num_cards] = score/numlists
    print(scores)

    # plots scores
    plot_scores(scores)
    

if __name__ == "__main__":
    main()