from gensim.models import Word2Vec
import tensorflow as tf
import numpy as np

LS = tf.keras.models.load_model("../../models/lstm_2022/L1000S.h5")
# loads Word2Vec model
wv = Word2Vec.load("../../models/w2v/m3_2022.model").wv


def load_formatted_singles():
    # returns a conversion table of shape {f_name: uf_name}
    formatted_singles = []
    with open("../../data_21_01_2022/f_singles.txt", "r") as r:
        for line in r:
            line = line.rstrip("\n")
            formatted_singles.append(line)
    return formatted_singles


F_SINGLES = load_formatted_singles()
PRED_INDEXES = list(range(len(F_SINGLES)))


def card_from_LS(known_names, known_vecs, correction): 
    """
    takes as input a list of card vectors ("known")
    outputs a next card name and next card vector
    applies correction if "correction" is True
    """
    zeros = [[0.]*64]*60
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

def load_list(filename):
    cards = []
    with open(filename) as r:
        for line in r:
            line = line.rstrip("\n")
            cards.append(line)
    return cards

def get_accuracy(prediction, target):
    """
    computes the accuracy of prediction based on target
    returns the ratio of unique pairs of cards between the two
    """
    target = target.copy()
    score = 0
    len_target = len(target)
    for card in prediction:
        if card in target:
            score += 1
            target.remove(card) 
    return(score/len_target)


def main():
    decklist_subset = load_list("decklist_subset.txt")
    target_decklist = load_list("target_decklist.txt")
    cpu_prediction = list_from_LV(decklist_subset)
    cpu_accuracy = get_accuracy(cpu_prediction, target_decklist)

    print("information available: ", decklist_subset)
    print("\ntarget: ", target_decklist)
    print("\ncpu prediction: ", "\n".join(sorted(cpu_prediction)))
    print("\ncpu_accuracy: ", cpu_accuracy)


if __name__ == "__main__":
    main()
