from gensim.models import Word2Vec
from matplotlib import pyplot as plt
import tensorflow as tf
import numpy as np
import os
import random

LV = tf.keras.models.load_model("lstm_models/L600V.h5")
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

def cardvec_from_LS(known_names, known_vecs, correction): 
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

    pred = LV(input_data)
    pred = pred.numpy()         

    if correction == True:
        similars = wv.most_similar(pred)
        for similar in similars:
            cardname = similar[0]
            if known_names.count(cardname) < 4:
                break
        cardvec = wv[cardname]
    else:
        cardname = wv.most_similar(pred)[0][0]
        cardvec = wv[cardname]    
    
    return(cardname, cardvec)

def list_from_LV(pred_names):
    len_input_names = len(pred_names)
    # we also want a list of card vectors
    pred_vecs = [wv[cardname] for cardname in pred_names]

    while len(pred_names) < 60:
        next_cardname, next_cardvec = cardvec_from_LV(pred_names, pred_vecs, False)
        pred_vecs.append(next_cardvec)
        pred_names.append(next_cardname)

    return(pred_names[len_input_names:])

def get_accuracy(prediction, target):
    score = 0
    len_target = len(target)
    for card in prediction:
        if card in target:
            score += 1
            target.remove(card)
    if(False): # verbose predictions
        print("PREDICTION ---------------")
        print(prediction)
        print("TARGET---------------")
        print(target)
        print("ACCURACY: ", end=" ") 
        print(score/len_target)
    return(score/len_target)

def update_scores(scores, cards):
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
    num_known, score = list(scores.keys()), list(scores.values())
    fig, ax = plt.subplots(1, 1)

    ax.bar(num_known, score)

    ax.set_ylim(0, 1)

    ax.set_title("L600VN")
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